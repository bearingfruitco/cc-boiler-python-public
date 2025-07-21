# FreshSlate Data Privacy Handbook

## Overview

This handbook outlines our data privacy practices, compliance procedures, and implementation guidelines for GDPR, CCPA, and other privacy regulations.

## Privacy Principles

1. **Minimal Collection**: Only collect data necessary for service
2. **Purpose Limitation**: Use data only for stated purposes
3. **Transparency**: Clear communication about data use
4. **User Control**: Easy access, correction, and deletion
5. **Security First**: Protect data at rest and in transit
6. **Privacy by Design**: Built into every feature

## Data Classification

### Personal Identifiable Information (PII)
```typescript
interface PII {
  // Direct Identifiers
  name: string;
  email: string;
  phone: string;
  
  // Indirect Identifiers
  ip_address: string;
  device_id: string;
  
  // Sensitive Financial
  debt_amount: number;
  monthly_income: number;
  credit_score_range: string;
}
```

### Data Sensitivity Levels

| Level | Description | Examples | Storage | Retention |
|-------|-------------|----------|---------|-----------|
| **Critical** | Direct PII | Name, Email, Phone, SSN | Encrypted | 90 days* |
| **High** | Financial data | Debt amount, Income | Encrypted | 2 years |
| **Medium** | Behavioral | Page views, Clicks | Standard | 1 year |
| **Low** | Anonymous | Aggregated stats | Standard | Indefinite |

*Or until purpose fulfilled

## GDPR Compliance

### Legal Basis for Processing

1. **Consent**: For marketing communications
2. **Legitimate Interest**: For lead matching services
3. **Contract**: For service delivery
4. **Legal Obligation**: For compliance/audits

### Implementation

#### Cookie Consent
```typescript
// components/CookieConsent.tsx
import { useState, useEffect } from 'react';

export function CookieConsent() {
  const [consent, setConsent] = useState<{
    necessary: boolean;
    analytics: boolean;
    marketing: boolean;
  } | null>(null);

  const handleAcceptAll = () => {
    const fullConsent = {
      necessary: true,
      analytics: true,
      marketing: true,
      timestamp: new Date().toISOString(),
    };
    
    localStorage.setItem('cookie_consent', JSON.stringify(fullConsent));
    setConsent(fullConsent);
    initializeServices(fullConsent);
  };

  const handleAcceptSelected = (selected: Partial<typeof consent>) => {
    const customConsent = {
      necessary: true, // Always required
      analytics: selected.analytics || false,
      marketing: selected.marketing || false,
      timestamp: new Date().toISOString(),
    };
    
    localStorage.setItem('cookie_consent', JSON.stringify(customConsent));
    setConsent(customConsent);
    initializeServices(customConsent);
  };

  return consent === null ? (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg p-6">
      <div className="max-w-6xl mx-auto">
        <h3 className="text-size-2 font-semibold mb-3">Cookie Settings</h3>
        <p className="text-size-3 text-gray-600 mb-4">
          We use cookies to improve your experience. You can choose which cookies you're happy for us to use.
        </p>
        
        <div className="space-y-3 mb-6">
          <label className="flex items-center">
            <input type="checkbox" checked disabled className="mr-3" />
            <span>Necessary (Required)</span>
          </label>
          
          <label className="flex items-center">
            <input type="checkbox" id="analytics" className="mr-3" />
            <span>Analytics (Help us improve)</span>
          </label>
          
          <label className="flex items-center">
            <input type="checkbox" id="marketing" className="mr-3" />
            <span>Marketing (Personalized ads)</span>
          </label>
        </div>
        
        <div className="flex gap-4">
          <button onClick={handleAcceptAll} className="px-6 py-2 bg-blue-600 text-white rounded">
            Accept All
          </button>
          <button onClick={() => handleAcceptSelected({...})} className="px-6 py-2 border rounded">
            Accept Selected
          </button>
        </div>
      </div>
    </div>
  ) : null;
}
```

