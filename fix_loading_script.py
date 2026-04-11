import re

with open('dashboard.html', 'r') as f:
    content = f.read()

# Since the backend is external for local testing, the loader might stay forever if fetch fails due to CORS or local environment setup without the proxy.
# We need to make sure the fetch captures has a fallback to hide the loader so the UI can be previewed during errors or local testing
fetch_err_fix = """
            } catch (e) {
                console.error(e);
                document.getElementById('loader').style.display = 'none';
                document.getElementById('main-content').style.display = 'block';
                notify('Failed to load data from server', 'error');
            }
"""

content = re.sub(r'\} catch \(e\) \{\n                console.error\(e\);\n            \}', fetch_err_fix, content, flags=re.DOTALL)

with open('dashboard.html', 'w') as f:
    f.write(content)
