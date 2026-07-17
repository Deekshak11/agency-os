# Deployment Checklist - Agency OS Systems

## Pre-Deployment (Dependencies)
- [ ] Install Modal CLI: `pip install modal`
- [ ] Authenticate Modal: `modal setup`
- [ ] Verify environment variables in `.env`
- [ ] Refresh Google OAuth token

## System 1: Reply Triage Deployment
- [ ] Deploy webhook to Modal: `modal deploy scripts/reply_webhook.py`
- [ ] Get Modal webhook URL
- [ ] Configure Brevo inbound webhook with Modal URL
- [ ] Set up DNS MX records for receiving domain
- [ ] Test with mock email

## System 2: Proposal Generator Deployment
- [ ] Deploy Fathom webhook to Modal: `modal deploy scripts/fathom_webhook.py`
- [ ] Get Modal webhook URL
- [ ] Configure Fathom webhook with Modal URL
- [ ] Test with mock call transcript

## Final Integration
- [ ] Test System 1 end-to-end (send email → reply → auto-response)
- [ ] Test System 2 end-to-end (Fathom call → proposal generated)
- [ ] Test System 3 (interested reply → fulfillment → sheet sent)

## Environment Variables Needed

```bash
# OpenRouter (AI)
OPENROUTER_API_KEY=your_key

# Brevo (Email)
BREVO_API_KEY=your_key
SENDER_EMAIL=youremail@yourdomain.com
SENDER_NAME=DK

# Apify (Lead Finding)
APIFY_API_KEY=your_key

# Google Workspace
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
TRACKING_SHEET_ID=your_sheet_id
TRACKING_SHEET_NAME=sheet_name
GOOGLE_TOKEN_B64=base64_encoded_token

# Configuration
AUTO_SEND_INTERESTED=true
AUTO_SEND_QUESTION=false
AUTO_SEND_OBJECTION=false
```

## Current Status
- ✅ All systems built and tested locally
- ⏳ Ready for deployment