#### Data Access Request
```typescript
// app/api/privacy/access/route.ts
export async function POST(request: Request) {
  const { email, verification_code } = await request.json();
  
  // Verify identity
  const verified = await verifyIdentity(email, verification_code);
  if (!verified) {
    return Response.json({ error: 'Verification failed' }, { status: 401 });
  }
  
  // Gather all user data
  const userData = await gatherUserData(email);
  
  // Generate report
  const report = {
    generated_at: new Date().toISOString(),
    data_categories: {
      profile: userData.profile,
      leads: userData.leads,
      analytics: userData.analytics,
      communications: userData.communications,
    },
    data_sources: [
      'Application Database',
      'Analytics System',
      'Email Service',
    ],
    third_party_sharing: [
      'Debt resolution partners (with consent)',
      'Analytics providers (anonymized)',
    ],
  };
  
  // Log access request
  await logPrivacyRequest('access', email);
  
  return Response.json(report);
}

async function gatherUserData(email: string) {
  const [profile, leads, analytics, communications] = await Promise.all([
    supabase.from('users').select('*').eq('email', email).single(),
    supabase.from('leads').select('*').eq('email', email),
    getAnalyticsData(email),
    getEmailHistory(email),
  ]);
  
  return { profile, leads, analytics, communications };
}
```

#### Right to Erasure
```typescript
// app/api/privacy/delete/route.ts
export async function POST(request: Request) {
  const { email, verification_code, confirmation } = await request.json();
  
  // Verify identity and confirmation
  if (!confirmation || confirmation !== 'DELETE MY DATA') {
    return Response.json({ error: 'Confirmation required' }, { status: 400 });
  }
  
  const verified = await verifyIdentity(email, verification_code);
  if (!verified) {
    return Response.json({ error: 'Verification failed' }, { status: 401 });
  }
  
  // Execute deletion
  await executeDataDeletion(email);
  
  return Response.json({ 
    message: 'Data deletion completed',
    retention_notice: 'Some data may be retained for legal compliance',
  });
}

async function executeDataDeletion(email: string) {
  // Start transaction
  const deletionLog = await startDeletionLog(email);
  
  try {
    // 1. Anonymize leads (keep for business records)
    await supabase
      .from('leads')
      .update({
        name: 'DELETED',
        email: `deleted-${Date.now()}@example.com`,
        phone: '0000000000',
        ip_address: '0.0.0.0',
        deleted_at: new Date().toISOString(),
      })
      .eq('email', email);
    
    // 2. Delete from analytics
    await deleteAnalyticsData(email);
    
    // 3. Remove from email lists
    await unsubscribeAll(email);
    
    // 4. Delete from partner systems
    await notifyPartnersDeletion(email);
    
    // 5. Clear caches
    await clearUserCaches(email);
    
    await completeDeletionLog(deletionLog.id, 'success');
  } catch (error) {
    await completeDeletionLog(deletionLog.id, 'failed', error);
    throw error;
  }
}
```

### Data Portability
```typescript
// lib/privacy/portability.ts
export async function exportUserData(email: string): Promise<Blob> {
  const userData = await gatherUserData(email);
  
  // Format as JSON
  const jsonExport = JSON.stringify(userData, null, 2);
  
  // Also create CSV for leads
  const csvExport = convertToCSV(userData.leads);
  
  // Create zip file
  const zip = new JSZip();
  zip.file('user_data.json', jsonExport);
  zip.file('leads.csv', csvExport);
  zip.file('README.txt', generateReadme());
  
  return await zip.generateAsync({ type: 'blob' });
}
```

## CCPA Compliance

### California Consumer Rights

1. **Right to Know**: What data we collect
2. **Right to Delete**: Request deletion
3. **Right to Opt-Out**: Of data sale
4. **Right to Non-Discrimination**: Equal service

### Implementation

#### Do Not Sell Signal
```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Check for GPC (Global Privacy Control)
  const gpc = request.headers.get('sec-gpc');
  if (gpc === '1') {
    response.cookies.set('opt_out_sale', 'true', {
      maxAge: 60 * 60 * 24 * 365, // 1 year
      sameSite: 'lax',
      secure: true,
    });
  }
  
  return response;
}
```

