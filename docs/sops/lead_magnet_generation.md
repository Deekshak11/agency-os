# Directive: Lead Magnet Generation

## Goal
Generate a high-value "Investor Readiness" or "Financial Gap Analysis" report (Google Doc) for a specific lead, referenced in the cold email.

## Inputs
- **Lead Data**: Name, Company, Industry, Niche.
- **Context**: The specific "Gap" identified in the email (e.g., "Cash Flow Blind Spots", "Investor Readiness").

## Output
- **Google Doc**: Professional, formatted (Brennan Style), containing 3 specific insights.
- **Formatting**:
    -   Title: H1, Arial 18pt
    -   Headings: H2, Arial 14pt (Orange/Bold if Brennan style, otherwise standard)
    -   Body: Arial 10pt
    -   **Bolding**: Use specific bolding for emphasis (e.g., **20 startups**).

## Templates by Industry
(Source: Hormozi Framework - Solve ONE narrow painful problem)

### 1. Fractional CFOs (General SMB)
**Lead Magnet**: "Cash Flow Blind Spots Report"
- **Reports**: Hidden Cost Analysis, Revenue Timing Gaps, Profit Margin Breakdown.

### 2. Wedding/Event Businesses
**Lead Magnet**: "Recession-Proof Pricing Audit"
- **Reports**: Pricing vs. Market, Fixed Cost Vulnerability, Cash Reserve Recommendations.

### 3. Retail Businesses
**Lead Magnet**: "Inventory Cash Trap Analysis"
- **Reports**: Inventory Turnover, Dead Stock, Cash Liberation Plan.

### 4. Healthcare/Biotech
**Lead Magnet**: "Burn Rate Survival Report"
- **Reports**: Monthly Burn Rate, Runway Extension, Investor-Ready Metrics.

### 5. E-commerce/DTC
**Lead Magnet**: "Unit Economics Reality Check"
- **Reports**: True COGS, CAC Breakdown, LTV Optimization.

### 6. Growth-Stage/Tech Startups
**Lead Magnet**: "Investor Readiness Gap Analysis"
- **Reports**: Financial Metrics Scorecard, Unit Economics Health, Fundraising Narrative Gaps.

### 7. Nonprofits
**Lead Magnet**: "Grant Compliance Risk Report"
- **Reports**: Reporting Gaps, Audit Readiness, Compliance Fixes.

### 8. Real Estate/Property Management
**Lead Magnet**: "Property Portfolio Profit Leak Finder"
- **Reports**: Per-Property Profitability, Efficiency Gaps, Cash Flow Optimization.

### 9. Professional Services
**Lead Magnet**: "Billable Hour Profit Maximizer"
- **Reports**: True Hourly Rate, Unbillable Time Audit, Pricing Structure.

### 10. Manufacturing/Industrial
**Lead Magnet**: "Production Cost Breakdown Report"
- **Reports**: Direct vs Indirect Costs, Overhead Burden, Pricing Floor.

## Constraints & Rules
- **Formatting**: Must use Google Docs API `batchUpdate` for true formatting (not just markdown text).
- **Tone**: Professional, authoritative. No "cheerleading".
- **Reuse**: Check if Doc already exists for the company before creating a new one (File Reusability).
