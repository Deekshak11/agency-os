# Mailgun Configuration - Quick Guide

## Step 1: Add Receiving Domain (5 min)

1. **Go to**: Mailgun Dashboard → **Sending** → **Domains**
2. **Click**: "Add New Domain"
3. **Enter**: `replies.getaevylabs.com`
4. **Region**: Select **US**
5. **Click**: "Add Domain"

---

## Step 2: Configure DNS Records (15 min total)

Mailgun will show you DNS records. Add these to your domain provider (Namecheap/GoDaddy):

### MX Records (Required for receiving)
```
Type: MX
Host: replies
Value: mxa.mailgun.org
Priority: 10

Type: MX
Host: replies
Value: mxb.mailgun.org
Priority: 10
```

### TXT Records (For verification)
```
Type: TXT
Host: replies
Value: v=spf1 include:mailgun.org ~all

Type: TXT
Host: <mailgun_shows_you>._domainkey.replies
Value: <long_key_from_mailgun>
```

**Then**: Wait 10-15 mins for DNS propagation, click "Verify DNS" in Mailgun

---

## Step 3: Create Route (2 min)

Once domain is verified:

1. **Go to**: Mailgun Dashboard → **Sending** → **Routes**
2. **Click**: "Create Route"
3. **Configure**:
   - **Expression Type**: "Match Recipient"
   - **Recipient**: `.*@replies.getaevylabs.com`
   - **Actions**: Check "Forward"
   - **Forward URL**: `https://deekshakdk11--reply-triage-webhook-fastapi-app.modal.run/webhook/mailgun`
   - **Priority**: 0
4. **Click**: "Create Route"

---

## Step 4: Get API Key

1. **Go to**: Mailgun Dashboard → **Settings** → **API Keys**
2. **Copy**: Private API key (starts with `key-...`)

---

## Step 5: Add Modal Secrets

Run this command:

```bash
modal secret set agency-os MAILGUN_API_KEY=key-your-key-here MAILGUN_DOMAIN=replies.getaevylabs.com
```

---

## Step 6: Test It

Send email to: `test@replies.getaevylabs.com`

Check:
- **Mailgun Logs**: Should show "Delivered"
- **Modal Logs**: `modal app logs reply-triage-webhook` should show webhook trigger

---

**Where are you in this process?** Let me know which step you're on and I'll help!
