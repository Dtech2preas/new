import re

with open('dashboard.html', 'r') as f:
    content = f.read()

# Fix the renderData function to handle the empty state toggling cleanly with tailwind classes
render_data_js = """
        function renderData(items) {
            const desktopList = document.getElementById('desktop-list');
            const mobileList = document.getElementById('mobile-list');

            let userPlan = 'free';
            if (document.body.classList.contains('plan-gold')) userPlan = 'gold';
            else if (document.body.classList.contains('plan-premium')) userPlan = 'premium';
            else if (document.body.classList.contains('plan-basic')) userPlan = 'basic';

            desktopList.innerHTML = '';
            mobileList.innerHTML = '';

            const emptyMsg = document.getElementById('empty-msg');
            const desktopTable = document.querySelector('.desktop-table');

            if (items.length === 0) {
                if(emptyMsg) emptyMsg.classList.remove('hidden');
                if(desktopTable) desktopTable.classList.add('hidden');
                return;
            } else {
                if(emptyMsg) emptyMsg.classList.add('hidden');
                if(desktopTable) desktopTable.classList.remove('hidden');
            }

            items.forEach(item => {
"""
content = re.sub(r'function renderData\(items\) \{.*?items\.forEach\(item => \{', render_data_js, content, flags=re.DOTALL)

with open('dashboard.html', 'w') as f:
    f.write(content)
