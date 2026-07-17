# Modal Deployment Guide - Auto-Fulfillment Daemon

## Pre-Flight Checklist ✅

### 1. Token Validation
- [x] Token has `refresh_token` (auto-refresh capable)
- [x] Token expires: 2025-12-17T09:31:44Z
- [x] Gmail scopes include: `gmail.readonly`, `gmail.modify`

### 2. Whitelist Prepared
- [x] Test email added to `apify_leads.json`
- [x] Total whitelisted: 5,366 leads

### 3. Secrets Prepared
- Modal secret `google-token` with `GOOGLE_TOKEN_B64`

## Deployment Steps

### Step 1: Create Modal Secret

```bash
modal secret create google-token
```

When prompted, add key `GOOGLE_TOKEN_B64` with value from `prepare_modal_secret.py` output.

### Step 2: Deploy Daemon

```bash
modal deploy modal_deployments/auto_fulfillment_daemon_modal.py
```

Expected output:
- App name: `auto-fulfillment-daemon`
- Scheduled function: `check_for_replies` (runs every 1 minute)
- Uses Modal Volume for state persistence

### Step 3: Monitor Initial Runs

```bash
modal app logs auto-fulfillment-daemon
```

Watch for:
- `[WHITELIST] Loaded 5366 validated emails` ✅
- `[INFO] No new messages` or `[INFO] Found X unread messages`
- No authentication errors

## Cloud Physics Problems - SOLVED

### ✅ "Amnesia" Problem (Whitelist Sync)
**Solution**: Whitelist included in Modal image build
- `apify_leads.json` copied to `/root/apify_leads.json`
- Updated whitelist requires re-deployment: `modal deploy ...`

### ✅ "Token Death" Problem  
**Solution**: Token has `refresh_token` for auto-refresh
- Google APIs auto-refresh using `refresh_token`
- No browser interaction needed
- Daemon will run 24/7 without token expiry

## Architecture

### Scheduled Function
- **Trigger**: Every 1 minute via `modal.Period(minutes=1)`
- **Timeout**: 50 seconds (buffer before next run)
- **State**: Persisted via Modal Volume at `/mnt/state`

### Workflow
1. Load processed message IDs from Volume
2. Load whitelist from image (`/root/apify_leads.json`)
3. Check Gmail for unread messages
4. Filter: whitelist + "Re:" prefix + interested keywords
5. Trigger fulfillment webhook
6. Mark as read, save state to Volume

## Re-Deployment Workflow (When Adding New Leads)

1. Add new leads to local `apify_leads.json`
2. Re-deploy: `modal deploy modal_deployments/auto_fulfillment_daemon_modal.py`
3. New image includes updated whitelist
4. Daemon automatically uses new whitelist

## Next Steps

- [ ] Deploy to Modal
- [ ] Send test email to `deekshakdk11@gmail.com`
- [ ] Reply with "interested"
- [ ] Verify daemon catches reply and triggers fulfillment
- [ ] Monitor for 24 hours to confirm stability
