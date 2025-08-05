// Simple content script for 1688 image search extension
// This script runs on all web pages and provides additional functionality if needed

console.log("🎯 Simple ACBuy Search content script loaded!");

// Optional: Add a subtle indicator when hovering over images
// This helps users know they can right-click to search
document.addEventListener("DOMContentLoaded", function () {
  // Add a small visual indicator to images when hovered
  const style = document.createElement("style");
  style.textContent = `
        img:hover {
            box-shadow: 0 0 3px rgba(0, 123, 255, 0.5) !important;
            cursor: context-menu !important;
        }
    `;
  document.head.appendChild(style);
});

// Listen for any messages from the background script (if needed in the future)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("📨 Content script received message:", request);
  sendResponse({ status: "ok" });
});
