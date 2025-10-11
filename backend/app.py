from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import os

from config import get_config
from database.db_factory import get_repository
from auth import (
    generate_salt, 
    hash_master_password, 
    verify_master_password,
    generate_jwt_token,
    token_required
)
from crypto_utils import sanitize_input, validate_password_strength

# Initialize Flask app
app = Flask(__name__)
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(get_config(config_name))

# CORS Configuration
CORS(app, resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# WebSocket
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize database repository
db_repo = get_repository(get_config(config_name))

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
    else:
        response.headers['Access-Control-Allow-Origin'] = '*'
    
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'database': app.config['DATABASE_TYPE']}), 200

# Register
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = sanitize_input(data.get('username', ''))
        email = sanitize_input(data.get('email', ''))
        master_password = data.get('master_password', '')
        
        if not username or not email or not master_password:
            return jsonify({'error': 'All fields are required'}), 400
        
        is_valid, message = validate_password_strength(master_password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Check if user exists
        if db_repo.get_user_by_username(username):
            return jsonify({'error': 'Username already exists'}), 409
        
        if db_repo.get_user_by_email(email):
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create user
        salt = generate_salt()
        password_hash = hash_master_password(master_password, salt)
        
        user = db_repo.create_user(username, email, password_hash, salt)
        
        # Generate token
        token = generate_jwt_token(
            user['id'],
            user['username'],
            app.config['JWT_SECRET_KEY'],
            app.config['JWT_ALGORITHM'],
            app.config['JWT_EXPIRATION_HOURS']
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            },
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Login
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = sanitize_input(data.get('username', ''))
        master_password = data.get('master_password', '')
        
        if not username or not master_password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = db_repo.get_user_by_username(username)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not verify_master_password(master_password, user['salt'], user['master_password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = generate_jwt_token(
            user['id'],
            user['username'],
            app.config['JWT_SECRET_KEY'],
            app.config['JWT_ALGORITHM'],
            app.config['JWT_EXPIRATION_HOURS']
        )
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'username': user['username']
            },
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all passwords
@app.route('/api/passwords', methods=['GET'])
@token_required(lambda: app.config['JWT_SECRET_KEY'], lambda: app.config['JWT_ALGORITHM'])
def get_passwords():
    try:
        user_id = request.current_user['user_id']
        passwords = db_repo.get_passwords(user_id)
        
        return jsonify({'passwords': passwords}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create password
@app.route('/api/passwords', methods=['POST'])
@token_required(lambda: app.config['JWT_SECRET_KEY'], lambda: app.config['JWT_ALGORITHM'])
def create_password():
    try:
        user_id = request.current_user['user_id']
        data = request.json
        
        # Check password limit
        count = db_repo.get_password_count(user_id)
        if count >= app.config['MAX_PASSWORD_ENTRIES']:
            return jsonify({'error': 'Maximum password entries reached'}), 400
        
        website_url = sanitize_input(data.get('website_url', ''))
        website_name = sanitize_input(data.get('website_name', ''))
        username = data.get('username', '')
        encrypted_password = data.get('encrypted_password', '')
        iv = data.get('iv', '')
        notes = data.get('notes', '')
        
        if not website_url or not encrypted_password:
            return jsonify({'error': 'Website URL and password are required'}), 400
        
        password = db_repo.create_password(
            user_id,
            website_url,
            website_name or website_url,
            username,
            encrypted_password,
            iv,
            notes
        )
        
        return jsonify({
            'message': 'Password created successfully',
            'password': password
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get specific password
@app.route('/api/passwords/<password_id>', methods=['GET'])
@token_required(lambda: app.config['JWT_SECRET_KEY'], lambda: app.config['JWT_ALGORITHM'])
def get_password(password_id):
    try:
        user_id = request.current_user['user_id']
        password = db_repo.get_password_by_id(password_id, user_id)
        
        if not password:
            return jsonify({'error': 'Password not found'}), 404
        
        return jsonify({'password': password}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update password
@app.route('/api/passwords/<password_id>', methods=['PUT'])
@token_required(lambda: app.config['JWT_SECRET_KEY'], lambda: app.config['JWT_ALGORITHM'])
def update_password(password_id):
    try:
        user_id = request.current_user['user_id']
        data = request.json
        
        update_data = {}
        if 'website_url' in data:
            update_data['website_url'] = sanitize_input(data['website_url'])
        if 'website_name' in data:
            update_data['website_name'] = sanitize_input(data['website_name'])
        if 'username' in data:
            update_data['username'] = data['username']
        if 'encrypted_password' in data:
            update_data['encrypted_password'] = data['encrypted_password']
        if 'iv' in data:
            update_data['iv'] = data['iv']
        if 'notes' in data:
            update_data['notes'] = data['notes']
        
        success = db_repo.update_password(password_id, user_id, update_data)
        
        if not success:
            return jsonify({'error': 'Password not found'}), 404
        
        return jsonify({'message': 'Password updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete password
@app.route('/api/passwords/<password_id>', methods=['DELETE'])
@token_required(lambda: app.config['JWT_SECRET_KEY'], lambda: app.config['JWT_ALGORITHM'])
def delete_password(password_id):
    try:
        user_id = request.current_user['user_id']
        success = db_repo.delete_password(password_id, user_id)
        
        if not success:
            return jsonify({'error': 'Password not found'}), 404
        
        return jsonify({'message': 'Password deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Search passwords
@app.route('/api/passwords/search', methods=['POST'])
@token_required(lambda: app.config['JWT_SECRET_KEY'], lambda: app.config['JWT_ALGORITHM'])
def search_passwords():
    try:
        user_id = request.current_user['user_id']
        data = request.json
        query = sanitize_input(data.get('url', ''))
        
        passwords = db_repo.search_passwords(user_id, query)
        
        return jsonify({'passwords': passwords}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
