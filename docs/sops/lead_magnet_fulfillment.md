# Directive: Lead Magnet Fulfillment Engine

## Goal
When a lead replies, automatically generate a Google Sheet with 20 ICP leads + 3 lead magnet Google Docs as proof of value.

## Inputs
- **Trigger**: Lead status changed to "replied" or "generate LM" in tracking sheet
- **Lead Data**: Name, Company, Industry (from initial research)

## Tools / APIs
- **Apify API**: Find 20 ICP leads using "code_crafter/leads-finder"
- **OpenRouter (GPT-4o mini)**: Generate personalized connection messages + lead magnet content
- **Google Docs API**: Create 3 lead magnet documents
- **Google Sheets API**: Create deliverable sheet with 20 leads

## Process Flow
1. **Detect Trigger**: Monitor tracking sheet for "replied" status
2. **Extract Lead Info**: Get lead's industry/niche from initial research
3. **Find 20 ICPs**: 
   - Call Apify with industry, job title, company size (1-10)
   - Get: Name, Email, Company, Personal LinkedIn, Company LinkedIn
4. **Generate Content**:
   - For each of 20 leads: Create personalized connection message (GPT-4o mini)
   - For first 3 leads: Create lead magnet Google Doc (industry-specific template)
5. **Create Deliverable**:
   - Create Google Sheet with columns: Name, Email, Company, Personal LinkedIn, Company LinkedIn, Connection Message, Lead Magnet
   - First 3 rows: Link to Google Doc
   - Remaining 17 rows: "Ready to generate"
6. **Upload to Drive**: Save to shared Google Drive folder

## Lead Magnet Templates
See `context/lead_magnet_templates.md` for industry-specific templates.

## Budget Constraints
- Reuse existing research data (no new Perplexity calls)
- Only 3 lead magnets per fulfillment (GPT-4o mini)
- Total budget: $12 for 350 leads outreach campaign

## Output
- Google Sheet URL (view-only for recipient)
- 3 Google Doc URLs (embedded in sheet)
