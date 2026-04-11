import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the CSS for hiding the tabs since I messed up the JS switchTab logic when removing custom classes
tab_css = """
        .form-section { display: none; }
        .form-section.active { display: block; animation: slideIn 0.3s ease; }

        @keyframes slideIn { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: translateX(0); } }
"""
content = content.replace('/* Toast Notification */', tab_css + '\n        /* Toast Notification */')

with open('index.html', 'w') as f:
    f.write(content)
