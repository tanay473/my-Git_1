// Main JavaScript for Community Platform
document.addEventListener('DOMContentLoaded', function() {
  // Initialize role-based theming
  initializeRoleTheme();
  
  // Setup navigation and sidebar functionality
  setupNavigation();
  
  // Initialize workspace functionality
  initializeWorkspace();
  
  // Setup AI assistant if available
  setupAIAssistant();
  
  // Initialize version control UI
  initializeVersionControl();
});

// Set theme based on user role
function initializeRoleTheme() {
  const userRole = document.body.dataset.role;
  if (userRole) {
    document.body.classList.add(`${userRole}-theme`);
    
    // Update header color
    const header = document.querySelector('.header');
    if (header) {
      header.classList.add('role-header');
    }
    
    // Update sidebar active links
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
      link.addEventListener('mouseenter', function() {
        this.style.backgroundColor = `rgba(var(--${userRole}-color), 0.1)`;
      });
      link.addEventListener('mouseleave', function() {
        if (!this.classList.contains('active')) {
          this.style.backgroundColor = '';
        }
      });
    });
  }
}

// Setup navigation and sidebar functionality
function setupNavigation() {
  // Mobile menu toggle
  const menuToggle = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  
  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', function() {
      navMenu.classList.toggle('active');
      menuToggle.classList.toggle('active');
    });
  }
  
  // Sidebar navigation
  const sidebarLinks = document.querySelectorAll('.sidebar-link');
  const contentSections = document.querySelectorAll('.content-section');
  
  sidebarLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Remove active class from all links
      sidebarLinks.forEach(l => l.classList.remove('active'));
      
      // Add active class to clicked link
      this.classList.add('active');
      
      // Show corresponding content section
      const targetId = this.getAttribute('href').substring(1);
      contentSections.forEach(section => {
        section.style.display = section.id === targetId ? 'block' : 'none';
      });
    });
  });
  
  // Set first sidebar link as active by default
  if (sidebarLinks.length > 0 && contentSections.length > 0) {
    sidebarLinks[0].classList.add('active');
    contentSections.forEach((section, index) => {
      section.style.display = index === 0 ? 'block' : 'none';
    });
  }
}

// Initialize workspace functionality
function initializeWorkspace() {
  // Workspace creation
  const createWorkspaceBtn = document.getElementById('create-workspace-btn');
  const createWorkspaceModal = document.getElementById('create-workspace-modal');
  
  if (createWorkspaceBtn && createWorkspaceModal) {
    createWorkspaceBtn.addEventListener('click', function() {
      createWorkspaceModal.style.display = 'block';
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
      if (e.target === createWorkspaceModal) {
        createWorkspaceModal.style.display = 'none';
      }
    });
    
    // Close button
    const closeBtn = createWorkspaceModal.querySelector('.close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        createWorkspaceModal.style.display = 'none';
      });
    }
  }
  
  // Workspace invite functionality
  const inviteButtons = document.querySelectorAll('.invite-btn');
  inviteButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const workspaceId = this.dataset.workspaceId;
      generateInviteLink(workspaceId);
    });
  });
}

// Generate invite link for workspace
function generateInviteLink(workspaceId) {
  // In a real app, this would make an API call to generate a unique invite link
  const inviteLink = `${window.location.origin}/invite/${workspaceId}/${generateRandomString(10)}`;
  
  // Show invite link in modal or copy to clipboard
  const inviteLinkElement = document.getElementById('invite-link');
  if (inviteLinkElement) {
    inviteLinkElement.value = inviteLink;
    inviteLinkElement.select();
    document.execCommand('copy');
    alert('Invite link copied to clipboard!');
  }
}

// Generate random string for invite links
function generateRandomString(length) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// Setup AI assistant
function setupAIAssistant() {
  const aiForm = document.querySelector('.ai-form');
  const aiInput = document.querySelector('.ai-input input');
  const aiOutput = document.querySelector('.ai-output');
  
  if (aiForm && aiInput && aiOutput) {
    aiForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const query = aiInput.value.trim();
      if (query) {
        // Show loading state
        aiOutput.innerHTML = '<div class="ai-loading">Processing your request...</div>';
        
        // In a real app, this would make an API call to the Gemini API
        // For now, we'll simulate a response
        setTimeout(() => {
          const response = `This is a simulated AI response to: "${query}". In the actual implementation, this would connect to the Gemini API and provide relevant assistance based on the user's role and query.`;
          aiOutput.innerHTML = `<div class="ai-message">${response}</div>`;
          aiInput.value = '';
        }, 1000);
      }
    });
  }
}

// Initialize version control UI
function initializeVersionControl() {
  const commitBtn = document.getElementById('commit-changes');
  const revertBtn = document.getElementById('revert-changes');
  
  if (commitBtn) {
    commitBtn.addEventListener('click', function() {
      // In a real app, this would make an API call to commit changes
      alert('Changes committed successfully!');
    });
  }
  
  if (revertBtn) {
    revertBtn.addEventListener('click', function() {
      // In a real app, this would make an API call to revert changes
      if (confirm('Are you sure you want to revert all changes?')) {
        alert('Changes reverted successfully!');
      }
    });
  }
  
  // Version history toggle
  const versionHistoryBtn = document.getElementById('version-history-btn');
  const versionHistory = document.getElementById('version-history');
  
  if (versionHistoryBtn && versionHistory) {
    versionHistoryBtn.addEventListener('click', function() {
      versionHistory.style.display = versionHistory.style.display === 'none' ? 'block' : 'none';
    });
  }
}
