with open("admin.html", "r") as f:
    content = f.read()

# Add a little padding to the top of the analytics
content = content.replace('<div class="stats-grid">', '<div class="stats-grid" style="margin-top: 20px;">')

# Ensure User Database search renders correctly by checking where the search bar was placed
if 'id="user-search"' in content:
    print("User search is in html")
else:
    print("User search missing")

with open("admin.html", "w") as f:
    f.write(content)
