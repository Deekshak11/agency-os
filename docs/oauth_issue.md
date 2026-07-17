# OAuth Issue - For Later

The token.json (614 bytes) was created successfully, but there's a mismatch:

- Downloaded credentials file has `"web"` key (for web applications)
- Scripts expect `"installed"` key (for desktop applications)

**Fix needed:** Download the credentials from the "Antigravity" Desktop app OAuth client (not the web app one).

**For now:** Deploying System 1 without Google APIs. Will fix OAuth separately.
