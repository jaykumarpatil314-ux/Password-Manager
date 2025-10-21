# Security Policy

## Reporting a Vulnerability

The SecureVault team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

To report a security issue, please email [security@example.com](mailto:security@example.com) with a description of the issue, the steps you took to create it, affected versions, and if known, mitigations for the issue.

We will acknowledge your email within 48 hours and provide a detailed response within 72 hours indicating the next steps in handling your report.

## Security Measures

SecureVault implements the following security measures:

### Client-Side Encryption
- All sensitive data is encrypted using AES-256-GCM before transmission
- Encryption/decryption occurs exclusively on the client side
- Master password never leaves the user's device

### Key Derivation
- PBKDF2 with 100,000 iterations for key derivation
- Unique salt for each user
- Strong entropy sources for cryptographic operations

### Authentication
- Secure password hashing using bcrypt with appropriate work factors
- JWT tokens with short expiration times
- CSRF protection for all authenticated endpoints

### Data Protection
- Zero-knowledge architecture ensures the server never sees plaintext data
- No storage of plaintext credentials anywhere in the system
- Encrypted data is stored with additional server-side encryption

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Updates

Security updates will be released as soon as possible after a vulnerability is confirmed. Users will be notified through:

1. GitHub security advisories
2. Release notes
3. In-app notifications (when applicable)

## Best Practices for Users

1. Use a strong, unique master password
2. Keep your browser and extensions updated
3. Be vigilant about phishing attempts
4. Enable two-factor authentication when available
5. Regularly check for updates to the extension

## Security Audits

The SecureVault codebase undergoes regular security audits. Results and remediation efforts are documented in our security reports.

---

Thank you for helping keep SecureVault and its users safe!