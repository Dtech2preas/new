import re

with open('dashboard.html', 'r') as f:
    content = f.read()

# Add Tailwind and Google Fonts
head_additions = """
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/intro.js/7.2.0/intro.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/intro.js/7.2.0/introjs.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-main: #050505;
            --bg-card: #111111;
            --text-main: #ffffff;
            --text-sec: #888;
            --accent: #0070f3;
            --accent-hover: #005bb5;
            --border: #222;
            --success: #17c964;
            --danger: #f31260;
            --warning: #f5a524;
            --radius: 12px;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
        }

        .glass-card {
            background: rgba(17, 17, 17, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Basic Plan Theme */
        body.plan-basic {
            --bg-main: #0d1117;
            --bg-card: #161b22;
            --accent: #2f81f7;
            --accent-hover: #58a6ff;
            --border: #30363d;
        }

        /* Premium Plan Theme (High End) */
        body.plan-premium {
            --bg-main: #000000;
            --bg-card: #0a0a0a;
            --text-main: #f0f0f0;
            --accent: #9b59b6;
            --accent-hover: #8e44ad;
            --border: #333;
        }

        /* Gold Plan Theme (Luxury) */
        body.plan-gold {
            --bg-main: #000000;
            --bg-card: #0a0a0a;
            --text-main: #fffdf0;
            --accent: #ffd700;
            --accent-hover: #ffea00;
            --border: #444;
        }

        /* Gold Animated Gradient Text */
        body.plan-gold .logo span, body.plan-gold .gold-text {
            background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: shine 3s linear infinite;
            background-size: 200%;
        }

        @keyframes shine { to { background-position: 200% center; } }

        /* Smooth transitions */
        .stat-card {
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            border-color: var(--accent);
        }

        /* Desktop Sidebar Layout */
        @media (min-width: 1024px) {
            .app-layout {
                display: flex;
                min-height: 100vh;
            }
            .sidebar {
                width: 260px;
                flex-shrink: 0;
                border-right: 1px solid var(--border);
                background: var(--bg-card);
                position: fixed;
                height: 100vh;
                overflow-y: auto;
            }
            .main-content {
                flex-grow: 1;
                margin-left: 260px;
                padding: 32px;
                max-width: calc(100vw - 260px);
            }
            .mobile-header {
                display: none;
            }
        }

        @media (max-width: 1023px) {
            .sidebar {
                display: none; /* Can be toggled with JS later if needed */
            }
            .main-content {
                padding: 16px;
                padding-bottom: 80px;
            }
        }

        /* Smart Data Fields */
        .smart-field { background: rgba(255,255,255,0.03); padding: 8px 12px; border-radius: 6px; border: 1px solid var(--border); overflow: hidden; display: flex; flex-direction: column; }
        .smart-key { font-size: 0.7rem; color: var(--text-sec); text-transform: uppercase; margin-bottom: 4px; font-weight: 700; letter-spacing: 0.5px; }
        .smart-value { font-size: 0.95rem; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; color: var(--text-main); word-break: break-all; font-weight: 500;}

        .plan-premium .smart-field { border-color: rgba(155, 89, 182, 0.3); background: rgba(155, 89, 182, 0.05); }
        .plan-premium .smart-key { color: #bca0dc; }
        .plan-gold .smart-field { border-color: rgba(255, 215, 0, 0.3); background: linear-gradient(135deg, rgba(255,215,0,0.05), rgba(0,0,0,0)); }
        .plan-gold .smart-key { color: #ffd700; }

        .copy-icon { cursor: pointer; opacity: 0.5; transition: 0.2s; float: right; margin-top: -18px;}
        .copy-icon:hover { opacity: 1; color: var(--accent); }

        /* Toast Notification */
        #toast {
            visibility: hidden;
            min-width: 250px;
            background-color: var(--bg-card);
            color: var(--text-main);
            text-align: center;
            border-radius: 8px;
            padding: 16px;
            position: fixed;
            z-index: 9999;
            bottom: 30px;
            right: 30px;
            opacity: 0;
            transition: opacity 0.3s, bottom 0.3s, visibility 0.3s;
            border-left: 4px solid var(--accent);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        }
        #toast.show { visibility: visible; opacity: 1; bottom: 50px; }
        #toast.success { border-color: var(--success); }
        #toast.error { border-color: var(--danger); }

        /* Intro.js custom styling */
        .introjs-tooltip {
            background-color: var(--bg-card) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5) !important;
        }
        .introjs-arrow.top { border-bottom-color: var(--border) !important; }
        .introjs-arrow.bottom { border-top-color: var(--border) !important; }
        .introjs-button {
            background-color: var(--accent) !important;
            color: white !important;
            border: none !important;
            text-shadow: none !important;
            border-radius: 6px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
        }
        .introjs-skipbutton { background-color: transparent !important; color: var(--text-sec) !important; border: 1px solid var(--border) !important; }
        .introjs-bullets ul li a { background: #444 !important; }
        .introjs-bullets ul li a.active { background: var(--accent) !important; }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-main); }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #555; }

        .loading-spinner {
            border: 3px solid rgba(255,255,255,0.1);
            border-top: 3px solid var(--accent);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
"""

