from datetime import datetime
from bson import ObjectId

class Workspace:
    """
    Workspace model for the community platform.
    Represents a collaborative workspace for a project.
    """
    
    def __init__(self, name, description, owner_id, project_type=None):
        """
        Initialize a new Workspace.
        
        Args:
            name (str): Name of the workspace/project
            description (str): Description of the workspace/project
            owner_id (str): User ID of the workspace owner (typically a director)
            project_type (str, optional): Type of project (film, commercial, etc.)
        """
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.project_type = project_type
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.members = [owner_id]  # List of user IDs who are members
        self.member_roles = {owner_id: "director"}  # Mapping of user_id to role in this workspace
        self.status = "active"
        self.invite_links = {}  # Dictionary of invite_code: expiry_date
        
    def to_dict(self):
        """
        Convert Workspace object to dictionary for MongoDB storage.
        
        Returns:
            dict: Dictionary representation of the Workspace
        """
        return {
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "project_type": self.project_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "members": self.members,
            "member_roles": self.member_roles,
            "status": self.status,
            "invite_links": self.invite_links
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Workspace object from a dictionary.
        
        Args:
            data (dict): Dictionary containing workspace data
            
        Returns:
            Workspace: New Workspace object
        """
        workspace = cls(
            name=data.get("name"),
            description=data.get("description"),
            owner_id=data.get("owner_id"),
            project_type=data.get("project_type")
        )
        workspace.created_at = data.get("created_at", datetime.utcnow())
        workspace.updated_at = data.get("updated_at", datetime.utcnow())
        workspace.members = data.get("members", [workspace.owner_id])
        workspace.member_roles = data.get("member_roles", {workspace.owner_id: "director"})
        workspace.status = data.get("status", "active")
        workspace.invite_links = data.get("invite_links", {})
        return workspace
