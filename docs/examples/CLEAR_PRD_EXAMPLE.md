# User Authentication PRD Example

This example demonstrates a PRD that follows Grove's principles and passes our clarity linter.

## 🎯 Feature Overview

**Feature Name**: User Authentication System
**Priority**: P0 - Critical
**Timeline**: Sprint 14 (Jan 15-29, 2025)

## 📋 Requirements

### Functional Requirements

1. **User Registration**
   - Email/password registration with validation
   - Email must be valid format (RFC 5322)
   - Password minimum 8 characters, must include:
     - 1 uppercase letter
     - 1 lowercase letter
     - 1 number
     - 1 special character
   - Registration completion time: < 30 seconds
   - Success rate target: > 95%

2. **User Login**
   - Response time: < 200ms for authentication check
   - Support "Remember Me" for 30-day sessions
   - Failed login shows error within 500ms
   - Lock account after 5 failed attempts in 15 minutes

3. **Password Reset**
   - Reset email delivery: < 60 seconds
   - Token expiration: 1 hour
   - One-time use tokens only
   - Success confirmation within 2 seconds

### Performance Requirements

- **API Response Times**:
  - Login endpoint: p95 < 200ms, p99 < 500ms
  - Registration endpoint: p95 < 300ms, p99 < 800ms
  - Token validation: p95 < 50ms, p99 < 100ms

- **Concurrent Users**:
  - Support 10,000 concurrent authentications
  - Database connection pool: 100 connections
  - Redis cache hit rate: > 90%

### Security Requirements

- **Encryption**:
  - Passwords: bcrypt with cost factor 12
  - Tokens: AES-256-GCM encryption
  - Transport: TLS 1.3 only

- **Rate Limiting**:
  - Login attempts: 5 per minute per IP
  - Registration: 3 per hour per IP
  - Password reset: 3 per hour per email

## ✅ Acceptance Criteria

1. **User can register with email and password**
   - Given: Valid email and strong password
   - When: User submits registration form
   - Then: Account created within 30 seconds
   - And: Confirmation email sent within 60 seconds

2. **Invalid registration attempts show specific errors**
   - Given: Invalid email format
   - When: User attempts registration
   - Then: Error "Please enter a valid email address" shown within 100ms
   - And: No account is created

3. **User can login with correct credentials**
   - Given: Existing account with email "user@example.com"
   - When: User provides correct password
   - Then: JWT token returned within 200ms
   - And: User redirected to dashboard

4. **Failed login shows generic error**
   - Given: Any invalid credentials
   - When: Login attempted
   - Then: Error "Invalid email or password" shown
   - And: No information leaked about account existence

5. **Session persists based on "Remember Me"**
   - Given: User logs in with "Remember Me" checked
   - When: User returns after 7 days
   - Then: Still authenticated without re-login
   - And: Session valid for exactly 30 days

6. **Rate limiting prevents brute force**
   - Given: 5 failed login attempts in 1 minute
   - When: 6th attempt made
   - Then: Error "Too many attempts. Try again in 15 minutes"
   - And: All attempts blocked for 15 minutes

## 🏗️ Technical Approach

### Database Schema
```sql
-- Users table with specific constraints
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  locked_until TIMESTAMP NULL,
  failed_attempts INT DEFAULT 0
);

-- Sessions with exact expiration
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  token_hash VARCHAR(255) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### API Contracts

```typescript
// POST /api/auth/register
interface RegisterRequest {
  email: string;      // RFC 5322 valid email
  password: string;   // Min 8 chars, meets complexity
}

interface RegisterResponse {
  success: boolean;
  userId?: string;
  error?: {
    code: 'INVALID_EMAIL' | 'WEAK_PASSWORD' | 'EMAIL_EXISTS';
    message: string;
  };
}

// Response time SLA: p95 < 300ms
```

## 📊 Success Metrics

- **Registration Conversion**: > 85% completion rate
- **Login Success Rate**: > 95% for valid credentials  
- **Password Reset Completion**: > 90% of initiated resets
- **Security Incidents**: 0 breaches, < 10 blocked attacks/day
- **Performance SLA**: 99.9% requests under target time

## 🚨 Edge Cases

1. **Simultaneous Registration**
   - Two users register same email within 10ms
   - Expected: First succeeds, second gets "EMAIL_EXISTS"

2. **Session Extension**
   - User active at 29 days, 23 hours, 59 minutes
   - Expected: Session extends by exactly 30 more days

3. **Clock Skew**
   - Client clock differs by up to 5 minutes
   - Expected: Token validation allows 5-minute grace

## 📝 Notes

This PRD demonstrates:
- ✅ Specific metrics (200ms, not "fast")
- ✅ Measurable criteria (95%, not "most")
- ✅ Concrete examples (exact error messages)
- ✅ Testable conditions (can verify each criterion)

The clarity linter would pass this with no warnings in requirements sections!