content = re.sub(r'<style>[\s\S]*?</style>', head_additions, content)

# Update loading screen
loader_html = """
    <div id="loader" class="fixed inset-0 bg-[var(--bg-main)] z-[2000] flex flex-col justify-center items-center">
        <div class="loading-spinner mb-4"></div>
        <div class="text-[var(--accent)] font-semibold tracking-wide">Authenticating...</div>
    </div>
"""
content = re.sub(r'<div id="loader".*?</div>', loader_html, content, count=1)

# App Layout Structure
app_layout_start = """
    <div class="app-layout" id="main-content" style="display:none;">
        <!-- Sidebar (Desktop) -->
        <aside class="sidebar p-6 flex flex-col">
            <div class="logo text-2xl font-extrabold tracking-tight mb-10">D-TECH <span class="text-[var(--accent)]">HUB</span></div>

            <nav class="flex-1 space-y-2" id="tour-nav">
                <a href="#" class="flex items-center gap-3 px-4 py-3 bg-white/5 text-white rounded-xl font-medium transition-colors border border-[var(--border)]">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
                    Dashboard
                </a>
                <a href="deploy.html" class="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl font-medium transition-colors" id="tour-deploy">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path></svg>
                    Deploy Site
                </a>
                <a href="#" onclick="showProfile()" class="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl font-medium transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                    Profile
                </a>
            </nav>

            <div class="mt-auto">
                <div class="bg-black/30 p-4 rounded-xl border border-[var(--border)] mb-4 text-sm">
                    <div class="text-gray-400 mb-1 text-xs uppercase font-bold tracking-wider">Current Plan</div>
                    <div class="flex justify-between items-center">
                        <span id="sidebar-plan" class="font-bold text-white">LOADING</span>
                        <a href="#upgrade-section" class="text-[var(--accent)] text-xs font-semibold hover:underline">Upgrade</a>
                    </div>
                </div>
                <button onclick="logout()" class="w-full flex items-center justify-center gap-2 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl font-medium transition-colors border border-transparent hover:border-gray-800">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
                    Logout
                </button>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Mobile Header -->
            <header class="mobile-header flex justify-between items-center py-4 mb-6 border-b border-[var(--border)]">
                <div class="logo text-xl font-extrabold tracking-tight">D-TECH <span class="text-[var(--accent)]">HUB</span></div>
                <div class="flex items-center gap-3">
                    <span id="plan-badge-mobile" class="px-3 py-1 bg-[var(--bg-card)] border border-[var(--border)] rounded-full text-xs font-bold uppercase">FREE</span>
                    <button onclick="showProfile()" class="text-gray-400 hover:text-white">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                    </button>
                </div>
            </header>
"""
content = re.sub(r'<div class="container" id="main-content" style="display:none;">\s*<header>.*?</header>', app_layout_start, content, flags=re.DOTALL)

# Close app-layout div properly at the end
content = content.replace('<!-- UPGRADE SECTION / MODAL END -->', '')
content = content.replace('</div>\n\n    <div id="notification"', '        </main>\n    </div>\n\n    <div id="notification"')

# Hero Section styling
hero_html = """
        <div class="text-center mb-12 animate-[fadeIn_0.8s_ease]">
            <h2 id="greeting" class="text-3xl md:text-4xl font-extrabold mb-3 gold-text">Welcome Back</h2>
            <p class="text-gray-400 mb-8 max-w-lg mx-auto">Manage your deployments and captured data from one secure location.</p>
            <a href="deploy.html" class="inline-flex items-center justify-center px-8 py-4 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white font-bold rounded-full transition-all transform hover:-translate-y-1 hover:shadow-[0_10px_20px_rgba(0,0,0,0.3)] gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                Deploy New Site
            </a>
            <button onclick="startTour()" class="mt-4 block mx-auto text-sm text-gray-500 hover:text-[var(--accent)] underline decoration-dotted underline-offset-4">Need help? Take a tour</button>
        </div>
"""
content = re.sub(r'<div class="hero">.*?</div>', hero_html, content, flags=re.DOTALL)

