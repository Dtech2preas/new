import re

with open('plans.html', 'r') as f:
    content = f.read()

# Update title
content = content.replace('<title>D-TECH Hub | Dashboard</title>', '<title>D-TECH Hub | Plans</title>')

# Remove profile modal
content = re.sub(r'<!-- PROFILE MODAL -->.*?</div>\s*</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)

# Remove welcome back banner, stats, analytics, active sites, captured data
content = re.sub(r'<div class="text-center mb-12 animate-\[fadeIn_0\.8s_ease\]">.*?<!-- Upgrade Section -->', '<!-- Upgrade Section -->', content, flags=re.DOTALL)

# Update the Sidebar nav
# Add plans link and update active states
nav_html = """
            <nav class="flex-1 space-y-2" id="tour-nav">
                <a href="dashboard.html" class="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl font-medium transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
                    Dashboard
                </a>
                <a href="deploy.html" class="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl font-medium transition-colors" id="tour-deploy">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path></svg>
                    Deploy Site
                </a>
                <a href="profile.html" class="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl font-medium transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                    Profile
                </a>
                <a href="plans.html" class="flex items-center gap-3 px-4 py-3 bg-white/5 text-white rounded-xl font-medium transition-colors border border-[var(--border)]">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    Plans
                </a>
            </nav>
"""
content = re.sub(r'<nav class="flex-1 space-y-2" id="tour-nav">.*?</nav>', nav_html.strip(), content, flags=re.DOTALL)

# In Plans page, the active link in JS like startTour may not be needed, but let's keep it minimal for now.
# Replace <a href="#upgrade-section" ...>Upgrade</a> with <a href="plans.html" ...>Upgrade</a>
content = content.replace('<a href="#upgrade-section"', '<a href="plans.html"')
content = content.replace('onclick="showProfile()"', 'href="profile.html"')

# We also need to strip out JS that expects dashboard elements if it causes errors, but since they have checks, it might be fine.
# However, `fetchCaptures` updates UI heavily relying on stats. Let's keep updateUI but remove rendering data tables since they are gone.
# Let's see if we should write a cleaner JS script for plans.html later.

with open('plans.html', 'w') as f:
    f.write(content)
