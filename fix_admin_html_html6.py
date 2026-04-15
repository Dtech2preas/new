with open("admin.html", "r") as f:
    content = f.read()

search_html = """
        <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <input type="text" id="user-search" placeholder="Search users by name or code..." style="padding: 10px; width: 100%; max-width: 400px; border-radius: 6px; border: 1px solid #ddd;">
        </div>
"""
content = content.replace('<div id="users-container">', f'{search_html}\n<div id="users-container">')

with open("admin.html", "w") as f:
    f.write(content)
