# 🔐 Password Manager Backend

> A secure, zero-knowledge password manager backend built with Python Flask. Seamlessly switch between PostgreSQL and MongoDB with enterprise-grade security.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- 🔐 **Zero-Knowledge Architecture** - Server never sees plaintext passwords
- 🔄 **Multi-Database Support** - Switch between PostgreSQL and MongoDB seamlessly
- ☁️ **Cloud-Ready** - Works with MongoDB Atlas, AWS RDS, and more
- 🔑 **Strong Authentication** - Argon2 password hashing + JWT tokens
- 🛡️ **Client-Side Encryption** - AES-256-GCM with PBKDF2 key derivation
- 🌐 **RESTful API** - Clean, well-documented endpoints
- ⚡ **WebSocket Support** - Real-time sync capabilities (Flask-SocketIO)
- 🎯 **Repository Pattern** - Clean, maintainable architecture
- 📊 **Production Ready** - CORS, error handling, connection pooling

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Flask Application                      │
│                       (app.py)                           │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
              ┌─────────────────────┐
              │  Database Factory   │
              │   (db_factory.py)   │
              │  - Selects DB based │
              │    on environment   │
              └──────────┬──────────┘
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
┌──────────────────┐           ┌──────────────────┐
│   PostgreSQL     │           │     MongoDB      │
│   Repository     │           │    Repository    │
└──────────────────┘           └──────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | Flask 3.1.2 |
| **Databases** | PostgreSQL (SQLAlchemy) + MongoDB (PyMongo) |
| **Authentication** | Argon2-CFFI, PyJWT |
| **Security** | Cryptography library, CORS |
| **WebSocket** | Flask-SocketIO |
| **Environment** | python-dotenv |

---

## 📁 Project Structure

```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── auth.py                     # Authentication & JWT logic
├── crypto_utils.py             # Security utilities
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (gitignored)
├── .env.example                # Environment template
├── database/
│   ├── __init__.py
│   ├── base_repository.py      # Abstract repository interface
│   ├── db_factory.py           # Database factory/selector
│   ├── postgres_repository.py  # PostgreSQL implementation
│   └── mongodb_repository.py   # MongoDB implementation
└── models/
    ├── __init__.py
    └── postgres_models.py      # SQLAlchemy models
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (optional, for PostgreSQL mode)
- MongoDB (optional, for MongoDB mode)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/password-manager.git
cd password-manager/backend
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Selection (choose one: postgresql or mongodb)
DATABASE_TYPE=postgresql

# PostgreSQL Configuration
POSTGRES_URI=postgresql://username:password@localhost:5432/password_manager

# MongoDB Configuration (Local)
MONGODB_URI=mongodb://localhost:27017/password_manager

# MongoDB Atlas (Cloud)
# MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/password_manager?retryWrites=true&w=majority

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,chrome-extension://your-extension-id
```

### 5️⃣ Setup Database

**For PostgreSQL:**

```bash
# Create database
createdb password_manager

# Or using psql
psql -U postgres -c "CREATE DATABASE password_manager;"
```

**For MongoDB:**

MongoDB will auto-create the database on first connection.

**For MongoDB Atlas (Cloud):**
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Add database user
4. Whitelist IP address (0.0.0.0/0 for development)
5. Get connection string and add to `.env`

### 6️⃣ Run Application

```bash
python app.py
```

Expected output:

```
✓ Using PostgreSQL database
✓ PostgreSQL connection successful
 * Running on http://0.0.0.0:5000/
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment (development/production) | `development` | No |
| `SECRET_KEY` | Flask secret key | - | ✅ Yes |
| `JWT_SECRET_KEY` | JWT signing key | - | ✅ Yes |
| `DATABASE_TYPE` | Database type (`postgresql` or `mongodb`) | `postgresql` | ✅ Yes |
| `POSTGRES_URI` | PostgreSQL connection string | - | If using PostgreSQL |
| `MONGODB_URI` | MongoDB connection string | - | If using MongoDB |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `*` | No |

### 🔑 Generate Secret Keys

```python
import secrets
print(secrets.token_hex(32))  # Use for SECRET_KEY and JWT_SECRET_KEY
```

---

## 🔄 Database Switching

Switch databases by changing one environment variable - **no code changes required!**

### Use PostgreSQL

```bash
export DATABASE_TYPE=postgresql
export POSTGRES_URI=postgresql://user:pass@localhost:5432/password_manager
```

### Use MongoDB (Local)

```bash
export DATABASE_TYPE=mongodb
export MONGODB_URI=mongodb://localhost:27017/password_manager
```

### Use MongoDB Atlas (Cloud)

```bash
export DATABASE_TYPE=mongodb
export MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/password_manager?retryWrites=true&w=majority
```

---

## 📡 API Endpoints

### Authentication

#### Register User

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "master_password": "SecurePassword123"
}
```

**Response:** `201 Created`

```json
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid",
    "username": "johndoe",
    "email": "john@example.com"
  },
  "token": "jwt-token-here"
}
```

#### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "master_password": "SecurePassword123"
}
```

**Response:** `200 OK`

```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid",
    "username": "johndoe"
  },
  "token": "jwt-token-here"
}
```

---

### Password Management

All password endpoints require JWT token in Authorization header:

```http
Authorization: Bearer <jwt-token>
```

#### Get All Passwords

```http
GET /api/passwords
```

**Response:** `200 OK`

```json
{
  "passwords": [
    {
      "id": "uuid",
      "website_url": "https://github.com",
      "website_name": "GitHub",
      "username": "encrypted-blob",
      "encrypted_password": "encrypted-blob",
      "iv": "initialization-vector"
    }
  ]
}
```

#### Create Password

```http
POST /api/passwords
Content-Type: application/json

{
  "website_url": "https://github.com",
  "website_name": "GitHub",
  "username": "encrypted-username-blob",
  "encrypted_password": "encrypted-password-blob",
  "iv": "initialization-vector",
  "notes": "encrypted-notes"
}
```

**Response:** `201 Created`

```json
{
  "message": "Password created successfully",
  "password": { ... }
}
```

#### Update Password

```http
PUT /api/passwords/{password_id}
Content-Type: application/json

{
  "website_name": "Updated Name",
  "encrypted_password": "new-encrypted-blob"
}
```

**Response:** `200 OK`

```json
{
  "message": "Password updated successfully"
}
```

#### Delete Password

```http
DELETE /api/passwords/{password_id}
```

**Response:** `200 OK`

```json
{
  "message": "Password deleted successfully"
}
```

#### Search Passwords

```http
POST /api/passwords/search
Content-Type: application/json

{
  "url": "github"
}
```

**Response:** `200 OK`

```json
{
  "passwords": [ ... ]
}
```

---

### Health Check

```http
GET /health
```

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "database": "postgresql"
}
```

---

## 🔒 Security Features

### Zero-Knowledge Architecture

- **Master password never sent to server**
- **All encryption happens client-side** using Web Crypto API (AES-256-GCM)
- **Server stores only encrypted blobs**
- Even with database access, data is unreadable without master password

### Password Hashing

- **Argon2** - Memory-hard algorithm (winner of Password Hashing Competition)
- **Unique salt** per user (32 bytes)
- **Parameters**: time_cost=3, memory_cost=64MB, parallelism=4

### JWT Tokens

- **HS256 algorithm** (HMAC-SHA256)
- **24-hour expiration**
- **Signed with secret key**
- Stored client-side only (not in database)

### Input Validation

- Sanitization of all user inputs
- Password strength validation
- SQL injection prevention (parameterized queries)
- XSS prevention (input sanitization)

---

## 🧪 Development

### Run in Debug Mode

```bash
export FLASK_ENV=development
python app.py
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

### Code Formatting

```bash
# Install formatter
pip install black flake8

# Format code
black .

# Lint
flake8 app.py database/ models/
```

---

## 🚢 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn gevent
gunicorn -w 4 -b 0.0.0.0:5000 --worker-class eventlet app:app
```

### Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Build and run:**

```bash
docker build -t password-manager-backend .
docker run -p 5000:5000 --env-file .env password-manager-backend
```

### Environment-Specific Configs

**Production `.env`:**

```env
FLASK_ENV=production
DEBUG=False
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/password_manager
CORS_ORIGINS=https://yourdomain.com
```

### HTTPS Setup

Use reverse proxy (Nginx):

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🔀 Database Migration

### PostgreSQL to MongoDB

```bash
# 1. Export data from PostgreSQL
pg_dump password_manager > backup.sql

# 2. Write migration script (Python)
# 3. Import to MongoDB
# 4. Switch database type
export DATABASE_TYPE=mongodb
```

### MongoDB to PostgreSQL

```bash
# 1. Export from MongoDB
mongodump --uri="mongodb://localhost/password_manager" --out=./backup

# 2. Write migration script
# 3. Import to PostgreSQL
# 4. Switch database type
export DATABASE_TYPE=postgresql
```

---

## 🔧 Troubleshooting

### CORS Errors

Update `.env`:

```env
CORS_ORIGINS=chrome-extension://your-extension-id,http://localhost:3000
```

### MongoDB Authentication Failed

1. Check username/password in Atlas
2. URL-encode special characters in password
3. Whitelist IP address (0.0.0.0/0 for development)
4. Wait 2 minutes after creating user

### PostgreSQL Connection Error

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Create database
createdb password_manager

# Test connection
psql -U postgres -d password_manager
```

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

Need help? Reach out to us:

- **GitHub Issues**: [Report an issue](https://github.com/yourusername/password-manager/issues)
- **Email**: support@yourdomain.com

---

## 🙏 Acknowledgments

Built with amazing open-source technologies:

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) - Cloud database
- [PostgreSQL](https://www.postgresql.org/) - Relational database
- [Argon2](https://github.com/P-H-C/phc-winner-argon2) - Password hashing
- [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API) - Client-side encryption

---

<div align="center">

**Made with ❤️ by the Password Manager Team**

⭐ Star us on GitHub if you find this project useful!

</div>