# Google OAuth Setup Guide

> SOP for setting up Google OAuth credentials for API access (Sheets, Drive, Docs)

## Prerequisites
- Google Cloud Console access
- A Google Cloud project (or ability to create one)

---

## Step 1: Create Google Cloud Project

1. Go to: https://console.cloud.google.com/projectcreate
2. Project name: `Agency-OS`
3. Click "Create"
4. Wait for project creation (~30 seconds)

---

## Step 2: Enable Google Sheets API

1. Go to: https://console.cloud.google.com/apis/library/sheets.googleapis.com
2. Make sure "Agency-OS" project is selected in top dropdown
3. Click "Enable"

---

## Step 3: Configure OAuth Consent Screen

1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Select "External" user type → Click "Create"
3. Fill in required fields:
   - App name: `Agency OS`
   - User support email: (your Google email)
   - Developer contact: (your Google email)
4. Click "Save and Continue"
5. On "Scopes" page: Click "Save and Continue" (skip adding scopes)
6. On "Test users" page:
   - Click "Add Users"
   - Add your Google email
   - Click "Save and Continue"
7. Click "Back to Dashboard"

---

## Step 4: Create OAuth Credentials

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click "+ Create Credentials" → "OAuth client ID"
3. Application type: `Desktop app`
4. Name: `Agency OS Desktop`
5. Click "Create"
6. **Download JSON** button → saves `client_secret_*.json`

---

## Step 5: Install Credentials in Project

1. Rename the downloaded file to `credentials.json`
2. Move it to: `c:\Users\HP USER\OneDrive\Desktop\DK Antigravity Project\Agency_OS\credentials.json`

---

## Step 6: Generate Token (First Run)

Run this command in the project folder:
```powershell
& '.\python_env\python.exe' -c "
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
with open('token.json', 'w') as token:
    token.write(creds.to_json())
print('Token saved to token.json')
"
```

This will:
1. Open browser for Google login
2. Ask you to approve access
3. Save `token.json` for future use

---

## Verification

Test that it works:
```powershell
& '.\python_env\python.exe' scripts\analyze_sheet_leads.py
```

Should output the fCFO Leads analysis.

---

## Files Created
- `credentials.json` - OAuth client config (from Google Cloud Console)
- `token.json` - Access/refresh tokens (auto-generated after first login)

Both files are in `.gitignore` - never commit to GitHub.
