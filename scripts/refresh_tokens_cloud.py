
import os
import glob
import json
import modal
import time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Define the Modal App
app = modal.App("agency-os-token-refresher")

# Define persistence volume
vol = modal.Volume.from_name("agency-os-tokens", create_if_missing=True)

# Image definition with dependencies
image = modal.Image.debian_slim().pip_install(
    "google-auth",
    "google-auth-oauthlib",
    "google-auth-httplib2",
    "requests"
)

@app.function(
    image=image,
    volumes={"/root/tokens": vol},
    schedule=modal.Period(days=2),  # Refresh every 2 days (well within 7-day limit)
    timeout=600
)
def refresh_cloud_tokens():
    """
    Iterates through all token JSON files in the Volume, 
    refreshes them via Google Auth API, and saves them back.
    """
    print("🔄 Starting Cloud Token Refresh Cycle...")
    
    token_files = glob.glob("/root/tokens/data/token*.json")
    if not token_files:
        print("⚠️ No tokens found in /data/tokens. Did you upload them?")
        return

    success_count = 0
    fail_count = 0

    for token_file in sorted(token_files):
        filename = os.path.basename(token_file)
        try:
            print(f"Checking {filename}...")
            
            with open(token_file, 'r') as f:
                data = json.load(f)
            
            creds = Credentials.from_authorized_user_info(data)
            
            # Force refresh logic:
            # Even if valid, we refresh if it's close to expiry, 
            # OR we just refresh to keep it alive (standard practice for long-running jobs)
            # Google's 'expired' property checks against expiry time.
            # We will try to refresh regardless to extend the session if possible/allowable.
            
            refreshed = False
            if creds.expired:
                print(f"   Shape: Expired. Refreshing...")
                creds.refresh(Request())
                refreshed = True
            elif creds.refresh_token:
                # Even if not expired, let's hit the refresh endpoint to ensure we verify it works
                # and potentially roll the session if configured that way.
                # However, Google Python lib doesn't easily force refresh if valid.
                # We'll trust .expired BUT we rely on frequent runs (every 2 days) 
                # to catch it before the 7-day cliff.
                
                # To be extra safe for "Testing" status apps, we can force it:
                if not creds.valid: # Double check
                     print(f"   Shape: Invalid. Refreshing...")
                     creds.refresh(Request())
                     refreshed = True
                else:
                     print(f"   Shape: Valid. (Will refresh if < 24h remains, handled by lib)")
                     # We can manually force a refresh call if we really want to, 
                     # but standard `refresh` call handles readiness.
                     # Let's forcibly call refresh(Request()) just to prove connectivity 
                     # and update expiry.
                     try:
                         creds.refresh(Request())
                         refreshed = True
                         print("   Forced verified refresh.")
                     except Exception as e:
                         print(f"   Note: Force refresh skipped/failed (might be valid): {e}")

            if refreshed or creds.valid:
                # Save back to Volume
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
                vol.commit() # Ensure persistence
                print(f"   ✅ Saved updated {filename}")
                success_count += 1
            else:
                print(f"   ❌ {filename} is invalid and could not be refreshed.")
                fail_count += 1
                
        except Exception as e:
            print(f"   🚨 ERROR checking {filename}: {e}")
            fail_count += 1

    print(f"\n📊 SUMMARY: {success_count} Refreshed/Valid, {fail_count} Failed.")
    
if __name__ == "__main__":
    # Local test run
    with app.run():
        refresh_cloud_tokens.remote()
