from flask import Blueprint, request, jsonify, session
from src.models.database import db_manager
from src.models.workspace import Workspace
import logging
import secrets
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
workspace_bp = Blueprint('workspace', __name__)

@workspace_bp.route('/api/workspaces', methods=['POST'])
def create_workspace():
    """
    Create a new workspace.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create workspace object
    workspace = Workspace(
        name=data['name'],
        description=data['description'],
        owner_id=session['user_id'],
        project_type=data.get('project_type')
    )
    
    # Save to database
    workspace_id = db_manager.create_workspace(workspace.to_dict())
    
    if workspace_id:
        return jsonify({'message': 'Workspace created successfully', 'workspace_id': workspace_id}), 201
    else:
        return jsonify({'error': 'Failed to create workspace'}), 400

@workspace_bp.route('/api/workspaces/<workspace_id>', methods=['GET'])
def get_workspace(workspace_id):
    """
    Get a workspace by ID.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is a member of the workspace
    if session['user_id'] not in workspace_data.get('members', []):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({
        'id': str(workspace_data['_id']),
        'name': workspace_data['name'],
        'description': workspace_data['description'],
        'owner_id': workspace_data['owner_id'],
        'project_type': workspace_data.get('project_type'),
        'created_at': workspace_data['created_at'],
        'updated_at': workspace_data['updated_at'],
        'members': workspace_data['members'],
        'member_roles': workspace_data['member_roles'],
        'status': workspace_data['status']
    }), 200

@workspace_bp.route('/api/workspaces/<workspace_id>', methods=['PUT'])
def update_workspace(workspace_id):
    """
    Update a workspace.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is the owner of the workspace
    if workspace_data['owner_id'] != session['user_id']:
        return jsonify({'error': 'Only the workspace owner can update it'}), 403
    
    data = request.json
    
    # Don't allow updating owner_id
    if 'owner_id' in data:
        del data['owner_id']
    
    success = db_manager.update_workspace(workspace_id, data)
    
    if success:
        return jsonify({'message': 'Workspace updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update workspace'}), 400

@workspace_bp.route('/api/workspaces/<workspace_id>/members', methods=['POST'])
def add_workspace_member(workspace_id):
    """
    Add a member to a workspace.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is the owner of the workspace
    if workspace_data['owner_id'] != session['user_id']:
        return jsonify({'error': 'Only the workspace owner can add members'}), 403
    
    data = request.json
    
    # Validate required fields
    required_fields = ['user_id', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate role
    valid_roles = ['director', 'editor', 'music_director']
    if data['role'] not in valid_roles:
        return jsonify({'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400
    
    success = db_manager.add_workspace_member(workspace_id, data['user_id'], data['role'])
    
    if success:
        return jsonify({'message': 'Member added successfully'}), 200
    else:
        return jsonify({'error': 'Failed to add member'}), 400

@workspace_bp.route('/api/workspaces/<workspace_id>/members/<user_id>', methods=['DELETE'])
def remove_workspace_member(workspace_id, user_id):
    """
    Remove a member from a workspace.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is the owner of the workspace
    if workspace_data['owner_id'] != session['user_id']:
        return jsonify({'error': 'Only the workspace owner can remove members'}), 403
    
    # Prevent removing the owner
    if user_id == workspace_data['owner_id']:
        return jsonify({'error': 'Cannot remove the workspace owner'}), 400
    
    # Check if user is a member
    if user_id not in workspace_data.get('members', []):
        return jsonify({'error': 'User is not a member of this workspace'}), 400
    
    success = db_manager.remove_workspace_member(workspace_id, user_id)
    
    if success:
        return jsonify({'message': 'Member removed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to remove member'}), 400

@workspace_bp.route('/api/workspaces/<workspace_id>/invite', methods=['POST'])
def create_invite(workspace_id):
    """
    Create an invite link for a workspace.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is a member of the workspace
    if session['user_id'] not in workspace_data.get('members', []):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.json
    expiry_days = data.get('expiry_days', 7)
    
    invite_code = db_manager.create_invite_link(workspace_id, expiry_days)
    
    if invite_code:
        invite_url = f"/invite/{workspace_id}/{invite_code}"
        return jsonify({
            'message': 'Invite link created successfully',
            'invite_code': invite_code,
            'invite_url': invite_url,
            'expires_at': (datetime.utcnow() + timedelta(days=expiry_days)).isoformat()
        }), 201
    else:
        return jsonify({'error': 'Failed to create invite link'}), 400

@workspace_bp.route('/api/invite/<workspace_id>/<invite_code>', methods=['GET'])
def validate_invite(workspace_id, invite_code):
    """
    Validate an invite link.
    """
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    invite_links = workspace_data.get('invite_links', {})
    
    if invite_code not in invite_links:
        return jsonify({'error': 'Invalid invite code'}), 400
    
    expiry_date = invite_links[invite_code]
    
    if expiry_date < datetime.utcnow():
        return jsonify({'error': 'Invite link has expired'}), 400
    
    return jsonify({
        'valid': True,
        'workspace_name': workspace_data['name'],
        'workspace_description': workspace_data['description']
    }), 200

@workspace_bp.route('/api/invite/<workspace_id>/<invite_code>/accept', methods=['POST'])
def accept_invite(workspace_id, invite_code):
    """
    Accept an invite to join a workspace.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    invite_links = workspace_data.get('invite_links', {})
    
    if invite_code not in invite_links:
        return jsonify({'error': 'Invalid invite code'}), 400
    
    expiry_date = invite_links[invite_code]
    
    if expiry_date < datetime.utcnow():
        return jsonify({'error': 'Invite link has expired'}), 400
    
    # Check if user is already a member
    if session['user_id'] in workspace_data.get('members', []):
        return jsonify({'error': 'You are already a member of this workspace'}), 400
    
    # Add user to workspace with default role (editor)
    success = db_manager.add_workspace_member(workspace_id, session['user_id'], 'editor')
    
    if success:
        return jsonify({'message': 'Successfully joined workspace'}), 200
    else:
        return jsonify({'error': 'Failed to join workspace'}), 400

@workspace_bp.route('/api/workspaces/user', methods=['GET'])
def get_user_workspaces():
    """
    Get all workspaces for the current user.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_data = db_manager.get_user(user_id=session['user_id'])
    
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
    
    workspaces = []
    for workspace_id in user_data.get('workspaces', []):
        workspace_data = db_manager.get_workspace(workspace_id)
        if workspace_data:
            workspaces.append({
                'id': str(workspace_data['_id']),
                'name': workspace_data['name'],
                'description': workspace_data['description'],
                'project_type': workspace_data.get('project_type'),
                'role': workspace_data['member_roles'].get(session['user_id']),
                'created_at': workspace_data['created_at'],
                'updated_at': workspace_data['updated_at'],
                'member_count': len(workspace_data['members'])
            })
    
    return jsonify(workspaces), 200
