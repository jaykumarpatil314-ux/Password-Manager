console.log('SecureVault background service worker loaded');

chrome.runtime.onInstalled.addListener(() => {
  console.log('SecureVault installed');
});
