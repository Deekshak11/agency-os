---
name: Asset Cloning
description: Clone and personalize Google Sheets/Docs from verified Golden templates for leads
---

# Asset Cloning Skill

## When to Use
- User asks to create personalized lead magnets
- User mentions "Golden 10" or "clone assets"
- User needs to scale asset generation

## Core Principle
**Clone Verified Assets Only.** Never generate from scratch or use unverified templates.

## 🏆 The "Golden Source" (Verified)
Use **Carey's Sheet** as the master template. It is the ONLY one with correct data (Row 8 = Push Security).

- **Sheet ID**: `1V8JcKhV3QX-FQI32UVh8xylCEZxvMgrvhip2BeD68i4`
- **Placeholder Name**: `Carey`
- **Correct 5 Companies**:
  1. StartEngine
  2. HerculesAI
  3. Swanky
  4. Secure Data Tech
  5. **Push Security** (Row 8)

## 🎨 Golden Sheet Spec (V6 Standard)

| Element | Value | Notes |
|---------|-------|-------|
| Row 1 Height | **275px** | Reveal DK signature |
| Row 2 Height | **10px** | Buffer row |
| Column F Width | **400px** | Msg column |
| Column G Width | **400px** | Lead Magnet column |
| Tab Name | `{Name}'s 5 Specific Leads` | Personalization |

## ✍️ Content Replacements (Mandatory)

Run these Find/Replace operations on **both** Sheets and GDocs:

| Target | Replacement | Context |
|--------|-------------|---------|
| `Carey` | `{Lead Name}` | Primary personalization |
| `SaaS` | `B2B tech companies` | V6 Spec (Case-sensitive) |
| `saas` | `B2B tech companies` | V6 Spec (Case-sensitive) |
| `No Bounds` | `Solartech` | Fix potential contamination |

## Procedure
1. **Clone** the verified sheet (`1V8JcKhV3QX...`) to the target folder.
2. **Personalize Sheet**: Replace "Carey" → `{Lead Name}`.
3. **Personalize GDocs**:
   - Read GDoc URLs from Column G (Rows 4-8).
   - For each GDoc:
     - Extract ID.
     - Run batch updates for ALL replacements above (`Carey`, `SaaS`, etc.).
4. **Verify**: Check Row 8 matches "Push Security".

## Key Resources
- **Verified Template**: [Carey's Sheet](https://docs.google.com/spreadsheets/d/1V8JcKhV3QX-FQI32UVh8xylCEZxvMgrvhip2BeD68i4)
- **Primary Script**: `scripts/verified_asset_generator.py` (Core Logic) & `scripts/modal_verified_runner.py` (Production)
- **Verification Script**: `scripts/verify_golden_data.py`

## 🚫 Anti-Patterns
- **Do NOT** use the "True Master" (`1NJFeZq...`) - it has outdated "No Bounds" data.
- **Do NOT** generate GDocs from scratch - they lose the verified formatting.
- **Do NOT** skip GDoc personalization - linking to "Carey's" docs is confusing for leads.
- **Do NOT** guess ids - use the ID listed in this SKILL file.
- **Do NOT** Exceed Concurrency 3 for GDoc Ops: Google Docs API Write Limit is ~60/min. Parallel writes > 3 will trigger 429 errors.
- **Do NOT** Use Silent Fallbacks: If personalization fails, FAIL THE PROCESS. Never return a Master URL.

### 6. Verified Golden Set Replication (SOP - V7/V4)
When asked to "replicate the verified set" or "show a demo" or "fCFO Demo v7":

1.  **Source Data**: One Source of Truth -> `templates/verified_golden_leads.json`.
2.  **Template (Master Sheet)**: `1wpnpNJM1YK9xyrvJPgDmNWxSi8b4DnGcj5SV7TagXs8` ("Joe's Sheet").
3.  **V4 Intro Text (The "We Found You" Standard)**:
    *   **Text**: "It contains - **5 Specific Leads** we found you + **Personalized Email**..."
    *   **Formatting**: Uses **UTF-16 Indexing** for correct bold/link placement. (Python `len()` counts bytes, Google API counts UTF-16 units. Must use helper `s.encode('utf-16-le') // 2`).
    *   **Links**: "To Chat" / "To Call" links must be clickable and styled blue/underlined.
4.  **GDoc Personalization**:
    *   Clone 5 Master GDocs per lead.
    *   Find/Replace "Michelle" -> `{Lead First Name}`.
5.  **Execution**: Use `scripts/verified_asset_generator.py` (Central Logic).

### 7. Production Scaling & Rate Limits (Safe Mode)
To scale beyond 10 leads/min without `429 Too Many Requests`:

1.  **The Bottleneck**: Google Sheets API Quota is **60 Write Requests / min / User**.
    *   1 Asset = ~15 Write Ops.
    *   Max Throughput per Token = 4 Assets/min.
2.  **Token Rotation (CRITICAL)**:
    *   Mount `tokens/` folder with multiple `token_*.json` files relative to project root.
    *   Script must randomly select a token for *each* lead execution.
3.  **Concurrency Math**:
    *   **With Rotation (20+ tokens)**: Safe Concurrency = **30** (approx 450 writes/min total).
    *   **Without Rotation (1 token)**: Safe Concurrency = **3** (approx 45 writes/min).
4.  **Retry Strategy**:
    *   Implement **Exponential Backoff** with **Jitter**.
    *   Multiplier: `5x` (Wait 5s, 10s, 20s...).
    *   Never assume success; verify output in CSV.
