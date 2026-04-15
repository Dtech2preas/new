with open("admin.html", "r") as f:
    content = f.read()

# I messed up my replace regex and put it in multiple places where <style> was.
# Let's clean it up.

# Wait, `stats-grid` is only in the CSS. Where is the HTML?
