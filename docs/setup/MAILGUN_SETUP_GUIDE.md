# Mailgun Setup Guide - Instant Webhook Implementation

## Step 1: Sign Up for Mailgun Foundation

1. Go to: https://signup.mailgun.com/new/signup
2. Choose **Foundation Plan** ($ 35/mo)
3. Enter payment info (30-day trial, cancel anytime)
4. Verify email address

---

## Step 2: Add Receiving Domain

1. In Mailgun Dashboard → **Sending** → **Domains**
2. Click **Add New Domain**
3. Enter: `replies.getaevylabs.com`
4. Select **US** region
5. Click **Add Domain**

---

## Step 3: Configure DNS Records

Mailgun will show you these records to add in your domain registrar (Namecheap/GoDaddy/etc):

### MX Records (Required for receiving email)
```
Priority: 10
Host: replies
Value: mxa.mailgun.org

Priority: 10
Host: replies  
Value: mxb.mailgun.org
```

### TXT Records (For sending)
```
Host: replies
Value: v=spf1 include:mailgun.org ~all

Host: <random>._domainkey.replies
Value: <long DKIM key provided by Mailgun>
```

**Wait 10-15 minutes for DNS propagation**, then click **Verify DNS Settings** in Mailgun dashboard.

---

## Step 4: Create Mailgun Route

1. In Mailgun Dashboard → **Sending** → **Routes**
2. Click **Create Route**
3. Configure:
   - **Expression Type**: Match Recipient
   - **Recipient**: `.*@replies.getaevylabs.com` (regex to catch all)
   - **Actions**: 
     - ✅ Forward
     - **URL**: `https://deekshakdk11--reply-triage-webhook-fastapi-app.modal.run/webhook/mailgun`
   - **Priority**: 0
   - **Description**: Reply Triage Webhook
4. Click **Create Route**

---

## Step 5: Get API Credentials

1. In Mailgun Dashboard → **Settings** → **API Keys**
2. Copy **Private API key** (starts with `key-...`)
3. Note your **Domain name**: `replies.getaevylabs.com`

---

## Step 6: Add Secrets to Modal

```bash
modal secret set agency-os MAILGUN_API_KEY=key-your-api-key-here MAILGUN_DOMAIN=replies.getaevylabs.com
```

---

## Step 7: Test the Route

Send a test email to: `test@replies.getaevylabs.com`

### Check:
1. **Mailgun Logs**: Dashboard → **Sending** → **Logs** (should show received email)
2. **Modal Logs**: `modal app logs reply-triage-webhook` (should show webhook triggered)

**Expected output** in Modal logs:
```
📧 Mailgun Inbound: your-email@gmail.com
Classification: interested
🚀 Triggering Fast Fulfillment...
```

---

## Step 8: E2E Test

```bash
python send_e2e_test_email.py
```

1. Check inbox for test email
2. Reply with: "Yes interested"
3. **Check your watch** - time starts NOW!
4. Fulfillment email should arrive in <5 seconds ⚡

---

## Step 9: Stop Polling Daemon

Once E2E test passes:

```bash
modal app stop auto-fulfillment-daemon
```

You no longer need it - Mailgun webhooks are instant!

---

## Troubleshooting

### "Route not triggering"
- Check DNS verified in Mailgun dashboard
- Verify Route expression: `.*@replies.getaevylabs.com`
- Check Route URL has `/webhook/mailgun` path

### "Webhook receiving but not classifying"
- Check Modal secrets: `modal secret list`
- Verify OPENROUTER_API_KEY exists
- Check Modal logs for errors

### "Fulfillment not triggering"
- Verify classification shows "interested"
- Check Modal secrets for APIFY_API_KEY
- Verify fulfillment webhook URL is correct

---

## Cost Breakdown

| Service | Cost |
|---------|------|
| Mailgun Foundation | $35/mo |
| Modal (webhooks) | Free tier |
| OpenRouter (classification) | ~$0.10/day |

**Total**: ~$38/month for instant Speed-to-Lead

---

**Next Step**: Go to https://signup.mailgun.com and start Step 1!
