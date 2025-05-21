// Fix for login navigation issues
document.addEventListener('DOMContentLoaded', function() {
  // Get the login form
  const loginForm = document.getElementById('login-form');
  
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Get form data
      const username = document.querySelector('input[name="username"]').value;
      const password = document.querySelector('input[name="password"]').value;
      
      console.log('Login attempt:', username);
      
      // Store user data in localStorage for demo purposes
      localStorage.setItem('user_role', username.toLowerCase().includes('editor') ? 'editor' : 
                          (username.toLowerCase().includes('music') ? 'music_director' : 'director'));
      localStorage.setItem('username', username);
      localStorage.setItem('is_logged_in', 'true');
      
      // Determine which dashboard to redirect to based on username
      let dashboardUrl = '/director/dashboard';
      if (username.toLowerCase().includes('editor')) {
        dashboardUrl = '/editor/dashboard';
      } else if (username.toLowerCase().includes('music')) {
        dashboardUrl = '/music_director/dashboard';
      }
      
      // Redirect to appropriate dashboard
      console.log('Redirecting to:', dashboardUrl);
      window.location.href = dashboardUrl;
    });
  } else {
    console.error('Login form not found');
  }
});