#### Opt-Out Page
```typescript
// app/privacy/opt-out/page.tsx
export default function OptOutPage() {
  const [opted, setOpted] = useState(false);
  
  const handleOptOut = async () => {
    await fetch('/api/privacy/opt-out', {
      method: 'POST',
      body: JSON.stringify({ opt_out: true }),
    });
    
    setOpted(true);
  };
  
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-size-1 font-semibold mb-6">
        Do Not Sell My Personal Information
      </h1>
      
      {!opted ? (
        <>
          <p className="text-size-3 mb-6">
            You have the right to opt-out of the sale of your personal information.
            Clicking below will prevent us from sharing your data with partners
            for monetary consideration.
          </p>
          
          <button 
            onClick={handleOptOut}
            className="px-6 py-3 bg-blue-600 text-white rounded"
          >
            Opt Out of Sale
          </button>
        </>
      ) : (
        <div className="bg-green-50 p-4 rounded">
          <p className="text-green-800">
            ✓ You have successfully opted out of the sale of your personal information.
          </p>
        </div>
      )}
    </div>
  );
}
```

## Data Security Measures

### Encryption

#### At Rest
```typescript
// lib/encryption.ts
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const algorithm = 'aes-256-gcm';
const key = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex');

export function encryptPII(data: string): string {
  const iv = randomBytes(16);
  const cipher = createCipheriv(algorithm, key, iv);
  
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return iv.toString('hex') + ':' + authTag.toString('hex') + ':' + encrypted;
}

export function decryptPII(encryptedData: string): string {
  const parts = encryptedData.split(':');
  const iv = Buffer.from(parts[0], 'hex');
  const authTag = Buffer.from(parts[1], 'hex');
  const encrypted = parts[2];
  
  const decipher = createDecipheriv(algorithm, key, iv);
  decipher.setAuthTag(authTag);
  
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}
```

#### In Transit
- All connections use TLS 1.3+
- HSTS enabled with preload
- Certificate pinning for mobile apps

### Access Control

```typescript
// lib/privacy/access-control.ts
export const dataAccessLevels = {
  public: ['page_views', 'general_stats'],
  authenticated: ['own_profile', 'own_leads'],
  support: ['user_search', 'lead_status'],
  admin: ['all_data', 'exports', 'deletion'],
};

export async function checkDataAccess(
  user: User,
  dataType: string,
  resourceId?: string
): Promise<boolean> {
  // Check role-based access
  const allowedTypes = dataAccessLevels[user.role] || [];
  if (!allowedTypes.includes(dataType)) {
    return false;
  }
  
  // Check resource ownership
  if (resourceId && user.role === 'authenticated') {
    return await isResourceOwner(user.id, resourceId);
  }
  
  // Log access attempt
  await logDataAccess(user.id, dataType, resourceId);
  
  return true;
}
```

### Audit Logging

```typescript
// lib/privacy/audit.ts
interface PrivacyAuditLog {
  id: string;
  timestamp: Date;
  user_id?: string;
  action: 'access' | 'modify' | 'delete' | 'export';
  resource_type: string;
  resource_id?: string;
  ip_address: string;
  user_agent: string;
  result: 'success' | 'denied' | 'error';
  metadata?: Record<string, any>;
}

export async function logPrivacyEvent(
  action: PrivacyAuditLog['action'],
  details: Partial<PrivacyAuditLog>
): Promise<void> {
  const log: PrivacyAuditLog = {
    id: crypto.randomUUID(),
    timestamp: new Date(),
    action,
    ip_address: getClientIp(),
    user_agent: getUserAgent(),
    result: 'success',
    ...details,
  };
  
  // Write to append-only audit table
  await supabase
    .from('privacy_audit_logs')
    .insert(log);
  
  // Alert on suspicious activity
  if (await isSuspiciousActivity(log)) {
    await alertSecurityTeam(log);
  }
}
```

## Data Retention & Disposal

### Retention Schedule

```yaml
Lead Data:
  Active: 90 days
  Archived: 2 years
  Deletion: Automatic after archive period

Analytics:
  Raw Events: 13 months
  Aggregated: Indefinite
  PII in Events: 90 days

Communications:
  Email History: 1 year
  SMS History: 90 days
  Call Recordings: Not stored

Financial Data:
  Debt Information: 7 years (legal requirement)
  Income Data: 2 years
  Credit Info: Until purpose fulfilled
```

### Automated Disposal

