from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from database.base_repository import BaseRepository
from models.postgres_models import PostgresConnectionManager, User, PasswordEntry

class PostgresRepository(BaseRepository):
    """PostgreSQL implementation of the repository"""
    
    def __init__(self, database_uri: str):
        self.database_uri = database_uri
        self.manager = None
        self.session = None
    
    def initialize(self):
        """Initialize PostgreSQL connection"""
        self.manager = PostgresConnectionManager(self.database_uri)
        self.manager.create_tables()
        self.session = self.manager.get_session()
        print("✓ PostgreSQL database initialized")
    
    def close(self):
        """Close PostgreSQL connection"""
        if self.session:
            self.session.close()
    
    def create_user(self, username: str, email: str, password_hash: str, salt: str) -> Dict[str, Any]:
        """Create a new user"""
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            master_password_hash=password_hash,
            salt=salt
        )
        self.session.add(user)
        self.session.commit()
        return user.to_dict()
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        user = self.session.query(User).filter_by(username=username).first()
        return user.to_dict() if user else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        user = self.session.query(User).filter_by(email=email).first()
        return user.to_dict() if user else None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        user = self.session.query(User).filter_by(id=user_id).first()
        return user.to_dict() if user else None
    
    def create_password(self, user_id: str, website_url: str, website_name: str,
                       username: str, encrypted_password: str, iv: str, notes: str = '') -> Dict[str, Any]:
        """Create a new password entry"""
        password_entry = PasswordEntry(
            id=str(uuid.uuid4()),
            user_id=user_id,
            website_url=website_url,
            website_name=website_name,
            username=username,
            encrypted_password=encrypted_password,
            iv=iv,
            notes=notes
        )
        self.session.add(password_entry)
        self.session.commit()
        return password_entry.to_dict()
    
    def get_passwords(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all passwords for a user"""
        passwords = self.session.query(PasswordEntry).filter_by(user_id=user_id).all()
        return [pwd.to_dict() for pwd in passwords]
    
    def get_password_by_id(self, password_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific password entry"""
        password = self.session.query(PasswordEntry).filter_by(
            id=password_id, 
            user_id=user_id
        ).first()
        
        if password:
            password.last_used = datetime.utcnow()
            self.session.commit()
            return password.to_dict()
        return None
    
    def update_password(self, password_id: str, user_id: str, data: Dict[str, Any]) -> bool:
        """Update a password entry"""
        password = self.session.query(PasswordEntry).filter_by(
            id=password_id,
            user_id=user_id
        ).first()
        
        if not password:
            return False
        
        for key, value in data.items():
            if hasattr(password, key):
                setattr(password, key, value)
        
        password.updated_at = datetime.utcnow()
        self.session.commit()
        return True
    
    def delete_password(self, password_id: str, user_id: str) -> bool:
        """Delete a password entry"""
        password = self.session.query(PasswordEntry).filter_by(
            id=password_id,
            user_id=user_id
        ).first()
        
        if not password:
            return False
        
        self.session.delete(password)
        self.session.commit()
        return True
    
    def search_passwords(self, user_id: str, query: str) -> List[Dict[str, Any]]:
        """Search passwords by URL"""
        passwords = self.session.query(PasswordEntry).filter(
            PasswordEntry.user_id == user_id,
            PasswordEntry.website_url.ilike(f'%{query}%')
        ).all()
        return [pwd.to_dict() for pwd in passwords]
    
    def get_password_count(self, user_id: str) -> int:
        """Get count of password entries for a user"""
        return self.session.query(PasswordEntry).filter_by(user_id=user_id).count()
