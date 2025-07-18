# TCPA Compliance Module

## Overview

The TCPA (Telephone Consumer Protection Act) Compliance Module provides automated integration with TrustedForm and Jornaya for lead generation forms. It ensures your forms comply with TCPA regulations by capturing consent certificates and maintaining audit trails.

## Features

### 🔐 Certificate Providers
- **TrustedForm** - Industry-standard certificate generation
- **Jornaya LeadiD** - Real-time lead tracking and verification
- Both providers can be used simultaneously

### 📋 Compliance Features
- Automatic script injection
- Certificate capture and storage
- Consent tracking with timestamps
- IP address and user agent logging
- 90-day certificate retention (configurable)
- Audit trail generation

### 🛠️ Developer Experience
- Zero-config when disabled
- React hooks for easy integration
- Automatic form enhancement
- TypeScript support
- Design system compliance

## Installation

### 1. Enable TCPA Module

```bash
# Interactive setup
./scripts/setup-tcpa.sh

# Or use command
/tcpa-setup
```

### 2. Configure Providers

Add to `.env.local`:
```env
# TrustedForm
TRUSTEDFORM_API_KEY=your_api_key
TRUSTEDFORM_ACCOUNT_ID=your_account_id

# Jornaya
JORNAYA_ACCOUNT_ID=your_account_id
JORNAYA_CAMPAIGN_ID=your_campaign_id
```

### 3. Run Database Migration

```bash
bun run db:push
```

## Usage

### Basic Implementation

```tsx
import { TCPALeadForm } from '@/components/forms/tcpa/tcpa-lead-form';

export function ContactPage() {
  const handleSubmit = async (data) => {
    // Data automatically includes:
    // - trustedform_cert
    // - jornaya_leadid
    // - tcpa_timestamp
    // - consent_tcpa
    
    await submitToAPI(data);
  };
  
  return (
    <TCPALeadForm 
      onSubmit={handleSubmit}
      className="max-w-md mx-auto"
    />
  );
}
```

### Custom Implementation

```tsx
import { useTCPA } from '@/hooks/use-tcpa';

export function CustomForm() {
  const formRef = useRef<HTMLFormElement>(null);
  const { 
    enabled,
    getTCPAData,
    validateCompliance 
  } = useTCPA({ 
    autoInject: true,
    formRef 
  });
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(e.target);
    
    // Add TCPA data
    const tcpaData = await getTCPAData();
    Object.entries(tcpaData).forEach(([key, value]) => {
      formData.append(key, value);
    });
    
    // Validate compliance
    const compliance = await validateCompliance(formData);
    if (!compliance.valid) {
      alert(compliance.errors.join('\n'));
      return;
    }
    
    // Submit
    await submitForm(formData);
  };
  
  return (
    <form ref={formRef} onSubmit={handleSubmit}>
      {/* Your form fields */}
    </form>
  );
}
```

## Configuration

### Main Configuration (`.claude/tcpa.config.json`)

```json
{
  "enabled": true,
  "providers": {
    "trustedform": {
      "enabled": true,
      "accountId": "YOUR_ACCOUNT_ID",
      "apiKey": "YOUR_API_KEY",
      "retainCerts": true,
      "certRetentionDays": 90,
      "autoInject": true
    },
    "jornaya": {
      "enabled": true,
      "accountId": "YOUR_ACCOUNT_ID",
      "campaignId": "YOUR_CAMPAIGN_ID",
      "autoInject": true
    }
  },
  "compliance": {
    "requireConsent": true,
    "consentLanguage": "By checking this box...",
    "blockSubmissionWithoutCert": false,
    "auditLogRetention": 365
  }
}
```

## API Routes

The module creates these API endpoints:

### Certificate Verification
- `POST /api/tcpa/verify-trustedform` - Verify TrustedForm certificates
- `POST /api/tcpa/verify-jornaya` - Verify Jornaya LeadiD tokens

### Storage
- `POST /api/tcpa/store-certificate` - Store certificates for retention
- `POST /api/tcpa/store-consent` - Store consent records

### Utilities
- `GET /api/client-ip` - Get client IP address

## Database Schema

### Tables Created

1. **tcpa_certificates**
   - Stores TrustedForm certificates and Jornaya tokens
   - Automatic expiration tracking
   - Links to lead records

2. **tcpa_consents**
   - Records explicit consent
   - Timestamps and IP tracking
   - Links to certificates

3. **tcpa_verifications**
   - API verification results
   - Response data storage
   - Error tracking

## Security Considerations

### Data Protection
- Certificates stored encrypted at rest
- No PII in certificate URLs
- Audit logs for all access
- Automatic data expiration

### Compliance
- Follows TCPA best practices
- Maintains chain of custody
- Provides litigation support
- Regular compliance audits

## Testing

### Manual Testing
```bash
# Check configuration
/tcpa-setup status

# Test form with TCPA
# 1. Create a test form
# 2. Submit with phone number
# 3. Check for certificates in response
```

### Automated Testing
```typescript
import { render, fireEvent, waitFor } from '@testing-library/react';
import { TCPALeadForm } from '@/components/forms/tcpa/tcpa-lead-form';

test('captures TrustedForm certificate', async () => {
  const handleSubmit = jest.fn();
  const { getByLabelText, getByText } = render(
    <TCPALeadForm onSubmit={handleSubmit} />
  );
  
  // Fill form
  fireEvent.change(getByLabelText(/phone/i), {
    target: { value: '5551234567' }
  });
  
  // Check consent
  fireEvent.click(getByLabelText(/consent/i));
  
  // Submit
  fireEvent.click(getByText(/submit/i));
  
  await waitFor(() => {
    expect(handleSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        trustedform_cert: expect.stringContaining('https://cert.trustedform.com/')
      })
    );
  });
});
```

## Troubleshooting

### Certificates Not Generating

1. Check browser console for script errors
2. Verify account IDs are correct
3. Ensure scripts are loading (Network tab)
4. Check for ad blockers

### Forms Not Submitting

1. Verify consent checkbox is checked
2. Check API keys in `.env.local`
3. Review server logs for errors
4. Test certificate verification endpoint

### Common Issues

| Issue | Solution |
|-------|----------|
| Script blocked by CSP | Add trusted domains to CSP |
| Certificate expired | Reduce retention period |
| API rate limits | Implement caching |
| Missing certificates | Check script injection |

## Best Practices

### 1. Always Test in Development
- Use test account credentials
- Verify certificates generate
- Check retention policies

### 2. Monitor Usage
- Track API calls
- Monitor certificate costs
- Review compliance reports

### 3. Keep Documentation Updated
- Update consent language
- Document configuration changes
- Maintain audit trails

### 4. Regular Audits
- Weekly certificate checks
- Monthly compliance review
- Quarterly legal review

## Cost Considerations

### TrustedForm
- $0.XX per certificate
- Volume discounts available
- Monthly minimums may apply

### Jornaya
- Pricing varies by volume
- Setup fees may apply
- Custom enterprise pricing

## Legal Disclaimer

This module helps with TCPA compliance but does not guarantee it. Always consult with legal counsel to ensure your forms meet all applicable regulations.

## Resources

- [TrustedForm Documentation](https://activeprospect.com/docs/trustedform)
- [Jornaya Integration Guide](https://docs.jornaya.com)
- [FCC TCPA Guidelines](https://www.fcc.gov/consumers/guides/stop-unwanted-robocalls-and-texts)
- [TCPA Compliance Checklist](https://tcpacompliance.us)

## Support

For issues or questions:
1. Check troubleshooting guide
2. Review error logs
3. Contact provider support
4. File issue in GitHub
