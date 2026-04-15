import os
import re

toast_css = """
<style>
/* Toast Container */
#toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* Toast Element */
.custom-toast {
    background: rgba(17, 17, 17, 0.9);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: white;
    padding: 16px 24px;
    border-radius: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    opacity: 0;
    transform: translateX(100%);
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.custom-toast.show {
    opacity: 1;
    transform: translateX(0);
}

.custom-toast.success { border-left: 4px solid #17c964; }
.custom-toast.error { border-left: 4px solid #f31260; }
.custom-toast.warning { border-left: 4px solid #f5a524; }
</style>
<div id="toast-container"></div>
<script>
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;

    let icon = '✅';
    if(type === 'error') icon = '❌';
    if(type === 'warning') icon = '⚠️';

    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
</script>
"""

files_to_update = ['index.html', 'dashboard.html', 'deploy.html', 'profile.html', 'plans.html', 'admin-login.html', 'admin.html', 'captures.html']

for filename in files_to_update:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()

        # Add toast_css right before </body>
        if "id=\"toast-container\"" not in content:
            content = content.replace("</body>", f"{toast_css}\n</body>")

        # Replace alert('msg') with showToast('msg')
        # Replace alert(e.message) with showToast(e.message, 'error')
        # We need to be careful with regex replacement for alert

        content = re.sub(r"alert\(\s*(['\"`][^'\"]+['\"`])\s*\)", r"showToast(\1)", content)
        content = re.sub(r"alert\(\s*([a-zA-Z0-9_.]+)\s*\)", r"showToast(\1)", content)

        with open(filename, 'w') as f:
            f.write(content)
