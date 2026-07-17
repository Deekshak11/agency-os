
"""
Standardized Golden Sheet Generator
Matches "Archive Logic" for Intro formatting (Rich Text) + V4 Fixes (Values, Links).
"""
import time

# Constants
REF_SHEET_ID = "1IU5D-qs6UT0bhEdVTzu4VoKUBxPz2UecGoMSX-uOe4o"
LINKEDIN_URL = "https://www.linkedin.com/in/deekshak-dk"
CAL_URL = "https://calendar.app.google/i2JWsxvZUYCc16cv8"
BOLD_PHRASES = [
    "5 Specific Companies", "Personalized Email", "Personalized Lead Magnet",
    "AI Client Acquisition Engine", "HATE", "~10 Qualified Meetings in 30 Days FOR FREE"
]

def utf16_index(text, char_index):
    utf16_count = 0
    for i, char in enumerate(text):
        if i >= char_index: break
        if ord(char) > 0xFFFF: utf16_count += 2
        else: utf16_count += 1
    return utf16_count

def get_styled_intro(lead_name):
    # Using "DK" as the signer
    final_text = f"👋 {lead_name}, here's your asset :)\n\nIt contains - 5 Specific Companies that match your ICP + Personalized Email + Personalized Lead Magnet\n\nBuilt using my AI Client Acquisition Engine, as a sample of the output.\n\nWould you HATE ~10 Qualified Meetings in 30 Days FOR FREE Straight To Your Calendar?\n\nTo Discuss via Chat → {LINKEDIN_URL}\nTo Discuss via Call → {CAL_URL}\n\nAnyways, hoping you like it :)\nDK"
    
    base_format = {'fontFamily': 'Arial', 'fontSize': 12, 'bold': False}
    bold_format = {'fontFamily': 'Arial', 'fontSize': 12, 'bold': True}
    link_format = {'fontFamily': 'Arial', 'fontSize': 12, 'underline': True, 'foregroundColorStyle': {'rgbColor': {'red': 0.066, 'green': 0.333, 'blue': 0.8}}}
    
    # 1. Bold Runs
    format_ranges = []
    for phrase in BOLD_PHRASES:
        idx = final_text.find(phrase)
        if idx != -1:
            format_ranges.append((utf16_index(final_text, idx), utf16_index(final_text, idx + len(phrase)), 'bold', None))
            
    # 2. Link Runs
    for url in [LINKEDIN_URL, CAL_URL]:
        idx = final_text.find(url)
        if idx != -1:
            format_ranges.append((utf16_index(final_text, idx), utf16_index(final_text, idx + len(url)), 'link', url))
            
    format_ranges.sort(key=lambda x: x[0])
    
    text_runs = []
    current_pos = 0
    for start, end, fmt_type, url in format_ranges:
        if start > current_pos:
            text_runs.append({'startIndex': current_pos, 'format': base_format.copy()})
        if fmt_type == 'bold': text_runs.append({'startIndex': start, 'format': bold_format.copy()})
        elif fmt_type == 'link':
            fmt = link_format.copy()
            fmt['link'] = {'uri': url}
            text_runs.append({'startIndex': start, 'format': fmt})
        
        text_runs.append({'startIndex': end, 'format': base_format.copy()}) # Reset to base
        current_pos = end
        
    # CRITICAL V4 FIX: Ensure flow starts with Base format if first bold isn't at index 0
    if not text_runs or text_runs[0]['startIndex'] != 0:
        text_runs.insert(0, {'startIndex': 0, 'format': base_format.copy()})
        
    return final_text, text_runs

def create_and_polish_sheet(drive_service, sheets_service, folder_id, sheet_name, ref_sheet_id=REF_SHEET_ID):
    """
    Creates a new sheet from reference template and applies Golden Polish (Rich Text Intro).
    Returns (sheet_id, sheet_url).
    """
    try:
        # Extract First Name from Sheet Name (e.g. "Satish's 5 Leads") or use default
        first_name = sheet_name.split("'")[0] if "'" in sheet_name else "There"
        
        # 1. Copy Sheet
        print(f"Copying Source: {ref_sheet_id}...")
        file_metadata = {'name': sheet_name, 'parents': [folder_id]}
        new_sheet = drive_service.files().copy(fileId=ref_sheet_id, body=file_metadata).execute()
        nid = new_sheet.get('id')
        
        # 2. Prepare Intro
        final_text, text_runs = get_styled_intro(first_name)
        
        batch_reqs = [
            # A. Unhide Rows
            {"updateDimensionProperties": {"range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 0, "endIndex": 1000}, "properties": {"hiddenByUser": False}, "fields": "hiddenByUser"}},
            
            # B. Merge Header Row 1 (A1:G1)
            {
                "mergeCells": {
                    "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 7},
                    "mergeType": "MERGE_ALL"
                }
            },

            # C. Format Header Row 1 (The Pitch)
            {
                "updateCells": {
                    "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 1},
                    "rows": [{
                        "values": [{
                            "userEnteredValue": {"stringValue": final_text},
                            "textFormatRuns": text_runs,
                            "userEnteredFormat": {
                                "backgroundColor": {"red": 1, "green": 1, "blue": 1}, # White BG
                                "horizontalAlignment": "LEFT", # Left Aligned (User Request)
                                "verticalAlignment": "MIDDLE", 
                                "wrapStrategy": "WRAP",
                                "textFormat": {"fontSize": 12, "fontFamily": "Arial"}
                            }
                        }]
                    }],
                    "fields": "userEnteredValue,textFormatRuns,userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)"
                }
            },
            
            # D. Format Column Headers (Row 3) - Light Orange #FFE5CC
            {
                "updateCells": {
                    "range": {"sheetId": 0, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": 7},
                    "rows": [{
                        "values": [{"userEnteredFormat": {"backgroundColor": {"red": 1.0, "green": 0.898, "blue": 0.8}, "textFormat": {"bold": True, "fontFamily": "Arial", "fontSize": 10}, "horizontalAlignment": "LEFT", "verticalAlignment": "MIDDLE"}} for _ in range(7)]
                    }],
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
                }
            },

            # E. Set Row Heights (Row 1=275px, Row 2 Buffer=10px)
            {
                "updateDimensionProperties": {"range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 275}, "fields": "pixelSize"}
            },
            {
                "updateDimensionProperties": {"range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 1, "endIndex": 2}, "properties": {"pixelSize": 10}, "fields": "pixelSize"} # Buffer
            }
        ]
        
        sheets_service.spreadsheets().batchUpdate(spreadsheetId=nid, body={'requests': batch_reqs}).execute()
        
        # 3. Clear Sample Data
        sheets_service.spreadsheets().values().clear(spreadsheetId=nid, range="A4:Z100").execute()
        
        url = f"https://docs.google.com/spreadsheets/d/{nid}"
        print(f"✅ Created Golden Sheet: {url}")
        return nid, url
        
    except Exception as e:
        print(f"Sheet Creation Error: {e}")
        return None, None
