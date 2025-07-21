# Research Documentation Command

Spawn multiple agents to research and scrape documentation for new technologies.

## Usage
```bash
/research-docs [technology-list]
/rd [technology-list]

# Example:
/research-docs "Stripe API, Resend Email, Pusher WebSockets"
```

## What It Does

1. **Spawns Specialized Research Agents**
   - One agent per technology
   - Each focuses on official documentation
   - Creates structured MD files

2. **Documentation Scraping Strategy**
   ```
   For each technology:
   1. Find official documentation URL
   2. Identify key sections:
      - Quick start / Getting started
      - API reference
      - Common patterns
      - Error handling
      - Rate limits
   3. Create condensed reference
   ```

3. **Output Structure**
   ```
   docs/research/
   ├── stripe-api-reference.md
   ├── resend-email-guide.md
   └── pusher-websockets.md
   ```

## Multi-Agent Pattern

```typescript
// Main orchestrator
const technologies = parseTechnologies(args);
const agents = [];

// Spawn research agents
for (const tech of technologies) {
  agents.push({
    persona: "researcher",
    task: `Research ${tech} documentation`,
    focus: [
      "Official docs only",
      "Implementation patterns",
      "Common gotchas",
      "Rate limits/quotas"
    ]
  });
}

// Execute in parallel
await Promise.all(agents.map(agent => 
  spawnResearchAgent(agent)
));

// Consolidate findings
return consolidateResearch(agents);
```

## Integration with PRD Workflow

```bash
# 1. Research new technologies first
/research-docs "Stripe, NextAuth, Prisma"

# 2. Reference in PRD creation
/prd payment-system
# PRD will now include:
# - docs/research/stripe-api-reference.md
# - Key patterns discovered
# - Implementation considerations

# 3. Tasks have documentation context
/gt payment-system
# Tasks reference specific docs sections
```

## Best Practices

1. **Focus on Official Docs**
   - No blog posts or tutorials
   - Latest stable version
   - Direct from source

2. **Extract Key Patterns**
   ```markdown
   ## Stripe Webhooks Pattern
   - Must validate signatures
   - Use raw body (not parsed)
   - Idempotency keys required
   - Retry logic: 3x with backoff
   ```

3. **Note Critical Gotchas**
   ```markdown
   ## Common Errors
   - Rate limit: 100 req/sec
   - Max payload: 512KB
   - Timeout: 120 seconds
   - Required headers: X-API-Key
   ```

## Output Example

```markdown
# Stripe API Reference
Generated: 2024-01-26
Source: https://stripe.com/docs/api

## Quick Start
- Install: `npm install stripe`
- Initialize: `const stripe = require('stripe')(key)`
- Test mode: use `sk_test_` keys

## Key Patterns

### Creating Customers
```javascript
const customer = await stripe.customers.create({
  email: 'customer@example.com',
  metadata: { userId: 'user_123' }
});
```

### Webhook Validation
```javascript
const sig = headers['stripe-signature'];
const event = stripe.webhooks.constructEvent(
  rawBody, sig, endpointSecret
);
```

## Rate Limits
- Live mode: 100 req/sec
- Test mode: 25 req/sec
- Webhooks: 30 sec timeout

## Common Gotchas
- Always use idempotency keys
- Store webhook endpoint secret securely
- Use webhook events for state changes
- Test with stripe CLI locally
```

This provides focused, actionable documentation that speeds up implementation.
