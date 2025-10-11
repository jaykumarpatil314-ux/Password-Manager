class CryptoManager {
  constructor() {
    this.algorithm = 'AES-GCM';
    this.keyLength = 256;
    this.ivLength = 12;
    this.saltLength = 16;
    this.pbkdf2Iterations = 100000;
    this.cryptoAPI = this.getCryptoInstance();
  }

  getCryptoInstance() {
    if (typeof crypto !== 'undefined' && crypto.subtle) {
      return crypto;
    } else if (typeof self !== 'undefined' && self.crypto) {
      return self.crypto;
    } else if (typeof window !== 'undefined' && window.crypto) {
      return window.crypto;
    }
    throw new Error('Web Crypto API not available');
  }

  generateRandomBytes(length) {
    const array = new Uint8Array(length);
    this.cryptoAPI.getRandomValues(array);
    return array;
  }

  async deriveKey(masterPassword, salt) {
    const encoder = new TextEncoder();
    const passwordBuffer = encoder.encode(masterPassword);
    const keyMaterial = await this.cryptoAPI.subtle.importKey(
      'raw', passwordBuffer, 'PBKDF2', false, ['deriveBits', 'deriveKey']
    );
    return await this.cryptoAPI.subtle.deriveKey(
      { name: 'PBKDF2', salt, iterations: this.pbkdf2Iterations, hash: 'SHA-256' },
      keyMaterial,
      { name: this.algorithm, length: this.keyLength },
      false, ['encrypt', 'decrypt']
    );
  }

  async encrypt(plaintext, masterPassword) {
    try {
      const salt = this.generateRandomBytes(this.saltLength);
      const iv = this.generateRandomBytes(this.ivLength);
      const key = await this.deriveKey(masterPassword, salt);
      const encoder = new TextEncoder();
      const ciphertext = await this.cryptoAPI.subtle.encrypt(
        { name: this.algorithm, iv }, key, encoder.encode(plaintext)
      );
      const result = new Uint8Array(salt.length + iv.length + ciphertext.byteLength);
      result.set(salt, 0);
      result.set(iv, salt.length);
      result.set(new Uint8Array(ciphertext), salt.length + iv.length);
      return this.arrayBufferToBase64(result);
    } catch (error) {
      throw new Error('Encryption failed');
    }
  }

  async decrypt(encryptedData, masterPassword) {
    try {
      const dataBuffer = this.base64ToArrayBuffer(encryptedData);
      const salt = dataBuffer.slice(0, this.saltLength);
      const iv = dataBuffer.slice(this.saltLength, this.saltLength + this.ivLength);
      const ciphertext = dataBuffer.slice(this.saltLength + this.ivLength);
      const key = await this.deriveKey(masterPassword, salt);
      const plaintext = await this.cryptoAPI.subtle.decrypt(
        { name: this.algorithm, iv }, key, ciphertext
      );
      return new TextDecoder().decode(plaintext);
    } catch (error) {
      throw new Error('Decryption failed');
    }
  }

  generatePassword(length = 16, options = {}) {
    const settings = { lowercase: true, uppercase: true, numbers: true, symbols: true, ...options };
    let charset = '';
    if (settings.lowercase) charset += 'abcdefghijklmnopqrstuvwxyz';
    if (settings.uppercase) charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    if (settings.numbers) charset += '0123456789';
    if (settings.symbols) charset += '!@#$%^&*-_=+';
    if (!charset) throw new Error('Select at least one character type');
    
    const randomBytes = this.generateRandomBytes(length);
    let password = '';
    for (let i = 0; i < length; i++) {
      password += charset[randomBytes[i] % charset.length];
    }
    return password;
  }

  calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength += 25;
    if (password.length >= 12) strength += 15;
    if (password.length >= 16) strength += 10;
    if (/[a-z]/.test(password)) strength += 15;
    if (/[A-Z]/.test(password)) strength += 15;
    if (/[0-9]/.test(password)) strength += 10;
    if (/[^a-zA-Z0-9]/.test(password)) strength += 10;
    return Math.min(strength, 100);
  }

  arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.length; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  base64ToArrayBuffer(base64) {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    return bytes;
  }
}
