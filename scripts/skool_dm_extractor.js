// SKOOL DM EXTRACTOR - Run this in browser DevTools (F12 > Console)
// Make sure you're on skool.com and logged in first

(async function extractAllDMs() {
    const results = [];

    // Open chat panel
    document.querySelector('button[class*="ChatNotifications"]')?.click();
    await new Promise(r => setTimeout(r, 1500));

    // Get all chat links
    const chatLinks = Array.from(document.querySelectorAll('a[href*="/chat?ch="]'));
    console.log(`Found ${chatLinks.length} chats to extract...`);

    for (let i = 0; i < chatLinks.length; i++) {
        const link = chatLinks[i];
        const name = link.querySelector('[class*="Name"]')?.innerText || link.innerText.split('\n')[0];
        const preview = link.innerText;

        // Skip non-Synthesizers (check for other community badges)
        if (preview.includes('AI Automation Society') || preview.includes('AIS')) {
            console.log(`Skipping ${name} - not from Synthesizers`);
            continue;
        }

        console.log(`Extracting chat ${i + 1}: ${name}`);

        // Click to open chat
        link.click();
        await new Promise(r => setTimeout(r, 2000));

        // Scroll to top to get full history
        const chatContainer = document.querySelector('[class*="ChatContainer"]') ||
            document.querySelector('[class*="MessageList"]');
        if (chatContainer) {
            for (let j = 0; j < 10; j++) {
                chatContainer.scrollTop = 0;
                await new Promise(r => setTimeout(r, 300));
            }
        }

        // Extract all messages
        const messages = [];
        document.querySelectorAll('[class*="MessageRow"], [class*="message"]').forEach(el => {
            const text = el.innerText.trim();
            if (text && text.length > 0) {
                messages.push(text);
            }
        });

        results.push({
            contact: name,
            messageCount: messages.length,
            fullConversation: messages.join('\n---\n'),
            preview: preview.substring(0, 100)
        });

        // Close chat and reopen panel
        document.querySelector('[class*="ChatHeader"] button, button[aria-label*="close"]')?.click();
        await new Promise(r => setTimeout(r, 500));
        document.querySelector('button[class*="ChatNotifications"]')?.click();
        await new Promise(r => setTimeout(r, 1000));
    }

    console.log('=== EXTRACTION COMPLETE ===');
    console.log(JSON.stringify(results, null, 2));

    // Also copy to clipboard
    const output = results.map(r => `
=== ${r.contact} ===
Messages: ${r.messageCount}
${r.fullConversation}
`).join('\n\n');

    navigator.clipboard?.writeText(output);
    console.log('Results copied to clipboard!');

    return results;
})();
