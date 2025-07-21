---
name: verify
aliases: [verification, check-complete]
description: Run verification checks on features or tasks
category: quality
---

Run comprehensive verification to ensure implementations actually work.

## Usage
```bash
/verify [feature/task] [options]
```

## Options
- `--level`: Verification level (quick, standard, comprehensive)
- `--step`: Run specific verification step only
- `--verbose`: Show detailed output
- `--force`: Run even if recently verified

## Examples
```bash
# Verify current feature
/verify

# Verify specific feature
/verify user-auth

# Run comprehensive verification
/verify user-auth --level=comprehensive

# Run only unit tests
/verify --step=unit_tests

# Verbose output
/verify --verbose
```

## Verification Steps

### Quick Level
1. **tests_exist** - Verify test files exist
2. **recent_test_run** - Check if tests ran recently

### Standard Level (Default)
1. **tests_exist** - Verify test files exist
2. **unit_tests** - Run unit tests
3. **recent_test_run** - Verify recent test execution

### Comprehensive Level
1. **tests_exist** - Verify test files exist
2. **unit_tests** - Run unit tests
3. **integration_tests** - Run integration tests
4. **dependency_check** - Verify dependencies work
5. **regression_check** - Check for regressions

## Output
```
🔍 Running verification for: user-auth

✅ tests_exist: Found 3 test files
✅ unit_tests: 15 tests passed
✅ recent_test_run: Tests run 2 minutes ago

✅ Verification Complete - All checks passed!
```

## Integration with Workflow

This command is automatically triggered when:
- Claude claims something is "complete"
- Using `/fw complete`
- After `/pt` marks tasks done

## Verification Manifest

Results are stored in `.claude/verification-manifest.json`:
```json
{
  "feature_verifications": {
    "user-auth": {
      "last_verified": "2025-01-21T10:00:00Z",
      "verification_passed": true,
      "checks": [...]
    }
  }
}
```

## Troubleshooting

If verification fails:
1. Check test output with `--verbose`
2. Run specific step with `--step`
3. Fix issues and re-run
4. Use `/test` for detailed test debugging
