/**
 * Background service worker for Password Manager
 */

// Handle extension installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('Password Manager Extension installed');
  
  // Set default settings
  chrome.storage.local.set({
    settings: {
      autofillEnabled: true,
      autoLockMinutes: 15,
      passwordLength: 16
    }
  });
});

// Handle messages from content scripts and popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'loginFormDetected') {
    handleLoginFormDetected(request.url, sender.tab.id);
  }
  
  return true;
});

/**
 * Handle login form detection
 */
async function handleLoginFormDetected(url, tabId) {
  try {
    // Could trigger icon badge or notification
    chrome.action.setBadgeText({ text: '1', tabId: tabId });
    chrome.action.setBadgeBackgroundColor({ color: '#667eea', tabId: tabId });
  } catch (error) {
    console.error('Error handling login form detection:', error);
  }
}

/**
 * Auto-lock after inactivity
 */
let lockTimer = null;

chrome.storage.onChanged.addListener((changes, namespace) => {
  if (changes.current_user) {
    resetLockTimer();
  }
});

function resetLockTimer() {
  if (lockTimer) {
    clearTimeout(lockTimer);
  }
  
  chrome.storage.local.get('settings', (result) => {
    const autoLockMinutes = result.settings?.autoLockMinutes || 15;
    
    lockTimer = setTimeout(() => {
      lockExtension();
    }, autoLockMinutes * 60 * 1000);
  });
}

function lockExtension() {
  chrome.storage.local.remove(['auth_token', 'master_password_hint']);
  chrome.action.setBadgeText({ text: '🔒' });
}
