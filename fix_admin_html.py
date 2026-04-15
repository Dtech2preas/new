import re

with open("admin.html", "r") as f:
    content = f.read()

# 1. Add Admin Analytics section
analytics_html = """
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Users</h3>
                <div class="stat-value" id="stat-total-users"><div class="skeleton" style="width: 50%; height: 32px; margin: 10px 0;"></div></div>
            </div>
            <div class="stat-card">
                <h3>Active Subscriptions</h3>
                <div class="stat-value" id="stat-active-subs"><div class="skeleton" style="width: 50%; height: 32px; margin: 10px 0;"></div></div>
            </div>
            <div class="stat-card">
                <h3>Total Active Sites</h3>
                <div class="stat-value" id="stat-active-sites"><div class="skeleton" style="width: 50%; height: 32px; margin: 10px 0;"></div></div>
            </div>
            <div class="stat-card">
                <h3>Total Captures</h3>
                <div class="stat-value" id="stat-total-captures"><div class="skeleton" style="width: 50%; height: 32px; margin: 10px 0;"></div></div>
            </div>
        </div>
"""

# Insert before Users Management section
if '<div class="stats-grid">' not in content:
    content = content.replace("<h2>Users Management</h2>", f"{analytics_html}\n        <h2>Users Management</h2>")


# 2. Add search bar to users table
search_html = """
        <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
            <input type="text" id="user-search" placeholder="Search users by name or code..." style="padding: 10px; width: 100%; max-width: 400px; border-radius: 6px; border: 1px solid #ddd;">
        </div>
"""
if 'id="user-search"' not in content:
    content = content.replace("<table id=\"users-table\">", f"{search_html}\n        <table id=\"users-table\">")

# 3. Modify Users Table headers to add Action column
if '<th>Actions</th>' not in content:
    content = content.replace("<th>Status</th>", "<th>Status</th>\n                    <th>Actions</th>")

# 4. Modify User table rendering in loadUsers
table_row_old = """
                            <td><span class="status ${user.status}">${user.status}</span></td>
                        </tr>
"""
table_row_new = """
                            <td><span class="status ${user.status}">${user.status}</span></td>
                            <td>
                                <button onclick="actionUser('${uniqueCode}', 'suspend')" style="background: #f5a524; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-right: 5px;">Suspend</button>
                                <button onclick="actionUser('${uniqueCode}', 'ban')" style="background: #f31260; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-right: 5px;">Ban</button>
                                <button onclick="actionUser('${uniqueCode}', 'delete')" style="background: #333; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-right: 5px;">Delete</button>
                                <button onclick="updateUserPlan('${uniqueCode}')" style="background: #0070f3; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Edit Plan</button>
                            </td>
                        </tr>
"""
content = content.replace(table_row_old, table_row_new)


# 5. Add search logic and action logic in JS
js_logic = """
        // SEARCH LOGIC
        document.getElementById('user-search').addEventListener('input', function(e) {
            const term = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('#users-tbody tr');
            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(term) ? '' : 'none';
            });
        });

        // ADMIN ACTION LOGIC
        async function actionUser(uniqueCode, action) {
            if(!confirm(`Are you sure you want to ${action} user ${uniqueCode}?`)) return;
            try {
                const res = await fetch(WORKER_URL + '/api/admin/users/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + localStorage.getItem('admin_session') },
                    body: JSON.stringify({ action, uniqueCode })
                });
                const data = await res.json();
                if(data.success) {
                    showToast(`User ${action} successful`);
                    loadUsers();
                } else {
                    showToast(data.error || 'Action failed', 'error');
                }
            } catch(e) { showToast(e.message, 'error'); }
        }

        async function updateUserPlan(uniqueCode) {
            const plan = prompt("Enter new plan (free, basic, premium, gold):", "premium");
            if(!plan) return;
            const days = prompt("Enter days to add to expiry (leave blank to reset for free):", "30");
            try {
                const res = await fetch(WORKER_URL + '/api/admin/users/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + localStorage.getItem('admin_session') },
                    body: JSON.stringify({ action: 'update_plan', uniqueCode, plan: plan.toLowerCase(), expiryDays: days ? parseInt(days) : null })
                });
                const data = await res.json();
                if(data.success) {
                    showToast(`User plan updated to ${plan}`);
                    loadUsers();
                } else {
                    showToast(data.error || 'Action failed', 'error');
                }
            } catch(e) { showToast(e.message, 'error'); }
        }

        async function loadAnalytics() {
            try {
                const res = await fetch(WORKER_URL + '/api/admin/analytics', {
                    headers: { 'Authorization': 'Bearer ' + localStorage.getItem('admin_session') }
                });
                if(res.ok) {
                    const data = await res.json();
                    if(data.success) {
                        document.getElementById('stat-total-users').innerText = data.totalUsers;
                        document.getElementById('stat-active-subs').innerText = data.activeSubscriptions;
                        document.getElementById('stat-active-sites').innerText = data.totalActiveSites;
                        document.getElementById('stat-total-captures').innerText = data.totalCaptures;
                    }
                }
            } catch(e) { console.error("Failed to load analytics"); }
        }

        // Call it
        setTimeout(loadAnalytics, 500);
"""
if "function actionUser" not in content:
    content = content.replace("async function loadUsers() {", f"{js_logic}\n\n        async function loadUsers() {{")

# Add stat-card css
css_add = """
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center; }
        .stat-card h3 { margin: 0 0 10px 0; color: #555; font-size: 14px; text-transform: uppercase; }
        .stat-value { font-size: 28px; font-weight: bold; color: #0070f3; }
"""
if ".stats-grid {" not in content:
    content = content.replace("</style>", f"{css_add}\n    </style>")


with open("admin.html", "w") as f:
    f.write(content)
