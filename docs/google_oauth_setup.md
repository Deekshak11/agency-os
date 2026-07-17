# Google OAuth Setup Guide

## Issue: "invalid_client" Error

The `credentials.json` file has an invalid OAuth client ID. This needs to be regenerated from Google Cloud Console.

---

## Step-by-Step Fix

### 1. Go to Google Cloud Console

Open browser and navigate to: https://console.cloud.google.com

### 2. Select/Create Project

- Click project dropdown (top left)
- Either select existing project OR create new: "Agency OS"

### 3. Enable Required APIs

Go to "APIs & Services" → "Enable APIs and Services"

Enable these APIs:
- ✅ Google Docs API
- ✅ Google Drive API
- ✅ Google Sheets API

### 4. Create OAuth 2.0 Credentials

**APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**

**Configure OAuth consent screen (if first time):**
- User Type: **External**
- App name: **Agency OS**
- User support email: your email
- Developer contact: your email
- Scopes: Click "Add or Remove Scopes"
  - Select: `auth/documents`
  - Select: `auth/drive`
  - Select: `auth/spreadsheets`
- Test users: Add your Gmail address
- Click **Save and Continue**

**Create OAuth Client:**
- Application type: **Desktop app**
- Name: **Agency OS Desktop Client**
- Click **Create**

### 5. Download credentials.json

- Click **Download JSON** button
- Save file as `credentials.json`
- Move to: `C:\Users\user\Desktop\Agency_OS\credentials.json`

### 6. Generate token.json

Run this command:

```bash
cd C:\Users\user\Desktop\Agency_OS
python -c "from google_auth_oauthlib.flow import InstalledAppFlow; flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']); creds = flow.run_local_server(port=8080); open('token.json', 'w').write(creds.to_json()); print('✅ Token created!')"
```

**This will:**
1. Open browser with Google OAuth
2. Ask you to sign in
3. Ask you to allow access
4. Save `token.json` to current directory

---

## Alternative: Skip Google OAuth for Now

If you want to deploy the webhooks first and handle Google OAuth later:

1. **Comment out Google API calls** in scripts (temporary)
2. **Deploy to Modal** (webhooks don't need Google yet)
3. **Test webhook receivers** (they'll log errors for Google API calls)
4. **Fix OAuth later** when testing end-to-end

---

## For Modal Deployment

Modal uses environment variables, so you'll need to:

1. Generate `token.json` locally (above)
2. Base64 encode it for Modal:

```bash
# PowerShell
$token = Get-Content token.json -Raw
$bytes = [System.Text.Encoding]::UTF8.GetBytes($token)
$encoded = [Convert]::ToBase64String($bytes)
$encoded
```

3. Add to Modal secrets:

```bash
modal secret create google-token GOOGLE_TOKEN_B64="your_base64_token"
```

---

## Current Priority

**Option A:** Fix Google OAuth first (5-10 mins)
- Create new OAuth client
- Download credentials.json
- Generate token.json
- Then deploy to Modal

**Option B:** Deploy webhooks first (2 mins)
- Deploy to Modal without Google integration
- Test webhook receivers
- Fix Google OAuth later

**Recommended:** **Option A** - Fix OAuth now so everything works end-to-end.
