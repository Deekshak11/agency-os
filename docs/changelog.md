# Changelog

## [2.0.0] - 2025-12-07

### Added
- **Modal Cloud Integration**: Migrated Fulfillment Engine to Modal (`execution/modal_webhook.py`).
    - **Endpoint**: `https://deekshakdk11--cfo-agency-fulfillment-trigger-lm-generation.modal.run`
    - **Schedule**: Cron trigger (Every 15 mins) checks for new leads.
    - **Cloud Secrets**: `openrouter-api-key`, `apify-api-key`, `google-token`.
- **Dynamic Logic**: Implemented intelligent Lead Magnet selection based on "Niche Defined" or "Industry" column.
- **Personalized Sign-off**: Sheet Pitch now signs off as "Cheers, DK" (Agency Owner) instead of the lead's name.
- **Document Subtitles**: Added "By {User Name}" to generated PDF content.
- **Idempotency**: Added logic to skip rows that already have a Lead Magnet link.

### Changed
- **Casual Tone**: Automatically maps "Small Business" -> "SMBs" in pitch text.
- **Title De-duplication**: Logic to remove redundant H1 titles in generated docs.
- **Env Auth**: Updated `generate_lm_fast.py` to support `GOOGLE_TOKEN_JSON` env var for cloud execution.

### Fixed
- **NameError**: Resolved issue with function ordering in `generate_lm_fast.py`.
- **Duplicate Titles**: Validated title presence in generated content.

## [1.0.0] - 2025-11-27

### Added
- **Local Caching**: Added `apify_leads.json` support to `generate_lm_fast.py` to save Apify credits on re-runs.
- **Hyperlink Formulas**: Implemented `=HYPERLINK()` for all sheet columns to guarantee clickability.
- **Doc Formatting Parser**: Added support for bold (`**`) and headers (`#`) in Google Doc generation.
- **Deep Analysis Generation**: Upgraded `generate_lm_fast.py` to generate specific "3-gap" analysis emails based on Apify company descriptions.
- **Rich Text Formatting**: Implemented bold text parsing for Google Sheets pitch area.
- **Data Masking**: Added logic to mask contact info ("Available upon request") for leads 4-20.

### Changed
- **Sender Logic**: Updated script to use the actual lead's name (e.g., "Trevor") as the sender in all communications.
- **Sheet Columns**: Added "Email" column and ensured valid `https://` URLs for LinkedIn.
- **Formatting**: Updated Google Sheet generation to include merged pitch row, orange headers (#FCE5CD), and Arial 10 font.
- **Search Logic**: Refined Apify search terms to "Owner [Niche] [Location]" for better relevance.
- **File Structure**: Organized scripts into `execution/` folder with versioning (`v2`, `v3`, `fast`).

### Fixed
- **Redirect URI Mismatch**: Solved by using fixed port 8080 in OAuth flow.
- **Apify Field Mapping**: Corrected field names (`full_name`, `company_name`) in `generate_lm_fast.py` to match Apify dataset output.
- **Slow Execution**: Reduced execution time by parallelizing API calls and optimizing Apify wait times.
