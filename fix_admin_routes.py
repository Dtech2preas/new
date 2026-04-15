with open("worker.js", "r") as f:
    content = f.read()

# We need to insert the new admin routes correctly.
# The previous replace failed because it looked for something that wasn't there in the exact format.

old_admin_routes = """        if (url.pathname === '/api/admin/users' && request.method === 'GET') {
             return respond(await handleGetUsers(env));
        }

        return respond(new Response("Not Found", { status: 404 }));"""

new_admin_routes = """        if (url.pathname === '/api/admin/users' && request.method === 'GET') {
             return respond(await handleGetUsers(env));
        }
        if (url.pathname === '/api/admin/analytics' && request.method === 'GET') {
            return respond(await handleAdminAnalytics(env));
        }
        if (url.pathname === '/api/admin/users/action' && request.method === 'POST') {
            return respond(await handleAdminUserAction(request, env));
        }

        return respond(new Response("Not Found", { status: 404 }));"""

content = content.replace(old_admin_routes, new_admin_routes)

with open("worker.js", "w") as f:
    f.write(content)
