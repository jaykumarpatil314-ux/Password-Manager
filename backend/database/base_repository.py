from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class BaseRepository(ABC):
    """Abstract base class for database repositories"""
    
    @abstractmethod
    def initialize(self):
        """Initialize database connection"""
        pass
    
    @abstractmethod
    def close(self):
        """Close database connection"""
        pass
    
    # User operations
    @abstractmethod
    def create_user(self, username: str, email: str, password_hash: str, salt: str) -> Dict[str, Any]:
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        pass
    
    # Password operations
    @abstractmethod
    def create_password(self, user_id: str, website_url: str, website_name: str, 
                       username: str, encrypted_password: str, iv: str, notes: str = '') -> Dict[str, Any]:
        """Create a new password entry"""
        pass
    
    @abstractmethod
    def get_passwords(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all passwords for a user"""
        pass
    
    @abstractmethod
    def get_password_by_id(self, password_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific password entry"""
        pass
    
    @abstractmethod
    def update_password(self, password_id: str, user_id: str, data: Dict[str, Any]) -> bool:
        """Update a password entry"""
        pass
    
    @abstractmethod
    def delete_password(self, password_id: str, user_id: str) -> bool:
        """Delete a password entry"""
        pass
    
    @abstractmethod
    def search_passwords(self, user_id: str, query: str) -> List[Dict[str, Any]]:
        """Search passwords by URL"""
        pass
    
    @abstractmethod
    def get_password_count(self, user_id: str) -> int:
        """Get count of password entries for a user"""
        pass
