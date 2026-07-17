# Incident Report: Modal Scheduled Task Cost Overrun

**Date**: December 2025  
**Impact**: ~$120 cost over 4 days  
**Root Cause**: Orphaned scheduled task running 96x/day

## What Happened

An old experiment file (`execution/modal_webhook.py`) was deployed with a cron schedule (`schedule=modal.Cron("*/15 * * * *")`). This ran every 15 minutes (96 times/day) for 4 days, accumulating ~$120 in costs (~$30/day).

The issue was discovered only when the user reported credit depletion.

## Root Cause

When transitioning from scheduled polling architecture to webhook-based architecture, the old Modal deployment was never explicitly stopped. The file existed in the codebase, so it continued running in the cloud.

**Key failure**: Assumed stopping locally stops cloud execution. Cloud services are persistent by design.

## Prevention Protocol

### 1. PRE-DEPLOYMENT AUDIT
Before running any `deploy` command:
- Search codebase for: `schedule=`, `cron=`, `Period(`, `@scheduled`, `setInterval`
- Check for: auto-scaling configs, reserved capacity, always-on instances
- Review pricing model: per-request vs per-minute vs scheduled
- Ask: "What triggers this? Event-based preferred over time-based"

### 2. POST-DEPLOYMENT VERIFICATION
Within 1 hour of deployment:
- List all deployed services: `modal app list`
- Verify state: Check for "deployed" vs "stopped"
- Set up billing alerts IMMEDIATELY
- Test one cycle and verify expected behavior

### 3. CLEANUP PROTOCOL
When switching architectures:
- Explicitly STOP old deployments
- Don't assume local stop = cloud stop
- Search for orphaned experiments: `git log --all --grep="modal"`

### 4. MONTHLY AUDIT
Set calendar reminder to review all cloud deployments on 1st of month.

## Red Flags

- Any schedule tighter than hourly (`*/15` = 96/day, `*/5` = 288/day)
- "Always-on" configurations for dev/staging
- Multiple services doing same thing (forgot to clean up)
- Deployed experiments "just for testing"

## Emergency Stop Commands

- Modal: `modal app stop <app-id>`
- AWS Lambda: `aws lambda delete-function --function-name X`
- GCP: `gcloud functions delete <name>`

## Lesson Learned

**Infrastructure is NOT "set and forget". It's "deploy, verify, monitor, audit monthly". Silence = money burning.**

This applies to ALL cloud services: AWS Lambda, Google Cloud Functions, Modal, Vercel, Railway, Azure Functions, Heroku, Render, Fly.io, etc.
