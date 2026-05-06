document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.menu-item');
    const sections = document.querySelectorAll('.content-section');

    // 1. Sidebar Tab Switching Logic
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Get the target section from data-section attribute
            const targetId = item.getAttribute('data-section');

            // Remove active status from all menu items
            menuItems.forEach(i => i.classList.remove('active'));
            // Hide all content sections
            sections.forEach(s => s.style.display = 'none');

            // Set current clicked item to active
            item.classList.add('active');
            
            // Show the corresponding section
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.style.display = 'block';
            }
        });
    });

    // 2. Theme Toggle
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            const icon = themeBtn.querySelector('i');
            icon.className = document.body.classList.contains('dark-theme') 
                ? 'ph-bold ph-sun' 
                : 'ph-bold ph-moon';
        });
    }
});