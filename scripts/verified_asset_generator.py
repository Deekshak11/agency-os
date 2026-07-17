
"""
High-Fidelity Core Logic for Generating Verified fCFO Assets (V7).
Clones 'Joe's Sheet', Rebuilds Chinedu-Standard Intro, Handles V2 GDoc Personalization.
"""
import os
import sys
import re
import copy
import json
import time
import random

# Use exact IDs from STATUS.md / MEMORY.md
SHEET_TEMPLATE_ID = "1wpnpNJM1YK9xyrvJPgDmNWxSi8b4DnGcj5SV7TagXs8" # Joe's Sheet
FOLDER_ID = "1JcFpzXIcrzzQk96GXL5kdbBM19vXuL3a"
GOLDEN_DATA_PATH = os.path.join(os.path.dirname(__file__), "../templates/verified_golden_leads.json")

# V2 GDoc Masters (Runway Analysis Format)
GDOC_MASTERS = {
    "Stainless": "1Ywf_vAAlG_1Z-H6-UtgbOktETVTGbn6TOWn-eMI5qvM",
    "Dialogue AI": "1FvE4manakc5pLz6fgbrdxlMpu4CrYM4i8JPYPQ01TSc",
    "COGNNA": "1t4kSFwTzHuKz_yC__oXrOnpUgs7f28Xa88noC5ZcUOs",
    "Paramify": "1FvXE4vjaS-LE19d7NolOh23sH0fzVQwOKyUFOceM_YQ",
    "Cavela": "16mHLVgQ8k5H9M6gnAyLGz5UitLAR8rJZhr3H0xyS1YY"
}

def get_utf16_len(s):
    return len(s.encode('utf-16-le')) // 2

def get_chinedu_intro(lead_first_name):
    """
    Rebuilds the Intro using V4 Logic (Confirmed by User).
    Uses 'Chunk-based' construction for perfect UTF-16 alignment.
    Template: '5 Specific Leads we found you'
    """
    LINKEDIN_ME = "https://www.linkedin.com/in/deekshak-dk"
    CAL_ME = "https://calendar.app.google/i2JWsxvZUYCc16cv8"
    
    text_parts = [
        (f"👋 {lead_first_name}, here's your asset :)\n\n", None),
        ("It contains - ", None),
        ("5 Specific Leads", "bold"),
        (" we found you + ", None),
        ("Personalized Email", "bold"),
        (" to send + ", None),
        ("Personalized Lead Magnet", "bold"),
        (" to give value.\n\n", None),
        ("Built using my ", None),
        ("AI Client Acquisition Engine", "bold"),
        (", as a sample of what we can do.\n\n", None),
        ("Would you ", None),
        ("HATE ~10 Qualified Meetings in 30 Days FOR FREE", "bold"),
        (" Straight To Your Calendar?\n\n", None),
        ("Tell me here 👇\n\n", None),
        ("To Chat", "bold"),
        (" → ", None),
        (LINKEDIN_ME, "boldlink"),
        ("\n", None),
        ("To Call", "bold"),
        (" → ", None),
        (CAL_ME, "boldlink"),
        ("\n\n", None),
        ("Anyways, hoping you like it :)", None),
        ("\n", None),
        ("DK", None),
    ]
    
    full_text = ""
    text_format_runs = []
    current_pos = 0
    
    for text, fmt in text_parts:
        start = current_pos
        text_len = get_utf16_len(text)
        
        # Define Format Objects
        bold_style = {"bold": True, "fontFamily": "Arial", "fontSize": 12}
        base_style = {"bold": False, "underline": False, "fontFamily": "Arial", "fontSize": 12}
        link_style = {
            "bold": True, "underline": True, "fontFamily": "Arial", "fontSize": 12,
            "foregroundColor": {"red": 0.067, "green": 0.333, "blue": 0.800},
            "link": {"uri": text}
        }
        
        if fmt == "bold":
            text_format_runs.append({"startIndex": start, "format": bold_style})
        elif fmt == "boldlink":
            text_format_runs.append({"startIndex": start, "format": link_style})
        elif fmt is None:
            text_format_runs.append({"startIndex": start, "format": base_style})
        
        full_text += text
        current_pos += text_len
    
    
    # Final reset run removed (Causes 400 error if startIndex >= length)
            
    return full_text, text_format_runs

