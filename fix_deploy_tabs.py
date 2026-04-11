import re

with open('deploy.html', 'r') as f:
    content = f.read()

# Fix the deploy tabs layout
deploy_tabs = """
        <div class="glass-card p-6 md:p-10 rounded-2xl shadow-xl">
            <div class="mode-switch flex bg-white/5 p-1.5 rounded-xl mb-8">
                <div id="btn-mode-template" class="mode-btn active" onclick="setMode('template')">Use Template</div>
                <div id="btn-mode-custom" class="mode-btn" onclick="setMode('custom')">Custom HTML</div>
            </div>
"""

content = content.replace('<div class="mode-switch flex bg-white/5 p-1.5 rounded-xl mb-8">', deploy_tabs)

with open('deploy.html', 'w') as f:
    f.write(content)
