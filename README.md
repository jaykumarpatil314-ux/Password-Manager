<div align="center">

# 🔐 SecureVault

### Zero-Knowledge Password Manager

*Your passwords. Your control. Encrypted by default.*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1.2-orange.svg)](https://flask.palletsprojects.com/)
[![Chrome Extension](https://img.shields.io/badge/chrome-extension-yellow.svg)](https://developer.chrome.com/docs/extensions/)

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#️-architecture) • [Security](#-security) • [Documentation](#-documentation)

</div>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🔒 Security First

- **Zero-Knowledge Architecture**  
  Master password never leaves your device
  
- **Client-Side Encryption**  
  AES-256-GCM in the browser
  
- **Argon2 Password Hashing**  
  Resistant to GPU attacks
  
- **JWT Authentication**  
  Secure, stateless sessions
  
- **No Plaintext Storage**  
  Only encrypted blobs on server

</td>
<td width="50%">

### ⚡ Modern Stack

- **Multi-Database Support**  
  PostgreSQL or MongoDB
  
- **Cloud-Ready**  
  Atlas, AWS RDS compatible
  
- **Repository Pattern**  
  Clean architecture
  
- **WebSocket Support**  
  Real-time sync
  
- **RESTful API**  
  Well-documented endpoints

</td>
</tr>
</table>

### 🎨 Chrome Extension Features

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Search** | Instantly find passwords by website or name |
| 🎲 **Password Generator** | Create strong, unique passwords |
| 📋 **One-Click Copy** | Copy passwords with a single click |
| 💾 **Session Storage** | Secure master password caching |
| 🎨 **Minimal UI** | Clean, authentic design |

---

## 📸 Screenshots

<div align="center">

```
┌─────────────────────────────────────────────────┐
│           🔐 SecureVault                        │
│     Zero-Knowledge Password Manager             │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐      ┌──────────────┐        │
│  │    Login     │      │   Register   │        │
│  └──────────────┘      └──────────────┘        │
│                                                 │
│  Username:  [_____________________]             │
│                                                 │
│  Password:  [_____________________]             │
│                                                 │
│                 [ Login ]                       │
│                                                 │
└─────────────────────────────────────────────────┘
```

</div>

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.9 or higher
- ✅ PostgreSQL **or** MongoDB (or use MongoDB Atlas free tier)
- ✅ Google Chrome browser
- ✅ Node.js (optional, for frontend tooling)

### 📦 Installation

#### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/securevault.git
cd securevault
```

#### 2️⃣ Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run server
python app.py
```

✅ Backend will start at `http://localhost:5000`

#### 3️⃣ Setup Frontend (Chrome Extension)

```bash
cd frontend/securevault
```

**No build needed - ready to load!**

Install in Chrome:
1. Open `chrome://extensions/`
2. Enable **"Developer mode"** (top right)
3. Click **"Load unpacked"**
4. Select the `securevault/` folder

#### 4️⃣ Test It Out

1. 🔵 Click the SecureVault extension icon
2. 📝 Register a new account
3. ➕ Add a password
4. 🧪 Test search, copy, and edit features

---

## 📁 Project Structure

```
securevault/
│
├── 🐍 backend/                      # Python Flask Backend
│   ├── app.py                       # Main application
│   ├── config.py                    # Configuration
│   ├── auth.py                      # Authentication logic
│   ├── crypto_utils.py              # Security utilities
│   ├── requirements.txt             # Python dependencies
│   │
│   ├── database/                    # Repository Pattern
│   │   ├── base_repository.py       # Abstract interface
│   │   ├── db_factory.py            # Database selector
│   │   ├── postgres_repository.py   # PostgreSQL implementation
│   │   └── mongodb_repository.py    # MongoDB implementation
│   │
│   └── models/                      # Database Models
│       └── postgres_models.py
│
├── 🎨 frontend/                     # Chrome Extension
│   └── securevault/
│       ├── manifest.json            # Extension manifest
│       ├── popup.html               # User interface
│       ├── popup.css                # Styles
│       ├── popup.js                 # Main logic
│       ├── crypto.js                # Encryption module
│       ├── api.js                   # API client
│       ├── background.js            # Service worker
│       └── icons/                   # Extension icons
│
├── 📚 docs/                         # Documentation
│   ├── API.md                       # API reference
│   ├── ARCHITECTURE.md              # Architecture guide
│   └── SECURITY.md                  # Security details
│
├── .gitignore
├── LICENSE
└── README.md                        # You are here
```

---

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database Selection (choose one)
DATABASE_TYPE=postgresql              # or 'mongodb'

# PostgreSQL Configuration
POSTGRES_URI=postgresql://user:pass@localhost:5432/password_manager

# MongoDB Configuration (Local)
MONGODB_URI=mongodb://localhost:27017/password_manager

# MongoDB Atlas (Cloud - Free Tier Available)
# MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/password_manager

# CORS Configuration
CORS_ORIGINS=chrome-extension://your-extension-id
```

### 🔄 Switching Databases

One of the best features - **switch databases without changing code!**

**Use PostgreSQL:**
```bash
export DATABASE_TYPE=postgresql
```

**Use MongoDB:**
```bash
export DATABASE_TYPE=mongodb
```

That's it! No code changes required.

---

## 🏗️ Architecture

<div align="center">

```
┌─────────────────────────────────────────────────────────┐
│          Chrome Extension (Frontend)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │   Client-Side Encryption (AES-256-GCM)            │  │
│  │   Master Password Never Leaves Browser            │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ HTTPS / REST API
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Flask Backend (Python)                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │   JWT Authentication + Argon2 Hashing             │  │
│  │   Repository Pattern (Database Abstraction)       │  │
│  └──────────────────┬────────────────────────────────┘  │
└────────────────────┬┴───────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌─────────────────┐       ┌──────────────────┐
│   PostgreSQL    │       │   MongoDB Atlas  │
│  (Local/RDS)    │       │     (Cloud)      │
└─────────────────┘       └──────────────────┘
```

</div>

---

## 🔒 Security

### 🛡️ Zero-Knowledge Architecture

**What does "Zero-Knowledge" mean?**

Your master password is used **only** in your browser to derive an encryption key. The server **never** sees your master password or encryption key. Even if our database is compromised, your passwords remain secure.

### 🔐 Encryption Details

| Component | Specification |
|-----------|--------------|
| **Algorithm** | AES-256-GCM (Galois/Counter Mode) |
| **Key Derivation** | PBKDF2 with 100,000 iterations |
| **Initialization Vector** | Unique 12-byte IV per encryption |
| **Salt** | Unique 16-byte salt per user |

### 🔑 Password Hashing

| Component | Specification |
|-----------|--------------|
| **Algorithm** | Argon2 (PHC winner 2015) |
| **Time Cost** | 3 iterations |
| **Memory Cost** | 64 MB |
| **Parallelism** | 4 threads |
| **Salt** | Unique 32-byte salt per user |

### 🔐 API Security

- ✅ **JWT Tokens** - HS256 algorithm, 24-hour expiration
- ✅ **HTTPS** - All production traffic encrypted
- ✅ **CORS** - Restricted to specific origins
- ✅ **Input Validation** - All inputs sanitized
- 🔜 **Rate Limiting** - Prevent brute force (Coming soon)

---

## 📊 Database Support

<table>
<tr>
<td width="50%">

### 🐘 PostgreSQL

**Advantages:**
- ✅ ACID compliance
- ✅ Strong consistency
- ✅ Rich query capabilities
- ✅ Mature ecosystem

**Connection String:**
```
postgresql://user:password@localhost:5432/password_manager
```

</td>
<td width="50%">

### 🍃 MongoDB

**Advantages:**
- ✅ Flexible schema
- ✅ Horizontal scaling
- ✅ JSON-native
- ✅ Free cloud tier (Atlas)

**Local:**
```
mongodb://localhost:27017/password_manager
```

**Atlas (Cloud):**
```
mongodb+srv://user:pass@cluster.mongodb.net/password_manager
```

</td>
</tr>
</table>

> **Note:** Both databases work identically - switch anytime without code changes!

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=. --cov-report=html
```

### API Testing Examples

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Register:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username":"test",
    "email":"test@example.com",
    "master_password":"Test123!"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username":"test",
    "master_password":"Test123!"
  }'
```

---

## 🚢 Deployment

### Backend Deployment Options

<details>
<summary><b>🟣 Heroku</b></summary>

```bash
heroku create securevault-api
heroku config:set DATABASE_TYPE=mongodb
heroku config:set MONGODB_URI=mongodb+srv://...
git push heroku main
```
</details>

<details>
<summary><b>🐳 Docker</b></summary>

```bash
# Build image
docker build -t securevault-backend ./backend

# Run container
docker run -p 5000:5000 --env-file .env securevault-backend
```
</details>

<details>
<summary><b>☁️ AWS/GCP/Azure</b></summary>

- Deploy as containerized app
- Use managed database (RDS for PostgreSQL, Atlas for MongoDB)
- Enable HTTPS with SSL certificate
- Configure environment variables in cloud console
</details>

### Frontend Deployment

**Chrome Web Store:**

1. 📦 Zip the `frontend/securevault/` folder
2. 🌐 Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
3. ⬆️ Upload new extension
4. 📝 Fill in metadata and screenshots
5. 📤 Submit for review

---

## 📚 Documentation

Explore detailed documentation:

| Document | Description |
|----------|-------------|
| [📘 Backend README](backend/README.md) | Backend setup and API details |
| [🎨 Frontend README](frontend/README.md) | Extension installation guide |
| [📡 API Documentation](docs/API.md) | Complete API reference |
| [🔒 Security Details](docs/SECURITY.md) | Security architecture |
| [🏗️ Architecture Guide](docs/ARCHITECTURE.md) | System design overview |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. 💾 Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. 📤 Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. 🔀 Open a Pull Request

### Development Guidelines

- ✅ Follow PEP 8 for Python code
- ✅ Use ESLint for JavaScript
- ✅ Write tests for new features
- ✅ Update documentation
- ✅ Keep commits atomic and descriptive

---

## 🗺️ Roadmap

Our vision for the future:

- [ ] 🔐 Two-Factor Authentication (2FA)
- [ ] 🚨 Password breach checking (HIBP API)
- [ ] 🌐 Browser autofill integration
- [ ] 📱 Mobile app (React Native)
- [ ] 🤝 Password sharing (encrypted)
- [ ] 📝 Secure notes
- [ ] 📥 Import from other password managers
- [ ] 👨‍👩‍👧‍👦 Family/Team accounts
- [ ] 📊 Audit logs
- [ ] 🏠 Self-hosting guide

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with amazing open-source technologies:

<div align="center">

| Technology | Purpose |
|------------|---------|
| [Flask](https://flask.palletsprojects.com/) | Web framework |
| [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) | Cloud database |
| [PostgreSQL](https://www.postgresql.org/) | Relational database |
| [Argon2](https://github.com/P-H-C/phc-winner-argon2) | Password hashing |
| [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API) | Client-side encryption |
| [Chrome Extensions](https://developer.chrome.com/docs/extensions/) | Frontend platform |

</div>

---

## 📞 Support & Community

Need help or want to connect?

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/securevault/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/securevault/discussions)
- 📧 **Email**: support@securevault.com
- 🐦 **Twitter**: [@SecureVault](https://twitter.com/securevault)

---



<div align="center">

### Built with ❤️ by the SecureVault Team

**SecureVault** - *Because your passwords should stay yours.*

[⬆ Back to Top](#-securevault)

**If you find this project useful, please consider giving it a ⭐ star!**

</div>