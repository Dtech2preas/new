import re

with open('dashboard.html', 'r') as f:
    content = f.read()

# Update Sidebar nav
nav_html = """
            <nav class="flex-1 space-y-2" id="tour-nav">
                <a href="#" class="flex items-center gap-3 px-4 py-3 bg-white/5 text-white rounded-xl font-medium transition-colors border border-[var(--border)]">
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
                <a href="plans.html" class="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl font-medium transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    Plans
                </a>
            </nav>
"""
content = re.sub(r'<nav class="flex-1 space-y-2" id="tour-nav">.*?</nav>', nav_html.strip(), content, flags=re.DOTALL)

# Update sidebar and header links
content = content.replace('<a href="#upgrade-section"', '<a href="plans.html"')
content = content.replace('onclick="showProfile()"', 'href="profile.html"')

# Remove Profile Modal
content = re.sub(r'<!-- PROFILE MODAL -->.*?<div id="locked-msg"', '<div id="locked-msg"', content, flags=re.DOTALL)

# Remove stray profile sections that might have been duplicated/leftover
content = re.sub(r'<div class="profile-grid">.*?</div>\s*</div>', '', content, flags=re.DOTALL)
content = re.sub(r'<div class="profile-section">.*?</div>', '', content, flags=re.DOTALL)

# Remove Active Sites section
content = re.sub(r'<!-- ACTIVE SITES -->\s*<div class="section-header">\s*<h3>Active Sites</h3>\s*</div>\s*<div id="sites-list".*?</div>', '', content, flags=re.DOTALL)

# Remove Upgrade Plan Section
content = re.sub(r'<!-- Upgrade Section -->.*?</div>\s*</main>', '</main>', content, flags=re.DOTALL)

# Clean up JS that referenced the old DOM
content = re.sub(r'function showProfile\(\) \{.*?\n        \}', '', content, flags=re.DOTALL)
content = re.sub(r'function closeProfile\(\) \{.*?\n        \}', '', content, flags=re.DOTALL)
content = re.sub(r'window\.onclick = function\(event\) \{.*?\n        \}', '', content, flags=re.DOTALL)
content = re.sub(r'function renderSites\(sites\) \{.*?\n        \}', '', content, flags=re.DOTALL)
content = re.sub(r'function deleteSite\(subdomain\) \{.*?\n        \}', '', content, flags=re.DOTALL)
content = re.sub(r'async function saveRetentionPolicy\(\) \{.*?\n        \}', '', content, flags=re.DOTALL)

# Also remove `renderSites(sites);` call from `fetchCaptures`
content = content.replace('renderSites(sites);', '')


# Let's fix the table layout for Captured Data
style_start = content.find('<style>')
style_end = content.find('</style>')

# We can add custom responsive table styling to make the table look good on mobile and replace the mobile-cards approach
# or just heavily simplify the mobile-cards approach to look like a tight list/feed.
# User mentioned "Let try a table", "even if it may be restructuring and making them a bit smaller"

# Let's inject CSS to make the table fully responsive instead of using `display: none` for table on mobile.
table_css = """
        /* Redesigned Captured Data Table */
        .data-table-container {
            width: 100%;
            overflow-x: auto;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            background: var(--bg-card);
        }

        .desktop-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.85rem;
        }

        .desktop-table th, .desktop-table td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
        }

        .desktop-table th {
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-sec);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.75rem;
        }

        .desktop-table tbody tr:hover {
            background: rgba(255, 255, 255, 0.02);
        }

        .btn-delete {
            background: rgba(243, 18, 96, 0.1);
            color: var(--danger);
            border: 1px solid var(--danger);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-delete:hover {
            background: var(--danger);
            color: white;
        }

        .domain-badge {
            background: rgba(255, 255, 255, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: bold;
            color: var(--text-main);
        }

        /* Smart Grid Compact for Table */
        .smart-grid {
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-top: 8px;
        }
        .smart-field {
            background: transparent;
            padding: 0;
            border: none;
            display: flex;
            flex-direction: row;
            align-items: baseline;
            gap: 8px;
            border-bottom: 1px dashed rgba(255,255,255,0.1);
            padding-bottom: 4px;
        }
        .smart-field:last-child {
            border-bottom: none;
        }
        .smart-key {
            font-size: 0.7rem;
            color: var(--text-sec);
            width: 80px;
            flex-shrink: 0;
            margin-bottom: 0;
        }
        .smart-value {
            font-size: 0.8rem;
            word-break: break-all;
        }
        .copy-icon {
            position: relative;
            margin-top: 0;
            right: 0;
            top: 0;
        }

        /* Mobile Table Adjustments */
        @media (max-width: 768px) {
            .desktop-table th, .desktop-table td {
                padding: 8px 10px;
            }
            .desktop-table th:first-child, .desktop-table td:first-child {
                display: none; /* Hide timestamp column entirely to save space */
            }
            .smart-header {
                font-size: 0.8rem;
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            .smart-key {
                width: 60px;
                font-size: 0.65rem;
            }
            .smart-value {
                font-size: 0.75rem;
            }
        }
"""
content = content.replace('</style>', table_css + '\n</style>')

# Remove `.mobile-cards` elements since we're using desktop-table everywhere now
content = re.sub(r'<div class="mobile-cards".*?</div>', '', content, flags=re.DOTALL)
content = content.replace('mobileList.innerHTML = \'\';', '')
content = re.sub(r'// Mobile Card.*?mobileList\.appendChild\(card\);', '', content, flags=re.DOTALL)


# Wrap desktop-table in data-table-container
content = content.replace('<table class="desktop-table">', '<div class="data-table-container">\n            <table class="desktop-table">')
content = content.replace('</table>', '</table>\n            </div>')

with open('dashboard.html', 'w') as f:
    f.write(content)
