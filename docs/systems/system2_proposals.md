# System 2: Proposal Generator - Quick Start

## What You Have (80% Complete)

A **semi-automated proposal generation system** that:
1. Receives Fathom webhook when discovery call ends
2. Extracts client data from transcript using AI
3. Generates customized proposal content
4. Creates professional Google Doc
5. Notifies you for review
6. (TODO) Sends via email with approval

---

## Files Created

### Core Components
- `scripts/parse_transcript.py` - AI transcript parser (extracts client info, problems, goals)
- `scripts/generate_proposal_content.py` - AI proposal writer (customized for each client)
- `scripts/create_proposal_doc.py` - Google Doc creator (professional formatting)
- `scripts/generate_proposal.py` - Main orchestration script
- `scripts/fathom_webhook.py` - Fathom webhook receiver (auto-trigger)

---

## Setup (15 mins)

### 1. Configure Fathom Webhook (5 mins)

**In Fathom:**
1. Go to Settings → Integrations → Webhooks
2. Click "Add Webhook"
3. **URL:** `https://yourapp.modal.run/webhook/fathom` (after Modal deployment)
4. **Trigger:** "New AI Summary"
5. Save

### 2. Refresh Google OAuth Token (2 mins)

Your token expired. Refresh it:

```bash
cd C:\Users\user\Desktop\Agency_OS
python -c "from google_auth_oauthlib.flow import InstalledAppFlow; flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']); creds = flow.run_local_server(port=8080); open('token.json', 'w').write(creds.to_json())"
```

This will open browser → Sign in → Approve → Done

### 3. Test Locally (5 mins)

**Run full pipeline with Adrian transcript:**

```bash
python scripts\generate_proposal.py "Biz Project\adrian.txt"
```

**Expected output:**
- ✅ Extracted client data
- ✅ Generated proposal content
- ✅ Created Google Doc
- 🔗 Google Doc URL

### 4. Deploy to Modal (5 mins)

```bash
modal setup  # If not done already
modal deploy scripts/fathom_webhook.py
```

Copy the webhook URL and add to Fathom settings.

---

## How It Works

### Automatic Flow (With Fathom Webhook)

```
Discovery Call Ends
         ↓
Fathom processes transcript
         ↓
Webhook fires → Your Modal endpoint
         ↓
System extracts client data (AI)
         ↓
System generates proposal (AI)
         ↓
System creates Google Doc
         ↓
Email notification: "Proposal ready for [Client]"
         ↓
YOU: Review doc (30 secs)
         ↓
YOU: Record 2-min Loom video
         ↓
YOU: Click "Approve + Send"
         ↓
System emails proposal + video
```

### Manual Flow (Without Webhook)

If you prefer manual control:

```bash
python scripts\generate_proposal.py "path\to\transcript.txt"
```

---

## Current Output Structure

### Google Doc Sections:
1. **Header** - Client company x Agency OS
2. **Client Info** - Name, date, investment
3. **The Problem** - Extracted from call (bullet points)
4. **The Solution** - AI-generated for their niche
5. **Deliverables** - Month 1 vs Month 2-3 breakdown
6. **Timeline** - Week-by-week plan
7. **The Guarantee** - 10-20 meetings or FREE
8. **Investment** - $1,700/mo x 3 months
9. **Next Steps** - Clear action items
10. **Signature** - Cheers, DK

---

## What's Left (20% - Dec 11 Integration)

### When System 1 (Reply Triage) is live:

**Add to System 2:**
1. Email notification integration (reuse Brevo from System 1)
2. "Approve + Send" button workflow
3. Contract generation (optional - using template)

**For now:** You manually send proposals after reviewing Google Doc.

---

## Testing

### Test with existing transcripts:

```bash
# Adrian (casual call - Tech Consulting)
python scripts\generate_proposal.py "Biz Project\adrian.txt"
python scripts\generate_proposal.py "Biz Project\your_call.txt"
```

---

## Customization

### Change Pricing:

Edit `scripts/generate_proposal_content.py`:

```python
PRICING_MODEL = {
    "monthly_retainer": 1700,  # Change this
    "commitment_months": 3,     # Change this
    "guarantee": "Your custom guarantee text"
}
```

### Change Google Doc Styling:

Edit `scripts/create_proposal_doc.py`:

```python
# Brand colors
BRAND_PRIMARY = {"red": 0.2, "green": 0.4, "blue": 0.8}  # Blue
BRAND_ACCENT = {"red": 0.0, "green": 0.7, "blue": 0.4}   # Green
```

---

## Troubleshooting

### "Google auth error"
→ Run token refresh command (Step 2 above)

### "OpenRouter API error"
→ Check `OPENROUTER_API_KEY` in `.env`

### "Fathom webhook not firing"
→ Check webhook URL in Fathom settings
→ Check Modal logs: `modal app logs yourapp`

### "Proposal content looks off"
→ Adjust AI prompts in `generate_proposal_content.py`
→ Add more examples to system prompt

---

## Next Steps

1. ✅ **Refresh Google token** (run command above)
2. ✅ **Test locally** with Adrian transcript
3. ⏳ **Deploy to Modal** (when ready for live calls)
4. ⏳ **Connect Fathom webhook** (after Modal deployment)
5. ⏳ **Do discovery call** → Watch automation work!

---

## System Status

**✅ Built & 80% Functional**

**Remaining 20%:** Email sending (integrate with System 1 Brevo setup on Dec 11)

**Time saved:** 30-60 mins per proposal (was manual, now 2 mins + your 30-sec review)
