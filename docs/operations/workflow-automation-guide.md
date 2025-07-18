# FreshSlate Workflow Automation Guide

## Overview

We use n8n (self-hosted) and Make.com for workflow automation, reducing manual tasks and improving reliability.

## Automation Stack

- **n8n**: Self-hosted on Google Cloud Run for sensitive workflows
- **Make.com**: Cloud-based for simple integrations
- **Google Cloud Scheduler**: Cron jobs
- **Telegram Bot**: Team notifications

## n8n Workflows

### 1. Lead Processing Pipeline

```json
{
  "name": "Lead Processing Pipeline",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "lead-created",
        "responseMode": "onReceived",
        "responseData": "success"
      }
    },
    {
      "name": "Validate Lead",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "code": "// Validate lead data\nconst lead = $input.all()[0].json;\n\n// Check required fields\nif (!lead.email || !lead.phone || !lead.debt_amount) {\n  throw new Error('Missing required fields');\n}\n\n// Validate phone\nconst phoneRegex = /^\\d{10}$/;\nif (!phoneRegex.test(lead.phone.replace(/\\D/g, ''))) {\n  throw new Error('Invalid phone number');\n}\n\nreturn [{json: {...lead, validated: true}}];"
      }
    },
    {
      "name": "Check Duplicates",
      "type": "n8n-nodes-base.supabase",
      "parameters": {
        "operation": "select",
        "table": "leads",
        "filters": {
          "email": "={{ $json.email }}"
        }
      }
    },
    {
      "name": "Partner Matching",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.freshslate.com/v1/internal/match-partners",
        "method": "POST",
        "body": {
          "lead_id": "={{ $json.lead_id }}",
          "state": "={{ $json.state }}",
          "debt_amount": "={{ $json.debt_amount }}"
        }
      }
    },
    {
      "name": "Send to Partners",
      "type": "n8n-nodes-base.splitInBatches",
      "parameters": {
        "batchSize": 1
      }
    },
    {
      "name": "Notify Team",
      "type": "n8n-nodes-base.telegram",
      "parameters": {
        "chatId": "={{ $env.TELEGRAM_CHAT_ID }}",
        "text": "New Lead Processed:\nName: {{ $json.name }}\nDebt: ${{ $json.debt_amount }}\nPartners: {{ $json.matched_partners.length }}"
      }
    }
  ]
}
```

### 2. Daily Reporting Workflow

```yaml
Trigger: Every day at 9 AM PST
Steps:
  1. Query yesterday's metrics from BigQuery
  2. Generate report using Google Cloud Run function
  3. Upload to Google Drive
  4. Send summary to Telegram
  5. Update dashboard
```

### 3. Partner Performance Monitor

```yaml
Trigger: Every hour
Steps:
  1. Check partner response times
  2. Calculate acceptance rates
  3. Monitor API errors
  4. Alert if thresholds exceeded
  5. Auto-disable if critical failure
```

## Make.com Scenarios

### 1. Customer Communication Flow

```yaml
Trigger: Lead status change in Supabase
Modules:
  - Watch Supabase changes
  - Router (based on status)
    - Qualified: Send welcome email
    - Not Qualified: Send resources email
    - Converted: Send to CRM
  - Log to Google Sheets
```

### 2. Social Media Lead Capture

```yaml
Trigger: Facebook Lead Ad submission
Modules:
  - Facebook Lead Ads
  - Format data
  - POST to FreshSlate API
  - Add to email sequence
  - Notify sales team
```

## Google Cloud Run Functions

### Deployment Script

```bash
# deploy-function.sh
#!/bin/bash

FUNCTION_NAME=$1
REGION="us-central1"

# Build with Bun
bun run build

# Deploy to Cloud Run
gcloud run deploy $FUNCTION_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "NODE_ENV=production" \
  --memory 512Mi \
  --timeout 300
```

### Example Function: Generate Report

```typescript
// functions/generate-report/index.ts
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { generatePDF } from './pdf-generator';

const app = new Hono();

app.post('/generate-report', async (c) => {
  const { lead_id, template } = await c.req.json();
  
  // Fetch lead data
  const lead = await fetchLead(lead_id);
  
  // Generate PDF
  const pdf = await generatePDF(template, lead);
  
  // Upload to cloud storage
  const url = await uploadToGCS(pdf, `reports/${lead_id}.pdf`);
  
  // Notify via n8n webhook
  await fetch(process.env.N8N_WEBHOOK_URL, {
    method: 'POST',
    body: JSON.stringify({
      event: 'report_generated',
      lead_id,
      report_url: url
    })
  });
  
  return c.json({ success: true, url });
});

serve(app, { port: 8080 });
```

