import re

for file in ['plans.html', 'profile.html']:
    with open(file, 'r') as f:
        content = f.read()

    # Remove intro.js script, css, and tour functions from plans and profile since they don't apply there anymore.
    content = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/intro\.js/7\.2\.0/intro\.min\.js"></script>', '', content)
    content = re.sub(r'<link href="https://cdnjs\.cloudflare\.com/ajax/libs/intro\.js/7\.2\.0/introjs\.min\.css" rel="stylesheet">', '', content)

    with open(file, 'w') as f:
        f.write(content)
