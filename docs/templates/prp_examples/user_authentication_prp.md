# PRP: User Authentication System

## Metadata
- **Created**: 2024-01-15
- **Author**: System
- **Confidence**: 9/10
- **Complexity**: High
- **Type**: Full-Stack (API + Agent + Database)

## Goal
Create a complete user authentication system with JWT tokens, role-based access control, and secure password handling.

## Why
- **Business Value**: Secure user access is fundamental for any application
- **Technical Need**: Replace basic auth with production-ready system
- **Priority**: Critical

## What
Implement a full authentication system including:
- User registration with email verification
- Login with JWT tokens
- Password reset flow
- Role-based permissions
- Session management
- Security audit logging

### Success Criteria
- [ ] All endpoints return proper status codes
- [ ] JWT tokens expire and refresh correctly
- [ ] Password reset is secure (time-limited tokens)
- [ ] 100% test coverage for auth endpoints
- [ ] Security scan passes with no high/critical issues

## All Needed Context

### Documentation & References
```yaml
# FastAPI Security
- url: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
  why: JWT implementation pattern
  sections: ["OAuth2 with Password", "JWT tokens"]
  critical: Use HS256 algorithm

# Passlib Documentation  
- url: https://passlib.readthedocs.io/en/stable/
  why: Password hashing best practices
  sections: ["Quick Start", "Bcrypt"]

# Python JWT
- url: https://pyjwt.readthedocs.io/en/stable/
  why: Token generation and validation
  critical: Set expiration times

# Codebase Examples
- file: src/api/dependencies.py
  why: Existing dependency injection patterns
  pattern: get_current_user dependency

- file: src/models/base.py
  why: Base model structure
  gotcha: Uses model_config for Pydantic v2

# Cached Documentation
- docfile: PRPs/ai_docs/auth_best_practices.md
  why: Security guidelines and common vulnerabilities
```

### Current Codebase Structure
```bash
src/
├── api/
│   ├── __init__.py
│   ├── dependencies.py
│   └── endpoints/
│       └── __init__.py
├── models/
│   ├── __init__.py
│   └── base.py
├── db/
│   └── __init__.py
└── core/
    ├── __init__.py
    └── config.py
```

### Desired Structure After Implementation
```bash
src/
├── api/
│   ├── __init__.py
│   ├── dependencies.py
│   └── endpoints/
│       ├── __init__.py
│       └── [NEW] auth.py         # Auth endpoints
├── models/
│   ├── __init__.py
│   ├── base.py
│   └── [NEW] auth.py            # Auth models
├── db/
│   ├── __init__.py
│   └── [NEW] users.py           # User DB models
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── [NEW] security.py        # Security utilities
├── services/
│   └── [NEW] auth_service.py    # Business logic
└── tests/
    ├── [NEW] test_auth_api.py
    ├── [NEW] test_auth_service.py
    └── [NEW] test_security.py
```

### Known Gotchas & Critical Patterns
```python
# CRITICAL: Always hash passwords
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# GOTCHA: JWT secret must be strong and from environment
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Min 32 chars
if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise ValueError("JWT_SECRET_KEY must be at least 32 characters")

# PATTERN: Dependency injection for current user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user

# WARNING: Email verification tokens expire
EMAIL_VERIFICATION_EXPIRE_HOURS = 24
PASSWORD_RESET_EXPIRE_HOURS = 1
```

## Implementation Blueprint

### Task 1 - Security Foundation
```yaml
CREATE src/core/security.py:
  - Password hashing with bcrypt
  - JWT token creation/validation
  - Token expiration handling
  - Security constants

CREATE src/core/email.py:
  - Email sending utilities
  - Verification email templates
  - Password reset templates
```

### Task 2 - Database Models
```yaml
CREATE src/db/users.py:
  - User table with SQLAlchemy
  - Roles and permissions tables
  - Password reset tokens table
  - Audit log table
  
  Key fields:
  - email (unique, indexed)
  - hashed_password
  - is_active
  - is_verified
  - created_at
  - last_login
```

### Task 3 - Pydantic Models
```yaml
CREATE src/models/auth.py:
  - UserCreate (registration)
  - UserLogin (authentication)
  - Token (JWT response)
  - TokenData (JWT payload)
  - PasswordReset
  - UserResponse (safe user data)
```

### Task 4 - Service Layer
```yaml
CREATE src/services/auth_service.py:
  - User registration logic
  - Email verification
  - Login with token generation
  - Password reset flow
  - User activation/deactivation
  - Audit logging
```

### Task 5 - API Endpoints
```yaml
CREATE src/api/endpoints/auth.py:
  POST /auth/register
    - Create new user
    - Send verification email
    
  POST /auth/login
    - Validate credentials
    - Return JWT token
    
  POST /auth/refresh
    - Refresh expired token
    
  POST /auth/logout
    - Invalidate token
    
  GET /auth/verify/{token}
    - Verify email address
    
  POST /auth/forgot-password
    - Send reset email
    
  POST /auth/reset-password
    - Update password with token
    
  GET /auth/me
    - Get current user info
```

### Task 6 - Testing
```yaml
CREATE tests/test_auth_api.py:
  - Test all endpoints
  - Test error responses
  - Test rate limiting
  
CREATE tests/test_auth_service.py:
  - Unit tests for service
  - Mock email sending
  - Test token expiration
  
CREATE tests/test_security.py:
  - Test password hashing
  - Test JWT validation
  - Security edge cases
```

## Validation Loops

### Level 1: Syntax & Style
```bash
ruff check src/ --fix
ruff format src/
mypy src/ --strict
```

### Level 2: Unit Tests
```bash
pytest tests/test_auth_service.py -v
pytest tests/test_security.py -v
pytest tests/ --cov=src/core/security --cov=src/services/auth_service --cov-report=term-missing
# Expected: >90% coverage
```

### Level 3: Integration Tests
```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/test_auth_api.py -v -m integration

# Test email sending
python scripts/test_email_delivery.py

# Load test authentication
locust -f tests/load/auth_load_test.py --headless \
  --users 100 --spawn-rate 10 --run-time 60s
```

### Level 4: Security Validation
```bash
# Security scanning
bandit -r src/core/security.py src/api/endpoints/auth.py
safety check
pip-audit

# OWASP checks
python scripts/security_audit.py

# Test JWT security
python scripts/test_jwt_security.py

# Check for common vulnerabilities
# - SQL injection
# - Weak passwords
# - Token replay attacks
# - Brute force protection
```

## Deployment Checklist
- [ ] JWT_SECRET_KEY in environment (32+ chars)
- [ ] Email service configured
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Database migrations tested
- [ ] Monitoring alerts set up
- [ ] Audit logging verified

## Anti-Patterns to Avoid
- ❌ Don't store plain text passwords
- ❌ Don't use weak JWT secrets
- ❌ Don't skip email verification
- ❌ Don't allow unlimited login attempts
- ❌ Don't expose user IDs in URLs
- ❌ Don't return sensitive data in errors
- ❌ Don't trust client-side validation

## Confidence Score: 9/10

### Scoring Rationale:
- Documentation completeness: 2/2
- Pattern examples: 2/2
- Gotchas identified: 2/2
- Test coverage: 2/2
- Automation readiness: 1/2 (manual email testing needed)
