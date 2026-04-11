import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the modal layout which was broken when class="modal-overlay" was changed
modal_fix = """
    <!-- SET USERNAME MODAL -->
    <div class="modal-overlay hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-[1000] flex justify-center items-center" id="username-modal">
        <div class="glass-card p-8 rounded-2xl w-11/12 max-w-sm shadow-2xl border border-[var(--border)] relative">
            <h3 class="mt-0 text-xl font-bold text-[#0070f3] mb-2">Set Username</h3>
            <p class="text-gray-400 text-sm mb-6">To improve security, please set a username for your account.</p>
            <div id="modal-error" class="error-msg text-red-500 text-sm mb-4 hidden bg-red-500/10 p-3 rounded-lg border border-red-500/20"></div>
            <form onsubmit="handleSetUsername(event)">
                <div class="mb-5 text-left">
                    <label class="block mb-2 text-xs font-bold text-gray-500 uppercase tracking-wider">New Username</label>
                    <input type="text" id="modal-username" placeholder="Choose a username" minlength="3" required class="w-full px-4 py-3 bg-[#0a0a0a] border border-gray-800 rounded-xl text-white text-sm outline-none transition-all input-glow">
                </div>
                <button type="submit" class="w-full py-3.5 bg-[#0070f3] hover:bg-[#005bb5] text-white font-semibold rounded-xl transition-all transform hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed mt-2" id="btn-save-username">Save & Continue</button>
            </form>
        </div>
    </div>
"""

content = re.sub(r'<!-- SET USERNAME MODAL -->\n    <div class="modal-overlay" id="username-modal">.*?</div>\n    </div>', modal_fix, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
