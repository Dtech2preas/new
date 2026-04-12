import re

with open('plans.html', 'r') as f:
    content = f.read()

# Make sure plans.html checks the user's plan and displays it
# Let's restore the fetchCaptures call but we can simplify what it updates if we want, or just leave it. The missing elements might throw errors.
# Let's write a simple auth check for plans.html instead.
js_start = content.find('<script>')
js_end = content.rfind('</script>') + 9

new_js = """<script>
        const WORKER_URL = 'https://calm-bread-1d99.testdx24.workers.dev';
        const userCode = localStorage.getItem('user_code');

        // Auth Check
        if (!userCode) {
            window.location.href = 'index.html';
        }

        document.addEventListener('DOMContentLoaded', async () => {
            document.getElementById('loader').style.display = 'none';
            document.getElementById('main-content').style.display = '';

            // Check for payment return
            const urlParams = new URLSearchParams(window.location.search);
            const status = urlParams.get('status');
            const token = urlParams.get('token');
            const order_id = urlParams.get('order_id');

            if (status === 'success' && token && order_id) {
                document.getElementById('loader').innerText = 'Verifying Payment...';
                document.getElementById('loader').style.display = 'flex';
                try {
                    const verifyRes = await fetch(`${WORKER_URL}/api/pay/verify`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ token, order_id })
                    });
                    const verifyData = await verifyRes.json();
                    if (verifyData.success) {
                        notify("Payment verified! Your account has been upgraded.", "success");
                    } else {
                        notify(verifyData.error || "Payment verification failed.", "error");
                    }
                } catch (e) {
                    notify("Network error during verification.", "error");
                }

                // Clean up URL
                const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
                window.history.pushState({ path: newUrl }, '', newUrl);
            }

            fetchUserData();
        });

        async function fetchUserData() {
            try {
                const token = localStorage.getItem('session_token');
                const headers = {};
                if(token) headers['Authorization'] = `Bearer ${token}`;

                // Just fetch captures to get user details for now (since it's a bundled endpoint)
                const res = await fetch(`${WORKER_URL}/api/public/captures?code=${encodeURIComponent(userCode)}&page=1&limit=1`, {
                    headers: headers
                });

                const result = await res.json();

                if (result.success) {
                    updateUI(result);
                } else {
                    notify(result.error || 'Failed to load user data', 'error');
                }
            } catch (e) {
                console.error(e);
            }
        }

        function updateUI(data) {
            const plan = data.plan || 'free';
            document.body.className = `plan-${plan}`;

            const badgeM = document.getElementById('plan-badge-mobile');
            const badgeS = document.getElementById('sidebar-plan');
            if(badgeM) badgeM.innerText = plan.toUpperCase();
            if(badgeS) badgeS.innerText = plan.toUpperCase();

            if (data.pendingPlan === 'gold') {
                const msg = document.getElementById('pending-msg');
                if(msg) msg.style.display = 'block';
            }

            if (data.pendingPlan === 'premium') {
                const msg = document.getElementById('pending-premium-msg');
                if(msg) msg.style.display = 'block';
            }

            const lockedMsg = document.getElementById('locked-msg');
            if (!data.success && data.error === "Account Locked") {
                if(lockedMsg) lockedMsg.style.display = 'block';
            }
        }

        async function submitPayment() {
            const btn = document.getElementById('btn-pay');
            const msg = document.getElementById('pay-msg');
            const plan = document.getElementById('target-plan').value;

            let amount = 30;
            if (plan === 'basic') amount = 10;
            if (plan === 'premium') amount = 20;

            btn.disabled = true;
            btn.innerText = "Processing...";
            if(msg) msg.innerText = "";

            try {
                const res = await fetch(`${WORKER_URL}/api/pay/initiate`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        uniqueCode: userCode,
                        plan: plan,
                        amount: amount,
                        returnUrl: window.location.href.split('?')[0]
                    })
                });
                const data = await res.json();

                if(data.success && data.redirectUrl) {
                    window.location.href = data.redirectUrl;
                } else {
                    notify(data.error || "Failed to initiate payment", "error");
                    btn.disabled = false;
                    btn.innerText = "Pay / Extend";
                }
            } catch(e) {
                notify("Network Error", "error");
                btn.disabled = false;
                btn.innerText = "Pay / Extend";
            }
        }

        function logout() {
            localStorage.removeItem('user_code');
            localStorage.removeItem('session_token');
            window.location.href = 'index.html';
        }

        function notify(msg, type = 'success') {
            const toast = document.getElementById('toast');
            if(!toast) return;
            toast.innerText = msg;
            toast.className = '';
            toast.classList.add('show', type);
            setTimeout(() => { toast.classList.remove('show'); }, 3000);
        }
</script>"""

content = content[:js_start] + new_js + content[js_end:]

with open('plans.html', 'w') as f:
    f.write(content)
