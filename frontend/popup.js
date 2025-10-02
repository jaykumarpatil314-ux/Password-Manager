/**
 * Main popup logic for Password Manager Extension
 */

// Initialize modules
const crypto = new CryptoManager();
const api = new APIClient('http://localhost:5000');

// State management
let currentUser = null;
let masterPassword = null;
let passwords = [];
let currentPasswordId = null;

// DOM Elements
const loginScreen = document.getElementById('login-screen');
const mainScreen = document.getElementById('main-screen');
const loadingOverlay = document.getElementById('loading-overlay');

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
  await checkAuthentication();
  setupEventListeners();
});

/**
 * Check if user is already authenticated
 */
async function checkAuthentication() {
  const token = await api.getToken();
  const storedUser = await chrome.storage.local.get('current_user');
  
  if (token && storedUser.current_user) {
    currentUser = storedUser.current_user;
    showMainScreen();
  } else {
    showLoginScreen();
  }
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
  // Tab switching
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });

  // Auth forms
  document.getElementById('login-form').addEventListener('submit', handleLogin);
  document.getElementById('register-form').addEventListener('submit', handleRegister);
  document.getElementById('logout-btn').addEventListener('click', handleLogout);

  // Password strength meter
  document.getElementById('register-password').addEventListener('input', updatePasswordStrength);

  // Main screen actions
  document.getElementById('add-password-btn').addEventListener('click', () => showPasswordModal());
  document.getElementById('generate-password-btn').addEventListener('click', showGeneratorModal);
  document.getElementById('search-input').addEventListener('input', handleSearch);

  // Modal actions
  document.querySelectorAll('.close-btn, .cancel-btn').forEach(btn => {
    btn.addEventListener('click', closeModals);
  });
  document.getElementById('password-form').addEventListener('submit', handleSavePassword);
  document.getElementById('toggle-password-visibility').addEventListener('click', togglePasswordVisibility);
  document.getElementById('generate-modal-password').addEventListener('click', generatePasswordForModal);

  // Generator actions
  document.getElementById('password-length').addEventListener('input', (e) => {
    document.getElementById('length-value').textContent = e.target.value;
  });
  document.getElementById('regenerate-password').addEventListener('click', generatePassword);
  document.getElementById('copy-generated-password').addEventListener('click', copyGeneratedPassword);
}

/**
 * Switch between login and register tabs
 */
function switchTab(tabName) {
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.tab === tabName);
  });
  
  document.querySelectorAll('.auth-form').forEach(form => {
    form.classList.toggle('active', form.id === `${tabName}-form`);
  });
}

/**
 * Handle user login
 */
async function handleLogin(e) {
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
    
    await chrome.storage.local.set({ 
      current_user: currentUser,
      master_password_hint: username // For session only
    });
    
    showMainScreen();
    await loadPasswords();
    
  } catch (error) {
    showError('login-error', error.message || 'Login failed');
  } finally {
    showLoading(false);
  }
}

/**
 * Handle user registration
 */
async function handleRegister(e) {
  e.preventDefault();
  
  const username = document.getElementById('register-username').value.trim();
  const email = document.getElementById('register-email').value.trim();
  const password = document.getElementById('register-password').value;
  const confirmPassword = document.getElementById('register-confirm-password').value;
  
  if (!username || !email || !password) {
    showError('register-error', 'Please fill in all fields');
    return;
  }

  if (password !== confirmPassword) {
    showError('register-error', 'Passwords do not match');
    return;
  }

  const strength = crypto.calculatePasswordStrength(password);
  if (strength < 60) {
    showError('register-error', 'Please use a stronger password');
    return;
  }

  showLoading(true);

  try {
    const response = await api.register(username, email, password);
    
    masterPassword = password;
    currentUser = response.user;
    
    await chrome.storage.local.set({ 
      current_user: currentUser,
      master_password_hint: username
    });
    
    showMainScreen();
    await loadPasswords();
    
  } catch (error) {
    showError('register-error', error.message || 'Registration failed');
  } finally {
    showLoading(false);
  }
}

/**
 * Handle logout
 */
async function handleLogout() {
  await api.logout();
  await chrome.storage.local.clear();
  
  currentUser = null;
  masterPassword = null;
  passwords = [];
  
  showLoginScreen();
}

/**
 * Update password strength meter
 */
function updatePasswordStrength(e) {
  const password = e.target.value;
  const strength = crypto.calculatePasswordStrength(password);
  
  const strengthBar = document.getElementById('strength-bar');
  const strengthText = document.getElementById('strength-text');
  
  strengthBar.style.width = `${strength}%`;
  
  if (strength < 40) {
    strengthBar.style.background = '#dc3545';
    strengthText.textContent = 'Weak';
    strengthText.style.color = '#dc3545';
  } else if (strength < 70) {
    strengthBar.style.background = '#ffc107';
    strengthText.textContent = 'Medium';
    strengthText.style.color = '#ffc107';
  } else {
    strengthBar.style.background = '#28a745';
    strengthText.textContent = 'Strong';
    strengthText.style.color = '#28a745';
  }
}

