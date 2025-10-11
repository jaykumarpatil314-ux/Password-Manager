const cryptoManager = new CryptoManager();
const api = new APIClient('http://localhost:5000');

let currentUser = null;
let masterPassword = null;
let passwords = [];
let currentPasswordId = null;

const authScreen = document.getElementById('auth-screen');
const mainScreen = document.getElementById('main-screen');
const loading = document.getElementById('loading');
const toast = document.getElementById('toast');

// Initialize
(async function init() {
  try {
    const token = await api.getToken();
    const userData = await chrome.storage.local.get('current_user');
    const sessionData = await chrome.storage.session.get('master_password');
    
    if (token && userData.current_user) {
      currentUser = userData.current_user;
      if (sessionData.master_password) {
        masterPassword = sessionData.master_password;
      }
      showMainScreen();
      await loadPasswords();
    } else {
      showAuthScreen();
    }
  } catch (error) {
    showAuthScreen();
  }
})();

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.form').forEach(f => f.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(`${tab.dataset.tab}-form`).classList.add('active');
  });
});

// Login
document.getElementById('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;
  
  if (!username || !password) {
    showError('login-error', 'Please fill in all fields');
    return;
  }
  
  showLoading(true);
  try {
    const response = await api.login(username, password);
    masterPassword = password;
    currentUser = response.user;
    await chrome.storage.session.set({ master_password: password });
    await chrome.storage.local.set({ current_user: currentUser });
    showMainScreen();
    await loadPasswords();
    showToast('Welcome back!');
  } catch (error) {
    showError('login-error', error.message || 'Login failed');
  } finally {
    showLoading(false);
  }
});

// Register
document.getElementById('register-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('register-username').value.trim();
  const email = document.getElementById('register-email').value.trim();
  const password = document.getElementById('register-password').value;
  
  if (!username || !email || !password) {
    showError('register-error', 'Please fill in all fields');
    return;
  }
  
  const strength = cryptoManager.calculatePasswordStrength(password);
  if (strength < 60) {
    showError('register-error', 'Password too weak');
    return;
  }
  
  showLoading(true);
  try {
    const response = await api.register(username, email, password);
    masterPassword = password;
    currentUser = response.user;
    await chrome.storage.session.set({ master_password: password });
    await chrome.storage.local.set({ current_user: currentUser });
    showMainScreen();
    showToast('Account created successfully!');
  } catch (error) {
    showError('register-error', error.message || 'Registration failed');
  } finally {
    showLoading(false);
  }
});

// Password strength
document.getElementById('register-password').addEventListener('input', (e) => {
  const strength = cryptoManager.calculatePasswordStrength(e.target.value);
  const fill = document.getElementById('strength-fill');
  const text = document.getElementById('strength-text');
  fill.style.width = strength + '%';
  text.textContent = strength < 40 ? 'Weak' : strength < 70 ? 'Medium' : 'Strong';
});

// Logout
document.getElementById('logout-btn').addEventListener('click', async () => {
  await api.logout();
  await chrome.storage.local.clear();
  await chrome.storage.session.clear();
  currentUser = null;
  masterPassword = null;
  passwords = [];
  showAuthScreen();
  showToast('Logged out');
});

// Load passwords
async function loadPasswords() {
  if (!masterPassword) {
    const sessionData = await chrome.storage.session.get('master_password');
    if (sessionData.master_password) {
      masterPassword = sessionData.master_password;
    } else {
      return;
    }
  }
  
  showLoading(true);
  try {
    const response = await api.getPasswords();
    passwords = response.passwords || [];
    
    for (let pwd of passwords) {
      try {
        if (pwd.username && pwd.username.trim()) {
          pwd.decrypted_username = await cryptoManager.decrypt(pwd.username, masterPassword);
        } else {
          pwd.decrypted_username = '';
        }
      } catch (error) {
        pwd.decrypted_username = '[Error]';
      }
    }
    
    displayPasswords(passwords);
  } catch (error) {
    showToast('Failed to load passwords');
  } finally {
    showLoading(false);
  }
}

// Display passwords
function displayPasswords(passwordsToDisplay = passwords) {
  const list = document.getElementById('password-list');
  const empty = document.getElementById('empty-state');
  
  if (!passwordsToDisplay || passwordsToDisplay.length === 0) {
    list.style.display = 'none';
    empty.style.display = 'block';
    return;
  }
  
  list.style.display = 'block';
  empty.style.display = 'none';
  list.innerHTML = '';
  
  passwordsToDisplay.forEach(pwd => {
    const item = document.createElement('div');
    item.className = 'password-item';
    
    const header = document.createElement('div');
    header.className = 'password-header';
    header.innerHTML = `
      <div class="password-info">
        <div class="password-title">${escapeHtml(pwd.website_name || 'Untitled')}</div>
        <div class="password-url">${escapeHtml(pwd.website_url)}</div>
        ${pwd.decrypted_username ? `<div class="password-username">${escapeHtml(pwd.decrypted_username)}</div>` : ''}
      </div>
    `;
    
    const actions = document.createElement('div');
    actions.className = 'password-actions';
    
    const copyBtn = createButton('Copy', 'btn-primary', async () => await copyPassword(pwd.id));
    const editBtn = createButton('Edit', 'btn-secondary', async () => await editPassword(pwd.id));
    const deleteBtn = createButton('Delete', 'btn-secondary', async () => await deletePassword(pwd.id));
    
    actions.appendChild(copyBtn);
    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);
    
    item.appendChild(header);
    item.appendChild(actions);
    list.appendChild(item);
  });
}

