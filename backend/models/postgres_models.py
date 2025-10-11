from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    master_password_hash = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    passwords = relationship('PasswordEntry', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'master_password_hash': self.master_password_hash,
            'salt': self.salt,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PasswordEntry(Base):
    __tablename__ = 'password_entries'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    website_url = Column(String(500), nullable=False)
    website_name = Column(String(255))
    username = Column(Text)
    encrypted_password = Column(Text, nullable=False)
    iv = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used = Column(DateTime)
    
    user = relationship('User', back_populates='passwords')
    
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

class PostgresConnectionManager:
    def __init__(self, database_uri):
        self.engine = create_engine(database_uri, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
    
    def get_session(self):
        return self.Session()