/**
 * Load all passwords from backend
 */
async function loadPasswords() {
  if (!masterPassword) {
    // Request master password from user
    const password = prompt('Enter your master password to decrypt passwords:');
    if (!password) return;
    masterPassword = password;
  }

  showLoading(true);

  try {
    const response = await api.getPasswords();
    passwords = response.passwords;
    
    // Decrypt passwords client-side
    for (let pwd of passwords) {
      try {
        if (pwd.username) {
          pwd.decrypted_username = await crypto.decrypt(pwd.username, masterPassword);
        }
        if (pwd.notes) {
          pwd.decrypted_notes = await crypto.decrypt(pwd.notes, masterPassword);
        }
      } catch (error) {
        console.error('Decryption failed for password:', pwd.id);
      }
    }
    
    displayPasswords(passwords);
    
  } catch (error) {
    showError('main-error', 'Failed to load passwords');
  } finally {
    showLoading(false);
  }
}

/**
 * Display passwords in the list
 */
function displayPasswords(passwordsToDisplay) {
  const passwordList = document.getElementById('password-list');
  const noPasswords = document.getElementById('no-passwords');
  
  passwordList.innerHTML = '';
  
  if (passwordsToDisplay.length === 0) {
    passwordList.style.display = 'none';
    noPasswords.style.display = 'block';
    return;
  }
  
  passwordList.style.display = 'block';
  noPasswords.style.display = 'none';
  
  passwordsToDisplay.forEach(pwd => {
    const item = createPasswordItem(pwd);
    passwordList.appendChild(item);
  });
}

/**
 * Create password list item element
 */
function createPasswordItem(pwd) {
  const item = document.createElement('div');
  item.className = 'password-item';
  item.dataset.passwordId = pwd.id;
  
  item.innerHTML = `
    <div class="password-item-header">
      <div class="password-item-title">${escapeHtml(pwd.website_name || 'Untitled')}</div>
    </div>
    <div class="password-item-url">${escapeHtml(pwd.website_url)}</div>
    <div class="password-item-actions">
      <button class="autofill-btn" data-id="${pwd.id}">Autofill</button>
      <button class="copy-btn" data-id="${pwd.id}">Copy</button>
      <button class="edit-btn" data-id="${pwd.id}">Edit</button>
      <button class="delete-btn" data-id="${pwd.id}">Delete</button>
    </div>
  `;
  
  // Event listeners
  item.querySelector('.autofill-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    handleAutofill(pwd.id);
  });
  
  item.querySelector('.copy-btn').addEventListener('click', async (e) => {
    e.stopPropagation();
    await handleCopyPassword(pwd.id);
  });
  
  item.querySelector('.edit-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    showPasswordModal(pwd.id);
  });
  
  item.querySelector('.delete-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    handleDeletePassword(pwd.id);
  });
  
  return item;
}

/**
 * Handle search
 */
function handleSearch(e) {
  const query = e.target.value.toLowerCase().trim();
  
  if (!query) {
    displayPasswords(passwords);
    return;
  }
  
  const filtered = passwords.filter(pwd => {
    return pwd.website_name?.toLowerCase().includes(query) ||
           pwd.website_url?.toLowerCase().includes(query) ||
           pwd.decrypted_username?.toLowerCase().includes(query);
  });
  
  displayPasswords(filtered);
}
/**
 * Show password modal for add/edit
 */
function showPasswordModal(passwordId = null) {
  currentPasswordId = passwordId;
  const modal = document.getElementById('password-modal');
  const title = document.getElementById('modal-title');
  
  if (passwordId) {
    title.textContent = 'Edit Password';
    const pwd = passwords.find(p => p.id === passwordId);
    if (pwd) {
      document.getElementById('modal-website-url').value = pwd.website_url || '';
      document.getElementById('modal-website-name').value = pwd.website_name || '';
      document.getElementById('modal-username').value = pwd.decrypted_username || '';
      document.getElementById('modal-notes').value = pwd.decrypted_notes || '';
    }
  } else {
    title.textContent = 'Add Password';
    document.getElementById('password-form').reset();
  }
  
  modal.style.display = 'flex';
}

/**
 * Handle save password
 */
