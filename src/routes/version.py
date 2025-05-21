from flask import Blueprint, request, jsonify, session
from src.models.database import db_manager
from src.models.version import Version, FileContent
import hashlib
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
version_bp = Blueprint('version', __name__)

@version_bp.route('/api/workspaces/<workspace_id>/versions', methods=['POST'])
def create_version(workspace_id):
    """
    Create a new version (commit) in the workspace.
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
    
    # Validate required fields
    required_fields = ['file_path', 'content', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Generate content hash
    content_hash = hashlib.sha256(data['content'].encode()).hexdigest()
    
    # Create file content object
    file_content = FileContent(
        content_hash=content_hash,
        content=data['content'],
        content_type=data.get('content_type', 'text/plain'),
        size=len(data['content'])
    )
    
    # Get parent version if exists
    parent_version = None
    previous_versions = db_manager.get_file_versions(workspace_id, data['file_path'])
    if previous_versions:
        parent_version = previous_versions[0]['version_id']
    
    # Create version object
    version = Version(
        workspace_id=workspace_id,
        file_path=data['file_path'],
        content_hash=content_hash,
        author_id=session['user_id'],
        message=data['message'],
        parent_version_id=parent_version
    )
    
    # Save to database
    version_id = db_manager.create_version(version.to_dict(), file_content.to_dict())
    
    if version_id:
        return jsonify({
            'message': 'Version created successfully',
            'version_id': version_id,
            'content_hash': content_hash
        }), 201
    else:
        return jsonify({'error': 'Failed to create version'}), 400

@version_bp.route('/api/workspaces/<workspace_id>/versions/<version_id>', methods=['GET'])
def get_version(workspace_id, version_id):
    """
    Get a specific version by ID.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is a member of the workspace
    if session['user_id'] not in workspace_data.get('members', []):
        return jsonify({'error': 'Access denied'}), 403
    
    version_data = db_manager.get_version(version_id, workspace_id)
    
    if not version_data:
        return jsonify({'error': 'Version not found'}), 404
    
    # Get file content
    file_content_data = db_manager.get_file_content(version_data['content_hash'])
    
    if not file_content_data:
        return jsonify({'error': 'File content not found'}), 404
    
    return jsonify({
        'version_id': version_data['version_id'],
        'file_path': version_data['file_path'],
        'author_id': version_data['author_id'],
        'message': version_data['message'],
        'parent_version_id': version_data['parent_version_id'],
        'created_at': version_data['created_at'],
        'content': file_content_data['content'],
        'content_type': file_content_data['content_type']
    }), 200

@version_bp.route('/api/workspaces/<workspace_id>/files/<path:file_path>/versions', methods=['GET'])
def get_file_versions(workspace_id, file_path):
    """
    Get all versions of a specific file.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is a member of the workspace
    if session['user_id'] not in workspace_data.get('members', []):
        return jsonify({'error': 'Access denied'}), 403
    
    versions = db_manager.get_file_versions(workspace_id, file_path)
    
    result = []
    for version in versions:
        result.append({
            'version_id': version['version_id'],
            'author_id': version['author_id'],
            'message': version['message'],
            'created_at': version['created_at']
        })
    
    return jsonify(result), 200

@version_bp.route('/api/workspaces/<workspace_id>/files/<path:file_path>/latest', methods=['GET'])
def get_latest_file(workspace_id, file_path):
    """
    Get the latest version of a file.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is a member of the workspace
    if session['user_id'] not in workspace_data.get('members', []):
        return jsonify({'error': 'Access denied'}), 403
    
    versions = db_manager.get_file_versions(workspace_id, file_path)
    
    if not versions:
        return jsonify({'error': 'File not found'}), 404
    
    latest_version = versions[0]
    
    # Get file content
    file_content_data = db_manager.get_file_content(latest_version['content_hash'])
    
    if not file_content_data:
        return jsonify({'error': 'File content not found'}), 404
    
    return jsonify({
        'version_id': latest_version['version_id'],
        'file_path': latest_version['file_path'],
        'author_id': latest_version['author_id'],
        'message': latest_version['message'],
        'created_at': latest_version['created_at'],
        'content': file_content_data['content'],
        'content_type': file_content_data['content_type']
    }), 200

@version_bp.route('/api/workspaces/<workspace_id>/versions', methods=['GET'])
def get_workspace_versions(workspace_id):
    """
    Get recent versions in a workspace.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is a member of the workspace
    if session['user_id'] not in workspace_data.get('members', []):
        return jsonify({'error': 'Access denied'}), 403
    
    limit = request.args.get('limit', 20, type=int)
    versions = db_manager.get_workspace_versions(workspace_id, limit)
    
    result = []
    for version in versions:
        result.append({
            'version_id': version['version_id'],
            'file_path': version['file_path'],
            'author_id': version['author_id'],
            'message': version['message'],
            'created_at': version['created_at']
        })
    
    return jsonify(result), 200

@version_bp.route('/api/workspaces/<workspace_id>/files/<path:file_path>/revert/<version_id>', methods=['POST'])
def revert_to_version(workspace_id, file_path, version_id):
    """
    Revert a file to a specific version.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is a member of the workspace
    if session['user_id'] not in workspace_data.get('members', []):
        return jsonify({'error': 'Access denied'}), 403
    
    # Get the version to revert to
    version_data = db_manager.get_version(version_id, workspace_id)
    
    if not version_data:
        return jsonify({'error': 'Version not found'}), 404
    
    # Get file content
    file_content_data = db_manager.get_file_content(version_data['content_hash'])
    
    if not file_content_data:
        return jsonify({'error': 'File content not found'}), 404
    
    # Create a new version with the reverted content
    content_hash = version_data['content_hash']
    
    # Create version object
    version = Version(
        workspace_id=workspace_id,
        file_path=file_path,
        content_hash=content_hash,
        author_id=session['user_id'],
        message=f"Reverted to version {version_id}",
        parent_version_id=version_id
    )
    
    # Save to database (reusing existing file content)
    version_id = db_manager.create_version(version.to_dict(), None)
    
    if version_id:
        return jsonify({
            'message': 'Successfully reverted to previous version',
            'version_id': version_id
        }), 200
    else:
        return jsonify({'error': 'Failed to revert to version'}), 400

@version_bp.route('/api/workspaces/<workspace_id>/files', methods=['GET'])
def list_workspace_files(workspace_id):
    """
    List all files in a workspace.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    workspace_data = db_manager.get_workspace(workspace_id)
    
    if not workspace_data:
        return jsonify({'error': 'Workspace not found'}), 404
    
    # Check if user is a member of the workspace
    if session['user_id'] not in workspace_data.get('members', []):
        return jsonify({'error': 'Access denied'}), 403
    
    # Get list of files from database manager
    files = db_manager.list_workspace_files(workspace_id)
    
    return jsonify({
        'files': files,
        'count': len(files)
    }), 200
