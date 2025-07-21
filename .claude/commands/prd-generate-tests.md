# PRD Test Generation

Automatically generate executable tests from PRD acceptance criteria.

## Arguments:
- $FEATURE: Feature name or PRD file path
- $OPTIONS: --framework=vitest|jest|playwright --type=unit|integration|e2e

## Usage:

```bash
/prd generate-tests auth-system
/prd generate-tests user-profile --framework=vitest
/prd generate-tests checkout --type=e2e
```

## What It Does:

1. **Parses PRD Acceptance Criteria**
   - Extracts each criterion
   - Identifies testable assertions
   - Determines test type needed

2. **Generates Test Structure**
   - Creates test files
   - Organizes by test type
   - Links to PRD sections

3. **Creates Test Cases**
   - Happy path for each criterion
   - Edge cases based on requirements
   - Error scenarios

4. **Tracks Coverage**
   - Maps tests to PRD sections
   - Shows uncovered criteria
   - Updates as you implement

## Example:

### PRD Acceptance Criteria:
```markdown
## Acceptance Criteria
- Users can login with email and password
- Invalid credentials display error message
- Successful login redirects to dashboard
- Session persists for 24 hours
- Rate limiting prevents brute force (5 attempts/minute)
```

### Generated Tests:

```typescript
// tests/features/auth-system/login.test.ts
import { describe, test, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from '@/components/auth/LoginForm';

describe('Auth System: User Login', () => {
  // Links to PRD: auth-system-PRD.md#acceptance-criteria-1
  describe('Users can login with email and password', () => {
    test('successful login with valid credentials', async () => {
      const { user } = render(<LoginForm />);
      
      await user.type(screen.getByLabelText('Email'), 'user@example.com');
      await user.type(screen.getByLabelText('Password'), 'ValidPass123');
      await user.click(screen.getByRole('button', { name: 'Login' }));
      
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'ValidPass123'
      });
    });
    
    test('validates email format', async () => {
      const { user } = render(<LoginForm />);
      
      await user.type(screen.getByLabelText('Email'), 'invalid-email');
      await user.click(screen.getByRole('button', { name: 'Login' }));
      
      expect(screen.getByText('Invalid email format')).toBeInTheDocument();
    });
  });
  
  // Links to PRD: auth-system-PRD.md#acceptance-criteria-2
  describe('Invalid credentials display error message', () => {
    test('shows error for wrong password', async () => {
      mockLogin.mockRejectedValue({ code: 'INVALID_CREDENTIALS' });
      
      const { user } = render(<LoginForm />);
      await user.type(screen.getByLabelText('Email'), 'user@example.com');
      await user.type(screen.getByLabelText('Password'), 'WrongPass');
      await user.click(screen.getByRole('button', { name: 'Login' }));
      
      expect(screen.getByText('Invalid email or password')).toBeInTheDocument();
    });
  });
});

// tests/features/auth-system/login.e2e.ts
import { test, expect } from '@playwright/test';

test.describe('Auth System: Login Flow E2E', () => {
  // Links to PRD: auth-system-PRD.md#acceptance-criteria-3
  test('successful login redirects to dashboard', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'TestPass123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
  
  // Links to PRD: auth-system-PRD.md#acceptance-criteria-5
  test('rate limiting prevents brute force', async ({ page }) => {
    await page.goto('/login');
    
    // Attempt 6 logins (limit is 5)
    for (let i = 0; i < 6; i++) {
      await page.fill('[name="email"]', 'test@example.com');
      await page.fill('[name="password"]', `wrong${i}`);
      await page.click('button[type="submit"]');
    }
    
    await expect(page.locator('.error')).toContainText('Too many attempts');
  });
});
```

### Generated Test Plan:
```markdown
# Test Coverage Report: auth-system

## Acceptance Criteria Coverage
✅ Users can login with email and password (2 tests)
✅ Invalid credentials display error message (1 test)
✅ Successful login redirects to dashboard (1 test)
⚠️ Session persists for 24 hours (0 tests - needs implementation)
✅ Rate limiting prevents brute force (1 test)

## Test Distribution
- Unit tests: 3
- Integration tests: 0
- E2E tests: 2

## Uncovered Scenarios
- Session persistence testing
- Network error handling
- Concurrent login attempts

Run: /prd test-coverage auth-system
```

## Advanced Features:

### 1. Smart Test Generation
- Detects UI elements from PRD
- Infers API contracts
- Generates appropriate assertions

### 2. Test Helpers
```typescript
// Generated test utilities
export const authTestHelpers = {
  mockValidUser: () => ({
    email: 'test@example.com',
    password: 'ValidPass123'
  }),
  
  setupAuthMocks: () => {
    // Mock setup based on PRD
  }
};
```

### 3. Coverage Tracking
```bash
/prd test-coverage auth-system
```
Shows:
- Which criteria have tests
- Test execution results
- Links back to PRD

### 4. Test Evolution
- Updates tests when PRD changes
- Suggests new tests for new criteria
- Removes obsolete tests

## Integration:

Works with:
- `/pt` - Runs relevant tests after each task
- `/sv` - Validates test coverage for stage
- `/fw complete` - Ensures all criteria tested

## Configuration:

```json
// .claude/config.json
{
  "grove_enhancements": {
    "test_generation": {
      "enabled": true,
      "frameworks": {
        "unit": "vitest",
        "e2e": "playwright"
      },
      "coverage_target": 0.9,
      "include_edge_cases": true,
      "include_error_cases": true
    }
  }
}
```

## Benefits:
- PRD becomes single source of truth
- Tests directly map to requirements
- No missed acceptance criteria
- Faster test writing
- Living documentation
