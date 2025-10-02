/**
 * Content script for password autofill functionality
 */

// Listen for autofill messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'autofill') {
    autofillCredentials(request.username, request.password);
    sendResponse({ success: true });
  }
});

/**
 * Autofill credentials into login forms
 */
function autofillCredentials(username, password) {
  // Find username/email fields
  const usernameFields = document.querySelectorAll(
    'input[type="text"], input[type="email"], input[name*="user"], input[name*="email"], input[id*="user"], input[id*="email"]'
  );
  
  // Find password fields
  const passwordFields = document.querySelectorAll('input[type="password"]');
  
  // Fill username
  if (username && usernameFields.length > 0) {
    usernameFields[0].value = username;
    usernameFields[0].dispatchEvent(new Event('input', { bubbles: true }));
    usernameFields[0].dispatchEvent(new Event('change', { bubbles: true }));
  }
  
  // Fill password
  if (password && passwordFields.length > 0) {
    passwordFields[0].value = password;
    passwordFields[0].dispatchEvent(new Event('input', { bubbles: true }));
    passwordFields[0].dispatchEvent(new Event('change', { bubbles: true }));
  }
  
  // Highlight filled fields
  if (usernameFields[0]) {
    highlightField(usernameFields[0]);
  }
  if (passwordFields[0]) {
    highlightField(passwordFields[0]);
  }
}

/**
 * Highlight filled field
 */
function highlightField(field) {
  const originalBorder = field.style.border;
  field.style.border = '2px solid #28a745';
  
  setTimeout(() => {
    field.style.border = originalBorder;
  }, 2000);
}

/**
 * Detect login forms and notify extension
 */
function detectLoginForms() {
  const passwordFields = document.querySelectorAll('input[type="password"]');
  
  if (passwordFields.length > 0) {
    chrome.runtime.sendMessage({
      action: 'loginFormDetected',
      url: window.location.href
    });
  }
}

// Run detection on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', detectLoginForms);
} else {
  detectLoginForms();
}
