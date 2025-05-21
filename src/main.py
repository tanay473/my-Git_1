from flask import Flask, render_template, session, redirect, url_for
import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!
from src.models.database import db_manager
from src.routes.user import user_bp
from src.routes.workspace import workspace_bp
from src.routes.version import version_bp
from src.routes.ai import ai_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(workspace_bp)
app.register_blueprint(version_bp)
app.register_blueprint(ai_bp)

# Connect to MongoDB
# Flask 2.0+ removed before_first_request
# Using alternative approach with app factory pattern
def connect_db():
    db_manager.connect()

# Call connect_db at startup
with app.app_context():
    connect_db()

# Main routes
@app.route('/')
def index():
    """
    Render the home page.
    """
    return render_template('index.html')

@app.route('/login')
def login():
    """
    Render the login page.
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    """
    Render the registration page.
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard based on user role.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    
    if role == 'director':
        return render_template('director/dashboard.html')
    elif role == 'editor':
        return render_template('editor/dashboard.html')
    elif role == 'music_director':
        return render_template('music_director/dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/editor/dashboard')
def editor_dashboard():
    """
    Direct route to editor dashboard for demo purposes.
    """
    return render_template('editor/dashboard.html')

@app.route('/director/dashboard')
def director_dashboard():
    """
    Direct route to director dashboard for demo purposes.
    """
    return render_template('director/dashboard.html')

@app.route('/music_director/dashboard')
def music_director_dashboard():
    """
    Direct route to music director dashboard for demo purposes.
    """
    return render_template('music_director/dashboard.html')

@app.route('/community')
def community():
    """
    Render the community page.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('community/index.html')

@app.route('/editor/community')
def editor_community():
    """
    Render the editor-specific community page.
    """
    return render_template('community/editor_view.html')

@app.route('/director/community')
def director_community():
    """
    Render the director-specific community page.
    """
    return render_template('community/director_view.html')

@app.route('/music_director/community')
def music_director_community():
    """
    Render the music director-specific community page.
    """
    return render_template('community/music_director_view.html')

@app.route('/profile')
def profile():
    """
    Render the user profile page.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('profile.html')

@app.route('/editor/profile')
def editor_profile():
    """
    Render the editor-specific profile page.
    """
    return render_template('profile/editor_view.html')

@app.route('/director/profile')
def director_profile():
    """
    Render the director-specific profile page.
    """
    return render_template('profile/director_view.html')

@app.route('/music_director/profile')
def music_director_profile():
    """
    Render the music director-specific profile page.
    """
    return render_template('profile/music_director_view.html')

@app.route('/workspaces')
def workspaces():
    """
    Render the workspaces page.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('workspace/list.html')

@app.route('/editor/workspaces')
def editor_workspaces():
    """
    Render the editor-specific workspaces page.
    """
    return render_template('workspace/editor_view.html')

@app.route('/director/workspaces')
def director_workspaces():
    """
    Render the director-specific workspaces page.
    """
    return render_template('workspace/director_view.html')

@app.route('/music_director/workspaces')
def music_director_workspaces():
    """
    Render the music director-specific workspaces page.
    """
    return render_template('workspace/music_director_view.html')

@app.route('/workspaces/<workspace_id>')
def workspace_detail(workspace_id):
    """
    Render the workspace detail page.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('workspace/detail.html', workspace_id=workspace_id)

@app.route('/invite/<workspace_id>/<invite_code>')
def invite(workspace_id, invite_code):
    """
    Render the invite page.
    """
    return render_template('workspace/invite.html', workspace_id=workspace_id, invite_code=invite_code)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    # Use PORT environment variable if available, otherwise use 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
