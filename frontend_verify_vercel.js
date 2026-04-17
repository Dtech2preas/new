const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    let filePath = '.' + req.url;
    if (filePath == './') filePath = './deploy.html';
    const extname = String(path.extname(filePath)).toLowerCase();
    const mimeTypes = {
        '.html': 'text/html',
        '.js': 'text/javascript',
        '.css': 'text/css',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
    };
    const contentType = mimeTypes[extname] || 'application/octet-stream';
    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code == 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end('404', 'utf-8');
            } else {
                res.writeHead(500);
                res.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(3000, async () => {
    console.log('Server running on port 3000');

    // Setup Playwright
    const browser = await chromium.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();

    await page.addInitScript(() => {
        window.localStorage.setItem('user_code', 'test-user-code');
        window.localStorage.setItem('session_token', 'test-session-token');
        window.localStorage.setItem('tour_completed', 'true');
        window.localStorage.setItem('deploy_ad_pass', 'true'); // bypass deploy ad
    });

    await page.route('**/*/api/public/captures*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                plan: 'premium',
                total: 0,
                hidden: 0,
                siteCount: 0,
                data: [],
                sites: [],
                activityLog: []
            })
        });
    });

    await page.route('**/*/api/public/templates*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                data: ['Template A', 'Template B']
            })
        });
    });

    await page.route('**/*/api/public/check-subdomain*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                available: true
            })
        });
    });

    await page.route('**/*/api/public/deploy*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                url: 'https://test-subdomain.vercel.app'
            })
        });
    });


    console.log("Navigating to deploy.html");
    await page.goto('http://localhost:3000/deploy.html');
    await page.waitForLoadState('networkidle');

    // Type subdomain
    console.log("Typing subdomain");
    await page.fill('#subdomain', 'test-subdomain');
    await page.waitForTimeout(1000); // Wait for debounce and API

    console.log("Taking screenshot of deploy.html before deploy");
    await page.screenshot({ path: 'deploy_test_before.png' });

    // Select template
    console.log("Selecting template");
    await page.click('.template-card');

    // Click deploy
    console.log("Clicking deploy");
    await page.click('#deployBtn');

    // Wait for modal
    await page.waitForTimeout(2000);

    console.log("Taking screenshot of deploy.html after deploy");
    await page.screenshot({ path: 'deploy_test_after.png' });

    console.log("Navigating to dashboard.html");
    await page.route('**/*/api/public/captures*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                plan: 'premium',
                total: 0,
                hidden: 0,
                siteCount: 1,
                data: [],
                sites: [{ subdomain: 'test-subdomain', vercelUrl: 'https://test-subdomain.vercel.app' }],
                activityLog: []
            })
        });
    });
    await page.goto('http://localhost:3000/dashboard.html');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'dashboard_test_vercel.png' });

    console.log("Navigating to profile.html");
    await page.goto('http://localhost:3000/profile.html');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'profile_test_vercel.png' });

    await browser.close();
    server.close();
    process.exit(0);
});
