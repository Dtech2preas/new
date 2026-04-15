with open("admin.html", "r") as f:
    content = f.read()

analytics_html = """
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Users</h3>
                <div class="stat-value" id="stat-total-users"><div class="skeleton" style="width: 50%; height: 32px; margin: 10px auto;"></div></div>
            </div>
            <div class="stat-card">
                <h3>Active Subscriptions</h3>
                <div class="stat-value" id="stat-active-subs"><div class="skeleton" style="width: 50%; height: 32px; margin: 10px auto;"></div></div>
            </div>
            <div class="stat-card">
                <h3>Total Active Sites</h3>
                <div class="stat-value" id="stat-active-sites"><div class="skeleton" style="width: 50%; height: 32px; margin: 10px auto;"></div></div>
            </div>
            <div class="stat-card">
                <h3>Total Captures</h3>
                <div class="stat-value" id="stat-total-captures"><div class="skeleton" style="width: 50%; height: 32px; margin: 10px auto;"></div></div>
            </div>
        </div>
"""

# The tab content container id is "users", let's inject it right after <div id="users" class="tab-content">
content = content.replace('<div id="users" class="tab-content">', f'<div id="users" class="tab-content">\n{analytics_html}')

with open("admin.html", "w") as f:
    f.write(content)