async function handleSavePassword(e) {
  e.preventDefault();
  
  const websiteUrl = document.getElementById('modal-website-url').value.trim();
  const websiteName = document.getElementById('modal-website-name').value.trim();
  const username = document.getElementById('modal-username').value.trim();
  const password = document.getElementById('modal-password').value;
  const notes = document.getElementById('modal-notes').value.trim();
  
  if (!websiteUrl || !password) {
    showError('modal-error', 'Website URL and password are required');
    return;
  }

  showLoading(true);

  try {
    // Encrypt data client-side
    const encryptedPassword = await crypto.encrypt(password, masterPassword);
    const encryptedUsername = username ? await crypto.encrypt(username, masterPassword) : '';
    const encryptedNotes = notes ? await crypto.encrypt(notes, masterPassword) : '';
    
    const passwordData = {
      website_url: websiteUrl,
      website_name: websiteName,
      username: encryptedUsername,
      encrypted_password: encryptedPassword,
      notes: encryptedNotes,
      iv: 'client-side-handled'
    };
    
    if (currentPasswordId) {
      await api.updatePassword(currentPasswordId, passwordData);
    } else {
      await api.createPassword(passwordData);
    }
    
    closeModals();
    await loadPasswords();
    
  } catch (error) {
    showError('modal-error', error.message || 'Failed to save password');
  } finally {
    showLoading(false);
  }
}

/**
 * Handle delete password
 */
async function handleDeletePassword(passwordId) {
  if (!confirm('Are you sure you want to delete this password?')) {
    return;
  }

  showLoading(true);

  try {
    await api.deletePassword(passwordId);
    await loadPasswords();
  } catch (error) {
    alert('Failed to delete password');
  } finally {
    showLoading(false);
  }
}

/**
 * Handle copy password
 */
async function handleCopyPassword(passwordId) {
  const pwd = passwords.find(p => p.id === passwordId);
  if (!pwd) return;

  try {
    const decryptedPassword = await crypto.decrypt(pwd.encrypted_password, masterPassword);
    await navigator.clipboard.writeText(decryptedPassword);
    
    // Show temporary notification
    showNotification('Password copied to clipboard!');
  } catch (error) {
    alert('Failed to copy password');
  }
}

/**
 * Handle autofill
 */
async function handleAutofill(passwordId) {
  const pwd = passwords.find(p => p.id === passwordId);
  if (!pwd) return;

  try {
    const decryptedPassword = await crypto.decrypt(pwd.encrypted_password, masterPassword);
    const decryptedUsername = pwd.username ? await crypto.decrypt(pwd.username, masterPassword) : '';
    
    // Send message to content script
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, {
      action: 'autofill',
      username: decryptedUsername,
      password: decryptedPassword
    });
    
    window.close();
  } catch (error) {
    alert('Failed to autofill');
  }
}

/**
 * Show password generator modal
 */
function showGeneratorModal() {
  const modal = document.getElementById('generator-modal');
  modal.style.display = 'flex';
  generatePassword();
}

/**
 * Generate random password
 */
function generatePassword() {
  const length = parseInt(document.getElementById('password-length').value);
  const options = {
    lowercase: document.getElementById('include-lowercase').checked,
    uppercase: document.getElementById('include-uppercase').checked,
    numbers: document.getElementById('include-numbers').checked,
    symbols: document.getElementById('include-symbols').checked
  };
  
  try {
    const password = crypto.generatePassword(length, options);
    document.getElementById('generated-password-text').value = password;
  } catch (error) {
    alert(error.message);
  }
}

/**
 * Generate password for modal input
 */
function generatePasswordForModal() {
  const password = crypto.generatePassword(16);
  document.getElementById('modal-password').value = password;
}

/**
 * Copy generated password
 */
async function copyGeneratedPassword() {
  const password = document.getElementById('generated-password-text').value;
  await navigator.clipboard.writeText(password);
  showNotification('Password copied!');
}

/**
 * Toggle password visibility
 */
function togglePasswordVisibility() {
  const input = document.getElementById('modal-password');
  input.type = input.type === 'password' ? 'text' : 'password';
}

/**
 * Close all modals
 */
function closeModals() {
  document.querySelectorAll('.modal').forEach(modal => {
    modal.style.display = 'none';
  });
  document.getElementById('password-form').reset();
  currentPasswordId = null;
}

/**
 * Show/hide loading overlay
 */
function showLoading(show) {
  loadingOverlay.style.display = show ? 'flex' : 'none';
}

/**
 * Show error message
 */
function showError(elementId, message) {
  const errorElement = document.getElementById(elementId);
  errorElement.textContent = message;
  errorElement.classList.add('show');
  
  setTimeout(() => {
    errorElement.classList.remove('show');
  }, 5000);
}

/**
 * Show temporary notification
 */
function showNotification(message) {
  const notification = document.createElement('div');
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #28a745;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    z-index: 3000;
  `;
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.remove();
  }, 2000);
}

/**
 * Show login screen
 */
function showLoginScreen() {
  loginScreen.style.display = 'block';
  mainScreen.style.display = 'none';
}

/**
 * Show main screen
 */
function showMainScreen() {
  loginScreen.style.display = 'none';
  mainScreen.style.display = 'block';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
