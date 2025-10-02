<<<<<<< HEAD
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Password Manager Backend is running!"

if __name__ == '__main__':
    app.run(debug=True)
=======
"""
Main Flask application for Password Manager Backend
Implements REST API and WebSocket communication
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os

from config import get_config
from models import DatabaseManager, User, PasswordEntry
from auth import (
    generate_salt, hash_master_password, verify_master_password,
    generate_jwt_token, decode_jwt_token, token_required
)
from crypto_utils import sanitize_input, validate_password_strength

# Initialize Flask app
app = Flask(__name__)
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(get_config(config_name))

# Initialize CORS
CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins=app.config['CORS_ORIGINS'], async_mode='eventlet')

# Initialize database
db_manager = DatabaseManager(app.config['SQLALCHEMY_DATABASE_URI'])
db_manager.create_tables()

# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        
        # Validate input
        username = sanitize_input(data.get('username', ''), max_length=100)
        email = sanitize_input(data.get('email', ''), max_length=255)
        master_password = data.get('master_password', '')
        
        if not username or not email or not master_password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate password strength
        is_valid, message = validate_password_strength(master_password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Generate salt and hash password
        salt = generate_salt()
        password_hash = hash_master_password(master_password, salt)
        
        # Create user
        session = db_manager.get_session()
        try:
            user = User(
                username=username,
                email=email,
                master_password_hash=password_hash,
                salt=salt
            )
            session.add(user)
            session.commit()
            
            # Generate JWT token
            token = generate_jwt_token(
                user.id,
                user.username,
                app.config['JWT_SECRET_KEY'],
                app.config['JWT_ALGORITHM'],
                app.config['JWT_EXPIRATION_HOURS']
            )
            
            return jsonify({
                'message': 'User registered successfully',
                'user': user.to_dict(),
                'token': token
            }), 201
            
        except IntegrityError:
            session.rollback()
            return jsonify({'error': 'Username or email already exists'}), 409
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    try:
        data = request.get_json()
        
        username = sanitize_input(data.get('username', ''), max_length=100)
        master_password = data.get('master_password', '')
        
        if not username or not master_password:
            return jsonify({'error': 'Missing credentials'}), 400
        
        # Find user
        session = db_manager.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            
            if not user:
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Verify password
            if not verify_master_password(master_password, user.salt, user.master_password_hash):
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Generate JWT token
            token = generate_jwt_token(
                user.id,
                user.username,
                app.config['JWT_SECRET_KEY'],
                app.config['JWT_ALGORITHM'],
                app.config['JWT_EXPIRATION_HOURS']
            )
            
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict(),
                'token': token
            }), 200
            
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@app.route('/api/passwords', methods=['GET'])
@token_required(app.config['JWT_SECRET_KEY'], app.config['JWT_ALGORITHM'])
def get_passwords():
    """Get all password entries for authenticated user"""
    try:
        user_id = request.current_user['user_id']
        
        session = db_manager.get_session()
        try:
            entries = session.query(PasswordEntry).filter_by(user_id=user_id).all()
            return jsonify({
                'passwords': [entry.to_dict() for entry in entries]
            }), 200
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve passwords: {str(e)}'}), 500

@app.route('/api/passwords', methods=['POST'])
@token_required(app.config['JWT_SECRET_KEY'], app.config['JWT_ALGORITHM'])
def create_password():
    """Create new password entry"""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        # Validate input
        website_url = sanitize_input(data.get('website_url', ''), max_length=500)
        website_name = sanitize_input(data.get('website_name', ''), max_length=255)
        username = data.get('username', '')  # Already encrypted client-side
        encrypted_password = data.get('encrypted_password', '')
        iv = data.get('iv', '')
        notes = data.get('notes', '')
        
        if not website_url or not encrypted_password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        session = db_manager.get_session()
        try:
            # Check user password limit
            count = session.query(PasswordEntry).filter_by(user_id=user_id).count()
            if count >= app.config['MAX_PASSWORD_ENTRIES']:
                return jsonify({'error': 'Maximum password entries reached'}), 403
            
            # Create entry
            entry = PasswordEntry(
                user_id=user_id,
                website_url=website_url,
                website_name=website_name,
                username=username,
                encrypted_password=encrypted_password,
                iv=iv,
                notes=notes
            )
            session.add(entry)
            session.commit()
            
            return jsonify({
                'message': 'Password created successfully',
                'password': entry.to_dict()
            }), 201
            
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': f'Failed to create password: {str(e)}'}), 500

@app.route('/api/passwords/<password_id>', methods=['GET'])
@token_required(app.config['JWT_SECRET_KEY'], app.config['JWT_ALGORITHM'])
def get_password(password_id):
    """Get specific password entry"""
    try:
        user_id = request.current_user['user_id']
        
        session = db_manager.get_session()
        try:
            entry = session.query(PasswordEntry).filter_by(
                id=password_id,
                user_id=user_id
            ).first()
            
            if not entry:
                return jsonify({'error': 'Password not found'}), 404
            
            # Update last used timestamp
            entry.last_used = datetime.utcnow()
            session.commit()
            
            return jsonify({'password': entry.to_dict()}), 200
            
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve password: {str(e)}'}), 500

@app.route('/api/passwords/<password_id>', methods=['PUT'])
@token_required(app.config['JWT_SECRET_KEY'], app.config['JWT_ALGORITHM'])
def update_password(password_id):
    """Update password entry"""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        session = db_manager.get_session()
        try:
            entry = session.query(PasswordEntry).filter_by(
                id=password_id,
                user_id=user_id
            ).first()
            
            if not entry:
                return jsonify({'error': 'Password not found'}), 404
            
            # Update fields
            if 'website_url' in data:
                entry.website_url = sanitize_input(data['website_url'], max_length=500)
            if 'website_name' in data:
                entry.website_name = sanitize_input(data['website_name'], max_length=255)
            if 'username' in data:
                entry.username = data['username']
            if 'encrypted_password' in data:
                entry.encrypted_password = data['encrypted_password']
            if 'iv' in data:
                entry.iv = data['iv']
            if 'notes' in data:
                entry.notes = data['notes']
            
            entry.updated_at = datetime.utcnow()
            session.commit()
            
            return jsonify({
                'message': 'Password updated successfully',
                'password': entry.to_dict()
            }), 200
            
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': f'Failed to update password: {str(e)}'}), 500

@app.route('/api/passwords/<password_id>', methods=['DELETE'])
@token_required(app.config['JWT_SECRET_KEY'], app.config['JWT_ALGORITHM'])
def delete_password(password_id):
    """Delete password entry"""
    try:
        user_id = request.current_user['user_id']
        
        session = db_manager.get_session()
        try:
            entry = session.query(PasswordEntry).filter_by(
                id=password_id,
                user_id=user_id
            ).first()
            
            if not entry:
                return jsonify({'error': 'Password not found'}), 404
            
            session.delete(entry)
            session.commit()
            
            return jsonify({'message': 'Password deleted successfully'}), 200
            
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': f'Failed to delete password: {str(e)}'}), 500

@app.route('/api/passwords/search', methods=['POST'])
@token_required(app.config['JWT_SECRET_KEY'], app.config['JWT_ALGORITHM'])
def search_passwords():
    """Search password entries by URL"""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        url = sanitize_input(data.get('url', ''), max_length=500)
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        session = db_manager.get_session()
        try:
            # Search by partial URL match
            entries = session.query(PasswordEntry).filter(
                PasswordEntry.user_id == user_id,
                PasswordEntry.website_url.contains(url)
            ).all()
            
            return jsonify({
                'passwords': [entry.to_dict() for entry in entries]
            }), 200
            
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('connection_status', {'status': 'connected', 'timestamp': datetime.utcnow().isoformat()})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    pass

@socketio.on('authenticate')
def handle_authenticate(data):
    """Authenticate WebSocket connection"""
    try:
        token = data.get('token')
        
        if not token:
            emit('auth_error', {'error': 'Token is required'})
            return
        
        payload = decode_jwt_token(token, app.config['JWT_SECRET_KEY'], app.config['JWT_ALGORITHM'])
        
        if not payload:
            emit('auth_error', {'error': 'Invalid or expired token'})
            return
        
        # Join user-specific room
        user_id = payload['user_id']
        join_room(user_id)
        
        emit('authenticated', {'user_id': user_id, 'username': payload['username']})
        
    except Exception as e:
        emit('auth_error', {'error': str(e)})

@socketio.on('sync_request')
def handle_sync_request(data):
    """Handle real-time sync request"""
    try:
        token = data.get('token')
        
        if not token:
            emit('sync_error', {'error': 'Token is required'})
            return
        
        payload = decode_jwt_token(token, app.config['JWT_SECRET_KEY'], app.config['JWT_ALGORITHM'])
        
        if not payload:
            emit('sync_error', {'error': 'Invalid token'})
            return
        
        user_id = payload['user_id']
        
        # Get all password entries
        session = db_manager.get_session()
        try:
            entries = session.query(PasswordEntry).filter_by(user_id=user_id).all()
            emit('sync_response', {
                'passwords': [entry.to_dict() for entry in entries],
                'timestamp': datetime.utcnow().isoformat()
            })
        finally:
            session.close()
            
    except Exception as e:
        emit('sync_error', {'error': str(e)})

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
>>>>>>> 7bc2a62 (Backend for the password manager)
