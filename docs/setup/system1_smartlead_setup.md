# System 1: Reply Triage Setup - FINAL

## ✅ WORKING CONFIGURATION

**Webhook URL:**
```
https://deekshakdk11--reply-triage-webhook-fastapi-app.modal.run/webhook/brevo-inbound
```

---

## Setup in Smartlead (5 minutes)

### Step 1: Get Webhook URL
Copy: `https://deekshakdk11--reply-triage-webhook-fastapi-app.modal.run/webhook/brevo-inbound`

### Step 2: Configure in Smartlead
1. Go to **Settings** → **Webhooks**
2. Click **Add Webhook**
3. **Event:** Select "Email Reply"
4. **URL:** Paste webhook URL above
5. **Level:** Account (applies to all campaigns)
6. Click **Save**

### Step 3: Test
1. Click "Test Webhook" button
2. Check Modal logs: `modal app logs reply-triage-webhook`
3. Should see: `Classification: [type]` and `Drafted response:`

---

## What Happens When Someone Replies

```
Prospect replies to your email
    ↓
Smartlead fires webhook → Your System 1
    ↓
GPT-4o-mini classifies reply:
  • interested - Ready to book/get leads
  • question - Needs clarification
  • objection - Has concerns
  • not_interested - Opt-out
    ↓
System drafts appropriate response
    ↓
Logs to Modal (check logs)
    ↓
[TODO: Auto-send or queue for review]
```

---

## Current Status

✅ **Working:**
- Webhook receiving replies from Smartlead
- Classification (GPT-4o-mini)
- Response drafting
- Logging to Modal

⏳ **TODO (Next):**
- Google Sheet logging
- Auto-send responses (or manual approval)
- Fulfillment trigger for "interested"

---

## Check Logs

**See what's happening:**
```bash
modal app logs reply-triage-webhook
```

**Look for:**
- `📥 Smartlead webhook received:`
- `Classification: interested/question/objection/not_interested`
- `Drafted response: [text]`

---

## Costs

**Current setup:**
- Smartlead: $30/mo (existing)
- Modal: $0 (free tier, webhook usage minimal)
- OpenRouter: ~$0.001 per reply (GPT-4o-mini)

**Total:** ~$30/month

**No Brevo needed!** ✅

---

## Next Actions

1. ✅ Webhook configured
2. ⏳ Start cold email test (3 mailboxes, 10/day)
3. ⏳ Monitor first replies in Modal logs
4. ⏳ Add Google Sheet tracking
5. ⏳ Add auto-send/manual approval logic

---

## Troubleshooting

**Webhook not firing?**
- Check Smartlead webhook is enabled
- Verify URL is exact: `.../webhook/brevo-inbound`
- Test webhook in Smartlead settings

**Classification wrong?**
- Check Modal logs for actual classification
- GPT-4o-mini prompt can be adjusted if needed

**No logs showing?**
```bash
modal app logs reply-triage-webhook
```

Should show recent activity. If empty, webhook not reaching server.

---

**Time to test:** Send your first cold emails and watch the magic happen! 🚀
