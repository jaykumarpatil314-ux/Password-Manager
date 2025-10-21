# 🔐 SecureVault Chrome Extension

> A minimal, authentic, zero-knowledge password manager Chrome extension that pairs with a Python Flask backend. All sensitive data is encrypted client-side using AES‑256‑GCM; the backend never sees plaintext.

[![Chrome](https://img.shields.io/badge/Chrome-Extension-yellow.svg)](https://developer.chrome.com/docs/extensions/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-blue.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE.md)
[![GitHub](https://img.shields.io/badge/github-repo-green.svg)](https://github.com/jaykumarpatil314-ux/Password-Manager.git)

---

## ✨ Features

- 🔒 **Zero‑knowledge architecture** - Client‑side AES‑256‑GCM encryption
- 🎨 **Clean, minimal UI** with authentic feel
- 🔑 **Register/Login** with JWT session handling
- 📝 **Add, edit, delete** password entries
- 🔐 **Local, secure decryption** using master password
- 🎲 **Password generator** and strength indicator
- 🔍 **Search** across saved entries
- 🔔 **Toast notifications** and loading states
- 🛡️ **CSP‑compliant** (no inline scripts/handlers)

---

## 📁 Folder Structure

```
frontend/
├── manifest.json     # Extension manifest
├── popup.html        # Main extension UI
├── popup.css         # Styles
├── popup.js          # Main UI logic
├── crypto.js         # Encryption/decryption utilities
├── api.js            # Backend API communication
├── background.js     # Service worker
└── icons/            # Extension icons
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

---

## 🚀 Installation

### Prerequisites

- Google Chrome (latest)
- Flask backend running locally at http://localhost:5000

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/jaykumarpatil314-ux/Password-Manager.git
cd Password-Manager
```

2. **Load the extension in Chrome**

- Open Chrome and navigate to `chrome://extensions/`
- Enable "Developer mode" (toggle in the top-right corner)
- Click "Load unpacked" and select the `frontend` directory
- The SecureVault extension icon should appear in your toolbar

3. **Configure backend connection**

- Make sure the backend server is running (see [Backend README](../backend/README.md))
- The extension is pre-configured to connect to `http://localhost:5000`

---

## 🔧 Usage

1. **First-time setup**
   - Click the SecureVault icon in your Chrome toolbar
   - Register a new account with a strong master password
   - Your master password is used for encryption and never sent to the server

2. **Adding passwords**
   - Click the "+" button to add a new password
   - Enter website details and credentials
   - All data is encrypted before being sent to the server

3. **Retrieving passwords**
   - Search for a website in the search bar
   - Click on an entry to view details
   - Use the copy button to copy the password to clipboard

4. **Generating strong passwords**
   - When adding or editing a password, click "Generate"
   - Adjust length and character types as needed
   - The password strength indicator will show how secure it is

---

## 🔒 Security

- **Zero-Knowledge Design**: Your master password never leaves your device
- **Client-Side Encryption**: All sensitive data is encrypted with AES-256-GCM before transmission
- **Key Derivation**: PBKDF2 with 100,000 iterations to derive encryption key from master password
- **No Plaintext Storage**: Only encrypted data is sent to and stored on the server
- **Session Security**: JWT tokens with short expiration and secure storage

---

## 🧪 Development

### Extension Manifest

The extension uses Manifest V3, which is the latest extension platform from Chrome:

```json
{
  "manifest_version": 3,
  "name": "SecureVault",
  "version": "1.0.0",
  "description": "Zero-knowledge password manager",
  "permissions": ["storage", "clipboardWrite"],
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "background": {
    "service_worker": "background.js"
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

### API Communication

The extension communicates with the backend using the Fetch API:

```javascript
// Example from api.js
async function login(username, masterPassword) {
  try {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, master_password: masterPassword }),
    });
    
    return await response.json();
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}
```

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