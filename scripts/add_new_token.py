
import os
import json
import glob
from google_auth_oauthlib.flow import InstalledAppFlow

# SCOPES must match what the runner needs
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

CREDENTIALS_FILE = 'credentials.json'
TOKENS_DIR = 'tokens'

def generate_new_token():
    if not os.path.exists(TOKENS_DIR):
        os.makedirs(TOKENS_DIR)
    
    print("🔄 Starting Infinite Auth Loop. Press Ctrl+C directly or ask Agent to stop to exit.")
    
    while True:
        try:
            # Determine next token name DYNAMICALLY each iteration
            existing = glob.glob(os.path.join(TOKENS_DIR, "token_*.json"))
            # Extract numbers to be precise
            ids = []
            for f in existing:
                try:
                    # extraction: token_12.json -> 12
                    base = os.path.basename(f)
                    if base == 'token_prod.json': continue
                    num = int(base.replace('token_', '').replace('.json', ''))
                    ids.append(num)
                except:
                    pass
            
            next_id = max(ids) + 1 if ids else 2
            # Handle token_prod case (starts at 2 usually if prod exists, but let's just stick to max+1)
            
            new_token_path = os.path.join(TOKENS_DIR, f"token_{next_id}.json")
            
            print(f"\n🚀 Launching Auth for Token #{next_id}...")
            print(f"📂 Target: {new_token_path}")
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # Run local server
            # prompt='consent' forces the consent screen, ensuring we can check all boxes
            creds = flow.run_local_server(port=0, prompt='consent')
            
            # Save the credentials
            with open(new_token_path, 'w') as token:
                token.write(creds.to_json())
                
            print(f"✅ Success! Saved {os.path.basename(new_token_path)}")
            print("⏳ specific_gap: Waiting 2 seconds before next...")
            import time
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user.")
            break
        except Exception as e:
            print(f"\n⚠️ Error: {e}")
            print("Retrying in 5 seconds...")
            import time
            time.sleep(5)

if __name__ == '__main__':
    generate_new_token()
