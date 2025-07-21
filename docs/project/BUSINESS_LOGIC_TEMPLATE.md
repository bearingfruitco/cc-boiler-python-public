# Business Logic & Rules Template

## Purpose
This document defines HOW the system works - all rules, validations, workflows, and constraints that must be enforced in code. This is the source of truth for system behavior.

## Core Business Rules

### User Management
#### Registration Rules
- [ ] Email must be unique in system
- [ ] Email must be valid format (RFC 5322)
- [ ] Password minimum requirements:
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
  - Optional: special character
- [ ] Username requirements (if applicable):
  - Minimum 3 characters
  - Only alphanumeric and underscore
  - Must be unique

#### Authentication Rules
- [ ] Session timeout: [X hours/days]
- [ ] Maximum login attempts: [5] per [time period]
- [ ] Account lockout duration: [X minutes]
- [ ] 2FA: [Required/Optional]
- [ ] Password reset token validity: [24 hours]

#### User Roles & Permissions
| Role | Permissions | Restrictions |
|------|------------|--------------|
| Guest | View public content | No account access |
| User | CRUD own data | Cannot access others' data |
| Admin | CRUD all data | Cannot delete system data |

### Data Validation Rules

#### Common Field Rules
| Field Type | Validation Rules | Error Message |
|------------|-----------------|---------------|
| Email | Valid format, max 255 chars | "Please enter a valid email" |
| Phone | Valid format (country-specific) | "Please enter a valid phone number" |
| URL | Valid URL format | "Please enter a valid URL" |
| Date | Not in past (for future dates) | "Please select a future date" |

#### Business-Specific Fields
| Field | Rules | Error Message |
|-------|-------|---------------|
| [Field name] | [Validation rules] | [User-friendly error] |

### Business Workflows

#### [Workflow Name] Flow
**Trigger**: [What starts this workflow]

**Steps**:
1. **[Step Name]**
   - Validation: [What to check]
   - Action: [What happens]
   - Success: [Next step]
   - Failure: [Error handling]

2. **[Step Name]**
   - Validation: [What to check]
   - Action: [What happens]
   - Success: [Next step]
   - Failure: [Error handling]

**Completion**: [Final state/outcome]

### State Machines

#### [Entity] Status Transitions
```
[Initial] -> [State A] -> [State B] -> [Final]
     ↓           ↓           ↓
  [Error]    [Cancelled]  [Failed]
```

**Allowed Transitions**:
- From [State] to [State]: When [condition]
- From [State] to [State]: When [condition]

**Forbidden Transitions**:
- Cannot go from [State] to [State]
- Cannot skip [State]

### Business Calculations

#### [Calculation Name]
**Formula**: `result = (input1 * factor1) + (input2 * factor2)`

**Rules**:
- Minimum value: [X]
- Maximum value: [Y]
- Rounding: [2 decimal places]
- Special cases: [List edge cases]

### API Business Rules

#### General API Rules
- Rate limiting: [100] requests per [minute] per [user/IP]
- Authentication: Required for all endpoints except [/public/*]
- Response format: JSON
- Timezone: All timestamps in UTC
- Pagination: Default [20], max [100] items

#### Endpoint-Specific Rules
**POST /api/[resource]**
- Required fields: [field1, field2]
- Optional fields: [field3, field4]
- Validation: [Specific rules]
- Side effects: [What else happens]

### Data Integrity Rules

#### Referential Integrity
- [ ] Cannot delete [entity] if [related entities] exist
- [ ] Cascading deletes for [relationship]
- [ ] Soft delete only for [entities]

#### Data Consistency
- [ ] [Field A] + [Field B] must equal [Field C]
- [ ] If [Field X] is set, [Field Y] is required
- [ ] [Entity] must have at least one [related entity]

### Security Rules

#### Data Access
- Users can only access their own [entities]
- [Role] can access all [entities] in their [scope]
- Sensitive fields ([list]) are never exposed in API

#### PII Handling
- [ ] Encrypt at rest: [field list]
- [ ] Mask in logs: [field list]
- [ ] Audit trail required for: [operations]

### Compliance Rules

#### Data Retention
- [Entity]: Keep for [X years]
- [Entity]: Delete after [Y days] of inactivity
- Audit logs: Keep forever

#### Regional Requirements
- GDPR: [Specific requirements]
- CCPA: [Specific requirements]
- Other: [Industry-specific]

### Integration Rules

#### External Services
**[Service Name]**
- Retry policy: [3 attempts with exponential backoff]
- Timeout: [30 seconds]
- Fallback: [What to do if service is down]
- Rate limits: [Their limits]

### Notification Rules

#### Email Notifications
| Event | Recipient | Timing | Template |
|-------|-----------|---------|----------|
| Registration | User | Immediate | welcome |
| Password Reset | User | Immediate | reset |
| [Event] | [Who] | [When] | [template] |

#### In-App Notifications
| Event | Recipients | Priority | Expires |
|-------|-----------|----------|---------|
| [Event] | [User type] | [High/Med/Low] | [X days] |

### Error Handling Rules

#### User-Facing Errors
- Never expose system internals
- Always provide actionable message
- Include error code for support
- Log full error internally

#### System Errors
- Retry transient failures [3] times
- Circuit breaker after [10] failures
- Alert on-call for critical errors
- Graceful degradation for non-critical

### Performance Rules

#### Response Times
- API endpoints: < [200ms] p95
- Page load: < [3s] on 3G
- Search results: < [500ms]

#### Resource Limits
- Max file upload: [10MB]
- Max API response: [1MB]
- Max concurrent operations: [X per user]

### Testing Requirements

#### Required Test Coverage
- Unit tests: [80%] minimum
- Critical paths: [100%] coverage
- Business logic: Comprehensive tests
- Edge cases: All documented

## Glossary

| Term | Definition |
|------|------------|
| [Business term] | [Clear definition] |
| [Technical term] | [Simple explanation] |

## Change Log

| Date | Change | Reason |
|------|--------|---------|
| YYYY-MM-DD | Initial version | Project start |
| YYYY-MM-DD | Added [rule] | [Business reason] |