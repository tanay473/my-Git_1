from flask import Blueprint, request, jsonify, session
from src.models.database import db_manager
from src.models.user import User
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/api/users/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate role
    valid_roles = ['director', 'editor', 'music_director']
    if data['role'] not in valid_roles:
        return jsonify({'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400
    
    # Create user object
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],  # Will be hashed in database manager
        role=data['role'],
        full_name=data.get('full_name'),
        bio=data.get('bio'),
        profile_image=data.get('profile_image')
    )
    
    # Save to database
    user_id = db_manager.create_user(user.to_dict())
    
    if user_id:
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    else:
        return jsonify({'error': 'Failed to register user. Username or email may already exist.'}), 400

@user_bp.route('/api/users/login', methods=['POST'])
def login():
    """
    Login a user.
    """
    data = request.json
    
    # Validate required fields
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Get user by username
    user_data = db_manager.get_user(username=data['username'])
    
    if not user_data:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Check password
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    if user_data['password'] != hashed_password:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Set session
    session['user_id'] = str(user_data['_id'])
    session['username'] = user_data['username']
    session['role'] = user_data['role']
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': str(user_data['_id']),
            'username': user_data['username'],
            'email': user_data['email'],
            'role': user_data['role'],
            'full_name': user_data.get('full_name')
        }
    }), 200

@user_bp.route('/api/users/logout', methods=['POST'])
def logout():
    """
    Logout a user.
    """
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@user_bp.route('/api/users/profile', methods=['GET'])
def get_profile():
    """
    Get the current user's profile.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_data = db_manager.get_user(user_id=session['user_id'])
    
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': str(user_data['_id']),
        'username': user_data['username'],
        'email': user_data['email'],
        'role': user_data['role'],
        'full_name': user_data.get('full_name'),
        'bio': user_data.get('bio'),
        'profile_image': user_data.get('profile_image'),
        'workspaces': user_data.get('workspaces', [])
    }), 200

@user_bp.route('/api/users/profile', methods=['PUT'])
def update_profile():
    """
    Update the current user's profile.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    
    # Don't allow updating role through this endpoint
    if 'role' in data:
        del data['role']
    
    success = db_manager.update_user(session['user_id'], data)
    
    if success:
        return jsonify({'message': 'Profile updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update profile'}), 400

@user_bp.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a user by ID.
    """
    user_data = db_manager.get_user(user_id=user_id)
    
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
    
    # Don't expose sensitive information
    return jsonify({
        'id': str(user_data['_id']),
        'username': user_data['username'],
        'role': user_data['role'],
        'full_name': user_data.get('full_name'),
        'bio': user_data.get('bio'),
        'profile_image': user_data.get('profile_image')
    }), 200

@user_bp.route('/api/users/search', methods=['GET'])
def search_users():
    """
    Search for users by username or full name.
    """
    query = request.args.get('q', '')
    
    if not query or len(query) < 3:
        return jsonify({'error': 'Search query must be at least 3 characters'}), 400
    
    # This would need to be implemented in the database manager
    # For now, return a placeholder response
    return jsonify({'message': 'Search functionality not implemented yet'}), 501
