# Directive: Reply Triage & Auto-Drafter

## Goal
Automatically process incoming email replies from cold outreach campaigns. Classify intent, draft appropriate responses, update tracking, and optionally auto-send or queue for review.

## Inputs
- **Trigger**: Brevo inbound email webhook (POST to `/webhook/brevo-inbound`)
- **Webhook Payload**: JSON with email data (from, to, subject, body, message-ID)

## Tools / APIs
- **Webhook Receiver**: FastAPI (deployed on Modal)
- **AI Classification**: OpenRouter (GPT-4o-mini) for intent classification
- **Response Drafting**: OpenRouter (GPT-4o-mini) for contextual responses
- **Tracking**: Google Sheets API (update reply status)
- **Sending**: Brevo Transactional Email API
- **Fulfillment**: Existing `generate_lm_fast.py` script (for interested replies)

## Process Flow

### 1. Webhook Reception
- Brevo sends POST request to Modal endpoint when inbound email is received
- Webhook receiver validates payload structure
- Checks spam score (skip if > 5.0)
- Extracts: sender email, subject, body

### 2. Lead Lookup
- Query Google Sheets tracking sheet by email address
- Retrieve lead name, company, industry
- Fallback to generic greeting if not found

### 3. Classification
- AI classifies reply into 4 categories:
  - **interested**: "Yes send it over", "I'd love to see"
  - **question**: "How does this work?", "What's the catch?"
  - **objection**: "Already have a system", "Too busy"
  - **not_interested**: "Unsubscribe", "Not interested"

### 4. Response Drafting
- **Interested**: Send promised asset immediately (trigger fulfillment)
- **Question**: AI generates answer + restates value + CTA
- **Objection**: AI acknowledges gracefully, leaves door open
- **Not Interested**: Confirm unsubscribe, polite goodbye

**Style Guidelines (Nick Saraev):**
- Short sentences (3rd grade reading level)
- Conversational tone ("Hey [name]")
- No corporate jargon
- Max 100 words
- Sign off: "Cheers, DK"

### 5. Fulfillment (Interested Only)
- Call `trigger_fulfillment(lead_info)`
- Generates 20 ICP leads via Apify
- Creates 3 lead magnet Google Docs
- Builds Google Sheet deliverable
- Returns sheet URL

### 6. Auto-Send Logic
- **Interested**: Auto-send with deliverable URL (default: ON)
- **Question**: Queue for review (default: OFF)
- **Objection**: Queue for review (default: OFF)
- **Not Interested**: Auto-send unsubscribe confirmation (always ON)

### 7. Tracking Update
Update Google Sheets with:
- Reply Status: INTERESTED / QUESTION / OBJECTION / NOT_INTERESTED
- Reply Date: UTC timestamp
- Reply Snippet: First 200 chars
- Auto-Response Sent: Yes/No
- Fulfillment Triggered: Yes/No (for interested)

## Error Handling

### API Failures
- Classification error → Default to "question" (safest)
- Response drafting error → Use fallback template
- Send error → Queue for manual send

### Fulfillment Failures
- Apify timeout → Retry once, then notify user
- Google API error → Log error, send apologetic response, queue for manual fulfillment

### Rate Limiting
- OpenRouter: Implement exponential backoff
- Brevo: Respect API rate limits (check Brevo plan)
- Google: Use batch updates where possible

## Configuration

### Environment Variables
```
BREVO_API_KEY=your_key
BREVO_WEBHOOK_SECRET=optional_secret
SENDER_EMAIL=youremail@yourdomain.com
SENDER_NAME=DK
OPENROUTER_API_KEY=your_key
TRACKING_SHEET_ID=sheet_id
TRACKING_SHEET_NAME=Sheet1
GOOGLE_TOKEN_B64=base64_token
AUTO_SEND_INTERESTED=true
AUTO_SEND_QUESTION=false
AUTO_SEND_OBJECTION=false
```

### Deployment
- Platform: Modal (serverless, auto-scaling)
- Endpoint: `https://yourapp.modal.run/webhook/brevo-inbound`
- Authentication: Optional Brevo webhook signature validation

## Output

### Immediate Actions
- Auto-sent email (for interested/not_interested)
- Queued response (for question/objection)
- Updated tracking sheet

### Deliverables (Interested Replies)
- Google Sheet with 20 ICP leads
- 3 Google Doc lead magnets (for first 3 leads)
- Automated email with sheet URL

### Logs
- Modal logs: Classification, actions taken, errors
- Review queue: `reply_review_queue.json` (for manual review)

## Success Metrics
- **Velocity**: Reply processed in < 60 seconds
- **Accuracy**: Classification accuracy > 90%
- **Auto-send rate**: 80%+ for interested (remainder are edge cases)
- **Fulfillment uptime**: 95%+ success rate

## Next Steps
1. Deploy to Modal
2. Configure Brevo inbound webhook
3. Set DNS MX records (2-4hr wait for propagation)
4. Test with dummy emails
5. Monitor first 10 real replies for accuracy
6. Adjust auto-send settings based on quality
