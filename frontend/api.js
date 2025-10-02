/**
 * API communication module
 * Handles REST API and WebSocket connections with backend
 */

class APIClient {
  constructor(baseURL = 'http://0.0.0.0:5000') {
    this.baseURL = baseURL;
    this.token = null;
    this.socket = null;
  }

  /**
   * Set authentication token
   */
  setToken(token) {
    this.token = token;
    chrome.storage.local.set({ auth_token: token });
  }

  /**
   * Get authentication token
   */
  async getToken() {
    if (this.token) return this.token;
    
    const result = await chrome.storage.local.get('auth_token');
    this.token = result.auth_token || null;
    return this.token;
  }

  /**
   * Clear authentication token
   */
  async clearToken() {
    this.token = null;
    await chrome.storage.local.remove('auth_token');
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  /**
   * Make authenticated API request
   */
  async request(endpoint, options = {}) {
    const token = await this.getToken();
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const url = `${this.baseURL}${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Request failed with status ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  /**
   * Register new user
   */
  async register(username, email, masterPassword) {
    const data = await this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, master_password: masterPassword })
    });

    this.setToken(data.token);
    return data;
  }

  /**
   * Login user
   */
  async login(username, masterPassword) {
    const data = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, master_password: masterPassword })
    });

    this.setToken(data.token);
    return data;
  }

  /**
   * Logout user
   */
  async logout() {
    await this.clearToken();
  }

  /**
   * Get all password entries
   */
  async getPasswords() {
    return await this.request('/api/passwords', {
      method: 'GET'
    });
  }

  /**
   * Get specific password entry
   */
  async getPassword(passwordId) {
    return await this.request(`/api/passwords/${passwordId}`, {
      method: 'GET'
    });
  }

  /**
   * Create new password entry
   */
  async createPassword(passwordData) {
    return await this.request('/api/passwords', {
      method: 'POST',
      body: JSON.stringify(passwordData)
    });
  }

  /**
   * Update password entry
   */
  async updatePassword(passwordId, passwordData) {
    return await this.request(`/api/passwords/${passwordId}`, {
      method: 'PUT',
      body: JSON.stringify(passwordData)
    });
  }

  /**
   * Delete password entry
   */
  async deletePassword(passwordId) {
    return await this.request(`/api/passwords/${passwordId}`, {
      method: 'DELETE'
    });
  }

  /**
   * Search passwords by URL
   */
  async searchPasswords(url) {
    return await this.request('/api/passwords/search', {
      method: 'POST',
      body: JSON.stringify({ url })
    });
  }

  /**
   * Initialize WebSocket connection
   */
  initWebSocket() {
    return new Promise((resolve, reject) => {
      const wsURL = this.baseURL.replace('http', 'ws');
      this.socket = new WebSocket(`${wsURL}/socket.io/?transport=websocket`);

      this.socket.onopen = () => {
        console.log('WebSocket connected');
        resolve();
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };

      this.socket.onmessage = (event) => {
        this.handleWebSocketMessage(event.data);
      };

      this.socket.onclose = () => {
        console.log('WebSocket disconnected');
        this.socket = null;
      };
    });
  }

  /**
   * Handle WebSocket messages
   */
  handleWebSocketMessage(data) {
    try {
      const message = JSON.parse(data);
      // Handle different message types
      console.log('WebSocket message:', message);
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  }

  /**
   * Send WebSocket message
   */
  sendWebSocketMessage(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = APIClient;
}
