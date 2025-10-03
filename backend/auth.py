"""
Authentication module with Argon2 password hashing and JWT tokens
"""
import jwt
import secrets
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Initialize Argon2 password hasher
ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16
)

def generate_salt():
    """Generate a cryptographically secure salt"""
    return secrets.token_hex(32)

def hash_master_password(password, salt):
    """
    Hash master password using Argon2
    Returns: hashed password
    """
    salted_password = password + salt
    return ph.hash(salted_password)

def verify_master_password(password, salt, hashed_password):
    """
    Verify master password against stored hash
    Returns: True if valid, False otherwise
    """
    try:
        salted_password = password + salt
        ph.verify(hashed_password, salted_password)
        return True
    except VerifyMismatchError:
        return False

def generate_jwt_token(user_id, username, secret_key, algorithm='HS256', expiration_hours=24):
    """
    Generate JWT token for authenticated user
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=expiration_hours)
    }
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_jwt_token(token, secret_key, algorithm='HS256'):
    """
    Decode and verify JWT token
    Returns: payload dict or None if invalid
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(secret_key, algorithm='HS256'):
    """
    Decorator to protect routes with JWT authentication
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            # Get token from Authorization header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(' ')[1]  # Bearer <token>
                except IndexError:
                    return jsonify({'error': 'Invalid authorization header format'}), 401
            
            if not token:
                return jsonify({'error': 'Authentication token is missing'}), 401
            
            # Decode token
            payload = decode_jwt_token(token, secret_key, algorithm)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Pass user info to the route
            request.current_user = payload
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
