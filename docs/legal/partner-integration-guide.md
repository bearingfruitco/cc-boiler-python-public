# FreshSlate Partner Integration Guide

## Overview

This guide provides technical documentation for integrating new debt resolution partners into the FreshSlate platform. Partners receive qualified leads through our API based on matching criteria.

## Partner Types

### 1. Debt Settlement Companies
- Handle unsecured debt (credit cards, medical bills)
- Require minimum $10,000 debt
- Work in specific states only

### 2. Credit Counseling Agencies
- Non-profit organizations
- Handle all debt amounts
- Nationwide coverage

### 3. Bankruptcy Attorneys
- State-specific licensing
- Handle severe financial distress
- Referral-only model

### 4. Debt Consolidation Lenders
- Require good credit (650+)
- Maximum debt-to-income ratios
- Loan amount limits

## Integration Process

### Phase 1: Business Setup (Week 1)

#### Required Documentation
- [ ] Business license
- [ ] Insurance certificates
- [ ] State registrations
- [ ] Compliance certifications
- [ ] Privacy policy
- [ ] Terms of service

#### Commercial Agreement
```yaml
Contract Terms:
  - Lead pricing model (PPL/RevShare)
  - Volume commitments
  - Quality standards
  - SLA requirements
  - Payment terms
  - Termination clauses
```

#### Partner Profile Setup
```typescript
interface PartnerProfile {
  // Basic Information
  company_name: string;
  company_type: 'settlement' | 'counseling' | 'attorney' | 'lender';
  tax_id: string;
  
  // Contact Information
  primary_contact: {
    name: string;
    email: string;
    phone: string;
  };
  technical_contact: {
    name: string;
    email: string;
    phone: string;
  };
  
  // Coverage
  states_licensed: string[];
  services_offered: string[];
  
  // Lead Criteria
  min_debt_amount: number;
  max_debt_amount: number;
  debt_types_accepted: DebtType[];
  credit_score_requirements?: {
    min?: number;
    max?: number;
  };
  
  // Business Rules
  business_hours: {
    timezone: string;
    monday: { open: string; close: string };
    // ... other days
  };
  lead_cap_daily?: number;
  lead_cap_monthly?: number;
}
```

### Phase 2: Technical Integration (Week 2)

#### API Credentials
```bash
# Generate partner API credentials
POST /api/admin/partners
{
  "company_name": "Partner Company",
  "type": "settlement",
  "technical_contact_email": "tech@partner.com"
}

# Response
{
  "partner_id": "part_2kj3h4k2j3h4",
  "api_key": "sk_live_...",
  "webhook_secret": "whsec_...",
  "environment": "sandbox"
}
```

#### Webhook Configuration
```typescript
// Partner webhook endpoint requirements
interface WebhookPayload {
  event: 'lead.created' | 'lead.updated' | 'test.ping';
  created_at: string;
  data: {
    lead_id: string;
    partner_reference_id: string;
    lead_data: PartnerLead;
  };
  signature: string; // HMAC-SHA256
}

// Example webhook handler (partner side)
app.post('/webhooks/freshslate', (req, res) => {
  // Verify signature
  const signature = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(JSON.stringify(req.body))
    .digest('hex');
    
  if (signature !== req.headers['x-freshslate-signature']) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  // Process lead
  const { event, data } = req.body;
  
  switch (event) {
    case 'lead.created':
      await processNewLead(data.lead_data);
      break;
    case 'lead.updated':
      await updateLead(data.lead_id, data.lead_data);
      break;
  }
  
  // Acknowledge receipt
  res.json({ received: true });
});
```

#### Lead Acceptance API
```typescript
// POST /api/v1/partners/leads/{lead_id}/accept
{
  "partner_reference_id": "your-internal-id",
  "estimated_savings": 15000,
  "program_length_months": 36,
  "monthly_payment": 450,
  "agent_assigned": {
    "name": "John Smith",
    "email": "john@partner.com",
    "phone": "555-0123"
  }
}

// POST /api/v1/partners/leads/{lead_id}/reject
{
  "reason": "outside_service_area" | "debt_too_low" | "duplicate" | "other",
  "reason_detail": "Optional explanation"
}
```

### Phase 3: Testing & Validation (Week 3)

