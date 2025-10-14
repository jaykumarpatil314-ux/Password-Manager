class APIClient {
  constructor(baseURL = 'http://localhost:5000') {
    this.baseURL = baseURL
    this.token = null
  }

  async setToken(token) {
    this.token = token
    await chrome.storage.local.set({ auth_token: token })
  }

  async getToken() {
    if (this.token) return this.token
    const result = await chrome.storage.local.get('auth_token')
    this.token = result.auth_token || null
    return this.token
  }

  async clearToken() {
    this.token = null
    await chrome.storage.local.remove(['auth_token', 'current_user'])
  }

  async request(endpoint, options = {}) {
    const token = await this.getToken()
    console.log(`Making ${options.method || 'GET'} request to ${endpoint}`)
    console.log('Token exists:', !!token)
    console.log(
      'Token preview:',
      token ? token.substring(0, 20) + '...' : 'NO TOKEN'
    )

    const headers = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      ...options.headers,
    }
    if (token) headers['Authorization'] = `Bearer ${token}`

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers,
        mode: 'cors',
        credentials: 'include',
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Request failed')
      return data
    } catch (error) {
      throw error
    }
  }

  async register(username, email, masterPassword) {
    const data = await this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({
        username,
        email,
        master_password: masterPassword,
      }),
    })
    await this.setToken(data.token)
    return data
  }

  async login(username, masterPassword) {
    const data = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, master_password: masterPassword }),
    })
    await this.setToken(data.token)
    return data
  }

  async logout() {
    await this.clearToken()
  }

  async getPasswords() {
    return await this.request('/api/passwords', { method: 'GET' })
  }

  async createPassword(passwordData) {
    return await this.request('/api/passwords', {
      method: 'POST',
      body: JSON.stringify(passwordData),
    })
  }

  async updatePassword(passwordId, passwordData) {
    return await this.request(`/api/passwords/${passwordId}`, {
      method: 'PUT',
      body: JSON.stringify(passwordData),
    })
  }

  async deletePassword(passwordId) {
    return await this.request(`/api/passwords/${passwordId}`, {
      method: 'DELETE',
    })
  }

  async searchPasswords(url) {
    return await this.request('/api/passwords/search', {
      method: 'POST',
      body: JSON.stringify({ url }),
    })
  }
}
