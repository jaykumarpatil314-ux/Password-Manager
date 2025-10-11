SecureVault Chrome Extension (Frontend)

A minimal, authentic, zero-knowledge password manager Chrome extension that pairs with a Python Flask backend. All sensitive data is encrypted client-side using AES‑256‑GCM; the backend never sees plaintext.
Features

    Zero‑knowledge architecture (client‑side AES‑256‑GCM)

    Clean, minimal UI with authentic feel

    Register/Login with JWT session handling

    Add, edit, delete password entries

    Local, secure decryption using master password

    Password generator and strength indicator

    Search across saved entries

    Toast notifications and loading states

    CSP‑compliant (no inline scripts/handlers)

Folder Structure

text
securevault/
├── manifest.json
├── popup.html
├── popup.css
├── popup.js
├── crypto.js
├── api.js
├── background.js
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png

Prerequisites

    Google Chrome (latest)

    Flask backend running locally at http://localhost:5000

    Backend must implement:

        POST /api/auth/register

        POST /api/auth/login

        GET /api/passwords

        POST /api/passwords

        PUT /api/passwords/:id

        DELETE /api/passwords/:id

        POST /api/passwords/search

    CORS enabled for chrome extension and localhost

Installation

    Create the folder structure shown above.

    Copy all frontend files into the folder.

    Add PNG icons (any lock icon works) sized 16x16, 48x48, 128x128 in icons/.

    Open Chrome → go to chrome://extensions/.

    Enable Developer mode (top right).

    Click “Load unpacked” and select the securevault folder.

    Start the Flask backend (default http://localhost:5000).

    Click the extension icon to open the popup.

Configuration

    The frontend points to http://localhost:5000 by default.

    To change, edit the base URL in api.js:

        new APIClient('http://localhost:5000')

How It Works

    Master password never leaves the browser.

    crypto.js derives an AES‑256 key via PBKDF2 and encrypts credentials using AES‑GCM with a random IV.

    Only encrypted blobs are sent to the backend and stored in the database.

    Decryption happens in the popup using the stored master password (in chrome.storage.session).

Files Overview

    manifest.json

        MV3 manifest with storage and host permissions, background service worker, and default popup.

    popup.html

        Minimal UI: login/register, search, list, modal for add/edit, loading overlay, toast.

    popup.css

        Clean modern theme; neutral palette; responsive; subtle shadows and motion.

    popup.js

        UI logic and state:

            JWT handling via chrome.storage.local

            Master password stored in chrome.storage.session (cleared when browser closes)

            Add/Edit/Delete/Copy/Search flows

            CSP‑safe event listeners (no inline handlers)

    api.js

        Thin REST client with token injection, JSON handling, and CORS mode.

    crypto.js

        Web Crypto API wrapper:

            PBKDF2 key derivation

            AES‑GCM encrypt/decrypt

            Strong password generator and strength meter

    background.js

        MV3 service worker (lightweight; ready for future autofill features).

Usage

    Register a new account or log in.

    Add a password:

        Enter site URL/name, username/email, and password.

        Optionally click Generate to create a strong password.

        Save to store encrypted blobs in the backend.

    Search:

        Use the search bar to filter by name, URL, or username.

    Copy:

        Click Copy to decrypt and put the password on the clipboard.

    Edit/Delete:

        Click Edit to modify entry fields.

        Click Delete to permanently remove the entry.

    Logout:

        Click the logout button in the header to clear tokens and session.

Security Notes

    Master password is stored in chrome.storage.session to allow decryption during popup lifecycle and is cleared when the browser session ends.

    All encryption/decryption uses the Web Crypto API; no external libraries.

    The extension adheres to MV3 CSP: avoids inline handlers and code execution.

    Server receives only encrypted blobs for username, password, and notes.

Troubleshooting

    CORS errors:

        Ensure Flask has CORS enabled and allows chrome-extension://<your_id> and http://localhost:5000.

    Decryption failed:

        Master password missing or different from the one used at encryption time.

        The popup will reprompt if the session value is missing.

    No logs or UI updates:

        Right‑click popup → Inspect → check Console for errors.

    401 Unauthorized:

        Token expired; log in again.

Extending

    Autofill: Implement content scripts and page field detection, and message the background/popup for decryption.

    Sync: Use WebSocket channels to live-sync entry lists when edited on other devices.

    Theming: Add dark mode via a CSS toggle and prefers‑color‑scheme.

Privacy

SecureVault implements a zero‑knowledge model: plaintext secrets never leave the device. The backend is never able to decrypt stored credentials.

License
MIT