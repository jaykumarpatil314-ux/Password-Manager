"""
Database models for Password Manager
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    """User model - stores user authentication data"""
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    master_password_hash = Column(String(255), nullable=False)  # Argon2 hashed
    salt = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    password_entries = relationship('PasswordEntry', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PasswordEntry(Base):
    """Password Entry model - stores encrypted password data"""
    __tablename__ = 'password_entries'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    website_url = Column(String(500), nullable=False)
    website_name = Column(String(255))
    username = Column(Text)  # Encrypted
    encrypted_password = Column(Text, nullable=False)  # AES encrypted blob
    iv = Column(String(255))  # Initialization vector for AES
    notes = Column(Text)  # Encrypted notes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used = Column(DateTime)
    
    # Relationships
    user = relationship('User', back_populates='password_entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'website_url': self.website_url,
            'website_name': self.website_name,
            'username': self.username,
            'encrypted_password': self.encrypted_password,
            'iv': self.iv,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_used': self.last_used.isoformat() if self.last_used else None
        }

class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self, database_uri):
        self.engine = create_engine(database_uri, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables"""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
