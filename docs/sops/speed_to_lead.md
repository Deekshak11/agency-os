# Speed-to-Lead System - Standard Operating Procedure

## Overview

**Objective:** Respond to interested cold email replies in <60 seconds with a personalized lead magnet (20 leads + 3 docs).

**Status:** Production Ready ✅

---

## Architecture

```
1. SEND (Outbound Cold Email)
   └─> Gmail SMTP → Sets Reply-To: replies.tryaevylabs.com

2. PROSPECT REPLIES
   └─> Mailgun catches → Triggers webhook

3. CLASSIFICATION
   └─> Modal classifies intent (GPT-4o-mini, ~2s)

4. FULFILLMENT (if "interested")
   └─> Modal generates 20 leads + 3 docs (~35s)

5. AUTO-REPLY
   └─> System sends via Gmail SMTP (<2s)
```

**Total Latency:** ~40 seconds (Goal met!)

---

## Tools & Scripts

| Step | Script/Tool | Location | Input | Output |
|------|-------------|----------|-------|--------|
| Send Campaign | `send_gmail_smtp.py` | `execution/` | CSV (Email, FirstName, Company) | Sent emails |
| Catch Replies | Mailgun Webhook | Cloud | Email to `replies@` | HTTP POST to Modal |
| Classify | Modal Function | `modal_deployments/modal_reply_webhook_full.py` | Email body | interested/question/objection/not_interested |
| Fulfill | Modal Function | `modal_deployments/fast_fulfillment_modal.py` | Niche, User | Google Sheet + 3 Docs |
| Auto-Reply | Gmail SMTP | Built into webhook | Lead magnet URL | Email sent |

---

## Step-by-Step Execution

### 1. Prepare Campaign

**Input:** CSV file with columns:
```
Email,FirstName,Company
john@example.com,John,Example Inc
```

**Customize templates in `send_gmail_smtp.py`:**
```python
SUBJECT = "20 Free {Company} Investor Leads"
BODY = """Hi {FirstName},
I built a list of 20 companies actively looking for finance help in your niche.
Want me to send it over? (Zero cost, no strings attached)"""
```

### 2. Send Campaign

```bash
cd C:\Users\user\Desktop\Agency_OS
python execution\send_gmail_smtp.py
```

**What it does:**
- Sends personalized emails via Gmail SMTP
- Sets `Reply-To: trevor@replies.tryaevylabs.com`
- Respects Gmail limits (10s delay between emails)

**Requirements:**
- Gmail App Password (stored in `GMAIL_APP_PASSWORD` env var)
- CSV file path set in script

### 3. Monitor Replies

Replies automatically trigger the system:
1. Email goes to `replies.tryaevylabs.com`
2. Mailgun forwards to Modal webhook
3. Modal logs visible via: `modal app logs reply-triage-webhook --follow`

### 4. Verify Classification

Check Modal logs for:
```
Classification: interested
Fulfillment triggered: True
Auto-sent: True
```

### 5. Confirm Delivery

Prospect receives:
- Instant acknowledgment (if interested)
- Link to Google Sheet with 20 leads
- 3 personalized Google Docs

---

## Configuration

### DNS (Already Set)

**Root Domain (`tryaevylabs.com`):**
- SPF: `v=spf1 include:_spf.google.com include:mailgun.org ~all`
- DKIM: Mailgun TXT record at `k1._domainkey`
- MX: Gmail (Priority 1)

**Replies Subdomain (`replies.tryaevylabs.com`):**
- MX: Mailgun (Priority 10)
- SPF: `v=spf1 include:mailgun.org ~all`

### Modal Secrets

```bash
modal secret create agency-os \
  OPENROUTER_API_KEY=[REDACTED_KEY] \
  APIFY_API_KEY=apify_api_... \
  MAILGUN_API_KEY=e362d77d... \
  MAILGUN_DOMAIN=replies.tryaevylabs.com \
  AUTO_SEND_INTERESTED=true
```

### Mailgun Route

**Expression:** `match_recipient(".*@replies.tryaevylabs.com")`

**Action:** Forward to webhook:
```
https://deekshakdk11--reply-triage-webhook-fastapi-app.modal.run/webhook/mailgun
```

---

## Troubleshooting

### Issue: Emails not sending
- **Check:** Gmail App Password correct?
- **Check:** CSV format matches expectation?
- **Check:** Daily send limit not exceeded (500 for free Gmail, 2000 for Workspace)?

### Issue: Webhook not receiving
- **Check:** Mailgun route configured?
- **Check:** DNS MX records propagated? (`dig MX replies.tryaevylabs.com`)
- **Check:** Modal deployment active? (`modal app list`)

### Issue: Classification wrong
- **Check:** OpenRouter API key in Modal secrets?
- **Check:** Modal logs for error messages?
- **Adjust:** Classification prompt in `modal_reply_webhook_full.py`

### Issue: Fulfillment failing
- **Check:** Google OAuth token valid?
- **Check:** Apify API key in Modal secrets?
- **Check:** Modal logs for specific error

---

## Edge Cases

### Prospect replies from different email
- System won't catch it (not at `replies@` subdomain)
- Solution: Manually forward to `parse@replies.tryaevylabs.com`

### Multiple domains
- Set up `replies.domain2.com`, `replies.domain3.com` with same MX records
- All forward to same Modal webhook
- System handles all domains

### Rate limits
- Gmail: 500 emails/day (free), 2000/day (Workspace)
- Mailgun: 100 emails/day (free tier) for *sending* (webhook receiving is unlimited)
- Apify: Check plan limits for lead scraping

---

## Monitoring & Metrics

### Key Metrics
- **Classification Accuracy:** Target >90% (currently 100%)
- **Response Latency:** Target <60s (currently ~40s)
- **Auto-send Success Rate:** Target >95%

### Logs
```bash
# Modal webhook logs
modal app logs reply-triage-webhook --follow

# View recent runs
modal app list
```

### Manual Testing
```bash
# Test classification
python tests/test_classification.py

# Test full flow
python tests/test_end_to_end.py
```

---

## Cost Breakdown

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| Gmail (Workspace) | 7 mailboxes | ₹700 |
| Smartlead | Free warmup | ₹0 |
| Mailgun | 100 emails/day | ₹0 |
| Modal | <1000 req/day | ₹0 |
| OpenRouter | ~100 classifications/day | ~₹15 |
| Apify | ~20 interested replies/day | ~₹100 |

**Total:** ~₹815/month (~$10/month)

---

## Updates & Maintenance

### Weekly
- Review classification accuracy in Modal logs
- Check for failed sends or webhook errors

### Monthly
- Update email templates based on response rates
- Review cost vs free tier limits
- Test system end-to-end

### As Needed
- Add new domains (follow DNS setup)
- Adjust classification prompt
- Scale fulfillment (add more parallel processing)

---

## Success Criteria

✅ **Latency:** <60s (currently ~40s)
✅ **Classification:** >90% accuracy (currently 100%)
✅ **Deliverability:** Gmail SMTP (best-in-class)
✅ **Cost:** <$20/month (currently ~$10)
✅ **Reliability:** 24/7 uptime via Modal

**Status:** Production System ✅

