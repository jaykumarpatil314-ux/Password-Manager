# 🔐 Password Manager Backend

> A secure, zero-knowledge password manager backend built with Python Flask. Seamlessly switch between PostgreSQL and MongoDB with enterprise-grade security.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/github-repo-green.svg)](https://github.com/jaykumarpatil314-ux/Password-Manager.git)

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

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL or MongoDB (optional, can use MongoDB Atlas free tier)

### Installation

```bash
# Clone the repository
git clone https://github.com/jaykumarpatil314-ux/Password-Manager.git
cd Password-Manager/backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run the server
python app.py
```

The server will start at `http://localhost:5000`

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |
| POST | `/api/auth/refresh` | Refresh JWT token |
| POST | `/api/auth/logout` | Logout and invalidate token |

### Password Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/passwords` | Get all passwords (encrypted) |
| GET | `/api/passwords/:id` | Get a specific password |
| POST | `/api/passwords` | Create a new password |
| PUT | `/api/passwords/:id` | Update a password |
| DELETE | `/api/passwords/:id` | Delete a password |

### Example Request

```bash
# Register a new user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user",
    "email": "user@example.com",
    "master_password": "StrongPassword123!"
  }'
```

---

## 🔧 Configuration

Create a `.env` file in the backend directory:

```
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database Selection
DATABASE_TYPE=postgresql  # or 'mongodb'

# PostgreSQL Configuration
POSTGRES_URI=postgresql://user:pass@localhost:5432/password_manager

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/password_manager
# Or for MongoDB Atlas:
# MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/password_manager

# CORS Configuration
CORS_ORIGINS=chrome-extension://your-extension-id
```

---

## 🧪 Testing

```bash
# Run tests
python -m pytest test_backend.py

# With coverage report
pytest --cov=. --cov-report=term
```

---

## 📦 Project Structure

```
backend/
├── app.py                # Main Flask application
├── auth.py               # Authentication logic
├── config.py             # Configuration settings
├── crypto_utils.py       # Cryptography utilities
├── requirements.txt      # Python dependencies
├── test_backend.py       # Test suite
│
├── database/             # Database abstraction
│   ├── __init__.py
│   ├── base_repository.py      # Abstract interface
│   ├── db_factory.py           # Database selector
│   ├── mongodb_repository.py   # MongoDB implementation
│   └── postgres_repository.py  # PostgreSQL implementation
│
└── models/               # Database models
    ├── __init__.py
    └── postgres_models.py      # SQLAlchemy models
```

---

## 🔒 Security

- **Zero-Knowledge Design**: The server never sees plaintext passwords
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **Password Hashing**: Argon2id (winner of the Password Hashing Competition)
- **Encryption**: AES-256-GCM for all sensitive data
- **Authentication**: JWT with short expiration and refresh token rotation
- **Transport**: HTTPS with TLS 1.3
- **Database**: Encrypted connection and at-rest encryption

---

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guide](../CONTRIBUTING.md) for more details.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE.md) file for details.

---

<div align="center">
  <sub>Built with ❤️ for security and privacy</sub>
</div>