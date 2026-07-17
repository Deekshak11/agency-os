# Multi-Domain Mailgun Setup SOP

> Repeat for each sender domain to enable sender-matched replies.

## Prerequisites
- Mailgun account (Foundation plan $35/mo)
- DNS access for each domain
- Modal webhook deployed: `https://deekshakdk11--reply-triage-webhook-fastapi-app.modal.run/webhook/mailgun`

---

## Per-Domain Setup (~20 min each)

### Step 1: Add Domain in Mailgun (2 min)
1. Mailgun Dashboard → **Sending** → **Domains**
2. Click **Add New Domain**
3. Enter: `replies.{DOMAIN}.com` (e.g., `replies.aevylabsagency.com`)
4. Region: **US**
5. Click **Add Domain**

### Step 2: Add MX Records (5 min)
In your DNS provider (Hostinger/Namecheap/Cloudflare):

| Type | Host | Value | Priority |
|------|------|-------|----------|
| MX | replies | mxa.mailgun.org | 10 |
| MX | replies | mxb.mailgun.org | 10 |

### Step 3: Add TXT Records (5 min)
Mailgun will show you the exact values. Add:

| Type | Host | Value |
|------|------|-------|
| TXT | replies | `v=spf1 include:mailgun.org ~all` |
| TXT | `{key}._domainkey.replies` | (DKIM key from Mailgun) |

### Step 4: Verify DNS (10 min wait)
In Mailgun → Domain → Click **Verify DNS Settings**
Wait for green checkmarks on MX, SPF, DKIM.

### Step 5: Create Route (2 min)
1. Mailgun → **Sending** → **Routes**
2. Click **Create Route**
3. Configure:
   - **Expression**: `match_recipient(".*@replies.{DOMAIN}.com")`
   - **Action**: Forward → `https://deekshakdk11--reply-triage-webhook-fastapi-app.modal.run/webhook/mailgun`
   - **Priority**: 0
4. Click **Create Route**

---

## Domain Checklist

| Domain | MX | TXT | Route | Tested |
|--------|----|----|-------|--------|
| replies.getaevylabs.com | ✅ | ✅ | ✅ | ✅ |
| replies.aevylabsagency.com | ✅ | ✅ | ✅ | ⏳ |
| replies.aevylabsleads.com | ✅ | ✅ | ✅ | ⏳ |
| replies.aevylabslead.com | ✅ | ✅ | ✅ | ⏳ |
| replies.leadaevylabs.com | ✅ | ✅ | ✅ | ⏳ |
| replies.leadgenaevy.com | ✅ | ✅ | ✅ | ⏳ |

---

## Code Update Required

After adding domains, update `send_test_email.py` to use domain-specific Reply-To:

```python
# Map sender → reply-to domain
REPLY_TO_MAP = {
    "ava@getaevylabs.com": "test@replies.getaevylabs.com",
    "claire@aevylabsagency.com": "test@replies.aevylabsagency.com",
    "olivia@aevylabsleads.com": "test@replies.aevylabsleads.com",
    # ... etc
}
```

---

## Adding New Domains (Future)

When you buy a new domain for cold email:
1. Set up sender email (Google Workspace or similar)
2. Add app password to `credentials/{domain}.txt`
3. Follow this SOP to add `replies.{domain}`
4. Update REPLY_TO_MAP in sending scripts
5. Update SENDER_CREDENTIALS in `fast_fulfillment_modal.py`