```typescript
// scripts/data-disposal.ts
import { CronJob } from 'cron';

// Run daily at 2 AM
new CronJob('0 2 * * *', async () => {
  console.log('Starting data disposal job');
  
  // Delete expired leads
  const expiredLeads = await supabase
    .from('leads')
    .delete()
    .lt('created_at', getRetentionDate('leads'))
    .eq('archived', true);
  
  // Anonymize old analytics
  await anonymizeAnalytics();
  
  // Clear old audit logs
  await pruneAuditLogs();
  
  // Report results
  await reportDisposalResults({
    leads_deleted: expiredLeads.count,
    analytics_anonymized: true,
    logs_pruned: true,
  });
});

function getRetentionDate(dataType: string): Date {
  const retentionDays = {
    leads: 730, // 2 years
    analytics: 395, // 13 months
    audit_logs: 2555, // 7 years
  };
  
  const date = new Date();
  date.setDate(date.getDate() - retentionDays[dataType]);
  return date;
}
```

## Privacy Notices & Consent

### Privacy Policy Requirements

Must include:
1. Data types collected
2. Purpose of collection
3. Legal basis
4. Third-party sharing
5. Retention periods
6. User rights
7. Contact information

### Consent Management

```typescript
// lib/privacy/consent.ts
interface ConsentRecord {
  user_id: string;
  type: 'marketing' | 'analytics' | 'partners';
  granted: boolean;
  timestamp: Date;
  ip_address: string;
  version: string;
  withdrawal_timestamp?: Date;
}

export async function recordConsent(
  userId: string,
  type: ConsentRecord['type'],
  granted: boolean
): Promise<void> {
  const consent: ConsentRecord = {
    user_id: userId,
    type,
    granted,
    timestamp: new Date(),
    ip_address: getClientIp(),
    version: PRIVACY_POLICY_VERSION,
  };
  
  await supabase
    .from('consent_records')
    .insert(consent);
  
  // Update user preferences
  await updateUserPreferences(userId, { [type]: granted });
  
  // Sync with partners if withdrawn
  if (!granted) {
    await syncConsentWithdrawal(userId, type);
  }
}
```

## Third-Party Data Sharing

### Partner Data Sharing Agreement Template

```markdown
## Data Processing Agreement

Between: FreshSlate ("Controller")
And: [Partner Name] ("Processor")

### 1. Processing Scope
- Data Types: [List specific fields]
- Purpose: Lead matching and debt resolution services
- Duration: Until service completion or consent withdrawal

### 2. Processor Obligations
- Process only on documented instructions
- Ensure confidentiality
- Implement appropriate security measures
- Assist with compliance obligations
- Delete/return data after processing

### 3. Sub-processing
- Prior written consent required
- Same obligations apply

### 4. Security Measures
- Encryption in transit and at rest
- Access controls
- Regular security assessments
- Incident notification within 24 hours

### 5. Audit Rights
- Annual audits permitted
- 30-day notice required
```

### API Data Filtering

```typescript
// lib/privacy/data-filtering.ts
export function filterLeadDataForPartner(
  lead: Lead,
  partner: Partner
): PartnerLead {
  // Check consent
  if (!lead.partner_consent) {
    throw new Error('No consent for partner sharing');
  }
  
  // Filter based on partner agreement
  const allowedFields = partner.allowed_fields || DEFAULT_PARTNER_FIELDS;
  
  const filtered = {};
  for (const field of allowedFields) {
    if (field in lead && !NEVER_SHARE_FIELDS.includes(field)) {
      filtered[field] = lead[field];
    }
  }
  
  // Add sharing metadata
  filtered._shared_at = new Date().toISOString();
  filtered._shared_with = partner.id;
  filtered._consent_version = lead.consent_version;
  
  // Log sharing event
  logDataSharing(lead.id, partner.id, Object.keys(filtered));
  
  return filtered as PartnerLead;
}

const NEVER_SHARE_FIELDS = [
  'password_hash',
  'session_tokens',
  'internal_notes',
  'fraud_score',
];
```

## Incident Response

### Data Breach Procedure

1. **Immediate Actions** (0-4 hours)
   - Contain the breach
   - Assess scope and impact
   - Preserve evidence
   - Notify security team

2. **Investigation** (4-24 hours)
   - Determine what data was affected
   - Identify affected individuals
   - Understand attack vector
   - Document timeline

3. **Notification** (24-72 hours)
   - Notify authorities (if required)
   - Prepare user notifications
   - Update privacy policy
   - Inform partners

4. **Remediation**
   - Fix vulnerabilities
   - Enhance security measures
   - Update procedures
   - Conduct training

### Breach Notification Template

