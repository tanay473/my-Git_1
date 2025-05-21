/* Theme toggle functionality */
document.addEventListener('DOMContentLoaded', function() {
    // Add theme toggle button to header
    const header = document.querySelector('.header-container');
    if (header) {
        const themeToggle = document.createElement('div');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = '<button id="theme-toggle-btn" class="theme-toggle-btn"><i class="fas fa-moon"></i></button>';
        themeToggle.style.marginLeft = '1rem';
        header.appendChild(themeToggle);
        
        // Set up theme toggle functionality
        const toggleBtn = document.getElementById('theme-toggle-btn');
        if (toggleBtn) {
            // Check if user has a theme preference stored
            const currentTheme = localStorage.getItem('theme') || 'dark';
            document.body.classList.add(`${currentTheme}-theme`);
            
            // Update button icon based on current theme
            toggleBtn.innerHTML = currentTheme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            
            // Add click event listener
            toggleBtn.addEventListener('click', function() {
                const isDark = document.body.classList.contains('dark-theme');
                
                if (isDark) {
                    document.body.classList.remove('dark-theme');
                    document.body.classList.add('light-theme');
                    localStorage.setItem('theme', 'light');
                    toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
                } else {
                    document.body.classList.remove('light-theme');
                    document.body.classList.add('dark-theme');
                    localStorage.setItem('theme', 'dark');
                    toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
                }
            });
        }
    }
});
