import re

with open("captures.html", "r") as f:
    content = f.read()

# 1. Add search bar and pagination controls
search_html = """
        <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
            <input type="text" id="capture-search" placeholder="Search captures..." style="padding: 10px; width: 100%; max-width: 400px; border-radius: 6px; border: 1px solid #ddd;">
            <div>
                <button id="prev-page" style="padding: 8px 12px; background: #eee; border: 1px solid #ddd; cursor: pointer; border-radius: 4px;">&laquo; Prev</button>
                <span id="page-info" style="margin: 0 10px; font-weight: bold;">Page 1</span>
                <button id="next-page" style="padding: 8px 12px; background: #eee; border: 1px solid #ddd; cursor: pointer; border-radius: 4px;">Next &raquo;</button>
            </div>
        </div>
"""
if 'id="capture-search"' not in content:
    content = content.replace("<div id=\"loading\">Loading data...</div>", f"<div id=\"loading\">Loading data...</div>\n{search_html}")

# 2. Add pagination and search logic to JS
js_logic = """
        let allCaptures = [];
        let filteredCaptures = [];
        let currentPage = 1;
        const itemsPerPage = 20;

        function renderTable() {
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';

            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const pageData = filteredCaptures.slice(start, end);

            if (filteredCaptures.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5" class="empty">No captured data found.</td></tr>`;
                document.getElementById('page-info').innerText = 'Page 1 of 1';
                return;
            }

            const totalPages = Math.ceil(filteredCaptures.length / itemsPerPage) || 1;
            document.getElementById('page-info').innerText = `Page ${currentPage} of ${totalPages}`;

            pageData.forEach(cap => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><code>${cap.siteKey}</code></td>
                    <td><code>${cap.captureId || 'N/A'}</code></td>
                    <td><div class="timestamp">${new Date(cap.timestamp).toLocaleString()}</div></td>
                    <td>${cap.ip}</td>
                    <td><pre>${JSON.stringify(cap.payload, null, 2)}</pre></td>
                `;
                tbody.appendChild(tr);
            });
        }

        document.getElementById('capture-search').addEventListener('input', function(e) {
            const term = e.target.value.toLowerCase();
            filteredCaptures = allCaptures.filter(cap => {
                const searchStr = JSON.stringify(cap).toLowerCase();
                return searchStr.includes(term);
            });
            currentPage = 1;
            renderTable();
        });

        document.getElementById('prev-page').addEventListener('click', () => {
            if (currentPage > 1) { currentPage--; renderTable(); }
        });

        document.getElementById('next-page').addEventListener('click', () => {
            const totalPages = Math.ceil(filteredCaptures.length / itemsPerPage);
            if (currentPage < totalPages) { currentPage++; renderTable(); }
        });
"""

# Modify loadData to use this
if "let allCaptures = []" not in content:
    # Need to intercept the assignment in loadData
    content = content.replace("const data = await res.json();", "const data = await res.json();\nallCaptures = data.captures || [];\nfilteredCaptures = [...allCaptures];\ncurrentPage = 1;")
    content = content.replace("data.captures.forEach(cap => {", "renderTable();\n/*")
    content = content.replace("tbody.appendChild(tr);", "tbody.appendChild(tr);\n*/")

    # insert js_logic before function loadData
    content = content.replace("async function loadData() {", f"{js_logic}\n\n        async function loadData() {{")

with open("captures.html", "w") as f:
    f.write(content)
