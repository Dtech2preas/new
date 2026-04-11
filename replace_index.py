import re

with open('index.html', 'r') as f:
    content = f.read()

# Add Tailwind and Google Fonts
head_additions = """
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #050505;
            color: #ffffff;
        }

        .glass-card {
            background: rgba(17, 17, 17, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .input-glow:focus {
            box-shadow: 0 0 0 2px rgba(0, 112, 243, 0.3);
            border-color: #0070f3;
        }

        .tab-btn {
            position: relative;
        }

        .tab-btn::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: #0070f3;
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .tab-btn.active::after {
            transform: scaleX(1);
        }

        .tab-btn.active {
            color: #0070f3;
        }

        /* Toast Notification */
        #toast {
            visibility: hidden;
            min-width: 250px;
            background-color: #333;
            color: #fff;
            text-align: center;
            border-radius: 8px;
            padding: 16px;
            position: fixed;
            z-index: 50;
            bottom: 30px;
            right: 30px;
            opacity: 0;
            transition: opacity 0.3s, bottom 0.3s, visibility 0.3s;
            border-left: 4px solid #0070f3;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        }

        #toast.show {
            visibility: visible;
            opacity: 1;
            bottom: 50px;
        }

        #toast.success { border-color: #10b981; }
        #toast.error { border-color: #ef4444; }
    </style>
"""

content = re.sub(r'<style>[\s\S]*?</style>', head_additions, content)

# Remove the old container class and style with Tailwind
content = content.replace('<div class="container">', '<div class="glass-card w-full max-w-md p-8 md:p-10 rounded-2xl shadow-2xl relative animate-[fadeIn_0.5s_ease-out]">')

# Typography
content = content.replace('<h1>D-TECH CLOUD</h1>', '<h1 class="text-3xl font-extrabold text-[#0070f3] mb-1 tracking-tight">D-TECH CLOUD</h1>')
content = content.replace('<p class="subtitle">Secure Deployment Platform</p>', '<p class="text-gray-400 text-sm mb-8 font-medium">Secure Deployment Platform</p>')

# Tabs
content = content.replace('<div class="tabs">', '<div class="flex mb-8 border-b border-gray-800">')
content = content.replace('class="tab-btn active"', 'class="tab-btn active flex-1 py-3 text-center text-sm font-semibold text-gray-500 hover:text-white transition-colors cursor-pointer outline-none"')
content = content.replace('class="tab-btn"', 'class="tab-btn flex-1 py-3 text-center text-sm font-semibold text-gray-500 hover:text-white transition-colors cursor-pointer outline-none"')

# Form inputs
content = content.replace('<div class="input-group">', '<div class="mb-5 text-left">')
content = content.replace('<label>', '<label class="block mb-2 text-xs font-bold text-gray-500 uppercase tracking-wider">')
content = content.replace('<input type="text"', '<input type="text" class="w-full px-4 py-3 bg-[#0a0a0a] border border-gray-800 rounded-xl text-white text-sm outline-none transition-all input-glow"')
content = content.replace('<input type="password"', '<input type="password" class="w-full px-4 py-3 bg-[#0a0a0a] border border-gray-800 rounded-xl text-white text-sm outline-none transition-all input-glow"')

# Checkboxes
content = content.replace('<div class="checkbox-group">', '<div class="flex items-center mb-6 text-sm text-gray-400">')
content = content.replace('<input type="checkbox"', '<input type="checkbox" class="w-4 h-4 text-[#0070f3] bg-gray-900 border-gray-700 rounded focus:ring-[#0070f3] focus:ring-2 accent-[#0070f3] mr-2"')
content = content.replace('<label for="login-remember">', '<label for="login-remember" class="font-medium cursor-pointer">')

# Buttons
content = content.replace('class="btn btn-primary"', 'class="w-full py-3.5 bg-[#0070f3] hover:bg-[#005bb5] text-white font-semibold rounded-xl transition-all transform hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed mt-2"')
content = content.replace('class="btn btn-secondary"', 'class="w-full py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white font-semibold rounded-xl transition-all mt-2 text-sm"')

# Errors
content = content.replace('class="error-msg"', 'class="error-msg text-red-500 text-sm mb-4 hidden bg-red-500/10 p-3 rounded-lg border border-red-500/20"')

# Display code
content = content.replace('class="code-display"', 'class="code-display bg-[#1a1a1a] border border-dashed border-[#0070f3] p-4 rounded-xl my-6 break-all font-mono text-lg text-[#0070f3] relative cursor-pointer hover:bg-[#222] transition-colors"')
content = content.replace('class="warning-text"', 'class="warning-text text-amber-500 text-xs mt-3 leading-relaxed text-left bg-amber-500/10 p-3 rounded-lg border border-amber-500/20"')

# Footer
content = content.replace('<div class="footer">', '<div class="mt-8 pt-6 border-t border-gray-800 text-xs text-gray-500 font-medium">')

# Add Toast HTML
toast_html = """
    <!-- Toast Notification -->
    <div id="toast">Message</div>
"""
content = content.replace('</body>', toast_html + '\n</body>')

# Update alert to use toast
content = content.replace("alert('Code copied!')", "showToast('Code copied to clipboard!', 'success')")

# Add toast JS
toast_js = """
        function showToast(message, type = 'success') {
            const toast = document.getElementById('toast');
            toast.innerText = message;
            toast.className = ''; // Reset classes
            toast.classList.add('show', type);

            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }
"""
content = content.replace('// Helpers', '// Helpers\n' + toast_js)

with open('index.html', 'w') as f:
    f.write(content)
