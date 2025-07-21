# FreshSlate Deployment Runbook

## Overview

This runbook provides step-by-step instructions for deploying FreshSlate to production. Follow each step carefully and use the rollback procedures if issues arise.

## Pre-Deployment Checklist

### Code Readiness
- [ ] All PRs approved and merged to `develop`
- [ ] `develop` branch tested in staging
- [ ] No critical bugs in staging
- [ ] Performance metrics meet targets
- [ ] Security scan passed

### Team Communication
- [ ] Deployment window scheduled
- [ ] Team notified in Slack
- [ ] On-call engineer identified
- [ ] Customer support aware

### Environment Verification
```bash
# Verify staging is stable
curl https://staging.freshslate.com/api/health
# Should return: {"status":"healthy"}

# Check error rates
# Go to Sentry dashboard - should be < 0.1%

# Verify database migrations
pnpm db:migrate:status
# All migrations should show as "applied"
```

## Deployment Steps

### Step 1: Create Release Branch
```bash
# From your local machine
git checkout develop
git pull origin develop
git checkout -b release/v1.2.3
git push origin release/v1.2.3
```

### Step 2: Run Pre-Deployment Tests
```bash
# Run full test suite
pnpm test
pnpm test:e2e
pnpm test:integration

# Check bundle size
pnpm build
pnpm analyze
# Ensure < 300KB gzipped
```

### Step 3: Update Version Numbers
```bash
# Update package.json version
npm version minor # or major/patch

# Update changelog
echo "## v1.2.3 - $(date +%Y-%m-%d)" >> CHANGELOG.md
echo "- Feature: Description" >> CHANGELOG.md
echo "- Fix: Description" >> CHANGELOG.md

# Commit changes
git add .
git commit -m "chore: bump version to v1.2.3"
git push origin release/v1.2.3
```

### Step 4: Create Pull Request to Main
```bash
# Create PR from release/v1.2.3 to main
# Use GitHub UI or CLI:
gh pr create --base main --head release/v1.2.3 \
  --title "Release v1.2.3" \
  --body "Release notes: ..."
```

### Step 5: Final Verification
- [ ] CI/CD pipeline passes
- [ ] Preview deployment works
- [ ] Lighthouse scores acceptable
- [ ] No TypeScript errors
- [ ] No ESLint warnings

### Step 6: Database Migrations
```bash
# If migrations needed, run them BEFORE deploying code
# Connect to production database
export DATABASE_URL=$PRODUCTION_DATABASE_URL

# Check migration status
pnpm db:migrate:status

# Apply migrations
pnpm db:migrate:deploy

# Verify migrations
pnpm db:migrate:status
```

### Step 7: Deploy to Production

#### Option A: Merge to Main (Automatic)
```bash
# Merge the PR to main
# Vercel will automatically deploy
```

#### Option B: Manual Vercel Deployment
```bash
# If automatic deployment fails
vercel --prod

# Or promote from preview
vercel promote [deployment-url]
```

### Step 8: Post-Deployment Verification

#### Health Checks
```bash
# API health
curl https://api.freshslate.com/health
# Expected: {"status":"healthy","version":"1.2.3"}

# Page loads
curl -I https://freshslate.com
# Expected: HTTP/2 200

# Quiz flow
curl https://freshslate.com/quiz
# Should load without errors
```

#### Monitoring Checks
1. **Sentry**: Check for new errors
2. **BetterStack**: Verify uptime monitors green
3. **Analytics**: Confirm events flowing
4. **Database**: Check connection pool metrics

#### Smoke Tests
```bash
# Run production smoke tests
ENVIRONMENT=production pnpm test:smoke

# Manual testing checklist:
# - [ ] Landing page loads
# - [ ] Quiz starts properly
# - [ ] Form submission works
# - [ ] Thank you page shows
# - [ ] Analytics events fire
```

### Step 9: Clear CDN Cache
```bash
# Purge Cloudflare cache
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'
```

### Step 10: Update Status Page
```bash
# Update BetterStack status page
curl -X POST "https://uptime.betterstack.com/api/v2/monitors/$MONITOR_ID/maintenance" \
  -H "Authorization: Bearer $BETTERSTACK_TOKEN" \
  -d "status=resolved"
```

