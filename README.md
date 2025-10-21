<div align="center">

# 🔐 SecureVault

### Zero-Knowledge Password Manager

_Your passwords. Your control. Encrypted by default._

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1.2-orange.svg)](https://flask.palletsprojects.com/)
[![Chrome Extension](https://img.shields.io/badge/chrome-extension-yellow.svg)](https://developer.chrome.com/docs/extensions/)
[![GitHub](https://img.shields.io/badge/github-repo-green.svg)](https://github.com/jaykumarpatil314-ux/Password-Manager.git)

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

| Feature                   | Description                                 |
| ------------------------- | ------------------------------------------- |
| 🔍 **Smart Search**       | Instantly find passwords by website or name |
| 🎲 **Password Generator** | Create strong, unique passwords             |
| 📋 **One-Click Copy**     | Copy passwords with a single click          |
| 💾 **Session Storage**    | Secure master password caching              |
| 🎨 **Minimal UI**         | Clean, authentic design                     |

---

## 🚀 Quick Start

### Backend Setup

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
# Edit .env with your database credentials and secret keys

# Run the server
python app.py
```

### Frontend Setup

```bash
# Navigate to the frontend directory
cd ../frontend

# Load the extension in Chrome
1. Open Chrome and navigate to chrome://extensions/
2. Enable "Developer mode"
3. Click "Load unpacked" and select the frontend directory
```

---

## 🏗️ Architecture

SecureVault follows a client-server architecture with end-to-end encryption:

```
┌─────────────────┐      ┌────────────────┐      ┌─────────────────┐
│                 │      │                │      │                 │
│  Chrome         │ HTTPS│  Flask Backend │ SQL/ │  Database       │
│  Extension      │──────│  API           │──────│  (PostgreSQL/   │
│  (Frontend)     │      │                │      │   MongoDB)      │
│                 │      │                │      │                 │
└─────────────────┘      └────────────────┘      └─────────────────┘
```

### Key Components:

1. **Frontend**: Chrome extension with client-side encryption/decryption
2. **Backend API**: Flask server handling authentication and encrypted data storage
3. **Database**: Flexible storage with PostgreSQL or MongoDB support

---

## 🔐 Security

SecureVault implements multiple layers of security:

- **Master Password**: Never transmitted to the server
- **Key Derivation**: Argon2id with high memory and iteration parameters
- **Encryption**: AES-256-GCM for all sensitive data
- **Authentication**: JWT with short expiration and refresh token rotation
- **Transport**: HTTPS with TLS 1.3
- **Database**: Encrypted connection and at-rest encryption

### Zero-Knowledge Design

Your master password is used to derive an encryption key locally. Only encrypted data is sent to the server, ensuring that even in case of a server breach, your passwords remain secure.

---

## 📚 Project Structure

```
├── backend/                  # Server-side code
│   ├── app.py                # Main Flask application
│   ├── auth.py               # Authentication logic
│   ├── config.py             # Configuration settings
│   ├── crypto_utils.py       # Server-side cryptography
│   ├── database/             # Database abstraction
│   │   ├── base_repository.py
│   │   ├── db_factory.py
│   │   ├── mongodb_repository.py
│   │   └── postgres_repository.py
│   ├── models/               # Data models
│   └── requirements.txt      # Python dependencies
│
└── frontend/                 # Chrome extension
    ├── api.js                # API communication
    ├── background.js         # Extension background script
    ├── crypto.js             # Client-side encryption
    ├── manifest.json         # Extension manifest
    ├── popup.html            # Extension UI
    ├── popup.css             # Styling
    └── popup.js              # UI logic
```

---

## 🛠️ Development

### Prerequisites

- Python 3.9+
- Chrome browser
- PostgreSQL or MongoDB

### Testing

```bash
# Run backend tests
cd backend
python -m pytest test_backend.py

# Frontend tests (coming soon)
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgements

- [Crypto.js](https://github.com/brix/crypto-js) for client-side encryption
- [Flask](https://flask.palletsprojects.com/) for the backend framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM
- [PyMongo](https://pymongo.readthedocs.io/) for MongoDB integration

---

<div align="center">
  <sub>Built with ❤️ for security and privacy</sub>
</div>


