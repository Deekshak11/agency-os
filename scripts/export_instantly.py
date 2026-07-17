import sys
import os
import csv
import argparse
from datetime import datetime

# Path setup for library imports
sys.path.insert(0, os.getcwd())
from scripts.library.google_services import get_google_services
from scripts.glassbox_core import log_event

AGENT_NAME = "InstantlyExporter"

def analyze_and_export(dry_run=False):
    log_event("START", "master_sheet", agent_name=AGENT_NAME)
    
    docs, sheets, drive = get_google_services()
    if not sheets:
        log_event("ERROR", "master_sheet", {"reason": "Auth Failure"}, agent_name=AGENT_NAME)
        return
        
    MASTER_SHEET_ID = "19M8Inwgbgb8qVbirt6hoEjr5YQ_Xb6WG-Co1DwdWUzA"
    
    try:
        print("=== Analyzing Master Sheet ===\n")
        res = sheets.spreadsheets().values().get(
            spreadsheetId=MASTER_SHEET_ID,
            range="'copy of ALL Leads'"
        ).execute()
        
        data = res.get('values', [])
        headers = data[0] if data else []
        rows = data[1:] if len(data) > 1 else []
        
        log_event("PROGRESS", "master_sheet", {"rows_found": len(rows)}, agent_name=AGENT_NAME)

        leads_with_assets = []
        for row in rows:
            while len(row) < 20: row.append('')
            url = row[17] if len(row) > 17 else ''
            if url and 'docs.google.com' in url:
                leads_with_assets.append(row)
        
        csv_filename = f"instantly_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        instantly_rows = []
        for row in leads_with_assets:
            email = row[3] if len(row) > 3 else ''
            if email and '@' in email:
                instantly_rows.append({
                    'email': email,
                    'first_name': row[0] if len(row) > 0 else '',
                    'company_name': row[4] if len(row) > 4 else '',
                    'lead_magnet_url': row[17] if len(row) > 17 else ''
                })
        
        if dry_run:
            print(f"🛠️ DRY RUN: Would export {len(instantly_rows)} leads to {csv_filename}")
            log_event("SUCCESS", "master_sheet", {"mode": "DRY_RUN", "count": len(instantly_rows)}, agent_name=AGENT_NAME)
            return

        # Write CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['email', 'first_name', 'company_name', 'lead_magnet_url'])
            writer.writeheader()
            writer.writerows(instantly_rows)
        
        log_event("SUCCESS", "master_sheet", {"file": csv_filename, "count": len(instantly_rows)}, agent_name=AGENT_NAME)
        print(f"✅ Exported {len(instantly_rows)} leads to {csv_filename}")

    except Exception as e:
        msg = str(e)
        log_event("ERROR", "master_sheet", {"error": msg}, agent_name=AGENT_NAME)
        print(f"❌ Error during export: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    analyze_and_export(dry_run=args.dry_run)
