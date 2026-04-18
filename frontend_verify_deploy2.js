const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3002;

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
    const context = await browser.newContext();
    const page = await context.newPage();

    // Add local storage setup before navigating
    await page.addInitScript(() => {
        window.localStorage.setItem('user_code', 'test_user_code');
        window.localStorage.setItem('session_token', 'test_session_token');
        window.localStorage.setItem('deploy_ad_pass', 'true');

        // Mock fetch locally to simulate available subdomain
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
                    plan: 'free',
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
            return originalFetch.apply(this, arguments);
        };
    });

    console.log('Navigating to deploy.html');
    await page.goto(`http://localhost:${PORT}/deploy.html`);

    // Type a subdomain that will trigger the mocked "available" response
    await page.fill('#subdomain', 'available-subdomain');

    // Wait for the message to appear
    await page.waitForTimeout(2000); // give debounce and fetch time to complete

    console.log('Taking screenshot of available subdomain state');
    await page.screenshot({ path: 'deploy_available_state.png', fullPage: true });

    await browser.close();
    server.close();
});
