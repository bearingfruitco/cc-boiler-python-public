Audit form component for security and compliance issues: $ARGUMENTS

Steps:

1. Read the form component file at: $ARGUMENTS

2. Scan for security violations:

   **Critical Issues (Block)**:
   - PII in console.log statements
   - PII in localStorage/sessionStorage
   - PII in URL parameters
   - Client-side storage of sensitive data
   - Missing encryption for PII fields
   - Tracking fields not auto-captured
   - Direct database access from client

   **High Priority Issues**:
   - Missing server-side validation
   - No audit logging
   - Missing consent tracking
   - Insecure data transmission
   - No field masking for sensitive data
   - Missing CSRF protection

   **Medium Priority Issues**:
   - Autocomplete enabled on sensitive fields
   - Copy/paste not disabled for SSN/credit cards
   - Missing rate limiting
   - No input sanitization
   - Missing field validation

3. Check compliance requirements:

   **HIPAA Compliance**:
   - PHI fields properly encrypted
   - Audit trail for all access
   - Access controls implemented
   - Data retention policies
   - BAA requirements met

   **GDPR Compliance**:
   - Explicit consent captured
   - Right to deletion implemented
   - Data portability supported
   - Privacy policy linked
   - Data minimization practiced

   **PCI Compliance**:
   - Credit card fields tokenized
   - No card data stored
   - TLS encryption enforced
   - PCI-compliant processors used

4. Generate security report:

```
=== FORM SECURITY AUDIT REPORT ===
Component: $ARGUMENTS
Date: [current date]
Compliance Level: [detected level]

CRITICAL VIOLATIONS: [count]
- [List each critical issue with line numbers]

HIGH PRIORITY ISSUES: [count]
- [List each high priority issue]

MEDIUM PRIORITY ISSUES: [count]
- [List each medium issue]

FIELD ANALYSIS:
- Total fields: [count]
- PII fields: [count] 
- Encrypted fields: [count]
- Properly masked: [count]

TRACKING COMPLIANCE:
- Auto-capture implemented: [yes/no]
- Prepopulation whitelist enforced: [yes/no]
- Cookie capture server-side: [yes/no]

RECOMMENDATIONS:
1. [Specific fixes for critical issues]
2. [Security enhancements needed]
3. [Compliance gaps to address]

SECURE CODE EXAMPLES:
[Provide corrected code snippets]
```

5. If auto-fix is requested (--fix flag):
   - Create backup of original file
   - Apply automatic fixes for:
     - Remove console.log with PII
     - Move localStorage to server-side
     - Add field masking
     - Implement proper validation
     - Add missing security headers
   - Show diff of changes

6. Integration checks:
   - Verify SecureFormHandler is used
   - Check API routes are protected
   - Validate encryption configuration
   - Ensure audit logging enabled

Output format:
- Show violations grouped by severity
- Provide specific line numbers
- Include fix examples
- Rate overall security score (A-F)
