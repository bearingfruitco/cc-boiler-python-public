# PRP: [FEATURE NAME]

## Metadata
- **Created**: [DATE]
- **Author**: [AUTHOR]
- **Confidence**: [1-10]
- **Complexity**: [Low/Medium/High]
- **Type**: [API/Agent/Pipeline/Library/Full-Stack]

## Goal
[Clear description of what needs to be built]

## Why
- **Business Value**: [Impact on users/system]
- **Technical Need**: [Problems this solves]
- **Priority**: [Critical/High/Medium/Low]

## What
[User-visible behavior and technical requirements]

### Success Criteria
- [ ] [Specific measurable outcome]
- [ ] [Performance requirement]
- [ ] [Security requirement]
- [ ] [Test coverage requirement]

## All Needed Context

### Documentation & References
```yaml
# Official Documentation
- url: https://docs.python.org/3/library/asyncio.html
  why: Async patterns for concurrent operations
  sections: ["coroutines", "tasks", "streams"]

- url: https://fastapi.tiangolo.com/tutorial/security/
  why: Authentication patterns to follow
  critical: OAuth2 with Password flow

# Codebase Examples
- file: src/api/auth.py
  why: Existing authentication pattern
  pattern: JWT token generation and validation

- file: src/models/user.py
  why: User model structure to extend
  gotcha: Uses SQLAlchemy 2.0 syntax

# Cached Documentation
- docfile: PRPs/ai_docs/pandas_gotchas.md
  why: Common pandas memory issues and solutions

- docfile: PRPs/ai_docs/async_patterns.md
  why: Project-specific async conventions
```

### Current Codebase Structure
```bash
# Output of: tree -I '__pycache__|*.pyc|.git'
src/
├── agents/
│   └── base_agent.py
├── api/
│   ├── __init__.py
│   └── endpoints/
├── models/
│   └── __init__.py
└── utils/
    └── validators.py
```

### Desired Structure After Implementation
```bash
src/
├── agents/
│   ├── base_agent.py
│   └── [NEW] feature_agent.py  # Implements X functionality
├── api/
│   ├── __init__.py
│   └── endpoints/
│       └── [NEW] feature.py    # API endpoints for feature
├── models/
│   ├── __init__.py
│   └── [NEW] feature.py        # Pydantic models
└── tests/
    └── [NEW] test_feature.py   # Comprehensive tests
```

### Known Gotchas & Critical Patterns
```python
# CRITICAL: FastAPI dependency injection pattern
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # This pattern MUST be followed for all auth endpoints

# GOTCHA: Pydantic v2 requires explicit model_config
class FeatureModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
# PATTERN: All database operations use async context
async with get_db() as db:
    # Operations here
    
# WARNING: Rate limiting on external API
# Max 10 requests/second - use asyncio.Semaphore(10)
```

## Test Specifications (TDD Required)

### Unit Tests Required
```python
# tests/unit/test_[feature]_models.py
class TestFeatureModel:
    """Test Pydantic model validation and behavior."""
    
    def test_valid_creation(self):
        """Model should accept valid data."""
        # Given valid input matching schema
        # When model created
        # Then validation passes and fields set correctly
    
    def test_validation_errors(self):
        """Model should reject invalid data with clear errors."""
        # Given invalid input (missing required, wrong types)
        # When model created
        # Then ValidationError with specific field errors
    
    def test_custom_validators(self):
        """Business rule validators should enforce constraints."""
        # Given data violating business rules
        # When validated
        # Then appropriate error messages

# tests/unit/test_[feature]_service.py
class TestFeatureService:
    """Test business logic layer."""
    
    async def test_create_with_valid_data(self):
        """Service should create resource with valid data."""
        # Given valid DTO and mocked dependencies
        # When create_feature called
        # Then resource created and returned
    
    async def test_duplicate_prevention(self):
        """Service should prevent duplicate creation."""
        # Given existing resource
        # When creating duplicate
        # Then DuplicateError raised
    
    async def test_transaction_rollback(self):
        """Failed operations should rollback cleanly."""
        # Given operation that will fail mid-transaction
        # When executed
        # Then no partial data persisted
```

### Integration Tests Required
```python
# tests/integration/test_[feature]_api.py
class TestFeatureAPI:
    """Test API endpoints with real dependencies."""
    
    async def test_create_endpoint_success(self, client, auth_headers):
        """POST /[feature] should create and return resource."""
        # Given authenticated request with valid payload
        # When endpoint called
        # Then 201 Created with resource data
    
    async def test_auth_required(self, client):
        """Endpoints should require authentication."""
        # Given request without auth headers
        # When endpoint called
        # Then 401 Unauthorized
    
    async def test_validation_errors_returned(self, client, auth_headers):
        """Invalid input should return structured errors."""
        # Given request with invalid data
        # When endpoint called
        # Then 422 with field-specific errors
    
    async def test_rate_limiting(self, client, auth_headers):
        """Rate limits should be enforced."""
        # Given multiple rapid requests
        # When limit exceeded
        # Then 429 Too Many Requests
```

### E2E Tests Required
```python
# tests/e2e/test_[feature]_scenarios.py
class TestFeatureScenarios:
    """Test complete user workflows."""
    
    async def test_complete_workflow(self):
        """User should complete full feature workflow."""
        # Given fresh system state
        # When user performs complete workflow
        # Then expected final state achieved
    
    async def test_error_recovery(self):
        """System should handle and recover from errors."""
        # Given workflow with injected failures
        # When errors occur
        # Then graceful degradation and recovery
```