#### Sandbox Testing
```typescript
// Test lead generator
async function generateTestLead(): Promise<TestLead> {
  return {
    name: `Test User ${Date.now()}`,
    email: `test+${Date.now()}@freshslate.com`,
    phone: '5555551234',
    state: 'CA',
    debt_amount: 25000,
    debt_types: ['credit_card', 'medical'],
    monthly_payment: 800,
    credit_score_range: 'fair',
    // Test flag prevents billing
    _test_mode: true,
  };
}

// Integration test suite
describe('Partner Integration', () => {
  test('receives webhook on lead creation', async () => {
    const lead = await generateTestLead();
    const webhook = await waitForWebhook(30000); // 30s timeout
    
    expect(webhook.event).toBe('lead.created');
    expect(webhook.data.lead_data.email).toBe(lead.email);
  });
  
  test('accepts lead successfully', async () => {
    const lead = await generateTestLead();
    
    const response = await partnerApi.acceptLead(lead.id, {
      partner_reference_id: 'TEST-123',
      estimated_savings: 10000,
    });
    
    expect(response.status).toBe('accepted');
  });
  
  test('handles rejection properly', async () => {
    const lead = await generateTestLead();
    
    const response = await partnerApi.rejectLead(lead.id, {
      reason: 'debt_too_low',
    });
    
    expect(response.status).toBe('rejected');
  });
});
```

#### Validation Checklist
- [ ] Webhook delivery confirmed
- [ ] Signature validation working
- [ ] Lead acceptance flow tested
- [ ] Lead rejection flow tested
- [ ] Error handling verified
- [ ] Rate limiting respected
- [ ] Timeout handling implemented

### Phase 4: Production Launch (Week 4)

#### Go-Live Steps

1. **Production Credentials**
   ```bash
   # Switch from sandbox to production
   PUT /api/admin/partners/{partner_id}/promote
   {
     "environment": "production",
     "confirmed": true
   }
   ```

2. **Gradual Rollout**
   ```typescript
   // Traffic allocation configuration
   const partnerConfig = {
     partner_id: 'part_2kj3h4k2j3h4',
     status: 'active',
     traffic_allocation: {
       percentage: 10, // Start with 10% of matching leads
       ramp_schedule: [
         { day: 1, percentage: 10 },
         { day: 7, percentage: 25 },
         { day: 14, percentage: 50 },
         { day: 30, percentage: 100 },
       ],
     },
   };
   ```

3. **Monitoring Setup**
   - Lead delivery metrics
   - Acceptance/rejection rates
   - Response times
   - Error rates

## API Reference

### Authentication
```bash
# API Key in header
curl -H "Authorization: Bearer sk_live_..." \
  https://api.freshslate.com/v1/partners/profile
```

### Endpoints

#### Get Partner Profile
```bash
GET /api/v1/partners/profile

Response:
{
  "partner_id": "part_2kj3h4k2j3h4",
  "company_name": "ABC Debt Relief",
  "status": "active",
  "stats": {
    "leads_received_today": 45,
    "leads_received_month": 892,
    "acceptance_rate": 0.73,
    "average_response_time": 145 // seconds
  }
}
```

#### Update Lead Criteria
```bash
PUT /api/v1/partners/criteria
{
  "min_debt_amount": 15000,
  "states_licensed": ["CA", "TX", "FL", "NY"],
  "debt_types_accepted": ["credit_card", "medical", "personal_loan"],
  "business_hours": {
    "timezone": "America/Los_Angeles",
    "monday": { "open": "08:00", "close": "18:00" }
  }
}
```

#### Get Lead Details
```bash
GET /api/v1/partners/leads/{lead_id}

Response:
{
  "lead_id": "lead_9k3j4h5k3j4h5",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-01-15T11:00:00Z", // 30 min to respond
  "data": {
    "debt_amount": 25000,
    "state": "CA",
    "debt_types": ["credit_card"],
    // ... other fields per agreement
  }
}
```

#### Lead Status Webhook
```bash
POST /api/v1/partners/leads/{lead_id}/status
{
  "status": "contacted" | "enrolled" | "rejected" | "completed",
  "contacted_at": "2024-01-15T10:45:00Z",
  "notes": "Client enrolled in 36-month program"
}
```

## Lead Matching Algorithm

### Matching Criteria
```typescript
interface MatchingCriteria {
  // Hard requirements (must match)
  state: string;
  debt_amount: number;
  
  // Soft requirements (scoring)
  debt_types: string[];
  credit_score?: string;
  