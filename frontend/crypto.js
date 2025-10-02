/**
 * Client-side cryptography module
 * Implements AES-256-GCM encryption with PBKDF2 key derivation
 */

class CryptoManager {
  constructor() {
    this.algorithm = 'AES-GCM';
    this.keyLength = 256;
    this.ivLength = 12;
    this.saltLength = 16;
    this.pbkdf2Iterations = 100000;
  }

  /**
   * Generate cryptographically secure random bytes
   */
  generateRandomBytes(length) {
    const array = new Uint8Array(length);
    crypto.getRandomValues(array);
    return array;
  }

  /**
   * Derive encryption key from master password using PBKDF2
   */
  async deriveKey(masterPassword, salt) {
    const encoder = new TextEncoder();
    const passwordBuffer = encoder.encode(masterPassword);

    // Import password as key material
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      passwordBuffer,
      'PBKDF2',
      false,
      ['deriveBits', 'deriveKey']
    );

    // Derive AES key
    const key = await crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: salt,
        iterations: this.pbkdf2Iterations,
        hash: 'SHA-256'
      },
      keyMaterial,
      {
        name: this.algorithm,
        length: this.keyLength
      },
      false,
      ['encrypt', 'decrypt']
    );

    return key;
  }

  /**
   * Encrypt data using AES-256-GCM
   */
  async encrypt(plaintext, masterPassword) {
    try {
      // Generate salt and IV
      const salt = this.generateRandomBytes(this.saltLength);
      const iv = this.generateRandomBytes(this.ivLength);

      // Derive key from master password
      const key = await this.deriveKey(masterPassword, salt);

      // Encrypt plaintext
      const encoder = new TextEncoder();
      const plaintextBuffer = encoder.encode(plaintext);

      const ciphertext = await crypto.subtle.encrypt(
        {
          name: this.algorithm,
          iv: iv
        },
        key,
        plaintextBuffer
      );

      // Combine salt + iv + ciphertext
      const resultBuffer = new Uint8Array(
        salt.length + iv.length + ciphertext.byteLength
      );
      resultBuffer.set(salt, 0);
      resultBuffer.set(iv, salt.length);
      resultBuffer.set(new Uint8Array(ciphertext), salt.length + iv.length);

      // Convert to base64
      return this.arrayBufferToBase64(resultBuffer);
    } catch (error) {
      console.error('Encryption error:', error);
      throw new Error('Encryption failed');
    }
  }

  /**
   * Decrypt data using AES-256-GCM
   */
  async decrypt(encryptedData, masterPassword) {
    try {
      // Convert from base64
      const dataBuffer = this.base64ToArrayBuffer(encryptedData);

      // Extract salt, IV, and ciphertext
      const salt = dataBuffer.slice(0, this.saltLength);
      const iv = dataBuffer.slice(this.saltLength, this.saltLength + this.ivLength);
      const ciphertext = dataBuffer.slice(this.saltLength + this.ivLength);

      // Derive key from master password
      const key = await this.deriveKey(masterPassword, salt);

      // Decrypt ciphertext
      const plaintextBuffer = await crypto.subtle.decrypt(
        {
          name: this.algorithm,
          iv: iv
        },
        key,
        ciphertext
      );

      // Convert to string
      const decoder = new TextDecoder();
      return decoder.decode(plaintextBuffer);
    } catch (error) {
      console.error('Decryption error:', error);
      throw new Error('Decryption failed - incorrect password or corrupted data');
    }
  }

  /**
   * Generate secure random password
   */
  generatePassword(length = 16, options = {}) {
    const defaults = {
      lowercase: true,
      uppercase: true,
      numbers: true,
      symbols: true
    };

    const settings = { ...defaults, ...options };

    let charset = '';
    if (settings.lowercase) charset += 'abcdefghijklmnopqrstuvwxyz';
    if (settings.uppercase) charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    if (settings.numbers) charset += '0123456789';
    if (settings.symbols) charset += '!@#$%^&*()_+-=[]{}|;:,.<>?';

    if (charset.length === 0) {
      throw new Error('At least one character type must be selected');
    }

    const randomBytes = this.generateRandomBytes(length);
    let password = '';

    for (let i = 0; i < length; i++) {
      password += charset[randomBytes[i] % charset.length];
    }

    // Ensure at least one character from each selected type
    if (settings.lowercase && !/[a-z]/.test(password)) {
      password = this.replaceRandomChar(password, 'abcdefghijklmnopqrstuvwxyz');
    }
    if (settings.uppercase && !/[A-Z]/.test(password)) {
      password = this.replaceRandomChar(password, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
    }
    if (settings.numbers && !/[0-9]/.test(password)) {
      password = this.replaceRandomChar(password, '0123456789');
    }
    if (settings.symbols && !/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) {
      password = this.replaceRandomChar(password, '!@#$%^&*()_+-=[]{}|;:,.<>?');
    }

    return password;
  }

  /**
   * Calculate password strength (0-100)
   */
  calculatePasswordStrength(password) {
    let strength = 0;

    // Length score
    if (password.length >= 8) strength += 20;
    if (password.length >= 12) strength += 10;
    if (password.length >= 16) strength += 10;

    // Character variety
    if (/[a-z]/.test(password)) strength += 15;
    if (/[A-Z]/.test(password)) strength += 15;
    if (/[0-9]/.test(password)) strength += 15;
    if (/[^a-zA-Z0-9]/.test(password)) strength += 15;

    return Math.min(strength, 100);
  }

  /**
   * Helper: Replace random character in string
   */
  replaceRandomChar(str, charset) {
    const randomBytes = this.generateRandomBytes(2);
    const position = randomBytes[0] % str.length;
    const char = charset[randomBytes[1] % charset.length];
    return str.substring(0, position) + char + str.substring(position + 1);
  }

  /**
   * Helper: Convert ArrayBuffer to Base64
   */
  arrayBufferToBase64(buffer) {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  /**
   * Helper: Convert Base64 to ArrayBuffer
   */
  base64ToArrayBuffer(base64) {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    return bytes;
  }

  /**
   * Hash data using SHA-256
   */
  async hash(data) {
    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(data);
    const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
    return this.arrayBufferToBase64(hashBuffer);
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CryptoManager;
}
