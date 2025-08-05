// Simple background script for 1688 image search extension

// Create context menu when extension is installed
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "searchImage",
    title: "Search on ACBuy",
    contexts: ["image"],
  });
  console.log("🚀 Simple 1688 Search extension installed!");
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "searchImage") {
    const imageUrl = info.srcUrl;
    console.log(`� Searching for image: ${imageUrl}`);

    try {
      // Call our simple server
      const response = await fetch("https://acbuy.cnicholson.hackclub.app/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image_url: imageUrl,
        }),
      });

      const result = await response.json();

      if (result.success) {
        // Open the search URL in a new tab
        chrome.tabs.create({
          url: result.search_url,
          active: true,
        });

        // Show success notification
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icons/icon48.png",
          title: "1688 Search Success!",
          message: "Search results opened in new tab",
        });

        console.log(`✅ Search completed: ${result.search_url}`);
      } else {
        throw new Error(result.error || "Search failed");
      }
    } catch (error) {
      console.error("❌ Search error:", error);

      // Show error notification
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icons/icon48.png",
        title: "1688 Search Error",
        message: `Failed to search: ${error.message}`,
      });
    }
  }
});

console.log("🎯 Simple 1688 Search background script loaded!");
