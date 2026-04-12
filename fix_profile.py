import re

with open("profile.html", "r") as f:
    content = f.read()

# The clean main content block we want
main_content = """<main class="main-content">
        <!-- Top Navigation -->
        <header class="top-nav flex items-center justify-between">
            <h1 class="text-2xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-100 to-gray-400">Profile</h1>
            <div class="user-menu cursor-pointer transform hover:scale-105 transition-all duration-300" onclick="window.location.href='profile.html'">
                <div class="avatar shadow-lg shadow-blue-500/20" id="userAvatar">U</div>
            </div>
        </header>

        <div class="flex-1 p-6 lg:p-8 space-y-6">
            <!-- Account Settings Block -->
            <div class="glass-card p-6 border border-[var(--border)] rounded-2xl relative overflow-hidden group">
                <div class="absolute inset-0 bg-gradient-to-br from-[var(--accent)]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div class="relative z-10 flex flex-col gap-6">
                    <h3 class="text-xl font-bold tracking-tight">Account Settings</h3>
                    <div class="profile-card border border-[var(--border)] transition-colors duration-300 p-6 rounded-xl flex items-center gap-6" id="profile-card-ui">
                        <div class="profile-avatar w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold bg-[var(--bg-main)] border border-[var(--border)] text-[var(--accent)] shadow-lg" id="profile-avatar-ui">👤</div>
                        <div class="profile-info flex-1">
                            <h4 id="profile-name" class="text-lg font-semibold m-0 text-[var(--text-main)] transition-colors duration-300">Loading...</h4>
                            <p id="profile-email" class="text-sm text-[var(--text-muted)] m-0 mt-1 transition-colors duration-300">Loading...</p>
                            <span id="profile-role" class="role-badge mt-2 inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-[var(--bg-main)] border border-[var(--border)] text-[var(--accent)] shadow-sm">USER</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Data Retention -->
            <div class="glass-card p-6 border border-[var(--border)] rounded-2xl">
                <div class="flex items-center gap-4 mb-4">
                    <div class="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                    </div>
                    <h3 class="text-lg font-semibold">Data Retention</h3>
                </div>
                <div class="bg-[var(--bg-main)] border border-[var(--border)] rounded-xl p-4 flex items-center justify-between transition-colors duration-300 hover:border-purple-500/30">
                    <div>
                        <p class="font-medium text-white mb-1">Clear Local Storage</p>
                        <p class="text-sm text-gray-400">Removes cached data and preferences from this device.</p>
                    </div>
                    <button onclick="clearSiteData()" class="btn-secondary px-4 py-2 hover:bg-red-500/10 hover:text-red-400 hover:border-red-500/50 transition-all duration-300 group">
                        <span class="group-hover:hidden">Clear Data</span>
                        <span class="hidden group-hover:inline">Confirm?</span>
                    </button>
                </div>
            </div>

            <!-- Security Activity -->
            <div class="glass-card p-6 border border-[var(--border)] rounded-2xl">
                <div class="flex items-center gap-4 mb-4">
                    <div class="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                    </div>
                    <h3 class="text-lg font-semibold">Security Activity</h3>
                </div>
                <div class="space-y-3">
                    <div class="bg-[var(--bg-main)] border border-[var(--border)] rounded-xl p-4 transition-colors duration-300 hover:border-blue-500/30">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm font-medium text-white flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full bg-green-400"></span>
                                Current Session
                            </span>
                            <span class="text-xs text-gray-500" id="current-session-time">Just now</span>
                        </div>
                        <p class="text-sm text-gray-400 flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path></svg>
                            <span id="current-ip">Detecting...</span> • Web Browser
                        </p>
                    </div>
                </div>
            </div>

            <!-- Gold Features -->
            <div id="gold-features" class="hidden">
                <div class="glass-card p-6 border border-yellow-500/30 rounded-2xl relative overflow-hidden bg-gradient-to-br from-yellow-500/5 to-transparent">
                    <div class="absolute top-0 right-0 p-4 opacity-10">
                        <svg class="w-24 h-24 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"></path></svg>
                    </div>
                    <div class="relative z-10">
                        <div class="flex items-center gap-3 mb-4">
                            <span class="text-2xl">👑</span>
                            <h3 class="text-lg font-bold text-yellow-400 tracking-tight">Gold Features</h3>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="bg-black/20 border border-yellow-500/20 rounded-xl p-4 backdrop-blur-sm">
                                <h4 class="font-medium text-yellow-100 mb-1">Priority Support</h4>
                                <p class="text-sm text-yellow-200/60">24/7 dedicated assistance</p>
                            </div>
                            <div class="bg-black/20 border border-yellow-500/20 rounded-xl p-4 backdrop-blur-sm">
                                <h4 class="font-medium text-yellow-100 mb-1">Advanced Analytics</h4>
                                <p class="text-sm text-yellow-200/60">Deep insights into site traffic</p>
                            </div>
                            <div class="bg-black/20 border border-yellow-500/20 rounded-xl p-4 backdrop-blur-sm">
                                <h4 class="font-medium text-yellow-100 mb-1">Custom Domains</h4>
                                <p class="text-sm text-yellow-200/60">Connect unlimited domains</p>
                            </div>
                            <div class="bg-black/20 border border-yellow-500/20 rounded-xl p-4 backdrop-blur-sm">
                                <h4 class="font-medium text-yellow-100 mb-1">Zero Ads</h4>
                                <p class="text-sm text-yellow-200/60">Completely ad-free experience</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Active Sites List -->
            <div class="glass-card p-6 border border-[var(--border)] rounded-2xl relative overflow-hidden group">
                <div class="absolute inset-0 bg-gradient-to-br from-[var(--accent)]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div class="relative z-10">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h2 class="text-xl font-bold tracking-tight mb-1">Active Sites</h2>
                            <p class="text-sm text-[var(--text-muted)]">Manage your deployed websites</p>
                        </div>
                    </div>
                    <div class="space-y-4" id="sites-list">
                        <!-- Dynamic sites will be loaded here -->
                    </div>
                </div>
            </div>

            <button onclick="logout()" class="w-full mt-6 py-4 rounded-xl border border-red-500/30 text-red-400 font-medium hover:bg-red-500/10 hover:border-red-500/50 transition-all duration-300 flex items-center justify-center gap-2 group">
                <svg class="w-5 h-5 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
                Sign Out
            </button>
        </div>
    </main>
"""

# Extract the parts we want to keep
# 1. From top to end of sidebar
sidebar_end_idx = content.find('</aside>') + len('</aside>')
part1 = content[:sidebar_end_idx]

# 2. Add the main content
part2 = "\n" + main_content + "\n</div>\n"

# 3. Toast and scripts at the end
toast_idx = content.find('<div id="toast"')
part3 = content[toast_idx:]

new_content = part1 + part2 + part3

with open("profile.html", "w") as f:
    f.write(new_content)
