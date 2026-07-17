# Infrastructure Cost Prevention Checklist

Use this checklist BEFORE and AFTER deploying to ANY cloud service.

## Pre-Deployment Checklist

### Code Audit
- [ ] Search for scheduled triggers: `schedule=`, `cron=`, `Period(`, `@scheduled`, `setInterval`
- [ ] Search for auto-scaling: `min_instances`, `max_instances`, `autoscaling`, `reserved`
- [ ] Search for polling loops: `while True`, `setTimeout`, background jobs
- [ ] Check for API calls in loops (could hit rate limits → retry loops → cost cascade)

### Architecture Review
- [ ] Is this event-driven (webhook) or time-driven (schedule)?
- [ ] Can I replace scheduled task with webhook/event trigger?
- [ ] Do I need this running 24/7 or only on-demand?
- [ ] What happens if this runs 1000x by mistake? (fail-safe?)

### Pricing Model Understanding
- [ ] Read pricing docs for the service
- [ ] Understand: per-request vs per-minute vs scheduled vs storage
- [ ] Calculate worst-case cost (if runs continuously for 1 month)
- [ ] Check free tier limits and what happens when exceeded

### Cleanup Old Deployments
- [ ] List all currently deployed apps in this service
- [ ] Stop/delete anything from previous experiments
- [ ] Verify no orphaned scheduled tasks from old code

## Post-Deployment Checklist (Within 1 Hour)

### Verify Deployment State
- [ ] Run list command: `modal app list`, `aws lambda list-functions`, etc.
- [ ] Check status: Is it "deployed" when it should be "stopped"?
- [ ] Look for background tasks you didn't expect

### Set Up Monitoring
- [ ] Configure billing alerts (even if on free tier)
- [ ] Set up threshold: Alert at 50%, 80%, 100% of expected monthly budget
- [ ] Add calendar reminder: "Infrastructure audit" on 1st of month

### Test One Cycle
- [ ] If scheduled: Wait for one execution, check logs
- [ ] If webhook: Send test payload, verify response
- [ ] Check cost dashboard: Did cost increase as expected?

### Document
- [ ] Note deployment in task.md or docs/
- [ ] Include: What it does, when it runs, expected cost
- [ ] Add to "Active Deployments" list

## Monthly Audit (1st of Month)

- [ ] List all deployments across all services
- [ ] Review last month's costs - any surprises?
- [ ] Check for deployments not used in 30 days → candidates for deletion
- [ ] Verify scheduled tasks are still needed
- [ ] Update cost estimates if traffic changed

## Red Flags (Immediate Investigation)

🚨 Schedule tighter than 1 hour (*/15, */5 = very expensive)
🚨 Multiple apps doing the same thing (forgot to clean up old version)
🚨 "Test" or "experimental" apps still running after project complete
🚨 Sudden 10x cost increase without 10x traffic increase
🚨 Cloud bill > expected by >20%

## Emergency Stop Commands

Have these ready before problems occur:

**Modal:**
```bash
modal app list
modal app stop <app-id>
```

**AWS Lambda:**
```bash
aws lambda list-functions
aws lambda delete-function --function-name <name>
# Or disable trigger:
aws events disable-rule --name <rule-name>
```

**Google Cloud Functions:**
```bash
gcloud functions list
gcloud functions delete <name>
```

**Vercel:**
```bash
vercel list
vercel remove <deployment-url>
```

**Heroku:**
```bash
heroku ps:scale web=0 -a <app-name>
heroku maintenance:on -a <app-name>
```

## Cost Multipliers to Watch

**Schedule frequency:** 
- Hourly × 30 days = 720 runs/month
- */15 mins × 30 days = 2,880 runs/month
- */5 mins × 30 days = 8,640 runs/month

**Retries:**
- 1 webhook with 3 retry attempts = 4× cost if always failing
- Exponential backoff misconfigured = infinite retries

**Data transfer:**
- Cross-region data transfer (20× more expensive than same-region)
- CDN bandwidth (first GB free, then $0.08-0.20/GB)

**Cold starts prevention:**
- "Keep-alive" pings every minute = 43,200 executions/month
- Better: Accept cold starts or use true serverless

## Lessons from Real Incidents

**Incident 1: Modal Credit Burn (Dec 2025)**
- What: Scheduled task every 15 mins for lead generation
- Cost: $30/day × 4 days = $120
- Cause: Old experiment file deployed with cron, never disabled
- Fix: `modal app stop`, deleted file, added this checklist

**Principles:**
1. Cloud infrastructure is NOT "set and forget"
2. Silence = money burning
3. "Just a test" deployments must be explicitly stopped
4. Switching architectures (scheduled → webhook) requires cleanup of old pattern
5. Free tier ≠ free forever (limits exist for a reason)

---

**Remember:** Infrastructure is a recurring cost. Treat it like a subscription - audit monthly, cancel what you don't use.
