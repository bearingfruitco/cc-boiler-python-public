# FreshSlate Security & Compliance Guide

## Overview

This document outlines security best practices, compliance requirements, and implementation guidelines for FreshSlate applications.

## Security Architecture

### Defense in Depth

```
Layer 1: Edge Security (Cloudflare)
├── DDoS Protection
├── WAF Rules
├── Bot Management
└── SSL/TLS Termination

Layer 2: Application Security (Next.js)
├── Input Validation
├── Output Encoding
├── Session Management
└── CSRF Protection

Layer 3: Data Security (Supabase)
├── Encryption at Rest
├── Row Level Security
├── Connection Encryption
└── Backup Encryption
```

## Authentication & Authorization

### API Authentication

```typescript
// lib/auth/api-key.ts
import { createHash } from 'crypto';

export async function validateApiKey(
  key: string,
  request: Request
): Promise<boolean> {
  // Hash the API key
  const hashedKey = createHash('sha256')
    .update(key)
    .digest('hex');
  
  // Check against database
  const { data: apiKey } = await supabase
    .from('api_keys')
    .select('*')
    .eq('key_hash', hashedKey)
    .single();
    
  if (!apiKey || !apiKey.active) {
    return false;
  }
  
  // Check rate limits
  const rateLimited = await checkRateLimit(apiKey.id);
  if (rateLimited) {
    throw new Error('Rate limit exceeded');
  }
  
  // Log usage
  await logApiUsage(apiKey.id, request);
  
  return true;
}
```

### Session Security

```typescript
// lib/auth/session.ts
import { SignJWT, jwtVerify } from 'jose';

const secret = new TextEncoder().encode(
  process.env.SESSION_SECRET!
);

export async function createSession(data: any) {
  const jwt = await new SignJWT(data)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('24h')
    .sign(secret);
    
  return jwt;
}

export async function verifySession(jwt: string) {
  try {
    const { payload } = await jwtVerify(jwt, secret);
    return payload;
  } catch {
    return null;
  }
}
```

## Input Validation & Sanitization

### Zod Schemas

```typescript
// lib/validation/schemas.ts
import { z } from 'zod';
import DOMPurify from 'isomorphic-dompurify';

// Custom sanitization
const sanitizedString = z.string().transform((val) => 
  DOMPurify.sanitize(val, { ALLOWED_TAGS: [] })
);

// Phone validation
const phoneNumber = z.string().regex(
  /^\+?1?\d{10,14}$/,
  'Invalid phone number'
);

// Email with disposable check
const email = z.string().email().refine(
  async (email) => {
    const domain = email.split('@')[1];
    const disposable = await checkDisposableEmail(domain);
    return !disposable;
  },
  'Disposable emails not allowed'
);

// Lead schema with sanitization
export const leadSchema = z.object({
  name: sanitizedString.min(2).max(100),
  email: email,
  phone: phoneNumber,
  debt_amount: z.number().min(1000).max(1000000),
  state: z.string().length(2).regex(/^[A-Z]{2}$/),
  message: sanitizedString.max(1000).optional(),
});

// SQL injection prevention
export const querySchema = z.object({
  search: z.string().regex(/^[\w\s-]+$/, 'Invalid characters'),
  limit: z.number().min(1).max(100),
  offset: z.number().min(0),
});
```

### XSS Prevention

```typescript
// lib/security/xss.ts
export function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'target'],
    ALLOW_DATA_ATTR: false,
  });
}

export function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;',
  };
  return text.replace(/[&<>"'/]/g, (char) => map[char]);
}
```

## CSRF Protection

```typescript
// lib/security/csrf.ts
import { randomBytes } from 'crypto';

export async function generateCsrfToken(): Promise<string> {
  const token = randomBytes(32).toString('hex');
  
  // Store in session
  await redis.setex(
    `csrf:${token}`,
    3600, // 1 hour
    '1'
  );
  
  return token;
}

export async function validateCsrfToken(token: string): Promise<boolean> {
  const exists = await redis.get(`csrf:${token}`);
  
  if (!exists) return false;
  
  // Delete after use (one-time token)
  await redis.del(`csrf:${token}`);
  
  return true;
}

// Middleware
export async function csrfMiddleware(request: Request) {
  if (['POST', 'PUT', 'DELETE'].includes(request.method)) {
    const token = request.headers.get('x-csrf-token');
    
    if (!token || !(await validateCsrfToken(token))) {
      return new Response('Invalid CSRF token', { status: 403 });
    }
  }
}
```

## Data Privacy & Compliance

### GDPR Compliance

```typescript
// lib/privacy/gdpr.ts
export async function handleDataRequest(
  email: string,
  type: 'export' | 'delete'
) {
  // Verify identity
  const verificationToken = await sendVerificationEmail(email);
  
  // Wait for verification...
  
  if (type === 'export') {
    const data = await exportUserData(email);
    return data;
  } else {
    await deleteUserData(email);
    return { success: true };
  }
}

async function exportUserData(email: string) {
  const data = await supabase
    .from('leads')
    .select('*')
    .eq('email', email);
    
  return {
    leads: data.data,
    exported_at: new Date().toISOString(),
  };
}

async function deleteUserData(email: string) {
  // Soft delete with anonymization
  await supabase
    .from('leads')
    .update({
      email: `deleted-${Date.now()}@example.com`,
      name: 'DELETED',
      phone: '0000000000',
      deleted_at: new Date().toISOString(),
    })
    .eq('email', email);
}
```

### CCPA Compliance

