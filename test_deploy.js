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
            res.writeHead(404, { 'Content-Type': 'text/html' });
            res.end('404', 'utf-8');
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(3001, async () => {
    console.log('Server running on port 3001');

    const browser = await chromium.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();

    await page.addInitScript(() => {
        window.localStorage.setItem('user_code', 'test-user-code');
        window.localStorage.setItem('session_token', 'test-session-token');
    });

    await page.route('**/*/api/public/captures*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                plan: 'premium',
                siteCount: 0
            })
        });
    });

    await page.route('**/*/api/public/templates*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                data: [{ name: 'Test Template', isGoldOnly: false }]
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

    await page.route('**/*/api/public/deploy', async route => {
        console.log('Deploy API called!');
        // Keep it pending for 12 seconds to see the counter update
        setTimeout(() => {
            route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({
                    success: true,
                    url: 'https://test.vercel.app'
                })
            });
        }, 12000);
    });

    await page.goto('http://localhost:3001/deploy.html');
    await page.waitForLoadState('networkidle');

    await page.fill('#subdomain', 'test');
    await page.waitForTimeout(1000); // Wait for availability check

    await page.click('.template-card'); // Select template

    console.log("Clicking deploy...");
    await page.click('#deployBtn');

    // Take screenshots during the deploy
    await page.waitForTimeout(2000);
    console.log("Screenshot at 2s (Preparing files...)");
    await page.screenshot({ path: 'deploy_2s.png' });

    await page.waitForTimeout(5000);
    console.log("Screenshot at 7s (Pushing to Vercel...)");
    await page.screenshot({ path: 'deploy_7s.png' });

    await page.waitForTimeout(4000);
    console.log("Screenshot at 11s (Setting up alias...)");
    await page.screenshot({ path: 'deploy_11s.png' });

    await page.waitForTimeout(2000);
    console.log("Screenshot at 13s (Complete)");
    await page.screenshot({ path: 'deploy_done.png' });

    await browser.close();
    server.close();
    process.exit(0);
});
