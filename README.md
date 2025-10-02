# Password Manager

A secure, client-side encrypted password manager with Chrome extension integration and PostgreSQL backend.

## Features

- **Client-Side Encryption**: All passwords are encrypted locally before being sent to the server
- **Chrome Extension**: Auto-fill credentials on websites
- **Password Generator**: Create strong, random passwords
- **Secure Authentication**: JWT-based authentication system
- **Search Functionality**: Quickly find saved passwords
- **Password Strength Checker**: Evaluate password security

## Architecture

- **Backend**: Python Flask API with PostgreSQL database
- **Frontend**: Chrome Extension (HTML/CSS/JavaScript)
- **Encryption**: Client-side encryption using Web Crypto API
- **Authentication**: JWT tokens with secure password hashing

## Security Features

- Master password never leaves the client
- All passwords encrypted before storage
- Argon2 password hashing
- SQL injection protection
- XSS protection with input sanitization
- CSRF protection
- Secure token-based authentication

## Project Structure

```
password-manager/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── .env
├── chrome-extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   └── api.js
├── README.md
├── BACKEND_SETUP.md
└── FRONTEND_SETUP.md
```

## Quick Start

1. **Backend Setup**: Follow instructions in [BACKEND_SETUP.md](BACKEND_SETUP.md)
2. **Frontend Setup**: Follow instructions in [FRONTEND_SETUP.md](FRONTEND_SETUP.md)

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Google Chrome browser

## Testing

Refer to [BACKEND_SETUP.md](backend/README.md) for detailed testing procedures including:
- Manual testing checklist
- Security testing
- Performance testing


## Support

For issues or questions:
- Check the setup guides for your specific component
- Review the testing checklist
- Verify all prerequisites are installed

## License

This project is provided as-is for educational purposes.

## Security Notice

This is a demonstration project. For production use, ensure:
- Proper SSL/TLS configuration
- Regular security audits
- Compliance with data protection regulations
- Professional security review

