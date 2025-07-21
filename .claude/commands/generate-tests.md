---
name: generate-tests
aliases: [gen-tests, tdd-tests, create-tests, gt-tests]
description: Generate comprehensive tests from PRD/PRP/Issues before implementation
category: Testing
---

# Generate Tests for: $ARGUMENTS

Generate comprehensive test suites based on specifications before implementation.

## Test Generation Strategy

### 1. Analyze Source Documents
- Extract acceptance criteria from PRD/PRP
- Identify test scenarios from issues
- Parse component specifications
- Extract performance requirements

### 2. Determine Test Types Needed
- **Unit Tests**: Individual functions/methods
- **Integration Tests**: Component interactions
- **E2E Tests**: Full user workflows
- **Performance Tests**: Load and response times
- **Security Tests**: Auth and validation

### 3. Generate Test Structure

```
tests/
├── unit/
│   ├── test_${feature}_models.py      # Data model tests
│   ├── test_${feature}_services.py    # Business logic tests
│   └── test_${feature}_utils.py       # Helper function tests
├── integration/
│   ├── test_${feature}_api.py         # API endpoint tests
│   └── test_${feature}_flow.py        # Multi-component tests
├── e2e/
│   └── test_${feature}_scenarios.py   # Complete user journeys
└── fixtures/
    └── ${feature}_fixtures.py         # Test data and mocks
```

## Test Template Patterns

### Unit Test Pattern
```python
import pytest
from src.models.${feature} import ${Model}
from src.services.${feature}_service import ${Service}

class Test${Model}:
    """Test ${Model} validation and behavior."""
    
    def test_valid_creation(self):
        """${Model} should accept valid data."""
        # Given
        valid_data = {...}
        
        # When
        model = ${Model}(**valid_data)
        
        # Then
        assert model.field == expected_value
    
    def test_validation_errors(self):
        """${Model} should reject invalid data."""
        # Given
        invalid_data = {...}
        
        # When/Then
        with pytest.raises(ValidationError):
            ${Model}(**invalid_data)
```

### Integration Test Pattern
```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

class Test${Feature}API:
    """Test ${feature} API endpoints."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_create_endpoint(self, client):
        """POST /${feature} should create resource."""
        # Given
        payload = {...}
        
        # When
        response = client.post("/${feature}", json=payload)
        
        # Then
        assert response.status_code == 201
        assert response.json()["id"] is not None
```

### Performance Test Pattern
```python
import pytest
import time
from locust import HttpUser, task, between

class ${Feature}LoadTest(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_endpoint_performance(self):
        """Endpoint should handle load."""
        start = time.time()
        response = self.client.get("/${feature}")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 0.2  # 200ms requirement
```

## Extraction Rules

### From PRD/PRP
- Each "Success Criteria" → Test Case
- Each "Validation Loop" → Test Type
- Each "Performance Requirement" → Benchmark
- Each "Security Requirement" → Security Test

### From Issues
- Each "Acceptance Criteria" → Test Scenario
- Each "Definition of Done" → Assertion
- Each "Edge Case" → Negative Test

### From Code Comments
- TODO/FIXME → Pending Test
- NOTE → Test Documentation
- CRITICAL → Priority Test

## Generation Process

1. **Parse Documents**
   ```bash
   # Check for existing specs
   /exists tests/test_${feature}
   
   # Load PRD/PRP
   cat PRPs/active/${feature}.md
   
   # Extract test requirements
   grep -E "(Success Criteria|Acceptance|Should|Must)" 
   ```

2. **Create Test Files**
   ```python
   # Auto-generate based on patterns
   for component in components:
       generate_unit_test(component)
       generate_integration_test(component)
   ```

3. **Add Fixtures**
   ```python
   # Generate test data
   @pytest.fixture
   def valid_${model}_data():
       return {
           "field": "test_value",
           # Based on model schema
       }
   ```

4. **Include Mocks**
   ```python
   # Mock external services
   @pytest.fixture
   def mock_bigquery(mocker):
       return mocker.patch('google.cloud.bigquery.Client')
   ```

## Output Format

### Test Manifest (tests/${feature}_manifest.json)
```json
{
  "feature": "${feature}",
  "generated_from": {
    "prd": "PRPs/active/${feature}.md",
    "issues": ["#123", "#124"],
    "timestamp": "2024-01-20T10:00:00Z"
  },
  "test_suites": {
    "unit": {
      "files": ["test_${feature}_models.py"],
      "count": 15,
      "coverage_target": 90
    },
    "integration": {
      "files": ["test_${feature}_api.py"],
      "count": 8,
      "coverage_target": 80
    },
    "e2e": {
      "files": ["test_${feature}_scenarios.py"],
      "count": 3,
      "coverage_target": 100
    }
  },
  "requirements": {
    "performance": {
      "response_time_95th": 200,
      "concurrent_users": 100
    },
    "security": {
      "auth_required": true,
      "input_validation": true
    }
  }
}
```

## Integration with Hooks

The test-generation-enforcer hook will:
1. Block code creation without tests
2. Validate test coverage requirements
3. Ensure tests match specifications

## Usage Examples

```bash
# Generate from active PRP
/generate-tests user-authentication

# Generate from specific issue
/generate-tests --issue #123

# Generate specific test type
/generate-tests --type unit models/user

# Regenerate after spec change
/generate-tests --update user-auth
```

## Success Criteria

- [ ] All acceptance criteria have corresponding tests
- [ ] Test structure matches project conventions
- [ ] Fixtures provide realistic test data
- [ ] Performance requirements are benchmarked
- [ ] Security concerns are tested
- [ ] Tests are executable immediately

## Next Steps

After generation:
1. Review generated tests
2. Run tests (they should fail - TDD!)
3. Implement code to make tests pass
4. Use `/test-runner` to validate