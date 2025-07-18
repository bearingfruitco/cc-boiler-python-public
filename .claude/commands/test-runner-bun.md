# Test Runner (Bun Edition)

Run tests using Bun's built-in test runner with intelligent scope detection.

## Arguments:
- $SCOPE: current|changed|related|all|watch
- $TYPE: unit|integration|e2e (optional)
- $COVERAGE: true|false (optional)

## Usage Examples:
```bash
/test-runner current         # Test current file
/test-runner changed         # Test modified files
/test-runner all --coverage  # Full test suite with coverage
/test-runner watch          # Watch mode
/tr changed                 # Short alias
```

## Steps:

### Scope: CURRENT
Test only current file/component:

```bash
# Detect current file from context
CURRENT_FILE=$(grep -E "^(Creating|Editing|Working on):" .claude/context/current.md | \
  head -1 | sed 's/.*: //' | sed 's/ .*//')

# Find related test file
if [[ $CURRENT_FILE == *.tsx || $CURRENT_FILE == *.ts ]]; then
  # Try multiple test file patterns
  TEST_PATTERNS=(
    "${CURRENT_FILE%.tsx}.test.tsx"
    "${CURRENT_FILE%.ts}.test.ts"
    "${CURRENT_FILE%.tsx}.spec.tsx"
    "${CURRENT_FILE%.ts}.spec.ts"
    "__tests__/${CURRENT_FILE}"
    "tests/${CURRENT_FILE%.tsx}.test.tsx"
  )
  
  for pattern in "${TEST_PATTERNS[@]}"; do
    if [ -f "$pattern" ]; then
      echo "🧪 Running test: $pattern"
      bun test "$pattern"
      break
    fi
  done
else
  echo "❌ No test found for $CURRENT_FILE"
  echo "💡 Create test with: /create-test $CURRENT_FILE"
fi
```

### Scope: CHANGED
Test all modified files:

```bash
# Get changed files
CHANGED=$(git diff --name-only HEAD | grep -E '\.(tsx?|jsx?)$' | grep -v test)

echo "🔍 Testing changed files..."

# Run tests for each changed file
for file in $CHANGED; do
  # Find corresponding test
  TEST_FILE="${file%.tsx}.test.tsx"
  if [ -f "$TEST_FILE" ]; then
    echo "Testing: $file"
    bun test "$TEST_FILE"
  else
    echo "⚠️ No test for: $file"
  fi
done

# Run with coverage if requested
if [[ "$COVERAGE" == "true" ]]; then
  bun test --coverage $CHANGED
fi
```

### Scope: RELATED
Test entire feature/issue:

```bash
# Get current branch/issue
ISSUE=$(git branch --show-current | grep -oE '[0-9]+')

if [ -n "$ISSUE" ]; then
  echo "🎯 Testing Issue #$ISSUE feature..."
  
  # Find all files related to issue
  RELATED=$(git log --name-only --grep="#$ISSUE" | \
    grep -E '\.(tsx?|jsx?)$' | grep -v test | sort -u)
  
  # Run tests with coverage
  bun test --coverage $(echo $RELATED | sed 's/\.tsx/.test.tsx/g')
  
  # Generate coverage report
  echo "📊 Coverage Report for Issue #$ISSUE"
  bun test --coverage --coverage-reporter=text
fi
```

### Scope: ALL
Run full test suite:

```bash
echo "🚀 Running all tests..."

# Run all tests with optional coverage
if [[ "$COVERAGE" == "true" ]]; then
  bun test --coverage
  
  # Show coverage summary
  echo ""
  echo "📊 Coverage Summary:"
  cat coverage/coverage-summary.json | jq -r '
    .total | 
    "Lines: \(.lines.pct)%\nStatements: \(.statements.pct)%\nFunctions: \(.functions.pct)%\nBranches: \(.branches.pct)%"
  '
else
  bun test
fi

# Check against thresholds
COVERAGE_THRESHOLD=80
CURRENT_COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
if (( $(echo "$CURRENT_COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
  echo "⚠️ Coverage below threshold: $CURRENT_COVERAGE% < $COVERAGE_THRESHOLD%"
fi
```

### Scope: WATCH
Run tests in watch mode:

```bash
echo "👀 Starting test watch mode..."
echo "Press Ctrl+C to stop"

# Bun's built-in watch mode
bun test --watch
```

### Type: E2E
Run Playwright E2E tests:

```bash
if [[ "$TYPE" == "e2e" ]]; then
  echo "🎭 Running E2E tests with Playwright..."
  
  # Ensure dev server is running
  if ! curl -s http://localhost:3000 > /dev/null; then
    echo "Starting dev server..."
    bun dev &
    DEV_PID=$!
    sleep 5
  fi
  
  # Run Playwright tests
  pnpm test:e2e
  
  # Clean up
  if [ -n "$DEV_PID" ]; then
    kill $DEV_PID
  fi
fi
```

## Integration with Hooks

The test runner integrates with pre-commit hooks:

```bash
# .claude/hooks/pre-commit/run-tests.sh
#!/bin/bash
# Automatically run tests for changed files before commit

CHANGED=$(git diff --cached --name-only | grep -E '\.(tsx?|jsx?)$')
if [ -n "$CHANGED" ]; then
  bun test $(echo $CHANGED | sed 's/\.tsx/.test.tsx/g')
fi
```

## Test Generation Helper

When no test exists, generate one:

```bash
# If no test found, create template
/test-runner generate Button

# Creates components/ui/Button.test.tsx:
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct design system classes', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button');
    
    // Check design system compliance
    expect(button.className).toMatch(/text-size-3/);
    expect(button.className).toMatch(/font-semibold/);
    expect(button.className).toMatch(/h-12/); // 48px = 12 * 4
  });
  
  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    screen.getByRole('button').click();
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## Performance Tracking

Track test performance over time:

```json
{
  "test-runs": {
    "2024-01-15": {
      "duration": "3.2s",
      "passed": 142,
      "failed": 0,
      "coverage": 87.3
    }
  }
}
```

## Aliases
- `/tr` - Short for test-runner
- `/test` - Alternative alias

This command ensures all code is tested using Bun's fast test runner!
