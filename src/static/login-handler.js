// Login handler for Community Platform
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get username and password
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Determine role based on username (for demo purposes)
            let role = 'director'; // Default role
            
            if (username.includes('editor')) {
                role = 'editor';
            } else if (username.includes('music')) {
                role = 'music_director';
            }
            
            // Store login info in localStorage
            localStorage.setItem('is_logged_in', 'true');
            localStorage.setItem('user_role', role);
            localStorage.setItem('username', username);
            
            // Redirect to appropriate dashboard
            window.location.href = `/${role}/dashboard`;
        });
    }
    
    // Check if already logged in
    const isLoggedIn = localStorage.getItem('is_logged_in') === 'true';
    const currentRole = localStorage.getItem('user_role');
    
    // If logged in and on login page, redirect to dashboard
    if (isLoggedIn && currentRole && window.location.pathname === '/login') {
        window.location.href = `/${currentRole}/dashboard`;
    }
});

// Logout functionality
function logout() {
    localStorage.removeItem('is_logged_in');
    localStorage.removeItem('user_role');
    localStorage.removeItem('username');
    window.location.href = '/login';
}

// Add logout button to all pages
document.addEventListener('DOMContentLoaded', function() {
    const navMenu = document.querySelector('.nav-menu');
    
    if (navMenu && localStorage.getItem('is_logged_in') === 'true') {
        const logoutItem = document.createElement('li');
        logoutItem.className = 'nav-item';
        
        const logoutLink = document.createElement('a');
        logoutLink.href = '#';
        logoutLink.className = 'nav-link logout-link';
        logoutLink.textContent = 'Logout';
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
        
        logoutItem.appendChild(logoutLink);
        navMenu.appendChild(logoutItem);
    }
});
