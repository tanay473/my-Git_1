from flask import render_template, session, redirect, url_for

def register_routes(app):
    """
    Register main routes for the application.
    
    Args:
        app (Flask): Flask application
    """
    
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
