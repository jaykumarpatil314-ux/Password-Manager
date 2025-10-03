"""
Cryptographic utilities for backend operations
"""
import secrets
import hashlib
import hmac

def generate_secure_token(length=32):
    """Generate cryptographically secure random token"""
    return secrets.token_urlsafe(length)

def constant_time_compare(val1, val2):
    """Constant-time comparison to prevent timing attacks"""
    return hmac.compare_digest(val1, val2)

def generate_session_id():
    """Generate unique session ID"""
    return secrets.token_hex(32)

def validate_password_strength(password):
    """
    Validate password strength
    Returns: (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and digits"
    
    return True, "Password is strong"

def sanitize_input(input_string, max_length=500):
    """Sanitize user input to prevent injection attacks"""
    if not input_string:
        return ""
    
    # Remove null bytes
    sanitized = input_string.replace('\x00', '')
    
    # Limit length
    sanitized = sanitized[:max_length]
    
    return sanitized.strip()
