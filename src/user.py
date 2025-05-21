from datetime import datetime
from bson import ObjectId

class User:
    """
    User model for the community platform.
    Represents a user with role-based access.
    """
    
    def __init__(self, username, email, password, role, full_name=None, bio=None, profile_image=None):
        """
        Initialize a new User.
        
        Args:
            username (str): Unique username for the user
            email (str): User's email address
            password (str): Hashed password
            role (str): User role (director, editor, music_director)
            full_name (str, optional): User's full name
            bio (str, optional): User's biography
            profile_image (str, optional): Path to profile image
        """
        self.username = username
        self.email = email
        self.password = password  # Should be hashed before storage
        self.role = role
        self.full_name = full_name
        self.bio = bio
        self.profile_image = profile_image
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.workspaces = []  # List of workspace IDs the user belongs to
        
    def to_dict(self):
        """
        Convert User object to dictionary for MongoDB storage.
        
        Returns:
            dict: Dictionary representation of the User
        """
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_image": self.profile_image,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "workspaces": self.workspaces
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a User object from a dictionary.
        
        Args:
            data (dict): Dictionary containing user data
            
        Returns:
            User: New User object
        """
        user = cls(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            full_name=data.get("full_name"),
            bio=data.get("bio"),
            profile_image=data.get("profile_image")
        )
        user.created_at = data.get("created_at", datetime.utcnow())
        user.updated_at = data.get("updated_at", datetime.utcnow())
        user.workspaces = data.get("workspaces", [])
        return user