# Stats Grid styling
stats_html = """
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 mb-10" id="tour-stats">
            <div class="stat-card glass-card p-6 rounded-2xl flex flex-col">
                <div class="flex items-center gap-3 mb-2 text-gray-400">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path></svg>
                    <span class="text-sm font-medium">Sites Deployed</span>
                </div>
                <span class="text-3xl font-extrabold" id="stat-sites">0</span>
            </div>
            <div class="stat-card glass-card p-6 rounded-2xl flex flex-col">
                <div class="flex items-center gap-3 mb-2 text-gray-400">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    <span class="text-sm font-medium">Total Captures</span>
                </div>
                <span class="text-3xl font-extrabold text-[var(--accent)]" id="stat-count">0</span>
            </div>
            <div class="stat-card glass-card p-6 rounded-2xl flex flex-col">
                <div class="flex items-center gap-3 mb-2 text-gray-400">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path></svg>
                    <span class="text-sm font-medium">Hidden</span>
                </div>
                <span class="text-3xl font-extrabold" id="stat-hidden">0</span>
            </div>
            <div class="stat-card glass-card p-6 rounded-2xl flex flex-col">
                <div class="flex items-center gap-3 mb-2 text-gray-400">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <span class="text-sm font-medium">Next Payment</span>
                </div>
                <span class="text-2xl font-extrabold truncate" id="stat-due">N/A</span>
            </div>
        </div>
"""
content = re.sub(r'<div class="stats-grid">.*?</div>\n\n        <!-- ANALYTICS', stats_html + '\n\n        <!-- ANALYTICS', content, flags=re.DOTALL)


# Header & Search/Filter replacement
data_header = """
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4" id="tour-data">
            <h3 class="text-xl font-bold flex items-center gap-2">
                <svg class="w-6 h-6 text-[var(--accent)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path></svg>
                Captured Data
            </h3>

            <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
                <!-- Search Bar -->
                <div class="relative flex-grow md:flex-grow-0">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    </div>
                    <input type="text" id="global-search" oninput="filterData()" placeholder="Search data..." class="w-full pl-10 pr-4 py-2 bg-[var(--bg-card)] border border-[var(--border)] rounded-lg text-sm text-white focus:outline-none focus:border-[var(--accent)] transition-colors">
                </div>

                <select id="site-filter" onchange="filterData()" class="py-2 pl-3 pr-8 bg-[var(--bg-card)] border border-[var(--border)] rounded-lg text-sm text-white focus:outline-none focus:border-[var(--accent)] appearance-none cursor-pointer">
                    <option value="all">All Sites</option>
                </select>

                <button onclick="fetchCaptures(1)" class="p-2 bg-[var(--bg-card)] border border-[var(--border)] rounded-lg text-gray-400 hover:text-white hover:border-[var(--accent)] transition-colors" title="Refresh Data">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                </button>
            </div>
        </div>

        <div id="premium-actions" style="display:none;" class="mb-4 flex flex-wrap gap-2">
            <button onclick="copyData()" class="text-sm px-3 py-1.5 bg-[var(--bg-card)] border border-[var(--border)] rounded-md hover:border-[var(--accent)] transition-colors flex items-center gap-1">📋 Copy JSON</button>
            <button onclick="downloadData()" class="text-sm px-3 py-1.5 bg-[var(--bg-card)] border border-[var(--border)] rounded-md hover:border-[var(--accent)] transition-colors flex items-center gap-1">📥 JSON Export</button>
            <button id="btn-csv" onclick="downloadCSV()" class="text-sm px-3 py-1.5 bg-[var(--bg-card)] border border-[var(--border)] rounded-md hover:border-[var(--accent)] transition-colors flex items-center gap-1 hidden">📊 CSV Export (Gold)</button>
        </div>
"""
content = re.sub(r'<div class="section-header">\s*<div style="display:flex; align-items:center; gap:15px;">.*?</div>\s*</div>', data_header, content, flags=re.DOTALL)


# Data Wrapper styling (Empty State)
empty_state_html = """
            <div id="empty-msg" class="hidden py-16 text-center border border-dashed border-gray-700 rounded-2xl bg-black/20">
                <svg class="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
                <h3 class="text-lg font-medium text-gray-300 mb-1">No captures found</h3>
                <p class="text-sm text-gray-500 mb-4">Deploy a site and share the link to start collecting data.</p>
                <a href="deploy.html" class="inline-block px-4 py-2 bg-[var(--bg-card)] border border-[var(--border)] text-sm font-medium rounded-lg hover:border-[var(--accent)] transition-colors">Deploy Now</a>
            </div>
"""
content = re.sub(r'<div id="empty-msg".*?</div>', empty_state_html, content, flags=re.DOTALL)

