import re

with open('dashboard.html', 'r') as f:
    content = f.read()

# Make the timestamp appear in the data column for mobile by changing the generateSmartContent logic
# Wait, actually we can just output the date as part of the smart-header.

js_render = """
                // Desktop Row
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="hidden md:table-cell" style="white-space:nowrap; color:var(--text-sec); font-size:0.85rem;">${dateStr}</td>
                    <td>
                        <div class="md:hidden text-xs text-gray-500 mb-2">${dateStr}</div>
                        ${contentHTML}
                    </td>
                    <td><button onclick="deleteItem('${item.key}')" class="btn-delete">Delete</button></td>
                `;
                desktopList.appendChild(tr);
"""
# Replace the old desktop row injection
content = re.sub(r'// Desktop Row.*?desktopList\.appendChild\(tr\);', js_render.strip(), content, flags=re.DOTALL)

# Let's fix the CSS where we said `display: none` for first child
content = content.replace('.desktop-table th:first-child, .desktop-table td:first-child {\n                display: none; /* Hide timestamp column entirely to save space */\n            }', '')

# And let's hide the Timestamp column header on mobile
content = content.replace('<th width="20%">Timestamp</th>', '<th width="20%" class="hidden md:table-cell">Timestamp</th>')


with open('dashboard.html', 'w') as f:
    f.write(content)
