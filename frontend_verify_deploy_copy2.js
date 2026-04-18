const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3006;

// Simple static server
const server = http.createServer((req, res) => {
    let filePath = path.join(__dirname, req.url === '/' ? 'deploy.html' : req.url);
    if (!fs.existsSync(filePath)) {
        res.writeHead(404);
        res.end('Not Found');
        return;
    }
    const ext = path.extname(filePath);
    let contentType = 'text/html';
    if (ext === '.js') contentType = 'text/javascript';
    if (ext === '.css') contentType = 'text/css';
    if (ext === '.png') contentType = 'image/png';
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(fs.readFileSync(filePath));
});

server.listen(PORT, async () => {
    console.log(`Server running on port ${PORT}`);
    const browser = await chromium.launch({ headless: true });
    // Need to grant clipboard permissions to test copy to clipboard functionality
    const context = await browser.newContext();
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
    const page = await context.newPage();

    let pageErrors = [];
    page.on('pageerror', error => {
        console.error('Page error:', error.message);
        pageErrors.push(error.message);
    });

    // Add local storage setup before navigating
    await page.addInitScript(() => {
        window.localStorage.setItem('user_code', 'test_user_code');
        window.localStorage.setItem('session_token', 'test_session_token');
        window.localStorage.setItem('deploy_ad_pass', 'true');

        // Mock fetch locally
        const originalFetch = window.fetch;
        window.fetch = async function() {
            if (arguments[0].includes('/api/public/check-subdomain')) {
                return new Response(JSON.stringify({
                    success: true,
                    available: true,
                    ownedByYou: false
                }), {
                    status: 200,
                    headers: { 'Content-type': 'application/json' }
                });
            }
            if (arguments[0].includes('/api/public/captures')) {
                return new Response(JSON.stringify({
                    success: true,
                    plan: 'gold', // use gold plan to avoid ad overlay intercepting clicks
                    siteCount: 0
                }), {
                    status: 200,
                    headers: { 'Content-type': 'application/json' }
                });
            }
            if (arguments[0].includes('/api/public/templates')) {
                return new Response(JSON.stringify({
                    success: true,
                    data: ['Test Template']
                }), {
                    status: 200,
                    headers: { 'Content-type': 'application/json' }
                });
            }
            if (arguments[0].includes('/api/public/deploy')) {
                return new Response(JSON.stringify({
                    success: true,
                    url: 'https://test-subdomain.vercel.app'
                }), {
                    status: 200,
                    headers: { 'Content-type': 'application/json' }
                });
            }
            return originalFetch.apply(this, arguments);
        };
    });

    console.log('Navigating to deploy.html');
    await page.goto(`http://localhost:${PORT}/deploy.html`);

    // Type a subdomain that will trigger the mocked "available" response
    await page.fill('#subdomain', 'test-subdomain');

    // Wait for the message to appear
    await page.waitForTimeout(1000);

    // Select template
    await page.click('.template-card');

    // Wait for it to select
    await page.waitForTimeout(500);

    // Click deploy
    await page.click('#deployBtn');

    // Wait for the deploy process
    await page.waitForTimeout(2000);

    // Click the copy URL button in the success modal
    await page.click('#success-modal button:has(svg)');

    await page.waitForTimeout(500);

    if (pageErrors.length > 0) {
        console.error("TEST FAILED: Found errors on page:", pageErrors);
    } else {
        console.log("TEST PASSED: No page errors detected.");
    }

    await browser.close();
    server.close();
});
