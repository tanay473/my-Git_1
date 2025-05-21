import os
import sys
import logging
from flask import Flask

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
    
    # Import and register blueprints
    from src.routes.user import user_bp
    from src.routes.workspace import workspace_bp
    from src.routes.version import version_bp
    from src.routes.ai import ai_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(workspace_bp)
    app.register_blueprint(version_bp)
    app.register_blueprint(ai_bp)
    
    # Connect to MongoDB
    from src.models.database import db_manager
    with app.app_context():
        db_manager.connect()
    
    # Import and register routes
    from src.routes import main_routes
    main_routes.register_routes(app)
    
    return app

# Create the application
app = create_app()

if __name__ == '__main__':
    # Use PORT environment variable if available, otherwise use 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
