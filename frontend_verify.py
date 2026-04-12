from playwright.sync_api import sync_playwright
import time

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Inject session token
        page.add_init_script("""
            localStorage.setItem('sessionToken', 'dummy_token');
        """)

        # View profile
        page.goto('file:///app/profile.html')
        time.sleep(2)
        page.screenshot(path='profile.png', full_page=True)

        browser.close()

verify_frontend()
