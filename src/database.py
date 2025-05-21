from pymongo import MongoClient
import os
import hashlib
import logging
from datetime import datetime, timedelta
import secrets
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Database manager for MongoDB connection and operations.
    Handles all database interactions for the community platform.
    """
    
    def __init__(self, connection_string=None):
        """
        Initialize the database manager.
        
        Args:
            connection_string (str, optional): MongoDB connection string
        """
        # Default to localhost if no connection string provided
        self.connection_string = connection_string or "mongodb://localhost:27017/"
        self.client = None
        self.db = None
        self.connected = False
        
    def connect(self, db_name="community_platform"):
        """
        Connect to MongoDB.
        
        Args:
            db_name (str, optional): Name of the database to use
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = MongoClient(self.connection_string)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            self.connected = True
            logger.info(f"Connected to MongoDB: {db_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            logger.info("Running in demo mode without MongoDB connection")
            self.connected = False
            # Create mock data for demo purposes
            self._setup_mock_data()
            return False
            
    def _setup_mock_data(self):
        """
        Set up mock data for demo mode when MongoDB is not available.
        """
        logger.info("Setting up mock data for demo mode")
        # This method will be called when MongoDB connection fails
        # It allows the application to run in a demo mode
    
    def close(self):
        """
        Close the MongoDB connection.
        """
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("MongoDB connection closed")
    
    def get_collection(self, collection_name):
        """
        Get a MongoDB collection.
        
        Args:
            collection_name (str): Name of the collection
            
        Returns:
            Collection: MongoDB collection object or None if not connected
        """
        if not self.connected:
            logger.warning("Not connected to MongoDB")
            return None
        
        return self.db[collection_name]
    
    # User operations
    def create_user(self, user_data):
        """
        Create a new user.
        
        Args:
            user_data (dict): User data dictionary
            
        Returns:
            str: ID of the created user or None if failed
        """
        if not self.connected:
            return None
        
        # Hash password before storing
        if "password" in user_data:
            user_data["password"] = self._hash_password(user_data["password"])
        
        try:
            users = self.get_collection("users")
            # Check if username or email already exists
            if users.find_one({"$or": [
                {"username": user_data.get("username")},
                {"email": user_data.get("email")}
            ]}):
                logger.warning("Username or email already exists")
                return None
            
            result = users.insert_one(user_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}")
            return None
    
    def get_user(self, user_id=None, username=None, email=None):
        """
        Get a user by ID, username, or email.
        
        Args:
            user_id (str, optional): User ID
            username (str, optional): Username
            email (str, optional): Email
            
        Returns:
            dict: User data or None if not found
        """
        if not self.connected:
            return None
        
        users = self.get_collection("users")
        query = {}
        
        if user_id:
            query["_id"] = ObjectId(user_id)
        elif username:
            query["username"] = username
        elif email:
            query["email"] = email
        else:
            return None
        
        return users.find_one(query)
    
    def update_user(self, user_id, update_data):
        """
        Update a user.
        
        Args:
            user_id (str): User ID
            update_data (dict): Data to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        # Don't allow updating username or email to existing values
        if "username" in update_data or "email" in update_data:
            users = self.get_collection("users")
            query = {"$or": []}
            
            if "username" in update_data:
                query["$or"].append({"username": update_data["username"]})
            
            if "email" in update_data:
                query["$or"].append({"email": update_data["email"]})
            
            existing = users.find_one(query)
            if existing and str(existing["_id"]) != user_id:
                logger.warning("Username or email already exists")
                return False
        
        # Hash password if it's being updated
        if "password" in update_data:
            update_data["password"] = self._hash_password(update_data["password"])
        
        update_data["updated_at"] = datetime.utcnow()
        
        try:
            users = self.get_collection("users")
            result = users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update user: {str(e)}")
            return False
    
    # Workspace operations
    def create_workspace(self, workspace_data):
        """
        Create a new workspace.
        
        Args:
            workspace_data (dict): Workspace data dictionary
            
        Returns:
            str: ID of the created workspace or None if failed
        """
        if not self.connected:
            return None
        
        try:
            workspaces = self.get_collection("workspaces")
            result = workspaces.insert_one(workspace_data)
            workspace_id = str(result.inserted_id)
            
            # Update user's workspaces list
            if "owner_id" in workspace_data:
                users = self.get_collection("users")
                users.update_one(
                    {"_id": ObjectId(workspace_data["owner_id"])},
                    {"$push": {"workspaces": workspace_id}}
                )
            
            return workspace_id
        except Exception as e:
            logger.error(f"Failed to create workspace: {str(e)}")
            return None
    
    def get_workspace(self, workspace_id):
        """
        Get a workspace by ID.
        
        Args:
            workspace_id (str): Workspace ID
            
        Returns:
            dict: Workspace data or None if not found
        """
        if not self.connected:
            return None
        
        workspaces = self.get_collection("workspaces")
        return workspaces.find_one({"_id": ObjectId(workspace_id)})
    
    def update_workspace(self, workspace_id, update_data):
        """
        Update a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            update_data (dict): Data to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        update_data["updated_at"] = datetime.utcnow()
        
        try:
            workspaces = self.get_collection("workspaces")
            result = workspaces.update_one(
                {"_id": ObjectId(workspace_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update workspace: {str(e)}")
            return False
    
    def add_workspace_member(self, workspace_id, user_id, role):
        """
        Add a member to a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            user_id (str): User ID
            role (str): Role in the workspace
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        try:
            # Update workspace members
            workspaces = self.get_collection("workspaces")
            workspace_result = workspaces.update_one(
                {"_id": ObjectId(workspace_id)},
                {
                    "$addToSet": {"members": user_id},
                    "$set": {f"member_roles.{user_id}": role}
                }
            )
            
            # Update user's workspaces
            users = self.get_collection("users")
            user_result = users.update_one(
                {"_id": ObjectId(user_id)},
                {"$addToSet": {"workspaces": workspace_id}}
            )
            
            return workspace_result.modified_count > 0 or user_result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to add workspace member: {str(e)}")
            return False
    
    def remove_workspace_member(self, workspace_id, user_id):
        """
        Remove a member from a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            user_id (str): User ID to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        try:
            # Update workspace members
            workspaces = self.get_collection("workspaces")
            workspace_result = workspaces.update_one(
                {"_id": ObjectId(workspace_id)},
                {
                    "$pull": {"members": user_id},
                    "$unset": {f"member_roles.{user_id}": ""}
                }
            )
            
            # Update user's workspaces
            users = self.get_collection("users")
            user_result = users.update_one(
                {"_id": ObjectId(user_id)},
                {"$pull": {"workspaces": workspace_id}}
            )
            
            return workspace_result.modified_count > 0 or user_result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to remove workspace member: {str(e)}")
            return False
    
    def create_invite_link(self, workspace_id, expiry_days=7):
        """
        Create an invite link for a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            expiry_days (int, optional): Number of days until the link expires
            
        Returns:
            str: Invite code or None if failed
        """
        if not self.connected:
            return None
        
        try:
            # Generate a random invite code
            invite_code = secrets.token_urlsafe(16)
            expiry_date = datetime.utcnow() + timedelta(days=expiry_days)
            
            workspaces = self.get_collection("workspaces")
            result = workspaces.update_one(
                {"_id": ObjectId(workspace_id)},
                {"$set": {f"invite_links.{invite_code}": expiry_date}}
            )
            
            if result.modified_count > 0:
                return invite_code
            return None
        except Exception as e:
            logger.error(f"Failed to create invite link: {str(e)}")
            return None
    
    # Version control operations
    def create_version(self, version_data, file_content_data=None):
        """
        Create a new version and store file content.
        
        Args:
            version_data (dict): Version metadata
            file_content_data (dict, optional): File content data
            
        Returns:
            str: Version ID or None if failed
        """
        if not self.connected:
            return None
        
        try:
            # First store the file content if provided
            if file_content_data:
                file_contents = self.get_collection("file_contents")
                # Check if content with this hash already exists
                existing_content = file_contents.find_one({"content_hash": file_content_data["content_hash"]})
                if not existing_content:
                    file_contents.insert_one(file_content_data)
            
            # Then store the version metadata
            versions = self.get_collection("versions")
            result = versions.insert_one(version_data)
            
            return version_data.get("version_id")
        except Exception as e:
            logger.error(f"Failed to create version: {str(e)}")
            return None
    
    def get_version(self, version_id, workspace_id):
        """
        Get a version by ID and workspace ID.
        
        Args:
            version_id (str): Version ID
            workspace_id (str): Workspace ID
            
        Returns:
            dict: Version data or None if not found
        """
        if not self.connected:
            return None
        
        versions = self.get_collection("versions")
        return versions.find_one({
            "version_id": version_id,
            "workspace_id": workspace_id
        })
    
    def get_file_content(self, content_hash):
        """
        Get file content by hash.
        
        Args:
            content_hash (str): Content hash
            
        Returns:
            dict: File content data or None if not found
        """
        if not self.connected:
            return None
        
        file_contents = self.get_collection("file_contents")
        return file_contents.find_one({"content_hash": content_hash})
    
    def get_file_versions(self, workspace_id, file_path):
        """
        Get all versions of a file.
        
        Args:
            workspace_id (str): Workspace ID
            file_path (str): File path
            
        Returns:
            list: List of version data
        """
        if not self.connected:
            return []
        
        versions = self.get_collection("versions")
        return list(versions.find({
            "workspace_id": workspace_id,
            "file_path": file_path
        }).sort("created_at", -1))
    
    def get_workspace_versions(self, workspace_id, limit=20):
        """
        Get recent versions in a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            limit (int, optional): Maximum number of versions to return
            
        Returns:
            list: List of version data
        """
        if not self.connected:
            return []
        
        versions = self.get_collection("versions")
        return list(versions.find({
            "workspace_id": workspace_id
        }).sort("created_at", -1).limit(limit))
    
    def list_workspace_files(self, workspace_id):
        """
        List all unique files in a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            
        Returns:
            list: List of unique file paths
        """
        if not self.connected:
            return []
        
        versions = self.get_collection("versions")
        # Use aggregation to get unique file paths
        pipeline = [
            {"$match": {"workspace_id": workspace_id}},
            {"$group": {"_id": "$file_path"}},
            {"$project": {"file_path": "$_id", "_id": 0}}
        ]
        
        result = list(versions.aggregate(pipeline))
        return [item["file_path"] for item in result]
    
    def _hash_password(self, password):
        """
        Hash a password using SHA-256.
        
        Args:
            password (str): Password to hash
            
        Returns:
            str: Hashed password
        """
        # In a real application, use a more secure method like bcrypt
        return hashlib.sha256(password.encode()).hexdigest()


# Singleton instance
db_manager = DatabaseManager()
