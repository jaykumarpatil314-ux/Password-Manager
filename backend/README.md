# Backend Setup Guide

This guide covers the complete setup and configuration of the Password Manager backend server.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [PostgreSQL Installation](#postgresql-installation)
3. [Database Setup](#database-setup)
4. [Python Environment Setup](#python-environment-setup)
5. [Environment Configuration](#environment-configuration)
6. [Running the Server](#running-the-server)
7. [Testing](#testing)
8. [Production Deployment](#production-deployment)

---

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- virtualenv (recommended)

---

## PostgreSQL Installation

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

### macOS

```bash
brew install postgresql
```

### Windows

Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/)

### Start PostgreSQL Service

**Linux:**
```bash
sudo service postgresql start
```

**macOS:**
```bash
brew services start postgresql
```

**Windows:**
PostgreSQL service starts automatically after installation.

---

## Database Setup

### Create Database and User

1. Access PostgreSQL shell:

```bash
sudo -u postgres psql
```

2. Run the following SQL commands:

```sql
CREATE DATABASE password_manager;
CREATE USER pmuser WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE password_manager TO pmuser;
\q
```

**Important**: Replace `'secure_password'` with a strong password of your choice.

### Verify Database Creation

```bash
psql -U pmuser -d password_manager -h localhost
# Enter the password you set above
```

If successful, you'll see the PostgreSQL prompt.

---

## Python Environment Setup

### Navigate to Backend Directory

```bash
cd backend
```

### Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Verify Installation

```bash
pip list
```

You should see Flask, psycopg2, PyJWT, and other dependencies listed.

---

## Environment Configuration

### Create Environment File

Create a `.env` file in the backend directory:

```bash
touch .env
```

### Add Configuration Variables

Open `.env` in your text editor and add:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=password_manager
DB_USER=pmuser
DB_PASSWORD=secure_password

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Server Configuration
PORT=5000
HOST=0.0.0.0
```

**Security Notes**:
- Replace `DB_PASSWORD` with the password you set during database setup
- Generate strong random values for `SECRET_KEY` and `JWT_SECRET_KEY`
- For production, set `FLASK_ENV=production` and `FLASK_DEBUG=False`

### Generate Secret Keys

You can generate secure secret keys using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Running the Server

### Start the Development Server

```bash
python app.py
```

You should see output similar to:

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Verify Server is Running

Open a new terminal and test the API:

```bash
curl http://localhost:5000/health
```

Expected response: `{"status": "ok"}`

---

## Testing

### Backend Tests

#### Unit Tests

If unit tests are available, run:

```bash
python -m pytest tests/
```

### Manual Testing Checklist

#### Authentication Tests

- [ ] Register new user with strong password
- [ ] Register with weak password (should fail with validation error)
- [ ] Register with duplicate username (should return 409 error)
- [ ] Login with correct credentials (should return JWT token)
- [ ] Login with incorrect credentials (should return 401 error)
- [ ] Logout and verify token is invalidated

#### Password Management Tests

- [ ] Add new password entry (requires authentication)
- [ ] Retrieve all passwords for authenticated user
- [ ] Edit existing password entry
- [ ] Delete password entry
- [ ] Search passwords by URL/domain
- [ ] Verify password encryption in database

#### Security Tests

**Database Security:**
```bash
# Connect to database and verify encryption
psql -U pmuser -d password_manager -h localhost
SELECT * FROM passwords;
# Verify 'password' field contains encrypted data, not plain text
```

**API Security:**
- [ ] Attempt to access protected endpoints without token (should return 401)
- [ ] Attempt to access another user's passwords (should return 403)
- [ ] Test SQL injection attempts (should be blocked)
- [ ] Test XSS attempts in input fields (should be sanitized)

**Token Security:**
- [ ] Verify token expiration works correctly
- [ ] Test with invalid/malformed tokens (should return 401)
- [ ] Verify token contains no sensitive information

### Performance Testing

#### Load Testing

Test with multiple password entries:

```bash
# Create 100+ test entries
for i in {1..100}; do
  curl -X POST http://localhost:5000/api/passwords \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"test$i.com\",\"username\":\"user$i\",\"password\":\"encrypted_pass$i\"}"
done
```

#### Performance Metrics

- [ ] Search response time < 200ms for 100 entries
- [ ] Encryption/decryption operations < 100ms
- [ ] API response time < 500ms
- [ ] Memory usage stable under load

---

## Production Deployment

### Security Hardening

1. **Use HTTPS**: Configure SSL/TLS certificates
2. **Update Environment**:
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```
3. **Database Security**:
   - Use strong database passwords
   - Restrict database access to application server only
   - Enable SSL for database connections

4. **Server Configuration**:
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Configure reverse proxy (Nginx, Apache)
   - Set up firewall rules

### Deployment with Gunicorn

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Database Migrations

For production, ensure proper database migration strategy:
- Use tools like Alembic for schema migrations
- Backup database before migrations
- Test migrations in staging environment

### Monitoring

Set up monitoring for:
- Server uptime
- API response times
- Error rates
- Database performance
- Disk space usage

### Backup Strategy

- Regular automated database backups
- Store backups in secure, separate location
- Test backup restoration periodically

---

## Troubleshooting

### Common Issues

**Database Connection Error:**
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database and user exist

**Import Errors:**
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Port Already in Use:**
- Change PORT in `.env` or kill process using port 5000
- Find process: `lsof -i :5000` (Linux/macOS) or `netstat -ano | findstr :5000` (Windows)

**Permission Errors:**
- Check file permissions
- Verify user has write access to log directory

---

## API Documentation

For detailed API endpoint documentation, refer to the API documentation file or use tools like Swagger/OpenAPI for interactive documentation.

### Quick Reference

- `POST /api/register` - Register new user
- `POST /api/login` - Authenticate user
- `GET /api/passwords` - Get all passwords
- `POST /api/passwords` - Add new password
- `PUT /api/passwords/:id` - Update password
- `DELETE /api/passwords/:id` - Delete password
- `GET /health` - Health check endpoint



License
MIT