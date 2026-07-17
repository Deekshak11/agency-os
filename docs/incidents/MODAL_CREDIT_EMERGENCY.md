# MODAL CREDIT BURN - EMERGENCY FIX

## ISSUE IDENTIFIED

**App:** `cfo-agency-fulfillment` (ap-CUUoJxuzRC5BZfN3nqw8ks)  
**File:** `execution/modal_webhook.py`  
**Problem:** Line 45 has scheduled function running EVERY 15 MINUTES

```python
@app.function(image=image, secrets=ALL_SECRETS, timeout=1800, 
              schedule=modal.Cron("*/15 * * * *"),  # ← THIS IS THE PROBLEM
              volumes={"/data": volume})
def generate_lm_background(niche: str = None):
    # Runs lead magnet generation every 15 minutes = 96 times/day!
```

## IMPACT

- **Frequency:** 96 executions per day (every 15 mins)
- **Cost per run:** ~$0.31 (Apify + Perplexity + GPT-4o-mini)
- **Daily burn:** 96 × $0.31 = **$29.76/day**
- **Monthly:** **~$900/month** if left running!

## ACTIONS TAKEN

✅ **STOPPED** the app immediately: `modal app stop ap-CUUoJxuzRC5BZfN3nqw8ks`

## ROOT CAUSE

This was from the original lead magnet system before we switched to webhook-based architecture. The scheduled task was meant for batch processing but was never disabled.

## RECOMMENDED FIX

**Option 1: Delete the file** (if not needed)
```bash
rm execution/modal_webhook.py
```

**Option 2: Remove schedule** (if keeping for manual triggering)
Change line 45 to:
```python
@app.function(image=image, secrets=ALL_SECRETS, timeout=1800, volumes={"/data": volume})
# Removed: schedule=modal.Cron("*/15 * * * *")
```

**Option 3: Redeploy without schedule**
Keep the trigger endpoint but remove the cron schedule.

## VERIFICATION

Current Modal apps:
- ✅ `reply-triage-webhook` - No schedule (webhook only)
- ✅ `fathom-proposal-webhook` - No schedule (webhook only)  
- ⚠️ `cfo-agency-fulfillment` - **STOPPED** (had schedule)

## PREVENTION

✅ Always audit Modal deployments for:
- `schedule=modal.Cron(...)` 
- `modal.Period(...)` 
- Any time-based triggers

✅ Use webhooks (event-driven) instead of schedules (time-driven) wherever possible

## NEXT STEPS

1. ✅ Confirm app is stopped
2. ⏳ Remove or fix modal_webhook.py
3. ⏳ Redeploy if needed (without schedule)
4. ⏳ Check Modal billing to see total damage
5. ⏳ Set up billing alerts