```typescript
// templates/breach-notification.tsx
export function BreachNotificationEmail({ user, breach }) {
  return (
    <EmailTemplate>
      <h1>Important Security Update</h1>
      
      <p>Dear {user.name},</p>
      
      <p>
        We recently discovered a security incident that may have affected 
        your personal information. We take this matter very seriously and 
        want to provide you with information about what happened and what 
        we're doing about it.
      </p>
      
      <h2>What Happened</h2>
      <p>{breach.description}</p>
      <p>Date discovered: {breach.discovered_date}</p>
      <p>Date of incident: {breach.incident_date}</p>
      
      <h2>Information Involved</h2>
      <ul>
        {breach.data_types.map(type => (
          <li key={type}>{type}</li>
        ))}
      </ul>
      
      <h2>What We're Doing</h2>
      <ul>
        <li>Secured the vulnerability</li>
        <li>Launched a thorough investigation</li>
        <li>Notified law enforcement</li>
        <li>Enhanced our security measures</li>
      </ul>
      
      <h2>What You Should Do</h2>
      <ul>
        <li>Monitor your accounts for unusual activity</li>
        <li>Consider placing a fraud alert on your credit file</li>
        <li>Review the security resources at [link]</li>
      </ul>
      
      <h2>For More Information</h2>
      <p>
        If you have questions, please contact our dedicated response team:
        <br />Email: security@freshslate.com
        <br />Phone: 1-800-XXX-XXXX
      </p>
      
      <p>
        We sincerely apologize for any inconvenience this may cause and 
        remain committed to protecting your information.
      </p>
      
      <p>Sincerely,<br />The FreshSlate Security Team</p>
    </EmailTemplate>
  );
}
```

## Training & Awareness

### Developer Training Topics

1. **Privacy by Design**
   - Minimize data collection
   - Purpose limitation
   - Data minimization
   - Default privacy settings

2. **Secure Coding**
   - Input validation
   - Output encoding
   - Parameterized queries
   - Encryption usage

3. **Compliance Requirements**
   - GDPR articles
   - CCPA provisions
   - Industry standards
   - Internal policies

### Privacy Checklist for Features

```markdown
## Privacy Impact Assessment

Feature: ________________
Date: ___________________
Developer: ______________

### Data Collection
- [ ] Is all data necessary?
- [ ] Is purpose clearly defined?
- [ ] Is consent obtained?
- [ ] Is data minimized?

### Storage
- [ ] Is PII encrypted?
- [ ] Are retention periods defined?
- [ ] Is access controlled?
- [ ] Are backups secured?

### Processing
- [ ] Is processing lawful?
- [ ] Are third parties vetted?
- [ ] Is data filtered appropriately?
- [ ] Are logs maintained?

### User Rights
- [ ] Can users access their data?
- [ ] Can users correct their data?
- [ ] Can users delete their data?
- [ ] Can users export their data?

### Security
- [ ] Is transport encrypted?
- [ ] Are vulnerabilities assessed?
- [ ] Is monitoring in place?
- [ ] Is incident response ready?

Approved by: _____________
Date: ___________________
```

## Compliance Calendar

### Regular Tasks

**Daily**
- Review privacy logs
- Check for access requests
- Monitor security alerts

**Weekly**
- Process deletion requests
- Review consent metrics
- Update opt-out lists

**Monthly**
- Privacy training session
- Audit access logs
- Review partner compliance
- Update documentation

**Quarterly**
- Privacy impact assessments
- Security assessments
- Policy reviews
- Compliance reporting

**Annually**
- Full privacy audit
- Policy updates
- Training refresh
- Vendor assessments

## Resources

### Internal Resources
- Privacy Policy: `/privacy-policy`
- Cookie Policy: `/cookie-policy`
- Data Request Portal: `/privacy/requests`
- Training Materials: `/docs/privacy-training`

### External Resources
- GDPR: https://gdpr.eu/
- CCPA: https://oag.ca.gov/privacy/ccpa
- IAPP: https://iapp.org/
- Privacy Tools: https://privacytools.io/

### Emergency Contacts
- Data Protection Officer: dpo@freshslate.com
- Legal Team: legal@freshslate.com
- Security Team: security@freshslate.com
- PR Team: pr@freshslate.com

Remember: Privacy is not just compliance—it's about respecting our users and building trust.