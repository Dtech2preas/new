with open("profile.html", "r") as f:
    content = f.read()

# Add a <script> block at the end to populate the profile data instead of dashboard script doing it.
script = """
    <script>
        document.addEventListener('DOMContentLoaded', async () => {
            const token = localStorage.getItem('sessionToken');
            if (!token) {
                window.location.href = 'index.html';
                return;
            }

            try {
                const response = await fetch('https://api.dtechgh.com/api/user/profile', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (response.ok) {
                    const data = await response.json();

                    const userAvatar = document.getElementById('userAvatar');
                    const profileAvatar = document.getElementById('profile-avatar-ui');
                    const initial = data.name ? data.name.charAt(0).toUpperCase() : '👤';

                    if (userAvatar) userAvatar.textContent = initial;
                    if (profileAvatar) profileAvatar.textContent = initial;

                    const profileName = document.getElementById('profile-name');
                    if (profileName) profileName.textContent = data.name || 'User';

                    const profileEmail = document.getElementById('profile-email');
                    if (profileEmail) profileEmail.textContent = data.email || 'No email provided';

                    const roleBadge = document.getElementById('profile-role');
                    if (roleBadge) {
                        roleBadge.textContent = (data.role || 'user').toUpperCase();
                        if (data.role === 'gold') {
                            roleBadge.className = 'role-badge mt-2 inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-yellow-500/10 border border-yellow-500/50 text-yellow-400 shadow-[0_0_10px_rgba(234,179,8,0.2)]';
                            document.getElementById('gold-features').classList.remove('hidden');
                        }
                    }

                    // Fetch Active Sites
                    const sitesResponse = await fetch('https://api.dtechgh.com/api/deployments/list', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });

                    if (sitesResponse.ok) {
                        const sitesData = await sitesResponse.json();
                        const sitesList = document.getElementById('sites-list');

                        if (sitesData.deployments && sitesData.deployments.length > 0) {
                            sitesList.innerHTML = sitesData.deployments.map(site => `
                                <div class="bg-[var(--bg-main)] border border-[var(--border)] rounded-xl p-4 flex items-center justify-between group transition-all duration-300 hover:border-blue-500/30">
                                    <div class="flex items-center gap-4">
                                        <div class="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-400 group-hover:scale-110 transition-transform">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path></svg>
                                        </div>
                                        <div>
                                            <h4 class="font-medium text-[var(--text-main)]"><a href="https://${site.url}" target="_blank" class="hover:text-blue-400 transition-colors">${site.url}</a></h4>
                                            <p class="text-xs text-[var(--text-muted)] mt-1 flex items-center gap-2">
                                                <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span> Active
                                                <span class="opacity-50">•</span>
                                                ${new Date(site.deployedAt).toLocaleDateString()}
                                            </p>
                                        </div>
                                    </div>
                                    <button class="p-2 text-gray-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors" title="Delete Deployment">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                    </button>
                                </div>
                            `).join('');
                        } else {
                            sitesList.innerHTML = `
                                <div class="text-center py-8 bg-[var(--bg-main)] border border-[var(--border)] rounded-xl">
                                    <div class="w-12 h-12 rounded-full bg-gray-500/10 flex items-center justify-center mx-auto mb-3">
                                        <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
                                    </div>
                                    <p class="text-[var(--text-muted)] text-sm">No active sites found.</p>
                                    <a href="deploy.html" class="inline-block mt-4 text-blue-400 text-sm hover:underline">Deploy a new site</a>
                                </div>
                            `;
                        }
                    }

                } else {
                    localStorage.removeItem('sessionToken');
                    window.location.href = 'index.html';
                }
            } catch (error) {
                console.error('Error fetching profile:', error);
            }
        });

        function logout() {
            localStorage.removeItem('sessionToken');
            window.location.href = 'index.html';
        }

        function clearSiteData() {
            if (confirm("Are you sure you want to clear all local data? You will be logged out.")) {
                localStorage.clear();
                window.location.href = 'index.html';
            }
        }
    </script>
</body>
</html>
"""

# Replace script at the bottom
script_start = content.rfind('<script src="dashboard.js"></script>')
if script_start != -1:
    content = content[:script_start] + script

    with open("profile.html", "w") as f:
        f.write(content)
