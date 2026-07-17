# Testing Plan - Mock Data (No Webhooks Needed)

## What We'll Test

### System 1: Reply Triage
**Test:** Send mock Brevo inbound email payload directly to webhook  
**Endpoint:** `https://deekshakdk11--reply-triage-webhook-fastapi-wrapper.modal.run/webhook/brevo-inbound`  
**Mock scenarios:**
1. "Interested" reply → Should trigger fulfillment + auto-response
2. "Question" reply → Should draft response + queue for review
3. "Objection" reply → Should draft objection handler
4. "Not interested" reply → Should auto-unsubscribe

### System 2: Proposal Generator
**Test:** Send mock Fathom transcript payload to webhook  
**Endpoint:** `https://deekshakdk11--fathom-proposal-webhook-fastapi-wrapper.modal.run/webhook/fathom`  
**Mock scenario:**
- Fathom call transcript → Should generate proposal doc

---

## Test 1: Interested Reply (System 1 + System 3)

### Mock Payload
```json
{
  "items": [{
    "Message-ID": "test-12345",
    "From": "test@client.com",
    "To": "dk@yourreply.com",
    "Subject": "Re: Outreach",
    "Body": "Yes, this looks interesting. Can you send over some examples of companies you've helped?",
    "spam": {"Score": 0.1}
  }]
}
```

### Expected Result
✅ Classified as "interested"  
✅ Triggers lead magnet generation (20 ICPs)  
✅ Creates Google Sheet  
✅ Sends auto-response with sheet link (if AUTO_SEND_INTERESTED=true)  
✅ Updates tracking sheet

---

## Test 2: Question Reply (System 1)

### Mock Payload
```json
{
  "items": [{
    "Message-ID": "test-67890",
    "From": "prospect@company.com",
    "To": "dk@yourreply.com",
    "Subject": "Re: Partnership opportunity",
    "Body": "What's your pricing model and how long does onboarding take?",
    "spam": {"Score": 0.2}
  }]
}
```

### Expected Result
✅ Classified as "question"  
✅ Drafts contextual response  
✅ Queues for manual review (AUTO_SEND_QUESTION=false)  
✅ Updates tracking sheet with draft

---

## Test 3: Proposal Generation (System 2)

### Mock Payload
```json
{
  "event": "ai_summary_completed",
  "call": {
    "id": "test-call-123",
    "title": "Discovery Call - Adrian",
    "transcript": "Adrian: We're a SaaS company doing $5M ARR. Main problem is we're spending too much on ads and not getting quality leads. We need 10-15 qualified meetings per month with enterprise clients. Current team is stretched thin with SDRs doing manual prospecting. Looking for someone to build an outbound system that actually works.",
    "participants": ["Adrian", "DK"],
    "duration": 1800
  }
}
```

### Expected Result
✅ Extracts client data (name, company, problems, goals)  
✅ Generates proposal content  
✅ Creates Google Doc proposal  
✅ Returns doc URL

---

## How to Run Tests

I'll create Python scripts to send these payloads and verify responses.

**After tests pass:** Tomorrow when you upgrade Brevo, just configure the webhook URL and it'll work automatically!
