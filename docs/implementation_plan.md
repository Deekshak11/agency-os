# Implementation Plan - n8n Sales Suite (Top Rated)

# Goal Description
Implement the **n8n Sales Suite** focusing exclusively on the "Top Rated" (Highest Hormozi Score) workflow for each of the 6 layers of the sales cycle. This replaces the previous generic "Speed Layer" objective with a targeted, high-value implementation strategy.

**Selected Workflows (The "Top Rated" Chain):**
1.  **Layer 1 (Speed):** `Workflow 2: The Multi-Channel Auto-Concierge` (WhatsApp) - **Score: 10/10**
    *   *Note:* Replaces "Discord Lead Router".
2.  **Layer 2 (Prep):** `Workflow 4: The Deep Dive Dossier` (Firecrawl + OpenAI) - **Score: 10/10**
3.  **Layer 3 (Convert):** `Workflow 8: The Instant Proposal Generator` (G-Docs) - **Score: 9/10** (Highest in layer)
4.  **Layer 4 (Pipe):** `Workflow 10: The Stale Deal Wakinator` (Baserow Monitoring) - **Score: 10/10**
5.  **Layer 5 (Close):** `Workflow 13: The Contract Automator` (DocuSeal) - **Score: 10/10**
6.  **Layer 6 (Follow):** `Workflow 17: The "Ghost" Buster` (Re-engagement) - **Score: 8/10** (Highest in layer)

## User Review Required
> [!IMPORTANT]
> **Priority vs. Rating Conflict**: You asked for "Top Rated" workflows. For Layer 1, **WhatsApp Concierge (10/10)** beats the **Lead Router (9/10)**. However, the Design Doc lists the Lead Router as "Priority 1" because it forces the Baserow setup.
> **Decision**: I have planned for **WhatsApp Concierge**, but this *implicitly requires* we set up the Baserow "Contacts" table first. I will include Baserow setup as a prerequisite.

> [!WARNING]
> **WhatsApp API Costs**: Workflow 2 requires the WhatsApp Business Cloud API (approx $5/mo + conversation fees). Ensure you are okay with this vs. the free Discord router.

> [!CAUTION]
> **Token Status**: The Google Workspace `token.json` restored from archive is **INVALID**. We need to re-authenticate before we can use Google Docs/Drive workflows (Layer 3 & 5).

## Proposed Changes

### Documentation
#### [NEW] [n8n_implementation_spec.md](file:///c:/Users/user/Desktop/Agency_OS/n8n_implementation_spec.md)
- Create a specific technical specification file for these 6 workflows.
- Detailed schemas for the Baserow tables required ("Contacts", "Deals", "Competitors").

### Infrastructure (Baserow)
#### [NEW] Baserow Setup
- We need to deploy/configure Baserow. Since we are in "Planning", the first step is defining the Schema.
- **Table 1: Contacts** (Name, Phone, Email, LinkedIn, Status)
- **Table 2: Deals** (Value, Stage, Proposal URL, Contract Status)

## Verification Plan

### Automated Tests
- **Token Check**: Re-run validation after new authentication.
- **n8n Health Check**: Verify n8n is running (User to confirm URL/Access).

### Manual Verification
- **Baserow Schema**: User to confirm Baserow is accessible and tables are created (once executed).
- **Workflow Load**: Import the specific n8n JSON templates for each of the 6 workflows.
