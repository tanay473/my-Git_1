from datetime import datetime
from bson import ObjectId

class Version:
    """
    Version model for the community platform.
    Represents a version of content with Git-like versioning.
    """
    
    def __init__(self, workspace_id, file_path, content_hash, author_id, message, parent_version_id=None):
        """
        Initialize a new Version.
        
        Args:
            workspace_id (str): ID of the workspace this version belongs to
            file_path (str): Path to the file within the workspace
            content_hash (str): Hash of the file content for integrity checking
            author_id (str): User ID of the version author
            message (str): Commit message describing the changes
            parent_version_id (str, optional): ID of the parent version (for history tracking)
        """
        self.workspace_id = workspace_id
        self.file_path = file_path
        self.content_hash = content_hash
        self.author_id = author_id
        self.message = message
        self.parent_version_id = parent_version_id
        self.created_at = datetime.utcnow()
        self.version_id = f"v{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.status = "committed"  # committed, reverted
        
    def to_dict(self):
        """
        Convert Version object to dictionary for MongoDB storage.
        
        Returns:
            dict: Dictionary representation of the Version
        """
        return {
            "workspace_id": self.workspace_id,
            "file_path": self.file_path,
            "content_hash": self.content_hash,
            "author_id": self.author_id,
            "message": self.message,
            "parent_version_id": self.parent_version_id,
            "created_at": self.created_at,
            "version_id": self.version_id,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Version object from a dictionary.
        
        Args:
            data (dict): Dictionary containing version data
            
        Returns:
            Version: New Version object
        """
        version = cls(
            workspace_id=data.get("workspace_id"),
            file_path=data.get("file_path"),
            content_hash=data.get("content_hash"),
            author_id=data.get("author_id"),
            message=data.get("message"),
            parent_version_id=data.get("parent_version_id")
        )
        version.created_at = data.get("created_at", datetime.utcnow())
        version.version_id = data.get("version_id", version.version_id)
        version.status = data.get("status", "committed")
        return version


class FileContent:
    """
    FileContent model for the community platform.
    Stores the actual content of files for the versioning system.
    """
    
    def __init__(self, content_hash, content, content_type, size):
        """
        Initialize a new FileContent.
        
        Args:
            content_hash (str): Hash of the file content (used as identifier)
            content (bytes/str): The actual file content
            content_type (str): MIME type of the content
            size (int): Size of the content in bytes
        """
        self.content_hash = content_hash
        self.content = content
        self.content_type = content_type
        self.size = size
        self.created_at = datetime.utcnow()
        
    def to_dict(self):
        """
        Convert FileContent object to dictionary for MongoDB storage.
        
        Returns:
            dict: Dictionary representation of the FileContent
        """
        return {
            "content_hash": self.content_hash,
            "content": self.content,
            "content_type": self.content_type,
            "size": self.size,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a FileContent object from a dictionary.
        
        Args:
            data (dict): Dictionary containing file content data
            
        Returns:
            FileContent: New FileContent object
        """
        file_content = cls(
            content_hash=data.get("content_hash"),
            content=data.get("content"),
            content_type=data.get("content_type"),
            size=data.get("size")
        )
        file_content.created_at = data.get("created_at", datetime.utcnow())
        return file_content
