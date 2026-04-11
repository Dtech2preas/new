import re

with open('dashboard.html', 'r') as f:
    content = f.read()

# Make sure Intro.js starts properly if the user is new (check localStorage)
tour_js = """
        // --- TOUR ---
        function startTour() {
            introJs().setOptions({
                steps: [
                    {
                        title: 'Welcome to Dashboard',
                        intro: 'This is where you manage your deployments and captured data.'
                    },
                    {
                        element: document.querySelector('#tour-stats'),
                        intro: 'Keep track of how many sites you have active and total data captured.'
                    },
                    {
                        element: document.querySelector('#tour-deploy'),
                        intro: 'Click here to deploy a new capture site using templates or custom HTML.'
                    },
                    {
                        element: document.querySelector('#tour-data'),
                        intro: 'All submitted data appears here. You can search, filter by site, and copy individual fields.'
                    }
                ],
                showProgress: true,
                showBullets: false
            }).start();
        }

        // Auto-start tour for new users
        if (!localStorage.getItem('tour_completed')) {
            setTimeout(() => {
                startTour();
                localStorage.setItem('tour_completed', 'true');
            }, 1500);
        }
"""
content = content.replace('// --- TOUR ---', tour_js)

# Ensure infinite scroll on mobile. We will add an intersection observer to the bottom of the list
infinite_scroll_html = """
            <div id="empty-msg" class="hidden py-16 text-center border border-dashed border-gray-700 rounded-2xl bg-black/20">
                <svg class="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
                <h3 class="text-lg font-medium text-gray-300 mb-1">No captures found</h3>
                <p class="text-sm text-gray-500 mb-4">Deploy a site and share the link to start collecting data.</p>
                <a href="deploy.html" class="inline-block px-4 py-2 bg-[var(--bg-card)] border border-[var(--border)] text-sm font-medium rounded-lg hover:border-[var(--accent)] transition-colors">Deploy Now</a>
            </div>
            <!-- Intersection Observer target for infinite scroll -->
            <div id="scroll-target" class="h-10 w-full"></div>
"""
content = re.sub(r'<div id="empty-msg".*?</div>', infinite_scroll_html, content, flags=re.DOTALL)

infinite_scroll_js = """
        // Infinite Scroll Setup
        let isLoadingMore = false;
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !isLoadingMore && currentPage < totalPages) {
                isLoadingMore = true;
                changePage(1);
            }
        }, { rootMargin: '100px' });

        document.addEventListener('DOMContentLoaded', () => {
            // ... existing DOMContentLoaded code ...
            const target = document.getElementById('scroll-target');
            if(target) observer.observe(target);
        });
"""
content = content.replace('const itemsPerPage = 10;', 'const itemsPerPage = 10;\n' + infinite_scroll_js)

# Modify changePage to handle appending vs replacing
change_page_js = """
        function changePage(delta) {
            const newPage = currentPage + delta;
            if (newPage > 0 && newPage <= totalPages) {
                fetchCaptures(newPage, delta > 0); // pass isAppend flag
            }
        }
"""
content = re.sub(r'function changePage\(delta\) \{.*?\}', change_page_js, content, flags=re.DOTALL)

fetch_captures_js = """
        async function fetchCaptures(page = 1, isAppend = false) {
            try {
                // ... fetch logic ...
                const res = await fetch(`${WORKER_URL}/api/public/captures?code=${encodeURIComponent(userCode)}&page=${page}&limit=${itemsPerPage}`);
                const result = await res.json();

                document.getElementById('loader').style.display = 'none';
                document.getElementById('main-content').style.display = 'block';

                if (!result.success && result.error === "Account Locked") {
                    handleLocked(result.accountStatus);
                    return;
                }

                if (result.success) {
                    currentUserData = result;
                    if (isAppend) {
                        currentData = currentData.concat(result.data);
                    } else {
                        currentData = result.data;
                        currentPage = page; // Reset if not appending
                    }

                    currentPage = page;
                    isLoadingMore = false;

                    const sites = result.sites || [];

                    if (result.pagination) {
                        totalPages = result.pagination.totalPages;
                        updatePaginationUI(result.pagination);
                    } else {
                        totalPages = 1;
                        document.getElementById('pagination-controls').style.display = 'none';
                    }

                    updateUI(result);
                    if(!isAppend) {
                        renderSites(sites);
                        populateFilter(sites);
                    }
                    renderData(currentData);

                    if (result.plan === 'free') {
                        triggerAds();
                    }
                } else {
                    notify(result.error || 'Failed to load data', 'error');
                }
            } catch (e) {
                console.error(e);
            }
        }
"""
content = re.sub(r'async function fetchCaptures\(page = 1\) \{.*?catch \(e\) \{.*?\}', fetch_captures_js, content, flags=re.DOTALL)


with open('dashboard.html', 'w') as f:
    f.write(content)
