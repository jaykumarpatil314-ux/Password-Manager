from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from urllib.parse import urlparse

from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, ConnectionFailure

from database.base_repository import BaseRepository

class MongoRepository(BaseRepository):
    """MongoDB implementation of the repository"""
    
    def __init__(self, database_uri: str):
        self.database_uri = database_uri
        self.client = None
        self.db = None
        self.users = None
        self.passwords = None
    
    def initialize(self):
        """Initialize MongoDB connection"""
        try:
            # Connect to MongoDB
            self.client = MongoClient(
                self.database_uri,
                maxPoolSize=50,
                minPoolSize=10,
                connectTimeoutMS=10000,
                socketTimeoutMS=45000,
                serverSelectionTimeoutMS=10000,
                retryWrites=True
            )
            
            # Test connection
            self.client.admin.command('ping')
            print("✓ MongoDB connection successful")
            
            # Extract database name from URI
            db_name = self._extract_database_name(self.database_uri)
            
            if not db_name:
                raise ValueError("Database name not found in MongoDB URI. "
                               "URI should be: mongodb://host:port/database_name")
            
            self.db = self.client[db_name]
            self.users = self.db.users
            self.passwords = self.db.password_entries
            
            # Create indexes
            self.users.create_index([('username', ASCENDING)], unique=True)
            self.users.create_index([('email', ASCENDING)], unique=True)
            self.passwords.create_index([('user_id', ASCENDING)])
            self.passwords.create_index([('user_id', ASCENDING), ('website_url', ASCENDING)])
            
            print(f"✓ MongoDB database initialized: {self.db.name}")
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            print(f"❌ MongoDB initialization error: {e}")
            raise
    
    def _extract_database_name(self, uri: str) -> str:
        """Extract database name from MongoDB connection URI"""
        try:
            # Parse the URI
            parsed = urlparse(uri)
            
            # Get path (e.g., '/database_name?options')
            path = parsed.path.strip('/')
            
            # Remove query parameters if any
            db_name = path.split('?')[0]
            
            # If no database name found, use default
            if not db_name:
                print("⚠️  No database name in URI, using default: 'password_manager'")
                return 'password_manager'
            
            return db_name
            
        except Exception as e:
            print(f"⚠️  Error parsing URI, using default database: {e}")
            return 'password_manager'
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")
    
    # ... rest of the methods remain the same ...
    
    def create_user(self, username: str, email: str, password_hash: str, salt: str) -> Dict[str, Any]:
        """Create a new user"""
        user_doc = {
            '_id': str(uuid.uuid4()),
            'username': username,
            'email': email,
            'master_password_hash': password_hash,
            'salt': salt,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        try:
            self.users.insert_one(user_doc)
            return self._format_user(user_doc)
        except DuplicateKeyError:
            raise ValueError('Username or email already exists')
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        user = self.users.find_one({'username': username})
        return self._format_user(user) if user else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        user = self.users.find_one({'email': email})
        return self._format_user(user) if user else None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        user = self.users.find_one({'_id': user_id})
        return self._format_user(user) if user else None
    
    def create_password(self, user_id: str, website_url: str, website_name: str,
                       username: str, encrypted_password: str, iv: str, notes: str = '') -> Dict[str, Any]:
        """Create a new password entry"""
        password_doc = {
            '_id': str(uuid.uuid4()),
            'user_id': user_id,
            'website_url': website_url,
            'website_name': website_name,
            'username': username,
            'encrypted_password': encrypted_password,
            'iv': iv,
            'notes': notes,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'last_used': None
        }
        
        self.passwords.insert_one(password_doc)
        return self._format_password(password_doc)
    
    def get_passwords(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all passwords for a user"""
        passwords = self.passwords.find({'user_id': user_id})
        return [self._format_password(pwd) for pwd in passwords]
    
    def get_password_by_id(self, password_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific password entry"""
        password = self.passwords.find_one({'_id': password_id, 'user_id': user_id})
        
        if password:
            # Update last_used timestamp
            self.passwords.update_one(
                {'_id': password_id},
                {'$set': {'last_used': datetime.utcnow()}}
            )
            password['last_used'] = datetime.utcnow()
            return self._format_password(password)
        return None
    
    def update_password(self, password_id: str, user_id: str, data: Dict[str, Any]) -> bool:
        """Update a password entry"""
        data['updated_at'] = datetime.utcnow()
        
        result = self.passwords.update_one(
            {'_id': password_id, 'user_id': user_id},
            {'$set': data}
        )
        
        return result.modified_count > 0
    
    def delete_password(self, password_id: str, user_id: str) -> bool:
        """Delete a password entry"""
        result = self.passwords.delete_one({'_id': password_id, 'user_id': user_id})
        return result.deleted_count > 0
    
    def search_passwords(self, user_id: str, query: str) -> List[Dict[str, Any]]:
        """Search passwords by URL"""
        passwords = self.passwords.find({
            'user_id': user_id,
            'website_url': {'$regex': query, '$options': 'i'}
        })
        return [self._format_password(pwd) for pwd in passwords]
    
    def get_password_count(self, user_id: str) -> int:
        """Get count of password entries for a user"""
        return self.passwords.count_documents({'user_id': user_id})
    
    def _format_user(self, user_doc: Dict) -> Dict[str, Any]:
        """Format MongoDB user document to standard format"""
        if not user_doc:
            return None
        
        return {
            'id': user_doc['_id'],
            'username': user_doc['username'],
            'email': user_doc['email'],
            'master_password_hash': user_doc['master_password_hash'],
            'salt': user_doc['salt'],
            'created_at': user_doc['created_at'].isoformat() if user_doc.get('created_at') else None,
            'updated_at': user_doc['updated_at'].isoformat() if user_doc.get('updated_at') else None
        }
    
    def _format_password(self, pwd_doc: Dict) -> Dict[str, Any]:
        """Format MongoDB password document to standard format"""
        if not pwd_doc:
            return None
        
        return {
            'id': pwd_doc['_id'],
            'user_id': pwd_doc['user_id'],
            'website_url': pwd_doc['website_url'],
            'website_name': pwd_doc.get('website_name'),
            'username': pwd_doc.get('username'),
            'encrypted_password': pwd_doc['encrypted_password'],
            'iv': pwd_doc.get('iv'),
            'notes': pwd_doc.get('notes'),
            'created_at': pwd_doc['created_at'].isoformat() if pwd_doc.get('created_at') else None,
            'updated_at': pwd_doc['updated_at'].isoformat() if pwd_doc.get('updated_at') else None,
            'last_used': pwd_doc['last_used'].isoformat() if pwd_doc.get('last_used') else None
        }
