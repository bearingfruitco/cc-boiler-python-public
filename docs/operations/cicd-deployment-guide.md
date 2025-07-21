# CI/CD & Deployment Guide

## Overview

This guide covers the complete CI/CD pipeline, deployment strategies, and environment management for FreshSlate applications.

## GitHub Repository Structure

```
freshslate/
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   ├── CODEOWNERS         # Code ownership
│   ├── dependabot.yml     # Dependency updates
│   └── pull_request_template.md
├── apps/                   # Monorepo structure
│   ├── web/               # Main application
│   ├── admin/             # Admin dashboard
│   └── landing/           # Marketing pages
├── packages/              # Shared packages
│   ├── ui/                # Component library
│   ├── database/          # Database schemas
│   └── config/            # Shared configs
└── infrastructure/        # IaC files
    ├── terraform/
    └── kubernetes/
```

## Branch Protection Rules

```yaml
main:
  - Require pull request reviews (2)
  - Dismiss stale reviews
  - Require status checks
  - Require branches up to date
  - Include administrators
  - Restrict push access

develop:
  - Require pull request reviews (1)
  - Require status checks
  - Auto-merge enabled for bots

feature/*:
  - No restrictions
  - Auto-delete after merge
```

## CI Pipeline

### Pull Request Workflow

```yaml
# .github/workflows/pr.yml
name: Pull Request
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup pnpm
        uses: pnpm/action-setup@v3
        with:
          version: 9
          
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Type check
        run: pnpm typecheck
        
      - name: Lint
        run: pnpm lint
        
      - name: Format check
        run: pnpm format:check
        
      - name: Test
        run: pnpm test:ci
        
      - name: Build
        run: pnpm build
        
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  preview:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy Preview
        uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          
      - name: Comment Preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Preview: ${process.env.VERCEL_URL}`
            })
```

### Main Branch Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup deployment
        uses: pnpm/action-setup@v3
        with:
          version: 9
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: pnpm db:migrate:deploy
        
      - name: Deploy to Vercel
        uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          
      - name: Purge CDN
        run: |
          curl -X POST "https://api.cloudflare.com/client/v4/zones/${{ secrets.CLOUDFLARE_ZONE }}/purge_cache" \
            -H "Authorization: Bearer ${{ secrets.CLOUDFLARE_TOKEN }}" \
            -H "Content-Type: application/json" \
            --data '{"purge_everything":true}'
            
      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Environment Management

### Environment Variables

```bash
# .env.example
# ===== Required for all environments =====
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000

# ===== Database =====
DATABASE_URL=postgresql://user:pass@localhost:5432/freshslate
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_ROLE_KEY=xxx

# ===== Analytics =====
NEXT_PUBLIC_RUDDERSTACK_KEY=xxx
NEXT_PUBLIC_RUDDERSTACK_URL=https://xxx.dataplane.rudderstack.com

# ===== Monitoring =====
NEXT_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ORG=freshslate
SENTRY_PROJECT=web
SENTRY_AUTH_TOKEN=xxx

# ===== External Services =====
BETTERSTACK_TOKEN=xxx
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxx

# ===== Security =====
SESSION_SECRET=xxx # min 32 chars
ENCRYPTION_KEY=xxx # 64 hex chars
CRON_SECRET=xxx

# ===== Feature Flags =====
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_CHAT=false
```

### Vercel Environment Setup

```typescript
// scripts/setup-vercel-env.ts
import { vercel } from '@vercel/client';

const environments = ['production', 'preview', 'development'];

async function setupEnvironment(env: string) {
  const secrets = {
    // Database
    DATABASE_URL: { value: process.env[`${env}_DATABASE_URL`], target: [env] },
    SUPABASE_SERVICE_ROLE_KEY: { value: process.env[`${env}_SUPABASE_KEY`], target: [env] },
    
    // Add all other secrets...
  };
  
  for (const [key, config] of Object.entries(secrets)) {
    await vercel.env.add({
      key,
      value: config.value,
      target: config.target,
    });
  }
}
```

## Database Migrations

### Migration Workflow

```bash
# Create migration
pnpm db:migrate:create add_user_preferences

# Apply migration locally
pnpm db:migrate:up

# Generate types
pnpm db:generate:types

# Deploy to production
pnpm db:migrate:deploy
```

### Migration CI/CD

```yaml
# .github/workflows/migration.yml
name: Database Migration
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  migrate:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          pnpm install
          pnpm db:migrate:deploy
          
      - name: Verify migration
        run: pnpm db:migrate:status
```

## Deployment Strategies

### Blue-Green Deployment

```typescript
// vercel.json
{
  "functions": {
    "app/api/*": {
      "maxDuration": 10
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Deployment-Id",
          "value": "{{VERCEL_DEPLOYMENT_ID}}"
        }
      ]
    }
  ]
}
```

### Canary Releases

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const canaryPercentage = 10; // 10% of traffic
  const isCanary = Math.random() * 100 < canaryPercentage;
  
  if (isCanary && process.env.CANARY_URL) {
    return NextResponse.rewrite(new URL(process.env.CANARY_URL));
  }
}
```