## Rollback Procedures

### Immediate Rollback (< 5 minutes)
```bash
# List recent deployments
vercel list

# Rollback to previous deployment
vercel rollback [previous-deployment-url]

# Or use instant rollback alias
vercel alias [old-deployment] freshslate.com
```

### Database Rollback
```bash
# If migrations need reverting
export DATABASE_URL=$PRODUCTION_DATABASE_URL

# Rollback last migration
pnpm db:migrate:rollback

# Or restore from backup
pg_restore -d $DATABASE_URL backups/pre-deployment-backup.sql
```

### Emergency Procedures
1. **Enable maintenance mode**
   ```bash
   vercel env pull
   echo "NEXT_PUBLIC_MAINTENANCE_MODE=true" >> .env.production
   vercel env add NEXT_PUBLIC_MAINTENANCE_MODE production
   vercel --prod
   ```

2. **Switch to fallback**
   ```bash
   # Point DNS to static fallback page
   cloudflare-cli dns update freshslate.com A 192.0.2.1
   ```

3. **Notify stakeholders**
   ```bash
   # Send alerts
   ./scripts/notify-incident.sh "Deployment rollback initiated"
   ```

## Post-Deployment Tasks

### Monitoring Period (2 hours)
- [ ] Watch error rates every 15 minutes
- [ ] Monitor performance metrics
- [ ] Check conversion rates
- [ ] Review user feedback
- [ ] Monitor database performance

### Documentation
- [ ] Update deployment log
- [ ] Document any issues encountered
- [ ] Update runbook if needed
- [ ] Share lessons learned

### Communication
```bash
# Notify team of successful deployment
curl -X POST $SLACK_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "text": "✅ Deployment v1.2.3 completed successfully",
    "attachments": [{
      "color": "good",
      "fields": [
        {"title": "Version", "value": "1.2.3", "short": true},
        {"title": "Environment", "value": "Production", "short": true},
        {"title": "Deployed by", "value": "'$USER'", "short": true},
        {"title": "Duration", "value": "X minutes", "short": true}
      ]
    }]
  }'
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

## Deployment Schedule

### Regular Deployments
- **Tuesday/Thursday**: 2:00 PM PST
- **Never on Friday**: Unless critical hotfix
- **Avoid**: Monday mornings, holidays

### Emergency Hotfixes
1. Create hotfix branch from main
2. Apply minimal fix
3. Fast-track through staging
4. Deploy immediately
5. Backport to develop

## Troubleshooting

### Common Issues

#### Build Failures
```bash
# Clear cache and rebuild
rm -rf .next
pnpm install --force
pnpm build
```

#### Environment Variables Missing
```bash
# Pull from Vercel
vercel env pull

# Verify all required vars
pnpm check:env
```

#### Database Connection Issues
```bash
# Test connection
pnpm db:test-connection

# Reset connection pool
vercel env rm DATABASE_URL production
vercel env add DATABASE_URL production
```

### Escalation Path
1. Try rollback procedures
2. Check troubleshooting guide
3. Contact on-call engineer
4. Escalate to CTO if needed

## Deployment Log Template

```markdown
## Deployment Log - v1.2.3

**Date**: 2024-XX-XX
**Time**: 14:00-14:30 PST
**Deployed by**: [Name]
**Type**: Regular / Hotfix

### Changes
- Feature: [Description]
- Fix: [Description]

### Pre-deployment metrics
- Error rate: 0.05%
- Avg response time: 245ms
- Conversion rate: 3.2%

### Post-deployment metrics
- Error rate: 0.04%
- Avg response time: 235ms
- Conversion rate: 3.3%

### Issues encountered
- None / [Description]

### Notes
- [Any additional observations]
```

## Contact List

- **On-call Engineer**: Check PagerDuty
- **DevOps Lead**: [Name] - [Phone]
- **CTO**: [Name] - [Phone]
- **Customer Success**: [Name] - [Email]

Remember: Stay calm, follow the procedures, and communicate clearly. Every deployment is a learning opportunity.