# Add Toast HTML
content = content.replace('<div id="notification" class="notification">Message</div>', '<div id="toast">Message</div>')

# Update UI function to handle sidebar
update_ui_js = """
        function updateUI(data) {
            const plan = data.plan || 'free';
            document.body.className = `plan-${plan}`;

            const badgeM = document.getElementById('plan-badge-mobile');
            const badgeS = document.getElementById('sidebar-plan');
            if(badgeM) badgeM.innerText = plan.toUpperCase();
            if(badgeS) badgeS.innerText = plan.toUpperCase();

            // Limits
"""
content = content.replace('function updateUI(data) {\n            const plan = data.plan || \'free\';\n            document.body.className = `plan-${plan}`;\n\n            const badge = document.getElementById(\'plan-badge\');\n            badge.innerText = plan.toUpperCase();\n\n            // Limits', update_ui_js)

# Update generateSmartContent to add copy buttons
smart_content_js = """
            if (keys.length === 0) {
                fieldsHTML = '<div class="smart-field"><span class="smart-value" style="color:var(--text-sec); font-style:italic;">No form data captured</span></div>';
            } else {
                for (const [key, value] of Object.entries(formData)) {
                    if (isGold && hiddenFields.includes(key)) continue;

                    let actionBtn = '';
                    if (isGold) {
                        actionBtn = `<button class="hide-btn" data-domain="${escapeHtml(domain)}" data-key="${escapeHtml(key)}">✕</button>`;
                    }

                    const safeVal = escapeHtml(String(value));
                    fieldsHTML += `
                        <div class="smart-field relative group">
                            ${actionBtn}
                            <span class="smart-key">${escapeHtml(key)}</span>
                            <span class="smart-value">${safeVal}</span>
                            <svg onclick="copyText('${safeVal.replace(/'/g, "\\'")}')" class="w-4 h-4 copy-icon text-gray-500 hover:text-[var(--accent)] absolute right-2 top-8 md:opacity-0 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                        </div>`;
                }
            }
"""
content = re.sub(r'if \(keys\.length === 0\) \{.*?for \(const \[key, value\] of Object\.entries\(formData\)\) \{.*?</div>`;\n                }\n            }', smart_content_js, content, flags=re.DOTALL)

# Update Filter Data to include Search
filter_data_js = """
        function filterData() {
            const siteFilter = document.getElementById('site-filter').value;
            const searchQ = document.getElementById('global-search').value.toLowerCase();

            let filtered = currentData;

            if (siteFilter !== 'all') {
                filtered = filtered.filter(item => {
                    const d = item.data || {};
                    const url = d.url || '';
                    return url.includes(`//${siteFilter}.`);
                });
            }

            if (searchQ) {
                filtered = filtered.filter(item => {
                    const d = item.data || {};
                    const formDataStr = JSON.stringify(d.formData || {}).toLowerCase();
                    return formDataStr.includes(searchQ);
                });
            }

            renderData(filtered);
        }

        function copyText(text) {
            navigator.clipboard.writeText(text).then(() => notify("Copied value", "success"));
        }
"""
content = re.sub(r'function filterData\(\) \{.*?renderData\(filtered\);\n        }', filter_data_js, content, flags=re.DOTALL)

# Update notification to use toast
notify_js = """
        function notify(msg, type = 'success') {
            const toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.className = '';
            toast.classList.add('show', type);
            setTimeout(() => { toast.classList.remove('show'); }, 3000);
        }

        // --- TOUR ---
        function startTour() {
            introJs().setOptions({
                steps: [
                    {
                        title: 'Welcome to Dashboard',
                        intro: 'This is where you manage your deployments and captured data.'
                    },
                    {
                        element: document.querySelector('#tour-stats'),
                        intro: 'Keep track of how many sites you have active and total data captured.'
                    },
                    {
                        element: document.querySelector('#tour-deploy'),
                        intro: 'Click here to deploy a new capture site using templates or custom HTML.'
                    },
                    {
                        element: document.querySelector('#tour-data'),
                        intro: 'All submitted data appears here. You can search, filter by site, and copy individual fields.'
                    }
                ],
                showProgress: true,
                showBullets: false
            }).start();
        }
"""
content = re.sub(r'function notify\(msg, type = \'info\'\) \{.*?setTimeout.*?\}', notify_js, content, flags=re.DOTALL)

with open('dashboard.html', 'w') as f:
    f.write(content)
