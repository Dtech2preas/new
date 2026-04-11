import re

with open('dashboard.html', 'r') as f:
    content = f.read()

# Let's completely remove the loading screen for testing to see what's rendering.
# It seems my previous fixes might have failed because the loader uses display flex, so block/none might be acting weird depending on execution order.
content = content.replace('<div id="loader"', '<div id="loader" style="display:none !important;"')

with open('dashboard.html', 'w') as f:
    f.write(content)
