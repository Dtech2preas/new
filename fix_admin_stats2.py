import re

with open("admin.html", "r") as f:
    content = f.read()

# I see what I did wrong. The `stats-grid` was injected but it was probably outside the tab content.
# Let's check where it got injected by looking at the line before it.
