# PRD: n8n Sales Suite Implementation

## Overview
Implement the "Top Rated" workflows for the Agency OS n8n Sales Suite. This session focuses on Phases 2 (Database) and 3 (Workflows).

## Task 1: Baserow Scaffolding
**Goal**: Deploy and configure the core Baserow tables required for the suite.
- [ ] **Deploy Baserow**: If not using SaaS, ensure a Baserow instance is running (or use Cloud). *Decision*: Use Baserow.io Free Tier or Self-Hosted? -> Assume **Baserow.io** for speed unless `docker-compose` is found.
- [ ] **Create Database**: Name it "Agency OS".
- [ ] **Create Table 'Contacts'**:
    - Fields: `Name` (Text), `Status` (Single Select: New, Contacted, Qualified, Negotiation, Closed-Won, Lost, Ghosted), `Email` (Email), `Phone` (Phone Number), `LinkedIn` (URL), `Company` (Link to 'Companies'), `Last Contact` (Date), `Lead Score` (Number), `Notes` (Long Text).
- [ ] **Create Table 'Deals'**:
    - Fields: `Name` (Text), `Contact` (Link to 'Contacts'), `Stage` (Single Select: Discovery, Proposal, Contract Sent, Closed-Won, Closed-Lost), `Value` (Number), `Proposal URL` (URL), `Contract Status` (Single Select: Draft, Sent, Signed, Paid).
- [ ] **Create Table 'Competitors'**:
    - Fields: `Name` (Text), `URL` (URL), `Last Scrape Hash` (Text).
- [ ] **Create API Token**: Generate a Database Token with Create/Read/Update/Delete permissions. Save it to `secrets.json` (or Modal Volume).

## Task 2: Workflow 2 - WhatsApp Concierge (Speed Layer)
**Goal**: Implement the "Multi-Channel Auto-Concierge" using WhatsApp Cloud API.
**Ref**: `n8n Sales Suite Design.md` (Workflow 2).
- [ ] **n8n Setup**: Ensure n8n is active.
- [ ] **Create Credential**: Add `Baserow API` credential in n8n.
- [ ] **Create Credential**: Add `OpenAI API` credential in n8n.
- [ ] **Create Credential**: Add `WhatsApp Cloud API` credential in n8n.
- [ ] **Build Workflow**:
    1.  **Trigger**: `Webhook` (POST /chat/incoming).
    2.  **Lookup**: `Baserow` Node -> Get Row in 'Contacts' where `Phone` equals input.
    3.  **Router**: `If` Node (Found? Yes/No).
    4.  **Branch Yes (Client)**: Pass to `Slack` or ignore (for now).
    5.  **Branch No (Lead)**:
        -   `OpenAI` Node: "Classify Intent: Service_Inquiry vs Other".
        -   `Switch` Node: Based on Intent.
        -   `WhatsApp` Node: Send Template "intro_v1" (Needs Meta Approval) OR Send Freeform if within 24h window (Test Mode).
- [ ] **Test**: Send a mock payload to the Webhook and verify a new row/message log.

## Task 3: Workflow 4 - Deep Dive Dossier
Implement the research agent using Firecrawl.
- Create new n8n Workflow "Deep Dive Dossier".
- Add Webhook/Button Trigger (from Baserow).
- Add Firecrawl Node (Scrape URL as Markdown).
- Add OpenAI Node (Analyze Strategy/Pain Points).
- Add Google Docs Node (Append to Template).
- Add Slack/Discord Node (Notify User).

## Task 4: Workflow 10 - Stale Deal Wakinator
Implement the stale deal monitor.
- Create new n8n Workflow "Stale Deal Wakinator".
- Add Schedule Trigger (Weekly).
- Add Baserow Node (Filter: Stage=Negotiation AND Last_Contact > 7 days).
- Add Discord/Slack Node (Send Alert List).
