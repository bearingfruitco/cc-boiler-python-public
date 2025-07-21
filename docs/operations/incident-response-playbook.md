# FreshSlate Incident Response Playbook

## Overview

This playbook provides step-by-step procedures for handling production incidents. Follow the severity guidelines to determine the appropriate response level.

## Incident Severity Levels

### SEV 1 - Critical (Complete Outage)
- **Impact**: Site completely down, no leads captured
- **Response Time**: Immediate (< 5 minutes)
- **Examples**: 
  - 500 errors on all pages
  - Database unreachable
  - Payment processing down

### SEV 2 - High (Major Feature Broken)
- **Impact**: Core functionality impaired, significant lead loss
- **Response Time**: < 30 minutes
- **Examples**:
  - Quiz flow broken
  - Lead submission failing
  - Analytics not tracking

### SEV 3 - Medium (Degraded Performance)
- **Impact**: Poor user experience, some lead loss
- **Response Time**: < 2 hours
- **Examples**:
  - Slow page loads (> 5s)
  - Intermittent errors
  - Partner API issues

### SEV 4 - Low (Minor Issues)
- **Impact**: Minimal user impact
- **Response Time**: Next business day
- **Examples**:
  - UI glitches
  - Non-critical features broken
  - Documentation issues

## Initial Response (First 15 Minutes)

### 1. Assess the Situation
```bash
# Check site status
curl -I https://freshslate.com
curl https://freshslate.com/api/health

# Check monitoring dashboards
# - BetterStack: https://uptime.betterstack.com
# - Sentry: https://sentry.io/freshslate
# - Vercel: https://vercel.com/freshslate

# Check recent deployments
vercel list --limit 5
```

### 2. Declare Incident
```bash
# Post in #incidents Slack channel
"🚨 [SEV X] Incident Declared: [Brief description]
Status: Investigating
Impact: [User impact]
Lead: @[your-name]"

# Create incident in BetterStack
curl -X POST https://uptime.betterstack.com/api/v2/incidents \
  -H "Authorization: Bearer $BETTERSTACK_TOKEN" \
  -d '{
    "name": "Brief description",
    "severity": "sev1",
    "status": "investigating"
  }'
```

### 3. Establish War Room
- **SEV 1-2**: Create video call immediately
- **SEV 3-4**: Slack thread sufficient
- **Roles**:
  - Incident Commander (IC)
  - Technical Lead
  - Communications Lead
  - Scribe (document actions)

### 4. Initial Diagnostics
```bash
# Error logs
tail -f vercel logs
sentry issues --project freshslate --status unresolved

# Database health
pnpm db:health-check

# Redis status
redis-cli ping

# Check external services
curl https://status.supabase.com/api/v2/status.json
```

## Mitigation Strategies

### Quick Wins (Try First)

#### 1. Restart Services
```bash
# Restart Vercel functions
vercel dev --force

# Clear Redis cache
redis-cli FLUSHALL

# Reset database connections
# (Happens automatically on Supabase)
```

#### 2. Enable Maintenance Mode
```typescript
// Set environment variable
vercel env add NEXT_PUBLIC_MAINTENANCE_MODE=true production

// Or use feature flag
updateFeatureFlag('maintenance_mode', true);
```

#### 3. Rollback Deployment
```bash
# List recent deployments
vercel list

# Instant rollback
vercel rollback [previous-deployment-url]

# Or promote old deployment
vercel alias [old-deployment] freshslate.com
```

### Service-Specific Responses

#### Database Issues
```sql
-- Check active connections
SELECT count(*) FROM pg_stat_activity;

-- Kill long-running queries
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE duration > interval '5 minutes';

-- Emergency connection pool reset
ALTER DATABASE freshslate SET CONNECTION LIMIT 50;
```

#### High Traffic/DDoS
```bash
# Enable Cloudflare Under Attack mode
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -d '{"value":"under_attack"}'

# Rate limit specific IPs
cloudflare-cli firewall create --action block --ip $BAD_IP
```

#### API Partner Outage
```typescript
// Switch to fallback partner
updatePartnerConfig({
  primary: 'partner_b',
  fallback: 'partner_c',
  circuit_breaker: true
});

// Or disable partner matching temporarily
featureFlag.set('partner_matching', false);
```

## Communication Templates

### Customer-Facing Status Page
```markdown
## Investigating Lead Submission Issues
**Posted**: [Time] PST

We are currently investigating reports of issues with lead submission. 
Our team is working to resolve this as quickly as possible.

**Update [Time+15min]**: We've identified the issue and are implementing a fix.

**Resolved [Time+30min]**: The issue has been resolved. All systems operational.
```

### Internal Updates (Every 15-30 min)
```
UPDATE [Time]:
- Current Status: [Investigating/Identified/Monitoring/Resolved]
- Actions Taken: [List actions]
- Next Steps: [What's happening next]
- ETA: [Best estimate]
```

