with open("admin.html", "r") as f:
    content = f.read()

# Let's see if the html is actually there
if '<div class="stats-grid">' in content:
    print("HTML exists")
else:
    print("HTML does NOT exist")
