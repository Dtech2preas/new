import os

# Let's add basic spinners and skeletons CSS.
loading_css = """
<style>
/* Spinner */
.spinner {
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-left-color: #ffffff;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
    display: inline-block;
    vertical-align: middle;
    margin-right: 8px;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

/* Skeleton */
.skeleton {
    background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%);
    background-size: 200% 100%;
    animation: skeleton-loading 1.5s infinite;
    border-radius: 4px;
}
@keyframes skeleton-loading { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
</style>
"""

files_to_update = ['dashboard.html', 'deploy.html', 'profile.html', 'plans.html', 'admin.html', 'captures.html']

for filename in files_to_update:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()

        if ".spinner {" not in content:
            content = content.replace("</head>", f"{loading_css}\n</head>")

            with open(filename, 'w') as f:
                f.write(content)