### Performance Requirements
```python
# tests/performance/test_[feature]_load.py
class FeatureLoadTest(HttpUser):
    """Load test for feature endpoints."""
    
    @task
    def test_create_performance(self):
        # Target: 95th percentile < 200ms
        # Load: 100 concurrent users
        # Duration: 5 minutes sustained
```

### Test Data & Fixtures
```python
# tests/fixtures/[feature]_fixtures.py
@pytest.fixture
def valid_feature_data():
    """Valid test data matching schema."""
    return {
        "field1": "test_value",
        "field2": 123,
        # All required fields with valid values
    }

@pytest.fixture
def mock_external_service(mocker):
    """Mock external dependencies."""
    return mocker.patch('external.service.call')
```

## Implementation Blueprint

### Task Breakdown
```yaml
Task 1 - Data Models:
  CREATE src/models/feature.py:
    - Define Pydantic models with validation
    - Include model_config for v2 compatibility
    - Add custom validators for business logic
    
  CREATE src/db/feature.py:
    - SQLAlchemy models matching Pydantic
    - Include indexes for query performance
    - Add created_at, updated_at timestamps

Task 2 - Core Logic:
  CREATE src/services/feature_service.py:
    - Business logic separated from API
    - Dependency injection for testability
    - Comprehensive error handling
    
  MODIFY src/services/__init__.py:
    - Export new service functions

Task 3 - API Endpoints:
  CREATE src/api/endpoints/feature.py:
    - RESTful endpoints using FastAPI
    - Proper status codes and responses
    - OpenAPI documentation via docstrings
    
  MODIFY src/api/router.py:
    - Register new router with prefix

Task 4 - Agent Integration:
  CREATE src/agents/feature_agent.py:
    - Extend BaseAgent class
    - Implement required methods
    - Add to agent registry

Task 5 - Testing:
  CREATE tests/test_feature_models.py:
    - Pydantic model validation tests
    - Edge case coverage
    
  CREATE tests/test_feature_api.py:
    - API endpoint tests with TestClient
    - Auth flow testing
    - Error response validation
    
  CREATE tests/test_feature_integration.py:
    - End-to-end workflow tests
    - Performance benchmarks
```

### Implementation Patterns

```python
# Pattern 1: Async Service Layer
class FeatureService:
    def __init__(self, db: AsyncSession, cache: Redis):
        self.db = db
        self.cache = cache
    
    async def create_feature(self, data: FeatureCreate) -> Feature:
        # Validation
        await self.validate_business_rules(data)
        
        # Transaction with rollback
        async with self.db.begin():
            db_feature = FeatureDB(**data.model_dump())
            self.db.add(db_feature)
            await self.db.flush()
            
            # Cache invalidation
            await self.cache.delete(f"feature:{db_feature.id}")
            
        return Feature.model_validate(db_feature)

# Pattern 2: API Endpoint with Dependencies
@router.post("/features", response_model=FeatureResponse)
async def create_feature(
    data: FeatureCreate,
    current_user: User = Depends(get_current_user),
    service: FeatureService = Depends(get_feature_service),
    limiter: RateLimiter = Depends(get_rate_limiter),
):
    await limiter.check(current_user.id)
    
    try:
        feature = await service.create_feature(data)
        return FeatureResponse(
            status="success",
            data=feature,
            message="Feature created successfully"
        )
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Validation Loops

### Level 1: Syntax & Style (Automated by Hooks)
```bash
# Run automatically via pre-commit hooks
ruff check src/ --fix           # Linting with fixes
ruff format src/                # Formatting
mypy src/ --strict              # Type checking

# Expected: All pass with no errors
```

### Level 2: Unit Tests
```bash
# Test models and business logic
pytest tests/test_feature_models.py -v
pytest tests/test_feature_service.py -v

# Coverage requirement
pytest tests/ --cov=src/features --cov-report=term-missing
# Expected: >80% coverage
```

### Level 3: Integration Tests
```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/test_feature_integration.py -v -m integration

# API contract tests
pytest tests/test_feature_api.py -v

# Load test
locust -f tests/load/feature_load_test.py --headless \
  --users 100 --spawn-rate 10 --run-time 60s
```

### Level 4: Security & Production Validation
```bash
# Security scan
bandit -r src/features/
safety check
pip-audit

# Performance profiling
python -m cProfile -o profile.stats src/features/benchmark.py
snakeviz profile.stats

# Memory profiling
mprof run python src/features/memory_test.py
mprof plot

# Production smoke test
curl -X POST https://staging-api.example.com/features \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## Deployment Checklist
- [ ] All validation loops pass
- [ ] Database migrations created and tested
- [ ] API documentation updated
- [ ] Monitoring alerts configured
- [ ] Feature flags configured (if applicable)
- [ ] Rollback plan documented

## Anti-Patterns to Avoid
- ❌ Don't use sync functions in async context
- ❌ Don't bypass the service layer for database access
- ❌ Don't catch all exceptions - be specific
- ❌ Don't hardcode configuration values
- ❌ Don't skip input validation
- ❌ Don't ignore rate limiting
- ❌ Don't commit without tests

## Confidence Score: [X]/10

### Scoring Rationale:
- Documentation completeness: [X]/2
- Pattern examples: [X]/2
- Gotchas identified: [X]/2
- Test coverage: [X]/2
- Automation readiness: [X]/2
