from playwright.sync_api import sync_playwright
import time
import os

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Inject session token
        page.add_init_script("""
            localStorage.setItem('sessionToken', 'dummy_token');
        """)

        pwd = os.getcwd()

        # View dashboard
        page.goto(f'file://{pwd}/dashboard.html')
        time.sleep(2)
        page.screenshot(path='dashboard_verified.png', full_page=True)

        # View plans
        page.goto(f'file://{pwd}/plans.html')
        time.sleep(2)
        page.screenshot(path='plans_verified.png', full_page=True)

        browser.close()

verify_frontend()
