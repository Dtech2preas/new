import re
import os

# Function to update all HTML files to use the new Authorization header
def update_auth_headers(filename):
    if not os.path.exists(filename):
        return

    with open(filename, 'r') as f:
        content = f.read()

    # Dashboard.html fetch updates
    if filename == 'dashboard.html':
        # Add sessionToken header to fetchCaptures
        fetch_replacement = """
                const token = localStorage.getItem('session_token');
                const headers = {};
                if(token) headers['Authorization'] = `Bearer ${token}`;

                const res = await fetch(`${WORKER_URL}/api/public/captures?code=${encodeURIComponent(userCode)}&page=${page}&limit=${itemsPerPage}`, {
                    headers: headers
                });
"""
        content = re.sub(r'const res = await fetch\(`\$\{WORKER_URL\}/api/public/captures\?code=\$\{encodeURIComponent\(userCode\)\}&page=\$\{page\}&limit=\$\{itemsPerPage\}`\);', fetch_replacement, content)

        # Update deleteItem
        delete_replacement = """
            try {
                const token = localStorage.getItem('session_token');
                const headers = {};
                if(token) headers['Authorization'] = `Bearer ${token}`;

                const res = await fetch(`${WORKER_URL}/api/public/captures?code=${encodeURIComponent(userCode)}&key=${encodeURIComponent(key)}`, {
                    method: 'DELETE',
                    headers: headers
                });
"""
        content = re.sub(r'try \{\n                const res = await fetch\(`\$\{WORKER_URL\}/api/public/captures\?code=\$\{encodeURIComponent\(userCode\)\}&key=\$\{encodeURIComponent\(key\)\}`, \{ method: \'DELETE\' \}\);', delete_replacement, content)

        # Update deleteSite
        delete_site_rep = """
            try {
                const token = localStorage.getItem('session_token');
                const headers = {};
                if(token) headers['Authorization'] = `Bearer ${token}`;

                const res = await fetch(`${WORKER_URL}/api/public/sites?code=${encodeURIComponent(userCode)}&subdomain=${encodeURIComponent(subdomain)}`, {
                    method: 'DELETE',
                    headers: headers
                });
"""
        content = re.sub(r'try \{\n                const res = await fetch\(`\$\{WORKER_URL\}/api/public/sites\?code=\$\{encodeURIComponent\(userCode\)\}&subdomain=\$\{encodeURIComponent\(subdomain\)\}`, \{ method: \'DELETE\' \}\);', delete_site_rep, content)

        # Add data retention settings to profile modal
        profile_additions = """
                <div class="profile-section">
                    <h4 class="text-[var(--accent)] font-semibold mb-2">Data Retention Policy</h4>
                    <p class="text-xs text-gray-500 mb-3">Auto-delete old captured data to save space and manage privacy.</p>
                    <div class="flex gap-2">
                        <select id="retention-select" class="bg-[var(--bg-card)] border border-[var(--border)] text-white text-sm rounded-lg p-2 focus:border-[var(--accent)] outline-none flex-1">
                            <option value="7">7 Days (Default Free)</option>
                            <option value="30">30 Days</option>
                            <option value="90">90 Days (Gold)</option>
                        </select>
                        <button onclick="saveRetentionPolicy()" class="bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">Save</button>
                    </div>
                </div>

                <div class="profile-section">
                    <h4 class="font-semibold mb-3">Security Activity</h4>
"""
        content = content.replace('<div class="profile-section">\n                    <h4>Security Activity</h4>', profile_additions)

        # Add JS to save retention policy
        retention_js = """
        async function saveRetentionPolicy() {
            const days = document.getElementById('retention-select').value;
            const token = localStorage.getItem('session_token');
            const headers = { 'Content-Type': 'application/json' };
            if(token) headers['Authorization'] = `Bearer ${token}`;

            try {
                const res = await fetch(`${WORKER_URL}/api/auth/settings`, {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify({ retentionDays: days })
                });
                const data = await res.json();
                if(data.success) {
                    notify("Retention policy updated successfully", "success");
                } else {
                    notify(data.error || "Failed to update", "error");
                }
            } catch(e) {
                notify("Network error", "error");
            }
        }
"""
        content = content.replace('function closeProfile() {', retention_js + '\n        function closeProfile() {')

        # Set current retention in modal if available
        retention_set_js = """
            if(currentUserData.retentionDays) {
                document.getElementById('retention-select').value = currentUserData.retentionDays;
            }
"""
        content = content.replace('// Status & Expiry', retention_set_js + '\n            // Status & Expiry')

        # Clear token on logout
        content = content.replace("localStorage.removeItem('user_code');", "localStorage.removeItem('user_code');\n            localStorage.removeItem('session_token');")

    elif filename == 'deploy.html':
        deploy_auth = """
            const token = localStorage.getItem('session_token');
            const headers = {'Content-Type': 'application/json'};
            if(token) headers['Authorization'] = `Bearer ${token}`;

            try {
                const res = await fetch(`${WORKER_URL}/api/public/deploy`, {
                    method: 'POST',
                    headers: headers,
"""
        content = re.sub(r'try \{\n                const res = await fetch\(`\$\{WORKER_URL\}/api/public/deploy`, \{\n                    method: \'POST\',\n                    headers: \{\'Content-Type\': \'application/json\'\},', deploy_auth, content)

    elif filename == 'index.html':
        # Update saveSession to include token
        save_session_new = """
        function saveSession(code, username, remember, sessionToken) {
            localStorage.setItem('user_code', code);
            if(sessionToken) localStorage.setItem('session_token', sessionToken);
            if(username) localStorage.setItem('user_name', username);

            if (remember) {
                localStorage.setItem('remember_me', 'true');
            } else {
                localStorage.removeItem('remember_me');
            }
        }
"""
        content = re.sub(r'function saveSession\(code, username, remember\) \{.*?\}', save_session_new, content, flags=re.DOTALL)

        # Update handleLogin calls to pass sessionToken
        content = content.replace('saveSession(data.code, username, remember);', 'saveSession(data.code, username, remember, data.sessionToken);')
        content = content.replace('saveSession(code, null, true);', 'saveSession(code, null, true, data.sessionToken);')

    with open(filename, 'w') as f:
        f.write(content)

update_auth_headers('index.html')
update_auth_headers('dashboard.html')
update_auth_headers('deploy.html')
