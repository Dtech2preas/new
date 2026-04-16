const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    let filePath = '.' + req.url;
    if (filePath == './') filePath = './dashboard.html';
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

    // Inject mock user details and set tour_completed to true so overlay doesn't block clicks
    await page.addInitScript(() => {
        window.localStorage.setItem('user_code', 'test-user-code');
        window.localStorage.setItem('session_token', 'test-session-token');
        window.localStorage.setItem('tour_completed', 'true');
    });

    // We will intercept the fetch requests to the worker to simulate responses
    await page.route('**/*/api/public/captures*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                plan: 'free',
                total: 0,
                hidden: 0,
                siteCount: 0,
                data: [],
                sites: [],
                activityLog: []
            })
        });
    });

    console.log("Navigating to dashboard.html");
    await page.goto('http://localhost:3000/dashboard.html');
    await page.waitForLoadState('networkidle');

    console.log("Taking screenshot of dashboard");
    await page.screenshot({ path: 'dashboard_test.png' });

    console.log("Checking if trial banner exists");
    const banner = await page.$('#trial-banner');
    const isBannerVisible = await banner.isVisible();
    console.log('Trial Banner visible:', isBannerVisible);

    // Route for the trial API
    await page.route('**/*/api/auth/start-trial', route => {
        console.log('Start trial API called!');
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                user: { plan: 'premium', trial_used: true }
            })
        });
    });

    if (isBannerVisible) {
        console.log("Clicking claim trial button...");
        await page.click('#trial-banner button');
        await page.waitForTimeout(1000);
        console.log("Taking screenshot after claiming trial");
        await page.screenshot({ path: 'dashboard_after_trial.png' });
    }

    // Check Profile
    await page.route('**/*/api/public/captures*', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify({
                success: true,
                plan: 'premium', // now premium
                total: 0,
                hidden: 0,
                siteCount: 0,
                data: [],
                sites: [],
                user: {
                    name: 'Test User',
                    role: 'USER'
                }
            })
        });
    });

    console.log("Navigating to profile.html");
    await page.goto('http://localhost:3000/profile.html');
    await page.waitForLoadState('networkidle');
    console.log("Taking screenshot of profile");
    await page.screenshot({ path: 'profile_test.png' });

    console.log("Checking if residual clear button exists");
    const residualBtn = await page.$('button[onclick="clearResidualData()"]');
    console.log('Residual clear button exists:', !!residualBtn);

    await browser.close();
    server.close();
    process.exit(0);
});
