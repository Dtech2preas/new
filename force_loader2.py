import re

with open('dashboard.html', 'r') as f:
    content = f.read()

# Force override for visual test
force_hide = """
        // Init
        document.addEventListener('DOMContentLoaded', async () => {
            // Force hide loader for verification purposes
            document.getElementById('loader').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
"""
content = content.replace("// Init\n        document.addEventListener('DOMContentLoaded', async () => {\n            // Force hide loader for verification purposes\n            setTimeout(() => {\n                const l = document.getElementById('loader');\n                const m = document.getElementById('main-content');\n                if(l) l.style.display = 'none';\n                if(m) m.style.display = 'block';\n            }, 1000);", force_hide)

with open('dashboard.html', 'w') as f:
    f.write(content)