### Partner Notification (If Needed)
```
Subject: FreshSlate API Service Disruption

Dear Partner,

We are currently experiencing [brief description] affecting [specific services].

Impact: [How it affects them]
ETA for resolution: [Time estimate]

We will update you every 30 minutes until resolved.

Technical contact: [email/phone]
```

## Resolution & Recovery

### Verify Fix
```bash
# Run smoke tests
ENVIRONMENT=production pnpm test:smoke

# Check key metrics
- Error rate back to normal (< 0.1%)
- Response times normal (< 300ms)
- Lead flow resumed
- No new Sentry errors

# Monitor for 30 minutes before declaring resolved
```

### Clear Caches
```bash
# Cloudflare
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -d '{"purge_everything":true}'

# Redis
redis-cli FLUSHALL

# Browser caches (update version)
vercel env add NEXT_PUBLIC_APP_VERSION=$(date +%s) production
```

### Update Status
```bash
# BetterStack
curl -X PATCH "https://uptime.betterstack.com/api/v2/incidents/$INCIDENT_ID" \
  -H "Authorization: Bearer $BETTERSTACK_TOKEN" \
  -d '{"status": "resolved"}'

# Slack
"✅ [SEV X] Incident Resolved: [Brief description]
Duration: [X minutes]
Root Cause: [One line summary]
Post-mortem: [Link to doc]"
```

## Post-Incident (Within 48 Hours)

### 1. Post-Mortem Document
```markdown
# Incident Post-Mortem: [Title]

## Summary
- **Date**: [Date]
- **Duration**: [Start] - [End] PST
- **Severity**: SEV [1-4]
- **Impact**: [User/business impact]

## Timeline
- [Time]: Initial report received
- [Time]: Incident declared
- [Time]: Root cause identified
- [Time]: Fix deployed
- [Time]: Incident resolved

## Root Cause
[Technical explanation of what went wrong]

## Contributing Factors
- [Factor 1]
- [Factor 2]

## Resolution
[What fixed the issue]

## Impact
- Leads lost: [Number]
- Revenue impact: $[Amount]
- Users affected: [Number]

## Lessons Learned
### What Went Well
- [Thing 1]
- [Thing 2]

### What Went Poorly
- [Thing 1]
- [Thing 2]

## Action Items
- [ ] [Owner]: [Action] by [Date]
- [ ] [Owner]: [Action] by [Date]

## Prevention
[How we'll prevent this in the future]
```

### 2. Update Runbooks
- Add new scenarios discovered
- Update contact information
- Improve detection methods
- Document new tools/scripts

### 3. Schedule Review Meeting
- All stakeholders present
- Review post-mortem
- Assign action items
- Set follow-up dates

## Emergency Contacts

### Escalation Chain
1. **On-Call Engineer**: Check PagerDuty
2. **Engineering Lead**: [Name] - [Phone]
3. **CTO**: [Name] - [Phone]
4. **CEO**: [Name] - [Phone] (SEV 1 only)

### External Contacts
- **Vercel Support**: enterprise@vercel.com
- **Supabase Support**: support@supabase.io
- **Cloudflare Support**: [Phone from dashboard]
- **Key Partner Contact**: [Name] - [Phone]

## Quick Reference Scripts

### Health Check All Services
```bash
#!/bin/bash
echo "🔍 System Health Check"
echo "====================="

# API Health
echo -n "API: "
curl -s https://freshslate.com/api/health | jq -r '.status'

# Database
echo -n "Database: "
pnpm db:health-check

# Redis
echo -n "Redis: "
redis-cli ping

# External Services
echo -n "Supabase: "
curl -s https://status.supabase.com/api/v2/status.json | jq -r '.status.description'

echo "====================="
```

### Emergency Notification
```bash
#!/bin/bash
# notify-incident.sh
MESSAGE=$1
SEVERITY=$2

# Slack
curl -X POST $SLACK_WEBHOOK \
  -d "{\"text\":\"🚨 [$SEVERITY] $MESSAGE\"}"

# PagerDuty
curl -X POST https://events.pagerduty.com/v2/enqueue \
  -H "Content-Type: application/json" \
  -d "{
    \"routing_key\": \"$PAGERDUTY_KEY\",
    \"event_action\": \"trigger\",
    \"payload\": {
      \"summary\": \"$MESSAGE\",
      \"severity\": \"error\",
      \"source\": \"freshslate\"
    }
  }"
```

// lib/notifications/telegram.ts
export async function sendTelegramNotification(message: string, type: 'info' | 'warning' | 'critical' = 'info') {
  const emoji = {
    info: 'ℹ️',
    warning: '⚠️',
    critical: '🚨'
  };
  
  await fetch(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: process.env.TELEGRAM_CHAT_ID,
      text: `${emoji[type]} ${message}`,
      parse_mode: 'HTML'
    })
  });
}

## Remember

1. **Stay Calm**: Panic makes things worse
2. **Communicate**: Over-communication is better than silence
3. **Document**: Write down everything you do
4. **Learn**: Every incident makes us better
5. **Blameless**: Focus on systems, not people

The goal is to restore service quickly while learning how to prevent future incidents.