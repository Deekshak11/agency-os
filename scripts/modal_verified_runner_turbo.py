
import csv
import os
import sys
import glob
import random
import json
import modal

# Use the exact same image definition pattern that worked in batch2
image = modal.Image.debian_slim(python_version="3.10")\
    .pip_install(
        "google-api-python-client", 
        "google-auth-httplib2", 
        "google-auth-oauthlib", 
        "requests", 
        "python-dotenv"
    )\
    .add_local_dir("c:/Users/user/Desktop/Agency_OS/scripts", remote_path="/root/scripts")\
    .add_local_dir("c:/Users/user/Desktop/Agency_OS/templates", remote_path="/root/templates")

# Define persistence volumes
vol = modal.Volume.from_name("agency-os-tokens", create_if_missing=True)
log_vol = modal.Volume.from_name("agency-os-logs", create_if_missing=True)

from glassbox_core import log_event

AGENT_NAME = "AssetRunner"

app = modal.App("verified-fcfo-turbo-runner-v2")

# CONFIG
CONCURRENCY = 30 # Safe Mode: 30 (Drastically reduced to prevent rate limits)
DATA_DIR = "c:/Users/user/Desktop/Agency_OS/data"
RESUME_FILE = os.path.join(DATA_DIR, "production_batch2_leads.json")
# Output to Production CSV
OUTPUT_CSV = os.path.join(DATA_DIR, "verified_assets_production_batch2.csv")

SECRETS = [modal.Secret.from_name("agency-os")]

def get_modal_services():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    # Look in /root/tokens first (Production)
    token_files = glob.glob("/root/tokens/data/token*.json")
    if not token_files:
        token_files = glob.glob("tokens/token*.json") # Local fallback
        
    if not token_files:
        return None, None, None
        
    # RANDOM ROTATION
    t_path = random.choice(token_files)
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/documents'
    ]

    creds = Credentials.from_authorized_user_file(t_path, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:
            print(f"Failed to refresh {t_path}: {e}")

    drive = build('drive', 'v3', credentials=creds)
    docs = build('docs', 'v1', credentials=creds)
    sheets = build('sheets', 'v4', credentials=creds)

    return docs, sheets, drive

@app.function(
    image=image,
    secrets=SECRETS,
    volumes={"/root/tokens": vol, "/root/logs": log_vol},
    timeout=3600,
    concurrency_limit=CONCURRENCY
)
def process_verified_lead_turbo_v2(lead_row, dry_run=False):
    import sys
    import time
    sys.path.insert(0, "/root/scripts")
    from verified_asset_generator import generate_verified_asset
    from glassbox_core import log_event

    email = lead_row.get('email', '').strip()
    first = lead_row.get('firstName', 'Unknown')
    last = lead_row.get('lastName', '')
    full = f"{first} {last}".strip()

    # USER FILTER: Verified AND No CatchAll
    v_stat = lead_row.get('verificationStatus', '').strip().lower()
    c_stat = lead_row.get('catchAllStatus', '').strip().lower()

    if v_stat != 'valid' or c_stat != '':
        log_event("SKIPPED", email, {"reason": f"vStat:{v_stat}, cStat:{c_stat}"}, agent_name=AGENT_NAME)
        return None

    if not email or '@' not in email:
        log_event("ERROR", email, {"reason": "Invalid email"}, agent_name=AGENT_NAME)
        return None

    if dry_run:
        log_event("DRY_RUN", email, {"status": "SUCCESS_MOCK"}, agent_name=AGENT_NAME)
        return {"First Name": first, "Last Name": last, "Email": email, "Sheet_URL": "MOCK_URL", "Intro_Text": "MOCK_INTRO"}

    log_event("START", email, agent_name=AGENT_NAME)

    docs, sheets, drive = get_modal_services()
    if not docs:
        log_event("ERROR", email, {"reason": "Auth failure"}, agent_name=AGENT_NAME)
        return None

    def telemetry(event):
        log_event("PROGRESS", email, event, agent_name=AGENT_NAME)

    for attempt in range(5):
        try:
            url, body = generate_verified_asset(first, full, services=(docs, sheets, drive), telemetry_callback=telemetry)
            if url:
                log_event("SUCCESS", email, {"url": url}, agent_name=AGENT_NAME)
                return {
                    "First Name": first,
                    "Last Name": last,
                    "Email": email,
                    "Sheet_URL": url,
                    "Intro_Text": body
                }
        except Exception as e:
            msg = str(e)
            log_event("RETRY", email, {"attempt": attempt, "error": msg}, agent_name=AGENT_NAME)
            if "429" in msg or "Quota" in msg:
                wait = (2 ** attempt) * 3
                time.sleep(wait)
            else:
                log_event("FATAL", email, {"error": msg}, agent_name=AGENT_NAME)
                return None

    log_event("EXHAUSTED", email, agent_name=AGENT_NAME)
    return None

@app.local_entrypoint()
def main(dry_run: bool = False):
    if not os.path.exists(RESUME_FILE):
        print(f"❌ Resume file not found: {RESUME_FILE}")
        return

    with open(RESUME_FILE, 'r') as f:
        leads = json.load(f)

    # USER REQUEST: Cap Removed for Recovery
    # if len(leads) > 1000:
    #     leads = leads[:1000]
    #     print(f"⚠️ Capped at 1,000 leads for High-Fidelity evaluation.")

    if dry_run:
        print("🛠️ DRY RUN ENABLED - No assets will be created.")
        leads = leads[:5] # Test on 5 leads for speed

    print(f"🏭 Unleashing TURBO V2 (Glass Box) on {len(leads)} leads...")
    print(f"📊 High-Fidelity Output: {OUTPUT_CSV}")

    # Define fields
    fieldnames = ["First Name", "Last Name", "Email", "Sheet_URL", "Intro_Text"]

    # Header if new
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    # Process incrementally
    count = 0
    # Map with kwargs
    for res in process_verified_lead_turbo_v2.map(leads, kwargs={"dry_run": dry_run}):
        if res:
            with open(OUTPUT_CSV, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(res)
            count += 1
            if count % 10 == 0:
                print(f"✍️ Solid-Saved: {count} leads")

    print(f"\n🎉 TURBO V2 COMPLETE. {count} high-fidelity assets in {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
