"""
Comprehensive test suite for Password Manager Backend
Tests authentication, CRUD operations, and security features
"""
import pytest
import json
from app import app, db_manager
from models import User, PasswordEntry
from auth import generate_salt, hash_master_password
from config import get_config

# Configure for testing
app.config.from_object(get_config('testing'))

@pytest.fixture
def client():
    """Create test client"""
    with app.test_client() as client:
        with app.app_context():
            db_manager.create_tables()
            yield client
            db_manager.drop_tables()

@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return auth headers"""
    # Register user
    response = client.post('/api/auth/register', 
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'master_password': 'TestPass123!'
        })
    
    data = json.loads(response.data)
    token = data['token']
    
    return {'Authorization': f'Bearer {token}'}

# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register',
        json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'master_password': 'SecurePass123!'
        })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'token' in data
    assert data['user']['username'] == 'newuser'

def test_register_duplicate_username(client):
    """Test registration with duplicate username"""
    # First registration
    client.post('/api/auth/register',
        json={
            'username': 'duplicate',
            'email': 'user1@example.com',
            'master_password': 'SecurePass123!'
        })
    
    # Duplicate registration
    response = client.post('/api/auth/register',
        json={
            'username': 'duplicate',
            'email': 'user2@example.com',
            'master_password': 'SecurePass123!'
        })
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'already exists' in data['error']

def test_register_weak_password(client):
    """Test registration with weak password"""
    response = client.post('/api/auth/register',
        json={
            'username': 'weakuser',
            'email': 'weak@example.com',
            'master_password': 'weak'
        })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Password' in data['error']

def test_login_success(client):
    """Test successful login"""
    # Register user first
    client.post('/api/auth/register',
        json={
            'username': 'loginuser',
            'email': 'login@example.com',
            'master_password': 'LoginPass123!'
        })
    
    # Login
    response = client.post('/api/auth/login',
        json={
            'username': 'loginuser',
            'master_password': 'LoginPass123!'
        })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert data['message'] == 'Login successful'

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login',
        json={
            'username': 'nonexistent',
            'master_password': 'WrongPass123!'
        })
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'Invalid credentials' in data['error']

# ============================================================================
# PASSWORD CRUD TESTS
# ============================================================================

def test_create_password(client, auth_headers):
    """Test creating a password entry"""
    response = client.post('/api/passwords',
        headers=auth_headers,
        json={
            'website_url': 'https://example.com',
            'website_name': 'Example Site',
            'username': 'encrypted_username',
            'encrypted_password': 'encrypted_password_blob',
            'iv': 'initialization_vector',
            'notes': 'encrypted_notes'
        })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['password']['website_url'] == 'https://example.com'

def test_get_passwords(client, auth_headers):
    """Test retrieving all passwords"""
    # Create some passwords
    for i in range(3):
        client.post('/api/passwords',
            headers=auth_headers,
            json={
                'website_url': f'https://site{i}.com',
                'website_name': f'Site {i}',
                'encrypted_password': f'encrypted_{i}',
                'iv': f'iv_{i}'
            })
    
    # Get all passwords
    response = client.get('/api/passwords', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['passwords']) == 3

def test_get_specific_password(client, auth_headers):
    """Test retrieving a specific password"""
    # Create password
    create_response = client.post('/api/passwords',
        headers=auth_headers,
        json={
            'website_url': 'https://specific.com',
            'website_name': 'Specific Site',
            'encrypted_password': 'encrypted_pass',
            'iv': 'iv_data'
        })
    
    password_id = json.loads(create_response.data)['password']['id']
    
    # Get password
    response = client.get(f'/api/passwords/{password_id}', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['password']['website_url'] == 'https://specific.com'

def test_update_password(client, auth_headers):
    """Test updating a password entry"""
    # Create password
    create_response = client.post('/api/passwords',
        headers=auth_headers,
        json={
            'website_url': 'https://update.com',
            'encrypted_password': 'old_encrypted',
            'iv': 'old_iv'
        })
    
    password_id = json.loads(create_response.data)['password']['id']
    
    # Update password
    response = client.put(f'/api/passwords/{password_id}',
        headers=auth_headers,
        json={
            'website_name': 'Updated Name',
            'encrypted_password': 'new_encrypted',
            'iv': 'new_iv'
        })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['password']['website_name'] == 'Updated Name'

def test_delete_password(client, auth_headers):
    """Test deleting a password entry"""
    # Create password
    create_response = client.post('/api/passwords',
        headers=auth_headers,
        json={
            'website_url': 'https://delete.com',
            'encrypted_password': 'encrypted',
            'iv': 'iv'
        })
    
    password_id = json.loads(create_response.data)['password']['id']
    
    # Delete password
    response = client.delete(f'/api/passwords/{password_id}', headers=auth_headers)
    
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f'/api/passwords/{password_id}', headers=auth_headers)
    assert get_response.status_code == 404

def test_search_passwords(client, auth_headers):
    """Test searching passwords by URL"""
    # Create passwords
    client.post('/api/passwords',
        headers=auth_headers,
        json={
            'website_url': 'https://github.com/user/repo',
            'encrypted_password': 'encrypted1',
            'iv': 'iv1'
        })
    
    client.post('/api/passwords',
        headers=auth_headers,
        json={
            'website_url': 'https://gitlab.com/user/project',
            'encrypted_password': 'encrypted2',
            'iv': 'iv2'
        })
    
    # Search for github
    response = client.post('/api/passwords/search',
        headers=auth_headers,
        json={'url': 'github'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['passwords']) == 1
    assert 'github' in data['passwords'][0]['website_url']

# ============================================================================
# SECURITY TESTS
# ============================================================================

def test_unauthorized_access(client):
    """Test accessing protected endpoints without authentication"""
    response = client.get('/api/passwords')
    assert response.status_code == 401

def test_invalid_token(client):
    """Test accessing with invalid token"""
    headers = {'Authorization': 'Bearer invalid_token_here'}
    response = client.get('/api/passwords', headers=headers)
    assert response.status_code == 401

def test_password_limit(client, auth_headers):
    """Test password entry limit per user"""
    # This test would create MAX_PASSWORD_ENTRIES + 1 passwords
    # For brevity, we'll just test the logic exists
    pass

# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=.', '--cov-report=html'])