### Feature Flags

```typescript
// lib/features.ts
import { Vercel } from '@vercel/edge-config';

export async function isFeatureEnabled(
  feature: string,
  userId?: string
): boolean {
  const flags = await Vercel.get('feature-flags');
  const flag = flags[feature];
  
  if (!flag) return false;
  
  // Check if enabled globally
  if (flag.enabled) return true;
  
  // Check if user in rollout
  if (userId && flag.rollout) {
    const hash = hashUserId(userId);
    return hash < flag.rollout;
  }
  
  return false;
}
```

## Monitoring Deployments

### Health Checks

```typescript
// app/api/health/deployment/route.ts
export async function GET() {
  return Response.json({
    deployment: {
      id: process.env.VERCEL_DEPLOYMENT_ID,
      git_commit: process.env.VERCEL_GIT_COMMIT_SHA,
      git_branch: process.env.VERCEL_GIT_COMMIT_REF,
      deployed_at: process.env.VERCEL_DEPLOYED_AT,
    },
    status: 'healthy',
    timestamp: new Date().toISOString(),
  });
}
```

### Deployment Notifications

```typescript
// scripts/notify-deployment.ts
async function notifyDeployment() {
  const deployment = {
    environment: process.env.VERCEL_ENV,
    url: process.env.VERCEL_URL,
    commit: process.env.VERCEL_GIT_COMMIT_SHA,
    author: process.env.VERCEL_GIT_COMMIT_AUTHOR_NAME,
  };
  
  // Sentry release
  await createSentryRelease(deployment);
  
  // Slack notification
  await sendSlackNotification(deployment);
  
  // Update BetterStack
  await updateMonitor(deployment);
}
```

## Rollback Procedures

### Instant Rollback

```bash
# List recent deployments
vercel list

# Rollback to specific deployment
vercel rollback [deployment-url]

# Or use GitHub Actions
gh workflow run rollback -f deployment_id=xxx
```

### Database Rollback

```bash
# Rollback last migration
pnpm db:migrate:down

# Rollback to specific version
pnpm db:migrate:down --to 20240115120000

# Emergency SQL rollback
psql $DATABASE_URL < backups/pre-deployment.sql
```

## Performance Monitoring

### Build Performance

```yaml
# Track build times
- name: Build Performance
  run: |
    START_TIME=$(date +%s)
    pnpm build
    END_TIME=$(date +%s)
    BUILD_TIME=$((END_TIME - START_TIME))
    
    curl -X POST https://api.betterstack.com/metrics \
      -H "Authorization: Bearer ${{ secrets.BETTERSTACK_TOKEN }}" \
      -d "build_time=$BUILD_TIME"
```

### Bundle Analysis

```json
// package.json
{
  "scripts": {
    "analyze": "ANALYZE=true pnpm build",
    "analyze:server": "BUNDLE_ANALYZE=server pnpm build",
    "analyze:browser": "BUNDLE_ANALYZE=browser pnpm build"
  }
}
```

## Security Scanning

### Dependency Scanning

```yaml
# .github/workflows/security.yml
- name: Audit dependencies
  run: pnpm audit --audit-level=high

- name: Check licenses
  run: pnpm licenses list --prod

- name: Scan for secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: ${{ github.event.repository.default_branch }}
```

## Deployment Checklist

### Pre-Deployment

```markdown
- [ ] All tests passing
- [ ] Type checking passes
- [ ] No linting errors
- [ ] Bundle size acceptable
- [ ] Database migrations ready
- [ ] Environment variables updated
- [ ] Feature flags configured
- [ ] Monitoring alerts configured
```

### Post-Deployment

```markdown
- [ ] Health checks passing
- [ ] No error spike in Sentry
- [ ] Performance metrics normal
- [ ] Database queries performant
- [ ] CDN cache purged
- [ ] Stakeholders notified
- [ ] Documentation updated
```

## Disaster Recovery

### Backup Strategy

```yaml
Production:
  - Database: Hourly snapshots, 7-day retention
  - Redis: Daily backups, 3-day retention
  - Code: Git history + deployment snapshots
  - Env vars: Encrypted in Vercel + 1Password

Recovery:
  - RTO: 15 minutes
  - RPO: 1 hour
```

### Emergency Procedures

```bash
# 1. Immediate response
vercel rollback # Rollback application

# 2. Database recovery
pg_restore -d $DATABASE_URL backup.dump

# 3. Clear caches
redis-cli FLUSHALL

# 4. Notify team
./scripts/notify-incident.sh "Emergency rollback initiated"
```

---

A robust CI/CD pipeline is the backbone of reliable software delivery. Automate everything, monitor constantly, and always have a rollback plan.