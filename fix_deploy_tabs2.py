import re

with open('deploy.html', 'r') as f:
    content = f.read()

# Fix the styling for the switch mode buttons, since they got a bit messed up.
switch_fix = """
        <div class="glass-card p-6 md:p-10 rounded-2xl shadow-xl">
            <div class="flex bg-white/5 p-1.5 rounded-xl mb-8">
                <div id="btn-mode-template" class="flex-1 text-center py-3 rounded-lg cursor-pointer font-semibold transition-colors bg-[var(--bg-card)] text-[var(--accent)] shadow" onclick="setMode('template')">Use Template</div>
                <div id="btn-mode-custom" class="flex-1 text-center py-3 rounded-lg cursor-pointer font-semibold transition-colors text-gray-400 hover:text-white" onclick="setMode('custom')">Custom HTML</div>
            </div>
"""

content = re.sub(r'<div class="glass-card p-6 md:p-10 rounded-2xl shadow-xl">\n            <div class="mode-switch flex bg-white/5 p-1.5 rounded-xl mb-8">\n                <div id="btn-mode-template" class="mode-btn active" onclick="setMode\(\'template\'\)">Use Template</div>\n                <div id="btn-mode-custom" class="mode-btn" onclick="setMode\(\'custom\'\)">Custom HTML</div>\n            </div>', switch_fix, content, flags=re.DOTALL)

# Add JS logic to handle the custom styling for tailwind active states
js_fix = """
        function setMode(mode) {
            currentMode = mode;
            const btnTemplate = document.getElementById('btn-mode-template');
            const btnCustom = document.getElementById('btn-mode-custom');

            if (mode === 'template') {
                btnTemplate.className = 'flex-1 text-center py-3 rounded-lg cursor-pointer font-semibold transition-colors bg-[var(--bg-card)] text-[var(--accent)] shadow';
                btnCustom.className = 'flex-1 text-center py-3 rounded-lg cursor-pointer font-semibold transition-colors text-gray-400 hover:text-white';
                document.getElementById('section-template').classList.remove('hidden');
                document.getElementById('section-custom').classList.add('hidden');
            } else {
                btnCustom.className = 'flex-1 text-center py-3 rounded-lg cursor-pointer font-semibold transition-colors bg-[var(--bg-card)] text-[var(--accent)] shadow';
                btnTemplate.className = 'flex-1 text-center py-3 rounded-lg cursor-pointer font-semibold transition-colors text-gray-400 hover:text-white';
                document.getElementById('section-template').classList.add('hidden');
                document.getElementById('section-custom').classList.remove('hidden');
                setTimeout(() => { if(editor) editor.refresh(); }, 50);
            }
        }
"""
content = re.sub(r'function setMode\(mode\) \{.*?\}', js_fix, content, flags=re.DOTALL)

with open('deploy.html', 'w') as f:
    f.write(content)
