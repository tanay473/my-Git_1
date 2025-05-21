// Profile and logout functionality for Community Platform
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    const isLoggedIn = localStorage.getItem('is_logged_in') === 'true';
    const username = localStorage.getItem('username');
    const userRole = localStorage.getItem('user_role');
    
    if (isLoggedIn && username && userRole) {
        // Add logout button to navigation
        addLogoutButton();
        
        // Update profile link to show current user info
        updateProfileDisplay(username, userRole);
    }
});

// Add visible logout button to navigation
function addLogoutButton() {
    const navMenu = document.querySelector('.nav-menu');
    
    if (navMenu) {
        // Check if logout button already exists
        if (!document.querySelector('.logout-btn')) {
            // Create logout list item
            const logoutItem = document.createElement('li');
            logoutItem.className = 'nav-item';
            
            // Create logout button
            const logoutBtn = document.createElement('a');
            logoutBtn.href = '#';
            logoutBtn.className = 'nav-link logout-btn';
            logoutBtn.innerHTML = '<i class="fas fa-sign-out-alt"></i> Logout';
            logoutBtn.style.color = '#fff';
            logoutBtn.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
            logoutBtn.style.borderRadius = '4px';
            logoutBtn.style.padding = '8px 15px';
            
            // Add click event
            logoutBtn.addEventListener('click', function(e) {
                e.preventDefault();
                logout();
            });
            
            // Append to navigation
            logoutItem.appendChild(logoutBtn);
            navMenu.appendChild(logoutItem);
        }
    }
}

// Update profile display with user info
function updateProfileDisplay(username, role) {
    // Find profile link
    const profileLink = document.querySelector('.profile-link');
    
    if (profileLink) {
        // Create profile display container
        const profileDisplay = document.createElement('div');
        profileDisplay.className = 'profile-display';
        profileDisplay.style.display = 'flex';
        profileDisplay.style.alignItems = 'center';
        
        // Create avatar
        const avatar = document.createElement('div');
        avatar.className = 'profile-avatar';
        avatar.style.width = '24px';
        avatar.style.height = '24px';
        avatar.style.borderRadius = '50%';
        avatar.style.backgroundColor = '#fff';
        avatar.style.marginRight = '8px';
        avatar.style.display = 'flex';
        avatar.style.alignItems = 'center';
        avatar.style.justifyContent = 'center';
        avatar.style.fontSize = '12px';
        avatar.style.fontWeight = 'bold';
        avatar.style.color = '#4a6da7';
        avatar.textContent = username.charAt(0).toUpperCase();
        
        // Update profile link text and add avatar
        profileLink.innerHTML = '';
        profileLink.appendChild(avatar);
        profileLink.appendChild(document.createTextNode('Profile'));
        
        // Add tooltip with user info
        profileLink.title = `${username} (${formatRoleName(role)})`;
    }
}

// Format role name for display
function formatRoleName(role) {
    if (role === 'music_director') {
        return 'Music Director';
    }
    return role.charAt(0).toUpperCase() + role.slice(1);
}

// Logout function
function logout() {
    // Show logout confirmation
    const confirmLogout = confirm('Are you sure you want to logout?');
    
    if (confirmLogout) {
        // Clear user data from localStorage
        localStorage.removeItem('is_logged_in');
        localStorage.removeItem('user_role');
        localStorage.removeItem('username');
        
        // Show logout message
        const logoutMessage = document.createElement('div');
        logoutMessage.className = 'logout-message';
        logoutMessage.style.position = 'fixed';
        logoutMessage.style.top = '50%';
        logoutMessage.style.left = '50%';
        logoutMessage.style.transform = 'translate(-50%, -50%)';
        logoutMessage.style.padding = '20px';
        logoutMessage.style.backgroundColor = '#fff';
        logoutMessage.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        logoutMessage.style.borderRadius = '8px';
        logoutMessage.style.zIndex = '9999';
        logoutMessage.style.textAlign = 'center';
        logoutMessage.innerHTML = '<p>Logging out...</p>';
        
        document.body.appendChild(logoutMessage);
        
        // Redirect to login page after short delay
        setTimeout(function() {
            window.location.href = '/login';
        }, 1000);
    }
}
