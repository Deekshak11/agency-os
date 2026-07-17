# Final Configuration Steps - Before Testing

## What's Missing

✅ **Systems deployed to Modal**  
❌ **Modal environment variables** (API keys, tokens)  
❌ **Brevo webhook URL** configured  
❌ **Fathom webhook URL** configured

---

## Step 1: Set Modal Environment Variables (5 mins)

### 1.1 Base64-Encode Your Token

First, encode your `token.json` for cloud storage:

```powershell
# Run in PowerShell
cd C:\Users\user\Desktop\Agency_OS
$token = Get-Content token.json -Raw
$bytes = [System.Text.Encoding]::UTF8.GetBytes($token)
$encoded = [Convert]::ToBase64String($bytes)
$encoded | clip  # Copies to clipboard
Write-Host "✅ Token copied to clipboard!"
```

**Copy the output** (now in clipboard) - you'll need it in next step.

### 1.2 Create Modal Secret

Go to: https://modal.com/deekshakdk11/secrets

**Or via CLI:**

```powershell
# Set all environment variables at once
modal secret create agency-os `
  OPENROUTER_API_KEY="your_openrouter_key" `
  BREVO_API_KEY="your_brevo_key" `
  APIFY_API_KEY="your_apify_key" `
  GOOGLE_DRIVE_FOLDER_ID="1JcFpzXIcrzzQk96GXL5kdbBM19vXuL3a" `
  TRACKING_SHEET_ID="19M8Inwgbgb8qVbirt6hoEjr5YQ_Xb6WG-Co1DwdWUzA" `
  TRACKING_SHEET_NAME="Copy of 350 B2 (apollo)" `
  GOOGLE_TOKEN_B64="PASTE_YOUR_BASE64_TOKEN_HERE" `
  AUTO_SEND_INTERESTED="true" `
  AUTO_SEND_QUESTION="false" `
  AUTO_SEND_OBJECTION="false"
```

**Replace these values:**
- `your_openrouter_key` - From OpenRouter dashboard
- `your_brevo_key` - From Brevo API settings
- `your_apify_key` - From Apify console
- `PASTE_YOUR_BASE64_TOKEN_HERE` - The clipboard value from step 1.1

### 1.3 Link Secret to Apps

Update both Modal apps to use the secret:

```powershell
# Update System 1
modal deploy modal_reply_webhook.py --secret agency-os

# Update System 2  
modal deploy modal_fathom_webhook.py --secret agency-os
```

---

## Step 2: Configure Brevo Webhook (2 mins)

### 2.1 Go to Brevo Dashboard

1. Open: https://app.brevo.com/settings/webhooks
2. Click **"Add a new webhook"**

### 2.2 Add Webhook

**Webhook URL:**
```
https://deekshakdk11--reply-triage-webhook-fastapi-wrapper.modal.run/webhook/brevo-inbound
```

**Events to track:**
- ✅ **Inbound email** (this is the only one you need)

**Description:** Reply Triage System

Click **Save**

### 2.3 Test Connection (Optional)

Brevo has a "Test" button - click it to send a test payload.

**Expected result:** 200 OK response

---

## Step 3: Configure Fathom Webhook (2 mins)

### 3.1 Go to Fathom Settings

1. Open: https://app.fathom.video/settings
2. Navigate to **Integrations** → **Webhooks** (or API section)

### 3.2 Add Webhook

**Webhook URL:**
```
https://deekshakdk11--fathom-proposal-webhook-fastapi-wrapper.modal.run/webhook/fathom
```

**Trigger event:**
- ✅ **New AI Summary** (fires when Fathom finishes processing a call)

**Description:** Proposal Generator System

Click **Save**

### 3.3 Verify Connection

Fathom should show a green checkmark if the endpoint is reachable.

---

## Step 4: Verify Configuration (1 min)

### Check Modal Secrets

```powershell
modal secret list
```

**Should show:** `agency-os` secret

### Check Webhook Endpoints

**System 1 health check:**
```
https://deekshakdk11--reply-triage-webhook-fastapi-wrapper.modal.run/
```

**System 2 health check:**
```
https://deekshakdk11--fathom-proposal-webhook-fastapi-wrapper.modal.run/
```

**Open both URLs in browser** - should see:
```json
{
  "status": "active",
  "service": "...",
  "timestamp": "..."
}
```

---

## Step 5: Ready for Testing!

Once all 4 steps are complete, you're ready to test:

### System 1 Test (Reply Triage)
1. Send a cold email to a test address
2. Reply from that address with "Yes, send it over"
3. Check Modal logs: https://modal.com/apps/deekshakdk11/main/deployed/reply-triage-webhook
4. Verify response sent via Brevo
5. Check Google Sheet created (lead magnet fulfillment)

### System 2 Test (Proposal Generator)
1. Do a test call in Fathom
2. End call and wait 2-3 mins for processing
3. Check Modal logs: https://modal.com/apps/deekshakdk11/main/deployed/fathom-proposal-webhook
4. Verify Google Doc proposal created
5. Check email notification (if configured)

---

## Quick Command Reference

**Check your API keys from .env:**
```powershell
cat .env
```

**View Modal logs (real-time):**
```powershell
modal app logs reply-triage-webhook
modal app logs fathom-proposal-webhook
```

**Redeploy after changes:**
```powershell
modal deploy modal_reply_webhook.py --secret agency-os
modal deploy modal_fathom_webhook.py --secret agency-os
```

---

## Troubleshooting

### "Secret not found" error
**Fix:** Run the `modal secret create` command from Step 1.2

### "Environment variable not set" in logs
**Fix:** Redeploy with `--secret agency-os` flag

### Webhook returns 404
**Fix:** Check URL is exactly as shown (including `/webhook/brevo-inbound` path)

### Token expired error
**Fix:** Regenerate token.json using OAuth flow, re-encode to base64, update secret

---

## What You'll Need

From your `.env` file:
- [ ] OPENROUTER_API_KEY
- [ ] BREVO_API_KEY
- [ ] APIFY_API_KEY

From your Google setup:
- [ ] token.json (already have it)
- [ ] GOOGLE_DRIVE_FOLDER_ID (already set: `1JcFpzXIcrzzQk96GXL5kdbBM19vXuL3a`)

**Estimated time:** 10 minutes total

---

## Next Step

Complete these 4 config steps, then let me know when done. I'll help you run test scenarios to verify everything works end-to-end!