def clone_and_personalize_gdoc(master_name, lead_first_name, folder_id, services):
    docs, sheets, drive = services
    doc_id = GDOC_MASTERS.get(master_name)
    if not doc_id:
        raise ValueError(f"Unknown Master GDoc: {master_name}")

    # RETRY LOOP for Rate Limits
    for attempt in range(5):
        try:
            # 1. Copy
            copy_body = {
                "name": f"{master_name} - Runway Analysis", # Clean naming per MEMORY.md
                "parents": [folder_id]
            }
            copied = drive.files().copy(fileId=doc_id, body=copy_body).execute()
            new_doc_id = copied.get("id")
            
            # 2. Personalize (By Michelle -> By {FirstName})
            # Per MEMORY.md, V2 templates use "By Michelle" in subtitle
            requests = [
                {
                    "replaceAllText": {
                        "containsText": {"text": "Michelle", "matchCase": False},
                        "replaceText": lead_first_name
                    }
                }
            ]
            docs.documents().batchUpdate(documentId=new_doc_id, body={'requests': requests}).execute()
            
            # 3. Public Permission
            drive.permissions().create(fileId=new_doc_id, body={'type': 'anyone', 'role': 'reader'}).execute()
            
            return f"https://docs.google.com/document/d/{new_doc_id}"
            
        except Exception as e:
            if "429" in str(e):
                wait = (2 ** attempt) + random.random()
                print(f"  ⏳ GDoc Rate Limit for {master_name}. Retrying in {wait:.1f}s...")
                time.sleep(wait)
            else:
                raise e
    raise Exception(f"GDoc failure for {master_name}")

def generate_verified_asset(lead_first_name, lead_full_name, services, **kwargs):
    docs, sheets, drive = services
    
    # 1. Load Data
    with open(GOLDEN_DATA_PATH, 'r') as f:
        golden_data = json.load(f)

    # 2. Clone Sheet
    new_title = f"{lead_first_name}'s 5 Specific Leads"
    copy_body = {"name": new_title, "parents": [FOLDER_ID]}
    copied = drive.files().copy(fileId=SHEET_TEMPLATE_ID, body=copy_body).execute()
    sheet_id = copied.get("id")

    # 3. Rebuild A1 Intro (Chinedu Standard)
    intro_text, intro_runs = get_chinedu_intro(lead_first_name)
    
    # 4. Populate 5 Prospects
    new_rows = []
    for asset in golden_data:
        # Clone high-quality V2 GDoc
        doc_url = clone_and_personalize_gdoc(asset['Company'], lead_first_name, FOLDER_ID, services)
        
        # Email Body (Rebuilt with new GDoc URL)
        founder = asset["Name"].split()[0]
        v_points = asset.get("Points", [])
        points_block = "\n".join([f"- {p}" for p in v_points])
        
        msg = (f"SUBJECT: For {asset['Company']} [CONFIDENTIAL]\n---\n"
               f"Hey {founder},\n\n"
               f"So, I analysed the runway for {asset['Company']} based on what I could find publicly and put this together.\n\n"
               f"{doc_url}\n\n"
               f"It covers:\n"
               f"{points_block}\n\n"
               f"Worth a look?\n\n"
               f"Best,\n{lead_first_name}\n\n" 
               f"P.S. No cost. I usually only do this for my portfolio companies, but I like what you are building :)")
        
        new_rows.append([
            asset["Name"], asset["Email"], asset["LinkedIn"], asset["Company"], asset["CompanyLI"], msg, doc_url
        ])
        # Telemetry: Log doc creation success
        if "telemetry_callback" in kwargs:
            kwargs["telemetry_callback"]({"event": "DOC_CLONED", "company": asset["Company"], "url": doc_url})

    # 5. Batch Update Sheet
    requests = [
        # Intro A1
        {
            "updateCells": {
                "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 1},
                "rows": [{"values": [{"userEnteredValue": {"stringValue": intro_text}, "textFormatRuns": intro_runs, "userEnteredFormat": {"wrapStrategy": "WRAP", "verticalAlignment": "TOP", "backgroundColor": {"red": 1, "green": 1, "blue": 1}}}]}],
                "fields": "userEnteredValue,textFormatRuns,userEnteredFormat"
            }
        },
        # Data Rows 4-8
        {
            "updateCells": {
                "range": {"sheetId": 0, "startRowIndex": 3, "endRowIndex": 8, "startColumnIndex": 0, "endColumnIndex": 7},
                "rows": [{"values": [{"userEnteredValue": {"stringValue": str(cell)}} for cell in row]} for row in new_rows],
                "fields": "userEnteredValue"
            }
        }
    ]
    sheets.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={'requests': requests}).execute()
    
    # 6. Global Permissions
    drive.permissions().create(fileId=sheet_id, body={'type': 'anyone', 'role': 'reader'}).execute()
    
    if "telemetry_callback" in kwargs:
        kwargs["telemetry_callback"]({"event": "SHEET_READY", "url": f"https://docs.google.com/spreadsheets/d/{sheet_id}"})

    return f"https://docs.google.com/spreadsheets/d/{sheet_id}", intro_text
