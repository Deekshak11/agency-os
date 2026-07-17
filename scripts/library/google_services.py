
import os
import glob
import random
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_google_services():
    """Returns (docs, sheets, drive) services using local token.json rotation."""
    
    # Look for tokens in 'tokens/' or root
    token_files = glob.glob("tokens/token*.json")
    if not token_files:
        if os.path.exists("token.json"):
            token_files = ["token.json"]
    
    if not token_files:
        print("❌ No token files found.")
        return None, None, None
        
    t_path = random.choice(token_files)
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/documents'
    ]

    creds = Credentials.from_authorized_user_file(t_path, SCOPES)
    
    # Simple check for build
    try:
        drive = build('drive', 'v3', credentials=creds)
        docs = build('docs', 'v1', credentials=creds)
        sheets = build('sheets', 'v4', credentials=creds)
        return docs, sheets, drive
    except Exception as e:
        print(f"❌ Error building services: {e}")
        return None, None, None
