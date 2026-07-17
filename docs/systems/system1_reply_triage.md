# System 1: Reply Triage - Quick Start

## What You Have

A complete **automated reply handling system** that:
1. Receives email replies via Brevo webhook
2. Classifies intent with AI (interested/question/objection/reject)
3. Drafts contextual responses
4. Auto-fulfills lead magnet for "interested" replies
5. Updates Google Sheets tracking
6. Auto-sends or queues for review

## Files Created

### Core Components
- `scripts/reply_webhook.py` - FastAPI webhook receiver
- `scripts/classify_reply.py` - AI reply classifier (4 categories)
- `scripts/draft_response.py` - Response drafter with Nick Saraev style
- `scripts/update_tracking_sheet.py` - Google Sheets integration
- `scripts/handle_reply.py` - Main orchestration pipeline
- `scripts/send_brevo_reply.py` - Brevo email sender
- `scripts/test_reply_triage.py` - Test suite

### Documentation
- `docs/brevo_webhook_setup.md` - Complete setup guide
- `directives/reply_triage.md` - System directive/SOP

## Deployment Steps (30 mins + DNS wait)

### 1. Install Dependencies (2 mins)
```bash
cd C:\Users\user\Desktop\Agency_OS
pip install fastapi uvicorn modal python-dotenv
```

### 2. Set Up Environment Variables (3 mins)

Add to `.env`:
```bash
# Brevo
BREVO_API_KEY=your_brevo_api_key
SENDER_EMAIL=youremail@yourdomain.com
SENDER_NAME=DK

# OpenRouter (Already set)
OPENROUTER_API_KEY=existing_key

# Google Sheets (Already set)
TRACKING_SHEET_ID=19M8Inwgbgb8qVbirt6hoEjr5YQ_Xb6WG-Co1DwdWUzA
TRACKING_SHEET_NAME=Copy of 350 B2 (apollo)

# Auto-send config
AUTO_SEND_INTERESTED=true
AUTO_SEND_QUESTION=false
AUTO_SEND_OBJECTION=false
```

### 3. Configure DNS for Receiving Domain (5 mins + 2-4hr wait)

**Add MX records for `reply.yourdomain.com`:**
- MX Priority 10: `inbound1.sendinblue.com`
- MX Priority 20: `inbound2.sendinblue.com`

Check propagation: https://dnschecker.org/

### 4. Deploy to Modal (5 mins)
```bash
# Authenticate
modal setup

# Deploy webhook
cd scripts
modal deploy reply_webhook.py
```

Copy the webhook URL (e.g., `https://yourapp--reply-webhook.modal.run`)

### 5. Create Brevo Inbound Webhook (5 mins)

In Brevo dashboard:
1. Go to **Integrations → Webhooks**
2. Add new **Inbound** webhook
3. URL: `https://yourapp--reply-webhook.modal.run/webhook/brevo-inbound`
4. Event: `inboundEmailProcessed`
5. Save

### 6. Test the System (10 mins)

```bash
# Run test suite
python scripts/test_reply_triage.py
```

**Send test email:**
- To: `test@reply.yourdomain.com`
- Subject: "Re: Test"
- Body: "Yes, send it over!"

**Check Modal logs:**
```bash
modal app logs yourapp
```

**Expected:** Reply classified as "interested", fulfillment triggered, response sent.

## What Happens When Someone Replies

### "Interested" (e.g., "Yes, send it over!")
1. ✅ AI classifies as "interested"
2. 🔄 Triggers fulfillment:
   - Finds 20 ICP leads via Apify
   - Creates 3 lead magnet docs
   - Builds Google Sheet
3. 📧 Auto-sends email with sheet URL
4. 📊 Updates tracking sheet

### "Question" (e.g., "How does this work?")
1. ✅ AI classifies as "question"
2. 🤖 Drafts contextual answer
3. 📋 Queues for your review (`reply_review_queue.json`)
4. 📊 Updates tracking sheet

### "Objection" (e.g., "Already have a system")
1. ✅ AI classifies as "objection"
2. 🤖 Drafts graceful acknowledgment
3. 📋 Queues for your review
4. 📊 Updates tracking sheet

### "Not Interested" (e.g., "Unsubscribe")
1. ✅ AI classifies as "not_interested"
2. 📧 Auto-sends polite unsubscribe confirmation
3. 📊 Updates tracking sheet

## Monitoring & Optimization

### Check Review Queue
```bash
cat reply_review_queue.json
```

Review and manually send responses for questions/objections.

### Monitor Classification Accuracy
```bash
# Run classifier tests
python execution/test_reply_triage.py
```

Target: 90%+ accuracy

### Adjust Auto-Send Settings

Once confident in quality:
```bash
# In .env
AUTO_SEND_QUESTION=true  # Enable auto-send for questions
```

## Troubleshooting

See `docs/brevo_webhook_setup.md` for detailed troubleshooting steps.

**Quick checks:**
1. Modal logs: `modal app logs yourapp`
2. Brevo webhook logs: Brevo dashboard → Webhooks
3. Test individual components:
   ```bash
   python execution/classify_reply.py
   python execution/draft_response.py
   ```

## Next: Launch Outreach

Once the system is live and tested:

1. **Send your 350 emails via Brevo**
2. **Sit back and let automation handle replies**
3. **Review queue periodically for manual responses**
4. **Watch Google Sheets fill with "INTERESTED" statuses**

**Time saved:** 6+ hours/day of manual reply triage eliminated.

---

**System Status:** ✅ Built & Ready for Deployment

**Estimated setup time:** 30 mins + 2-4hr DNS propagation wait
