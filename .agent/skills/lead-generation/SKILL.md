---
name: Lead Generation
description: Scrape, validate, and prepare leads for outreach campaigns using Apify and Google Sheets
---

# Lead Generation Skill (V7 High-Fidelity)

## When to Use
- User asks to scrape leads from a niche
- User asks to prepare leads for Instantly campaign
- User asks to generate **fCFO Verified Assets** (Lead Magnets)

## Procedure

### 1. Scrape & Validate
1. Use Apify or Apollo for raw data.
2. Validate emails (Never Google).
3. **Verify Data**: Check `verificationStatus` (must be `valid`) and `catchAllStatus` (must be empty).

### 2. Generate Assets (V7 Standard)
**Critical**: We DO NOT generate content from scratch. We **CLONE** verified masters.

1. **Standard**: "Chinedu Standard" (Intro A1)
   - Exact Bolding: "HATE", "~10 Qualified Meetings", "AI Client Acquisition Engine".
   - Links: Clickable "To Chat" / "To Call".
   - Signature: "DK".
   - **Script**: `scripts/verified_asset_generator.py` (Handles this logic).

2. **GDoc Personalization**:
   - Source: **V2 "Runway Analysis" Masters** (Stainless, Dialogue, etc.).
   - Rule: Subtitle MUST match "By {First Name}" (e.g. "By Alex").
   - **NEVER** use generic "By Michelle" or "By Sarah" in production.

3. **Execution**:
   - **Tool**: `scripts/modal_verified_runner_turbo.py`
   - **Mode**: High-Concurrency (50 workers / 11 accounts).
   - **Output**: `data/verified_assets_turbo_v2.csv` (High-Fidelity).

### 3. Observability (Glass Box)
**Requirement**: All lead processing must be visible.
1. **Telemetry**: Use `scripts/glassbox_core.py` to log `START`, `PROGRESS`, and `SUCCESS` for every lead.
2. **Monitoring**: Run `modal run scripts/glass_box_monitor.py` during batch runs to track real-time sentiment and failure rates.

### 4. Campaign Prep
1. Export the verified CSV using `scripts/export_instantly.py`.
2. Import to Instantly.

## Key Resources
- **Verified Runner**: `scripts/modal_verified_runner_turbo.py`
- **Core Generator**: `scripts/verified_asset_generator.py`
- **Telemetry Core**: `scripts/glassbox_core.py`
- **Live Monitor**: `scripts/glass_box_monitor.py`

## Anti-Patterns
- **No V6/V5**: Do not use `v6_asset_rectifier.py` or `batch_generate_assets.py` for fCFOs.
- **No Fallbacks**: Do not fallback to generic "Sarah" templates on 429 errors. **Fail fast and retry.**
- **No Generics**: Every asset must address the lead by name in the A1 Intro and GDoc Subtitle.
