# Frontend Setup Guide (Chrome Extension)

This guide covers the installation and configuration of the Password Manager Chrome extension.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Extension Installation](#extension-installation)
3. [Configuration](#configuration)
4. [Features Overview](#features-overview)
5. [Usage Guide](#usage-guide)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Development](#development)

---

## Prerequisites

- Google Chrome browser (version 88 or higher)
- Backend server running (see [BACKEND_SETUP.md](BACKEND_SETUP.md))
- Basic understanding of Chrome extensions

---

## Extension Installation

### Load Unpacked Extension

1. **Open Chrome Extensions Page**
   - Navigate to `chrome://extensions/`
   - Or click Menu (⋮) → More Tools → Extensions

2. **Enable Developer Mode**
   - Toggle the "Developer mode" switch in the top right corner

3. **Load the Extension**
   - Click "Load unpacked" button
   - Navigate to and select the `chrome-extension` folder from the project
   - Click "Select Folder" (or "Open" on macOS)

4. **Verify Installation**
   - The Password Manager extension should appear in your extensions list
   - You should see the extension icon in your Chrome toolbar
   - If the icon is not visible, click the puzzle icon (🧩) and pin the extension

### Extension Permissions

The extension will request the following permissions:
- **Storage**: To save extension settings and cached data
- **Active Tab**: To auto-fill passwords on web pages
- **Host Permissions**: To communicate with the backend API

---

## Configuration

### Configure Backend URL

By default, the extension connects to `http://localhost:5000`. If your backend runs on a different URL:

1. **Open the Extension Files**
   - Navigate to `chrome-extension/api.js`

2. **Update the API URL**
   ```javascript
   const api = new APIClient('YOUR_BACKEND_URL');
   ```
   
   Example for remote server:
   ```javascript
   const api = new APIClient('https://api.yourpasswordmanager.com');
   ```

3. **Reload the Extension**
   - Go to `chrome://extensions/`
   - Click the reload icon (🔄) on the Password Manager extension card

### CORS Configuration

If using a remote backend, ensure CORS is properly configured in your backend to allow requests from the Chrome extension.

Add to your backend configuration:
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["chrome-extension://*"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## Features Overview

### 1. User Authentication
- Register new account
- Secure login with master password
- Logout functionality

### 2. Password Management
- Add new password entries
- View all saved passwords
- Edit existing passwords
- Delete passwords
- Search passwords by URL or username

### 3. Auto-Fill
- Automatically detect login forms
- Fill credentials with one click
- Support for multiple accounts per website

### 4. Password Generator
- Generate strong random passwords
- Customizable length (8-32 characters)
- Include/exclude character types:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters
- Real-time password strength indicator

### 5. Security Features
- Client-side encryption
- Master password never stored
- Automatic session timeout
- Secure clipboard copying

---

## Usage Guide

### First Time Setup

1. **Open the Extension**
   - Click the Password Manager icon in your toolbar

2. **Register an Account**
   - Click "Register" or "Sign Up"
   - Enter a username
   - Create a strong master password
   - Confirm your master password
   - Click "Register"

3. **Login**
   - Enter your username and master password
   - Click "Login"

### Adding a Password

1. **Navigate to a Login Page**
   - Visit any website with a login form

2. **Open the Extension**
   - Click the extension icon

3. **Add New Password**
   - Click "+ Add Password" button
   - The URL will be auto-filled if on a website
   - Enter username/email
   - Either:
     - Type a password manually, or
     - Click "Generate Password" for a strong random password
   - Click "Save"

### Using Auto-Fill

1. **Navigate to a Login Page**
   - Visit a website where you've saved credentials

2. **Trigger Auto-Fill**
   - Click the extension icon
   - Click the saved entry for that website
   - Or use the "Auto-fill" button

3. **Complete Login**
   - The extension will fill in your username and password
   - Click the website's login button

### Managing Passwords

**View Passwords:**
- Open extension popup
- All saved passwords are listed
- Use the search bar to filter

**Edit Password:**
- Click the edit icon (✏️) next to the password entry
- Modify the fields
- Click "Save Changes"

**Delete Password:**
- Click the delete icon (🗑️) next to the password entry
- Confirm deletion

**Copy Password:**
- Click the copy icon (📋) next to the password
- Password is copied to clipboard for 30 seconds

---

## Testing

### Manual Testing Checklist

#### Installation & Setup
- [ ] Extension loads without errors
- [ ] Extension icon appears in toolbar
- [ ] Popup opens when icon is clicked
- [ ] Backend connection successful

#### Authentication Flow
- [ ] Register new user
- [ ] Register with weak password (should show strength warning)
- [ ] Register with existing username (should show error)
- [ ] Login with correct credentials
- [ ] Login with incorrect credentials (should show error)
- [ ] Session persists after closing popup
- [ ] Logout clears session
- [ ] Session expires after timeout

#### Password Management
- [ ] Add new password with all fields
- [ ] Add password with generated password
- [ ] View all passwords in list
- [ ] Search filters passwords correctly
- [ ] Edit password updates successfully
- [ ] Delete password removes entry
- [ ] Copy password to clipboard works

#### Auto-Fill Functionality
- [ ] Auto-fill detects login forms
- [ ] Auto-fill fills correct credentials
- [ ] Auto-fill works on various websites:
  - [ ] Gmail/Google
  - [ ] Facebook
  - [ ] GitHub
  - [ ] Your test websites
- [ ] Multiple accounts for same site handled correctly

#### Password Generator
- [ ] Generate password creates random password
- [ ] Length slider works (8-32 characters)
- [ ] Character type toggles work:
  - [ ] Uppercase letters
  - [ ] Lowercase letters
  - [ ] Numbers
  - [ ] Special characters
- [ ] Password strength indicator updates
- [ ] Copy generated password works
- [ ] Use generated password in save form works

#### Security
- [ ] Master password not visible in console
- [ ] Passwords encrypted before storage
- [ ] Token stored securely
- [ ] No sensitive data in browser DevTools
- [ ] Extension only accesses allowed URLs

#### UI/UX
- [ ] All buttons responsive
- [ ] Forms validate input
- [ ] Error messages display correctly
- [ ] Success messages display correctly
- [ ] Loading states show during API calls
- [ ] Extension popup size appropriate
- [ ] Responsive on different screen sizes

### Test Websites

Test auto-fill on these common login pages:
- https://github.com/login
- https://accounts.google.com
- https://www.facebook.com
- https://twitter.com/login
- https://www.linkedin.com/login

---

## Troubleshooting

### Extension Not Loading

**Issue**: Extension doesn't appear after loading

**Solutions**:
- Verify you selected the correct folder (`chrome-extension`)
- Check for JavaScript errors in the extension console:
  - Go to `chrome://extensions/`
  - Click "Details" on the extension
  - Click "Inspect views: popup.html"
- Ensure `manifest.json` is valid JSON

### Cannot Connect to Backend

**Issue**: "Failed to connect to server" error

**Solutions**:
- Verify backend server is running (`http://localhost:5000/health`)
- Check the API URL in `api.js` matches your backend URL
- Verify CORS is configured correctly on backend
- Check browser console for network errors (F12 → Network tab)

### Auto-Fill Not Working

**Issue**: Extension doesn't auto-fill credentials

**Solutions**:
- Ensure you're on the correct website (URL matches saved entry)
- Check that login form has standard input fields
- Verify extension has permissions for the website
- Try manually selecting the input fields
- Check console for JavaScript errors

### Passwords Not Saving

**Issue**: Passwords don't persist after saving

**Solutions**:
- Check backend server logs for errors
- Verify authentication token is valid
- Check browser console for API errors
- Ensure database is running and accessible
- Verify storage permissions are granted

### Master Password Issues

**Issue**: Can't login or "Invalid credentials" error

**Solutions**:
- Verify caps lock is off
- Check for extra spaces in username/password
- Try resetting password (if implemented)
- Clear extension storage and re-register:
  - `chrome://extensions/`
  - Click "Details"
  - Click "Clear storage"

### Performance Issues

**Issue**: Extension is slow or unresponsive

**Solutions**:
- Check if you have many saved passwords (consider pagination)
- Clear browser cache
- Disable other extensions temporarily
- Check backend server performance
- Monitor Network tab for slow API calls

---

## Development

### Project Structure

```
chrome-extension/
├── manifest.json          # Extension configuration
├── popup.html            # Main popup interface
├── popup.js              # Popup logic and UI handling
├── api.js                # API communication layer
├── content-script.js     # Page interaction for auto-fill
├── background.js         # Background service worker
├── styles/
│   └── popup.css        # Styling
└── icons/
    ├── icon16.png       # Extension icons
    ├── icon48.png
    └── icon128.png
```

### Making Changes

1. **Edit Extension Files**
   - Modify HTML, CSS, or JavaScript files as needed

2. **Reload Extension**
   - Go to `chrome://extensions/`
   - Click reload icon on the extension card

3. **Test Changes**
   - Open the extension popup
   - Test modified functionality
   - Check console for errors

### Debugging

**View Popup Console:**
- Right-click extension icon → "Inspect popup"
- Or: Extensions page → Details → "Inspect views: popup.html"

**View Background Script Console:**
- Extensions page → Details → "Inspect views: background page"

**View Content Script Console:**
- Open any webpage
- Press F12 → Console tab
- Content script logs appear here

### Adding New Features

When adding features:
1. Update `manifest.json` if new permissions needed
2. Implement UI in `popup.html` and `popup.js`
3. Add API calls in `api.js` if backend integration required
4. Update this documentation
5. Test thoroughly before deployment

---

## Security Best Practices

### For Users

- Use a strong, unique master password
- Don't share your master password
- Logout when using shared computers
- Regularly update saved passwords
- Enable two-factor authentication on important accounts

### For Developers

- Never log sensitive data (passwords, tokens)
- Always use HTTPS for backend communication
- Validate all user inputs
- Implement proper error handling
- Keep dependencies updated
- Regular security audits

---

## Resources

- [Chrome Extension Developer Guide](https://developer.chrome.com/docs/extensions/)
- [Chrome Extension API Reference](https://developer.chrome.com/docs/extensions/reference/)
- [Web Crypto API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)

---

## Support

For backend-related issues, see [BACKEND_SETUP.md](BACKEND_SETUP.md).

For general questions, refer to the main [README.md](README.md).