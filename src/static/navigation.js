// Role-based navigation handler for Community Platform
document.addEventListener('DOMContentLoaded', function() {
  // Check if user is logged in
  const isLoggedIn = localStorage.getItem('is_logged_in') === 'true';
  const userRole = localStorage.getItem('user_role');
  
  if (isLoggedIn && userRole) {
    console.log('User is logged in with role:', userRole);
    setupRoleBasedNavigation(userRole);
  } else {
    console.log('User is not logged in');
  }
  
  // Handle main navigation links
  setupMainNavigation(isLoggedIn, userRole);
});

// Setup role-based navigation
function setupRoleBasedNavigation(role) {
  // Add role to body for CSS styling
  document.body.setAttribute('data-role', role);
  
  // Update header with role indicator
  const header = document.querySelector('.header');
  if (header) {
    const roleIndicator = document.createElement('div');
    roleIndicator.className = 'role-indicator';
    roleIndicator.textContent = formatRoleName(role);
    header.querySelector('.container').appendChild(roleIndicator);
  }
  
  // Add role-specific dashboard link if not present
  const navMenu = document.querySelector('.nav-menu');
  if (navMenu) {
    let dashboardLink = navMenu.querySelector('.dashboard-link');
    if (!dashboardLink) {
      dashboardLink = document.createElement('li');
      dashboardLink.className = 'nav-item dashboard-link';
      const link = document.createElement('a');
      link.className = 'nav-link';
      link.textContent = 'Dashboard';
      link.href = `/${role}/dashboard`;
      dashboardLink.appendChild(link);
      navMenu.appendChild(dashboardLink);
    } else {
      const link = dashboardLink.querySelector('a');
      if (link) {
        link.href = `/${role}/dashboard`;
      }
    }
  }
}

// Setup main navigation links to respect user role
function setupMainNavigation(isLoggedIn, role) {
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    const originalHref = link.getAttribute('href');
    
    // Skip login/register links
    if (originalHref === '/login' || originalHref === '/register') {
      return;
    }
    
    link.addEventListener('click', function(e) {
      // If user is not logged in, redirect to login
      if (!isLoggedIn && originalHref !== '/') {
        e.preventDefault();
        window.location.href = '/login';
        return;
      }
      
      // For community, workspaces, profile links, ensure they go to role-specific versions
      if (isLoggedIn && role && (originalHref === '/community' || originalHref === '/workspaces' || originalHref === '/profile')) {
        e.preventDefault();
        
        // Determine correct path based on role and original destination
        let path;
        if (originalHref === '/community') {
          path = `/${role}/community`;
        } else if (originalHref === '/workspaces') {
          path = `/${role}/workspaces`;
        } else if (originalHref === '/profile') {
          path = `/${role}/profile`;
        }
        
        // Navigate to role-specific path
        window.location.href = path;
      }
    });
  });
}

// Format role name for display
function formatRoleName(role) {
  if (role === 'music_director') {
    return 'Music Director';
  }
  return role.charAt(0).toUpperCase() + role.slice(1);
}

// Handle sidebar navigation within dashboards
function setupSidebarNavigation(role) {
  const sidebarLinks = document.querySelectorAll('.sidebar-link');
  
  sidebarLinks.forEach(link => {
    const originalHref = link.getAttribute('href');
    
    // Ensure sidebar links respect the current role
    if (originalHref && originalHref.startsWith('#')) {
      // These are internal page links, no change needed
    } else if (originalHref) {
      // External links should include role in path
      link.setAttribute('href', `/${role}${originalHref}`);
    }
  });
}

// Function to get current user role from localStorage
function getCurrentUserRole() {
  return localStorage.getItem('user_role') || 'director'; // Default to director if not set
}

// Function to navigate to role-specific dashboard
function goToDashboard() {
  const role = getCurrentUserRole();
  window.location.href = `/${role}/dashboard`;
}

// Function to navigate to role-specific page
function navigateToRolePage(page) {
  const role = getCurrentUserRole();
  window.location.href = `/${role}/${page}`;
}
