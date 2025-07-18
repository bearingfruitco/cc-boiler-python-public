# Security & Data Protection Documentation

## Overview

This boilerplate includes a comprehensive security system designed to protect Personally Identifiable Information (PII) and ensure compliance with data protection regulations like HIPAA and GDPR.

## Core Security Features

### 1. Field Registry System

All data fields are defined in a centralized registry with security metadata:

```
field-registry/
├── core/                  # Universal fields (tracking, device, etc.)
│   ├── tracking.json     # UTM parameters, click IDs
│   ├── cookies.json      # Marketing cookies
│   ├── device.json       # Browser/device info
│   ├── geographic.json   # IP-based location
│   └── journey.json      # User behavior tracking
├── verticals/            # Industry-specific fields
│   ├── debt.json        # Debt relief fields
│   ├── healthcare.json  # Medical fields (HIPAA)
│   └── standard.json    # General contact forms
└── compliance/          # Security rules
    ├── pii-fields.json  # PII classifications
    └── encryption.json  # Encryption requirements
```

### 2. PII Protection

The system automatically prevents PII exposure through:

#### Blocking Mechanisms
- **Console Logging**: PII is automatically redacted from console.log
- **Client Storage**: localStorage/sessionStorage blocks for PII fields
- **URL Parameters**: PII cannot be added to URLs or query strings
- **Error Tracking**: PII is masked in error messages

#### Pre-Tool Hook
The `07-pii-protection.py` hook runs before any file write to:
- Detect PII patterns (SSN, email, phone, etc.)
- Block violations before they're written
- Suggest secure alternatives

### 3. Secure Form Handling

#### Form Generation
```bash
/ctf ContactForm --vertical=debt --compliance=hipaa
```

This generates a form with:
- Automatic tracking field capture
- PII fields marked and encrypted
- Server-side only processing
- Audit logging built-in
- Consent tracking

#### Prepopulation Rules
Only these fields can be prepopulated from URLs:
- UTM parameters (utm_source, utm_medium, etc.)
- Click IDs (gclid, fbclid, ttclid)
- Partner/Campaign IDs
- NO PII fields ever

### 4. Data Flow Security

```
User Input → Client Validation → Server Processing → Encryption → Database
                ↓                      ↓                ↓
           No PII Logs          Audit Logging    Field-Level Encryption
```

### 5. Encryption

Three levels of encryption:
- **Transit**: All API calls use HTTPS
- **Field-Level**: Sensitive fields encrypted before storage
- **At Rest**: Database encryption for all tables

### 6. Audit Logging

Every access to PII is logged with:
- Who accessed (user/session ID)
- What was accessed (fields)
- When (timestamp)
- Why (purpose/context)
- Result (success/failure)

## Implementation Guide

### Creating a Secure Form

1. **Generate the form component**:
   ```bash
   /ctf LeadForm --vertical=debt
   ```

2. **Review generated security features**:
   - Check field classifications
   - Verify encryption settings
   - Confirm audit logging

3. **Test security**:
   ```bash
   /afs components/forms/LeadForm.tsx
   ```

### Adding New Fields

1. **Update field registry**:
   ```json
   // field-registry/verticals/custom.json
   {
     "custom_field": {
       "type": "STRING",
       "pii": true,
       "encryption": "field",
       "prepopulate": false,
       "validation": {
         "required": true
       }
     }
   }
   ```

2. **Regenerate types**:
   ```bash
   /gft custom
   ```

3. **Update forms to use new field**

### Security Checklist

Before deploying any form:

- [ ] Run `/afs` to audit security
- [ ] Verify no PII in console logs
- [ ] Check prepopulation whitelist
- [ ] Confirm encryption keys are set
- [ ] Test audit logging works
- [ ] Validate consent capture
- [ ] Check rate limiting
- [ ] Review error messages for PII

## Compliance Modes

### Standard Mode
- Basic PII protection
- 90-day data retention
- Standard audit logging

### HIPAA Mode
```bash
/ctf MedicalForm --compliance=hipaa
```
- PHI field encryption
- 7-year retention
- Detailed audit trails
- Access controls
- BAA compliance

### GDPR Mode
```bash
/ctf EUForm --compliance=gdpr
```
- Explicit consent required
- Right to deletion
- Data portability
- 30-day deletion
- Privacy by design

## API Security

### Rate Limiting
- 10 submissions per hour per IP
- Configurable via environment
- Automatic blocking of abusers

### Request Validation
- CSRF protection
- Request size limits
- Input sanitization
- Type validation

### Response Security
- No PII in responses
- Generic error messages
- Minimal data exposure
- Reference IDs only

## Environment Variables

Required for security features:

```bash
# Encryption Keys
FORM_ENCRYPTION_KEY=        # 32-byte key for field encryption
AUDIT_LOG_KEY=             # Separate key for audit logs
DATABASE_ENCRYPTION_KEY=    # Database field encryption

# Session Management
SESSION_SECRET=            # Session signing key
SESSION_DURATION=86400     # 24 hours

# Rate Limiting
RATE_LIMIT_WINDOW=3600     # 1 hour
RATE_LIMIT_MAX_REQUESTS=10 # Per window

# Compliance
COMPLIANCE_MODE=standard   # standard|hipaa|gdpr
PII_RETENTION_DAYS=90     # How long to keep PII
AUDIT_RETENTION_DAYS=2555 # 7 years for HIPAA
```

## Testing Security

### Manual Testing
1. Try to console.log email field
2. Attempt to store PII in localStorage
3. Add email to URL parameter
4. Submit form without consent
5. Exceed rate limit

### Automated Testing
```typescript
// tests/security/pii-protection.test.ts
describe('PII Protection', () => {
  it('blocks PII in console', () => {
    // Test that PII is redacted
  });
  
  it('prevents URL exposure', () => {
    // Test prepopulation whitelist
  });
  
  it('encrypts sensitive fields', () => {
    // Verify encryption happens
  });
});
```

## Common Issues

### "PII detected in console log"
**Solution**: Use `PIIDetector.createSafeObject()`:
```typescript
console.log(PIIDetector.createSafeObject(userData));
```

### "Cannot prepopulate email field"
**Solution**: Email is PII and cannot be prepopulated. Only tracking fields allowed.

### "Encryption key not found"
**Solution**: Set FORM_ENCRYPTION_KEY in .env.local

### "Audit log failed"
**Solution**: Check AUDIT_LOG_KEY and database permissions

## Security Best Practices

1. **Never trust client input** - Always validate server-side
2. **Minimize data collection** - Only collect what you need
3. **Encrypt early, decrypt late** - Minimize exposure window
4. **Log everything, store nothing** - Audit actions, not data
5. **Fail secure** - Default to denying access
6. **Keep keys separate** - Different keys for different purposes
7. **Regular audits** - Run `/afs` before every deployment

## Resources

- [OWASP Security Guidelines](https://owasp.org)
- [HIPAA Compliance Guide](https://www.hhs.gov/hipaa)
- [GDPR Requirements](https://gdpr.eu)
- Field Registry: `/field-registry/README.md`
- Security Utils: `/lib/security/`