function createButton(text, className, onClick) {
  const btn = document.createElement('button');
  btn.textContent = text;
  btn.className = className;
  btn.addEventListener('click', onClick);
  return btn;
}

// Copy password
async function copyPassword(passwordId) {
  try {
    const pwd = passwords.find(p => p.id === passwordId);
    if (!pwd) throw new Error('Password not found');
    
    showLoading(true);
    const decrypted = await cryptoManager.decrypt(pwd.encrypted_password, masterPassword);
    await navigator.clipboard.writeText(decrypted);
    showToast('Password copied!');
  } catch (error) {
    showToast('Failed to copy');
  } finally {
    showLoading(false);
  }
}

// Edit password
async function editPassword(passwordId) {
  const pwd = passwords.find(p => p.id === passwordId);
  if (!pwd) return;
  
  currentPasswordId = passwordId;
  
  showLoading(true);
  try {
    const decryptedPassword = await cryptoManager.decrypt(pwd.encrypted_password, masterPassword);
    
    document.getElementById('modal-title').textContent = 'Edit Password';
    document.getElementById('modal-url').value = pwd.website_url || '';
    document.getElementById('modal-name').value = pwd.website_name || '';
    document.getElementById('modal-username').value = pwd.decrypted_username || '';
    document.getElementById('modal-password').value = decryptedPassword;
    document.getElementById('modal-notes').value = '';
    
    document.getElementById('password-modal').style.display = 'flex';
  } catch (error) {
    showToast('Failed to load password');
  } finally {
    showLoading(false);
  }
}

// Delete password
async function deletePassword(passwordId) {
  if (!confirm('Delete this password?')) return;
  
  showLoading(true);
  try {
    await api.deletePassword(passwordId);
    showToast('Password deleted');
    await loadPasswords();
  } catch (error) {
    showToast('Failed to delete');
  } finally {
    showLoading(false);
  }
}

// Add password
document.getElementById('add-btn').addEventListener('click', () => {
  currentPasswordId = null;
  document.getElementById('modal-title').textContent = 'Add Password';
  document.getElementById('password-form').reset();
  document.getElementById('password-modal').style.display = 'flex';
});

// Save password
document.getElementById('password-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const url = document.getElementById('modal-url').value.trim();
  const name = document.getElementById('modal-name').value.trim();
  const username = document.getElementById('modal-username').value.trim();
  const password = document.getElementById('modal-password').value;
  const notes = document.getElementById('modal-notes').value.trim();
  
  if (!url || !password) {
    showError('modal-error', 'URL and password required');
    return;
  }
  
  showLoading(true);
  try {
    const encryptedPassword = await cryptoManager.encrypt(password, masterPassword);
    const encryptedUsername = username ? await cryptoManager.encrypt(username, masterPassword) : '';
    const encryptedNotes = notes ? await cryptoManager.encrypt(notes, masterPassword) : '';
    
    const passwordData = {
      website_url: url,
      website_name: name || url,
      username: encryptedUsername,
      encrypted_password: encryptedPassword,
      notes: encryptedNotes,
      iv: 'client-handled'
    };
    
    if (currentPasswordId) {
      await api.updatePassword(currentPasswordId, passwordData);
      showToast('Password updated');
    } else {
      await api.createPassword(passwordData);
      showToast('Password saved');
    }
    
    document.getElementById('password-modal').style.display = 'none';
    await loadPasswords();
  } catch (error) {
    showError('modal-error', error.message);
  } finally {
    showLoading(false);
  }
});

// Generate password
document.getElementById('generate-btn').addEventListener('click', () => {
  try {
    const generated = cryptoManager.generatePassword(16);
    document.getElementById('modal-password').value = generated;
    showToast('Password generated');
  } catch (error) {
    showToast('Generation failed');
  }
});

// Close modal
document.querySelectorAll('.modal-close').forEach(btn => {
  btn.addEventListener('click', () => {
    document.getElementById('password-modal').style.display = 'none';
  });
});

// Search
document.getElementById('search-input').addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  if (!query) {
    displayPasswords(passwords);
    return;
  }
  const filtered = passwords.filter(pwd => {
    const searchText = `${pwd.website_name} ${pwd.website_url} ${pwd.decrypted_username || ''}`.toLowerCase();
    return searchText.includes(query);
  });
  displayPasswords(filtered);
});

// Utilities
function showLoading(show) {
  loading.style.display = show ? 'flex' : 'none';
}

function showError(elementId, message) {
  const errorEl = document.getElementById(elementId);
  if (errorEl) {
    errorEl.textContent = message;
    errorEl.style.display = 'block';
    setTimeout(() => errorEl.style.display = 'none', 5000);
  }
}

function showToast(message) {
  toast.textContent = message;
  toast.style.display = 'block';
  setTimeout(() => toast.style.display = 'none', 3000);
}

function showAuthScreen() {
  authScreen.style.display = 'block';
  mainScreen.style.display = 'none';
}

function showMainScreen() {
  authScreen.style.display = 'none';
  mainScreen.style.display = 'block';
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}
