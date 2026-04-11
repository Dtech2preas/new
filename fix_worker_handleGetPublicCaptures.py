import re

with open('worker.js', 'r') as f:
    content = f.read()

# Add retentionDays to the output payload so the frontend can populate the select box
get_captures_update = """
        total: totalCount,
        hidden: hiddenCount,
        plan: user.plan,
        username: user.username,
        activityLog: user.activityLog || [],
        pendingPlan: user.pendingPlan,
        retentionDays: user.retentionDays || null,
        expiry: user.expiry,
"""
content = re.sub(r'total: totalCount,\n        hidden: hiddenCount,\n        plan: user.plan,\n        username: user.username,\n        activityLog: user.activityLog \|\| \[\],\n        pendingPlan: user.pendingPlan,\n        expiry: user.expiry,', get_captures_update, content)

with open('worker.js', 'w') as f:
    f.write(content)
