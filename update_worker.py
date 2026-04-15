import re

with open("worker.js", "r") as f:
    content = f.read()

# 1. Update getUser to properly reset plan if expired
# Already does:
#    if (user.expiry && Date.now() > user.expiry) {
#        user.plan = 'free';
#        user.expiry = null;

# 2. handleUserRegister: Free Trial Logic
content = re.sub(
    r"const user = \{\s*username: username,\s*plan: 'free',\s*strikes: 0,\s*status: 'active',\s*created: Date.now\(\),\s*expiry: null,",
    "const user = {\n            username: username,\n            plan: 'premium',\n            strikes: 0,\n            status: 'active',\n            created: Date.now(),\n            expiry: Date.now() + (3 * 24 * 60 * 60 * 1000),\n            trial_used: true,",
    content
)

# 3. handlePaymentVerify & handleVoucherAction logic
payment_upgrade_old = """        const now = Date.now();
        let currentExpiry = user.expiry || now;
        if (currentExpiry < now) currentExpiry = now;

        user.plan = orderData.plan;
        if (user.pendingPlan) delete user.pendingPlan;

        user.expiry = currentExpiry + (30 * 24 * 60 * 60 * 1000);"""

payment_upgrade_new = """        const now = Date.now();
        if (user.plan === orderData.plan) {
            let currentExpiry = user.expiry || now;
            if (currentExpiry < now) currentExpiry = now;
            user.expiry = currentExpiry + (30 * 24 * 60 * 60 * 1000);
        } else {
            user.plan = orderData.plan;
            user.expiry = now + (30 * 24 * 60 * 60 * 1000);
        }
        if (user.pendingPlan) delete user.pendingPlan;"""

content = content.replace(payment_upgrade_old, payment_upgrade_new)

voucher_upgrade_old = """            const now = Date.now();
            let currentExpiry = user.expiry || now;
            if (currentExpiry < now) currentExpiry = now;

            user.plan = voucher.plan;
            if (user.pendingPlan) delete user.pendingPlan;

            user.expiry = currentExpiry + (30 * 24 * 60 * 60 * 1000);"""

voucher_upgrade_new = """            const now = Date.now();
            if (user.plan === voucher.plan) {
                let currentExpiry = user.expiry || now;
                if (currentExpiry < now) currentExpiry = now;
                user.expiry = currentExpiry + (30 * 24 * 60 * 60 * 1000);
            } else {
                user.plan = voucher.plan;
                user.expiry = now + (30 * 24 * 60 * 60 * 1000);
            }
            if (user.pendingPlan) delete user.pendingPlan;"""

content = content.replace(voucher_upgrade_old, voucher_upgrade_new)

# 4. Adding Admin endpoints for analytics and user actions
admin_routes = """
        if (url.pathname === '/api/admin/users' && request.method === 'GET') {
            return respond(await handleGetAllUsers(env));
        }
"""

admin_routes_new = """
        if (url.pathname === '/api/admin/users' && request.method === 'GET') {
            return respond(await handleGetAllUsers(env));
        }
        if (url.pathname === '/api/admin/analytics' && request.method === 'GET') {
            return respond(await handleAdminAnalytics(env));
        }
        if (url.pathname === '/api/admin/users/action' && request.method === 'POST') {
            return respond(await handleAdminUserAction(request, env));
        }
"""

content = content.replace(admin_routes, admin_routes_new)

admin_funcs = """
async function handleAdminAnalytics(env) {
    try {
        const list = await env.SUBDOMAINS.list({ prefix: "user::" });
        let totalUsers = list.keys.length;
        let activeSubscriptions = 0;
        let totalActiveSites = 0;

        for (const key of list.keys) {
            const user = await env.SUBDOMAINS.get(key.name, { type: "json" });
            if (user && user.plan !== 'free' && (!user.expiry || user.expiry > Date.now())) {
                activeSubscriptions++;
            }
        }

        // Count sites
        const siteList = await env.SUBDOMAINS.list({ prefix: "site::" });
        totalActiveSites = siteList.keys.length;

        // Count captures
        const capturesList = await env.SUBDOMAINS.list({ prefix: "capture::" });
        let totalCaptures = capturesList.keys.length;

        return new Response(JSON.stringify({
            success: true,
            totalUsers,
            activeSubscriptions,
            totalActiveSites,
            totalCaptures
        }), { headers: { 'Content-Type': 'application/json' } });
    } catch (e) {
        return jsonError(e.message, 500);
    }
}

async function handleAdminUserAction(request, env) {
    try {
        const body = await request.json();
        const { action, uniqueCode, plan, expiryDays } = body;
        if (!uniqueCode || !action) return jsonError("Missing code or action");

        const userRaw = await env.SUBDOMAINS.get(`user::${uniqueCode}`);
        if (!userRaw) return jsonError("User not found");

        let user = JSON.parse(userRaw);

        if (action === 'suspend') {
            user.status = 'locked';
        } else if (action === 'ban') {
            user.status = 'banned';
        } else if (action === 'activate') {
            user.status = 'active';
        } else if (action === 'delete') {
            await env.SUBDOMAINS.delete(`user::${uniqueCode}`);
            await env.SUBDOMAINS.delete(`username::${user.username.toLowerCase()}`);
            return new Response(JSON.stringify({ success: true, message: "User deleted" }), { headers: { 'Content-Type': 'application/json' } });
        } else if (action === 'update_plan') {
            if (!plan) return jsonError("Missing plan");
            user.plan = plan;
            if (plan === 'free') {
                user.expiry = null;
            } else if (expiryDays) {
                user.expiry = Date.now() + (expiryDays * 24 * 60 * 60 * 1000);
            }
        } else {
            return jsonError("Unknown action");
        }

        await env.SUBDOMAINS.put(`user::${uniqueCode}`, JSON.stringify(user));
        return new Response(JSON.stringify({ success: true, user }), { headers: { 'Content-Type': 'application/json' } });
    } catch (e) {
        return jsonError(e.message, 500);
    }
}
"""

content = content + "\n" + admin_funcs

with open("worker.js", "w") as f:
    f.write(content)
