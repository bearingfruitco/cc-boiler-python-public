# Test Runner

Intelligent test execution with context awareness.

## Arguments:
- $SCOPE: current|changed|related|all
- $TYPE: unit|integration|e2e|visual
- $WATCH: true|false

## Why This Command:
- Run only relevant tests
- Track test coverage per feature
- Integrate with TODO system
- Maintain test context

## Steps:

### Scope: CURRENT
Test only current file/feature:

```bash
# Detect current file
CURRENT_FILE=$(grep "Location:" .claude/context/current.md | \
  head -1 | cut -d' ' -f2 | cut -d':' -f1)

# Find related test
TEST_FILE=$(echo $CURRENT_FILE | \
  sed 's/\.tsx$/.test.tsx/' | \
  sed 's|components/|__tests__/components/|')

# Run test
if [ -f "$TEST_FILE" ]; then
  npm test -- $TEST_FILE
else
  echo "❌ No test found for $CURRENT_FILE"
  echo "Create: $TEST_FILE"
  
  # Generate test template
  /create-component test ${CURRENT_FILE}
fi
```

### Scope: CHANGED
Test all modified files:

```bash
# Get changed files
CHANGED=$(git diff --name-only HEAD | grep -E '\.(tsx?|jsx?)$')

# Find their tests
for file in $CHANGED; do
  TEST=$(echo $file | sed 's/\.tsx$/.test.tsx/')
  if [ -f "$TEST" ]; then
    npm test -- $TEST --coverage
  fi
done

# Update context
echo "## Test Results
Files tested: $(echo $CHANGED | wc -w)
Coverage: $(cat coverage/coverage-summary.json | jq '.total.lines.pct')%
" >> .claude/context/current.md
```

### Scope: RELATED
Test entire feature:

```bash
# Get current issue
ISSUE=$(git branch --show-current | grep -oE '[0-9]+')

# Find all files related to issue
RELATED=$(git log --name-only --grep="#$ISSUE" | \
  grep -E '\.(tsx?|jsx?)$' | sort -u)

# Run tests with coverage
npm test -- --coverage --testPathPattern="(${RELATED})"

# Generate report
echo "## Feature Test Report - Issue #$ISSUE
Coverage: X%
Tests: Y passed, Z failed
TODOs: Added N test TODOs
"
```

### Test Generation
Create missing tests:

```bash
# For component without test
/test-runner generate LoginForm

# Creates:
cat > __tests__/components/auth/LoginForm.test.tsx << 'EOF'
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from '@/components/auth/LoginForm';

describe('LoginForm', () => {
  it('follows design system rules', () => {
    render(<LoginForm />);
    
    // Check typography
    const headings = screen.getAllByRole('heading');
    headings.forEach(h => {
      const classes = h.className;
      expect(classes).toMatch(/text-size-[1-4]/);
      expect(classes).toMatch(/font-(regular|semibold)/);
    });
    
    // Check spacing
    const container = screen.getByTestId('login-form');
    expect(container.className).toMatch(/p-[1234678]/);
  });
  
  it('handles form submission', async () => {
    // TODO: Mock API and test submission
  });
  
  it('displays validation errors', () => {
    // TODO: Test error states
  });
});
EOF
```

### Visual Regression Testing
Compare against baseline:

```bash
# Capture current state
/test-runner visual capture

# After changes
/test-runner visual compare

# Results
echo "## Visual Changes Detected
- LoginForm: 2 differences
  - Button color changed
  - Spacing increased
  
Review: .claude/visual-diffs/
"
```

## Coverage Tracking:

```json
{
  "issue-23": {
    "components": {
      "LoginForm": 85,
      "RegisterForm": 92,
      "AuthLayout": 100
    },
    "overall": 89,
    "target": 80,
    "status": "passing"
  }
}
```

## Integration with Other Commands:

```bash
# Before PR
/feature-workflow validate 23
> Running tests... ✅
> Coverage: 89% (target: 80%) ✅
> Visual regression: No changes ✅
