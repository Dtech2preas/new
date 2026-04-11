import re

with open('deploy.html', 'r') as f:
    content = f.read()

# I see the problem. The replace failed before so it duplicated the text. I need to clear the old HTML structure.
tabs_fix = """
        <div class="glass-card p-6 md:p-10 rounded-2xl shadow-xl">
            <div class="flex bg-white/5 p-1.5 rounded-xl mb-8">
                <div id="btn-mode-template" class="flex-1 text-center py-3 rounded-lg cursor-pointer font-semibold transition-colors bg-[var(--bg-card)] text-[var(--accent)] shadow" onclick="setMode('template')">Use Template</div>
                <div id="btn-mode-custom" class="flex-1 text-center py-3 rounded-lg cursor-pointer font-semibold transition-colors text-gray-400 hover:text-white" onclick="setMode('custom')">Custom HTML</div>
            </div>

            <div id="section-template" class="form-group">
"""

content = re.sub(r'<div class="glass-card p-6 md:p-10 rounded-2xl shadow-xl">\n            <div class="flex bg-white/5 p-1.5 rounded-xl mb-8">.*?<div id="section-template" class="form-group">', tabs_fix, content, flags=re.DOTALL)

with open('deploy.html', 'w') as f:
    f.write(content)
