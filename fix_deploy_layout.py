import re

with open('deploy.html', 'r') as f:
    content = f.read()

# Fix layout structure
layout_fix = """
    <div class="max-w-4xl mx-auto p-4 md:p-8" id="main-content">
        <header class="flex items-center mb-8 pb-4 border-b border-[var(--border)]">
            <a href="dashboard.html" class="back-link mr-4 flex items-center gap-2 text-gray-400 hover:text-[var(--accent)] transition-colors font-medium">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
                Dashboard
            </a>
            <h1 class="text-2xl font-bold">Deploy New Site</h1>
        </header>

        <div class="glass-card p-6 md:p-10 rounded-2xl shadow-xl">
            <div class="mode-switch flex bg-white/5 p-1.5 rounded-xl mb-8">
"""

content = re.sub(r'<div class="max-w-4xl mx-auto p-4 md:p-8" id="main-content">\n        <header class="flex items-center mb-8 pb-4 border-b border-\[var\(--border\)\]">\n.*?</header>\n\n        <div class="form-card">\n            <div class="mode-switch">', layout_fix, content, flags=re.DOTALL)

# Fix inputs and labels
inputs_fix = """
            <div class="form-group mb-6 mt-8 pt-6 border-t border-[var(--border)]">
                <label class="block mb-2 text-sm font-semibold text-gray-300">Subdomain Name</label>
                <input type="text" id="subdomain" placeholder="e.g., login-secure" oninput="updatePreview()" autocomplete="off" class="w-full px-4 py-3 bg-[var(--bg-main)] border border-[var(--border)] rounded-xl text-white outline-none focus:border-[var(--accent)] transition-colors">
                <div id="url-preview" class="preview-box mt-2 text-sm text-[var(--accent)] font-mono min-h-[20px]"></div>
            </div>

            <div class="form-group mb-8">
                <label class="block mb-2 text-sm font-semibold text-gray-300">Your Unique Code (Master Key)</label>
                <input type="text" id="uniqueCode" readonly class="w-full px-4 py-3 bg-white/5 border border-[var(--border)] rounded-xl text-gray-400 cursor-not-allowed outline-none">
            </div>

            <button onclick="deploy()" class="w-full py-4 bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white font-bold rounded-xl transition-all transform hover:-translate-y-1 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none" id="deployBtn">Deploy Site</button>
            <div id="message" class="hidden mt-4 p-4 rounded-lg text-center font-medium"></div>
        </div>
    </div>
"""

content = re.sub(r'<div class="form-group">\n                <label>Subdomain Name</label>.*?</div>\n    </div>', inputs_fix, content, flags=re.DOTALL)


with open('deploy.html', 'w') as f:
    f.write(content)
