---
name: tdd-config
aliases: [test-config, configure-tdd]
description: Configure Test-Driven Development settings
category: Testing
---

# Configure TDD Settings: $ARGUMENTS

Manage Test-Driven Development configuration for the project.

## Current Configuration

Loading from: .claude/hooks/config.json

```json
{
  "tdd": {
    "enforce": true,         // Block code without tests
    "coverage_threshold": 80, // Minimum test coverage %
    "allow_override": false  // Allow bypassing TDD
  },
  "test_validation": {
    "auto_run": true,        // Run tests after code changes
    "block_on_failure": true, // Block if tests fail
    "coverage_required": false // Require coverage threshold
  }
}
```

## Available Commands

### Enable/Disable TDD
```bash
# Enable TDD enforcement
/tdd-config enable

# Disable TDD (not recommended)
/tdd-config disable

# Allow override (warn but don't block)
/tdd-config allow-override
```

### Set Coverage Threshold
```bash
# Set minimum coverage percentage
/tdd-config coverage 90

# Disable coverage requirement
/tdd-config coverage off
```

### Configure Auto-Validation
```bash
# Enable auto test runs
/tdd-config auto-run on

# Set to warning mode (don't block on failure)
/tdd-config warn-only
```

## TDD Workflow Status

### Active Hooks
- **19-test-generation-enforcer**: $STATUS
  - Blocks code creation without tests
  - Checks for test file existence
  - Validates test coverage

- **12-code-test-validator**: $STATUS
  - Runs tests after code changes
  - Reports pass/fail status
  - Checks coverage if enabled

### Recent Activity
```
Last 5 TDD events:
- [timestamp] Blocked: user_service.py (no tests)
- [timestamp] Passed: auth_api.py (15/15 tests)
- [timestamp] Warning: data_model.py (70% coverage)
```

## Best Practices

### 1. Red-Green-Refactor Cycle
```
1. RED: Write failing test first
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve code maintaining green
```

### 2. Test Organization
```
tests/
├── unit/          # Fast, isolated tests
├── integration/   # Component interaction tests
├── e2e/          # Full workflow tests
└── fixtures/     # Shared test data
```

### 3. Coverage Guidelines
- **80%+**: Good baseline
- **90%+**: Excellent coverage
- **100%**: Only for critical paths

## Troubleshooting

### "Tests Required" Error
```bash
# Generate tests for current feature
/generate-tests [feature-name]

# Or create minimal test file
echo "import pytest" > tests/unit/test_[feature].py
```

### Tests Not Running
```bash
# Check pytest installation
pip install pytest pytest-cov pytest-asyncio

# Run tests manually
pytest tests/ -v
```

### Override for Emergency
```bash
# Temporary override (resets on restart)
/tdd-config override-once

# Or modify config.json directly
```

## Integration with Workflows

TDD is integrated into:
- `/chain tdd` - Full TDD workflow
- `/chain tf` - Test-first approach
- `/py-prd` - Includes test specs
- `/prp-create` - Generates test requirements

## Metrics

### Project Test Health
- Total Tests: $TOTAL_TESTS
- Average Coverage: $AVG_COVERAGE%
- TDD Compliance: $COMPLIANCE%
- Blocked Attempts: $BLOCKED_COUNT

### Benefits Realized
- Bugs Prevented: ~$BUGS_PREVENTED
- Refactor Confidence: High
- Documentation: Tests as specs
- Design Quality: Improved

## Next Steps

1. Ensure TDD is enabled
2. Set appropriate coverage threshold
3. Use `/chain tdd` for new features
4. Monitor test health regularly