```typescript
// lib/privacy/ccpa.ts
export async function optOutOfSale(email: string) {
  // Record opt-out
  await supabase
    .from('privacy_preferences')
    .upsert({
      email,
      sale_opt_out: true,
      opted_out_at: new Date().toISOString(),
    });
    
  // Notify partners
  await notifyPartnersOfOptOut(email);
}
```

### TCPA Compliance

```typescript
// components/TcpaConsent.tsx
export function TcpaConsent({ 
  onConsent 
}: { 
  onConsent: (consented: boolean) => void 
}) {
  return (
    <div className="p-4 bg-gray-50 rounded-lg">
      <label className="flex items-start gap-3">
        <input
          type="checkbox"
          required
          onChange={(e) => onConsent(e.target.checked)}
          className="mt-1"
        />
        <span className="text-sm text-gray-600">
          By checking this box and submitting this form, I provide my 
          signature expressly consenting to receive recurring automated 
          marketing and other texts, calls, and emails from FreshSlate 
          and its partners at the phone number and email address provided. 
          I understand that consent is not required to purchase and that 
          I may opt out at any time by replying STOP.
        </span>
      </label>
    </div>
  );
}
```

## Security Headers

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Security headers
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' *.googletagmanager.com *.google-analytics.com; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' data: https:; " +
    "font-src 'self' data:; " +
    "connect-src 'self' *.supabase.co *.sentry.io;"
  );
  
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=()'
  );
  
  // HSTS
  if (process.env.NODE_ENV === 'production') {
    response.headers.set(
      'Strict-Transport-Security',
      'max-age=31536000; includeSubDomains'
    );
  }
  
  return response;
}
```

## Secure Coding Practices

### Environment Variables

```typescript
// lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']),
  DATABASE_URL: z.string().url(),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1),
  SESSION_SECRET: z.string().min(32),
  ENCRYPTION_KEY: z.string().length(64),
});

export const env = envSchema.parse(process.env);
```

### Encryption

```typescript
// lib/security/encryption.ts
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const algorithm = 'aes-256-gcm';
const key = Buffer.from(env.ENCRYPTION_KEY, 'hex');

export function encrypt(text: string): string {
  const iv = randomBytes(16);
  const cipher = createCipheriv(algorithm, key, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return iv.toString('hex') + ':' + authTag.toString('hex') + ':' + encrypted;
}

export function decrypt(encryptedData: string): string {
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

## Vulnerability Scanning

### Dependency Scanning

```json
// package.json
{
  "scripts": {
    "audit": "pnpm audit --audit-level=moderate",
    "audit:fix": "pnpm audit --fix",
    "outdated": "pnpm outdated",
    "update:check": "pnpm update --dry-run"
  }
}
```

### GitHub Actions Security

```yaml
# .github/workflows/security.yml
name: Security
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
          
      - name: Run CodeQL
        uses: github/codeql-action/analyze@v2
        
      - name: Dependency Review
        uses: actions/dependency-review-action@v3
```

## Incident Response

### Security Incident Procedure

```typescript
// lib/security/incident.ts
export async function reportSecurityIncident(
  type: 'breach' | 'vulnerability' | 'suspicious_activity',
  details: any
) {
  // 1. Log incident
  await logger.error('SECURITY_INCIDENT', {
    type,
    details,
    timestamp: new Date().toISOString(),
  });
  
  // 2. Alert team
  await sendAlert({
    to: process.env.SECURITY_EMAIL!,
    subject: `[URGENT] Security Incident: ${type}`,
    body: JSON.stringify(details, null, 2),
  });
  
  // 3. Create incident in BetterStack
  await createIncident({
    title: `Security: ${type}`,
    severity: 'critical',
    description: details,
  });
  
  // 4. If breach, notify affected users
  if (type === 'breach') {
    await notifyAffectedUsers(details.affected_users);
  }
}
```

## Security Checklist

### Pre-Deployment

```markdown
- [ ] All dependencies updated
- [ ] Security headers configured
- [ ] Input validation on all endpoints
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Error messages sanitized
- [ ] Logs don't contain PII
- [ ] SSL/TLS properly configured
- [ ] Environment variables secured
- [ ] Database queries parameterized
```

### Post-Deployment

```markdown
- [ ] Security scan passed
- [ ] Penetration test scheduled
- [ ] Monitoring alerts configured
- [ ] Incident response tested
- [ ] Backup restoration verified
- [ ] Access logs reviewed
- [ ] Rate limits verified
- [ ] HTTPS enforcement confirmed
```

## Compliance Documentation

### Required Documents

```yaml
Privacy Policy:
  - Data collection practices
  - Third-party sharing
  - User rights
  - Contact information

Terms of Service:
  - Service description
  - User obligations
  - Liability limitations
  - Dispute resolution

Cookie Policy:
  - Types of cookies
  - Purpose of each
  - Opt-out methods
  - Third-party cookies
```

### Audit Trail

```typescript
// lib/audit/logger.ts
export async function auditLog(
  action: string,
  userId: string | null,
  details: any
) {
  await supabase
    .from('audit_logs')
    .insert({
      action,
      user_id: userId,
      ip_address: getClientIp(),
      user_agent: getUserAgent(),
      details,
      created_at: new Date().toISOString(),
    });
}
```

// CORS configuration for partner APIs
const corsOptions = {
  origin: function (origin, callback) {
    const allowedOrigins = [
      'https://freshslate.com',
      'https://*.freshslate.com',
      'https://partner1.com',
      'https://partner2.com'
    ];
    
    if (!origin || allowedOrigins.some(allowed => 
      origin.match(new RegExp(allowed.replace('*', '.*')))
    )) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
};

---

Security is not a feature, it's a requirement. Every line of code should be written with security in mind.