## Telegram Bot Commands

### Setup

```typescript
// bot/telegram-bot.ts
import { Telegraf } from 'telegraf';

const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN!);

// Commands for team
bot.command('stats', async (ctx) => {
  const stats = await getQuickStats();
  ctx.reply(`📊 Today's Stats:
  Leads: ${stats.leads_today}
  Qualified: ${stats.qualified_today}
  Conversion: ${stats.conversion_rate}%
  Revenue: $${stats.revenue_today}`);
});

bot.command('lead', async (ctx) => {
  const leadId = ctx.message.text.split(' ')[1];
  const lead = await getLead(leadId);
  ctx.reply(`Lead Details:
  Name: ${lead.name}
  Status: ${lead.status}
  Partner: ${lead.partner_name || 'Not matched'}`);
});

bot.command('alert', async (ctx) => {
  // Set up custom alerts
  const [_, type, threshold] = ctx.message.text.split(' ');
  await setAlert(ctx.chat.id, type, threshold);
  ctx.reply(`✅ Alert configured for ${type} > ${threshold}`);
});

bot.launch();
```

## Monitoring Automations

### n8n Health Check

```typescript
// monitors/n8n-health.ts
import { CronJob } from 'cron';

new CronJob('*/5 * * * *', async () => {
  try {
    const response = await fetch(`${N8N_URL}/healthz`);
    if (!response.ok) {
      await sendTelegramNotification('🚨 n8n is down!', 'critical');
    }
  } catch (error) {
    await sendTelegramNotification('🚨 n8n unreachable!', 'critical');
  }
});
```

## Security Considerations

### n8n Security

```yaml
Environment Variables:
  - Use Google Secret Manager
  - Rotate webhook tokens monthly
  - IP whitelist for admin access

Network:
  - Cloud Run with VPC connector
  - Private GKE cluster option
  - Firewall rules for webhooks
```

### Make.com Security

```yaml
Best Practices:
  - Use OAuth where possible
  - Store credentials in Make.com vault
  - Limit permissions to minimum required
  - Regular audit of scenarios
```

## Cost Optimization

### n8n on Cloud Run

```yaml
Configuration:
  Min instances: 0 (scale to zero)
  Max instances: 3
  Memory: 1GB
  CPU: 1
  Concurrency: 10

Cost: ~$20-50/month depending on usage
```

### Make.com Plan

```yaml
Recommended: Core plan ($99/month)
  - 10,000 operations
  - 5 minute interval
  - Unlimited scenarios

Alternative: Use n8n for everything (self-hosted)
```

## Common Automation Patterns

### 1. Retry with Exponential Backoff

```javascript
// n8n code node
const maxRetries = 3;
let attempt = 0;

while (attempt < maxRetries) {
  try {
    const result = await $http.post(url, data);
    return [{json: result}];
  } catch (error) {
    attempt++;
    if (attempt === maxRetries) throw error;
    
    const delay = Math.pow(2, attempt) * 1000;
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}
```

### 2. Batch Processing

```javascript
// Process leads in batches
const batchSize = 10;
const leads = $input.all();

for (let i = 0; i < leads.length; i += batchSize) {
  const batch = leads.slice(i, i + batchSize);
  await processBatch(batch);
  
  // Notify progress
  if (i % 50 === 0) {
    await $telegram.send(`Processed ${i}/${leads.length} leads`);
  }
}
```

### 3. Circuit Breaker

```javascript
// Prevent cascading failures
const circuitBreaker = {
  failures: 0,
  threshold: 5,
  timeout: 60000, // 1 minute
  lastFailure: null,
  
  async call(fn) {
    if (this.isOpen()) {
      throw new Error('Circuit breaker is open');
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  },
  
  isOpen() {
    return this.failures >= this.threshold && 
           Date.now() - this.lastFailure < this.timeout;
  },
  
  onSuccess() {
    this.failures = 0;
  },
  
  onFailure() {
    this.failures++;
    this.lastFailure = Date.now();
  }
};
```

## Debugging Workflows

### n8n Debug Mode

```bash
# Run n8n with debug logging
N8N_LOG_LEVEL=debug n8n start

# Test webhook locally
curl -X POST http://localhost:5678/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### Make.com Testing

1. Use "Run once" for testing
2. Check execution history
3. Use Data Store for debugging
4. Clone scenarios for testing

## Maintenance

### Weekly Tasks
- Review failed executions
- Check automation performance
- Update webhook URLs if needed
- Clean up test data

### Monthly Tasks
- Rotate API keys
- Review and optimize workflows
- Update documentation
- Cost analysis

Remember: Automation should make life easier, not more complex. Start simple and iterate!