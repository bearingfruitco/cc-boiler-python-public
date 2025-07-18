# Testing Guide

## Overview

This guide covers testing strategies for modern web applications, including unit tests, integration tests, and end-to-end tests.

## Testing Stack

- **Vitest** - Unit and integration testing
- **React Testing Library** - Component testing
- **Playwright** - End-to-end testing
- **MSW** - API mocking

## Project Setup

### Installation

```bash
# Install testing dependencies
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
pnpm add -D @testing-library/user-event @vitejs/plugin-react
pnpm add -D playwright @playwright/test
pnpm add -D msw
```

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './test/setup.ts',
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'test/',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
});
```

### Test Setup

```typescript
// test/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};
```

## Unit Testing

### Component Testing

```typescript
// components/__tests__/Button.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '../Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();
    
    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole('button'));
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('can be disabled', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Click me</Button>);
    expect(screen.getByRole('button')).toHaveClass('custom-class');
  });
});
```

### Hook Testing

```typescript
// hooks/__tests__/useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from '../useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments counter', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });

  it('decrements counter', () => {
    const { result } = renderHook(() => useCounter(5));
    
    act(() => {
      result.current.decrement();
    });
    
    expect(result.current.count).toBe(4);
  });
});
```

### Utility Function Testing

```typescript
// lib/__tests__/validation.test.ts
import { validateEmail, validatePhone, sanitizeInput } from '../validation';

describe('validation utilities', () => {
  describe('validateEmail', () => {
    it('validates correct email format', () => {
      expect(validateEmail('user@example.com')).toBe(true);
      expect(validateEmail('test.user+tag@domain.co.uk')).toBe(true);
    });

    it('rejects invalid email format', () => {
      expect(validateEmail('invalid')).toBe(false);
      expect(validateEmail('@example.com')).toBe(false);
      expect(validateEmail('user@')).toBe(false);
    });
  });

  describe('validatePhone', () => {
    it('validates US phone numbers', () => {
      expect(validatePhone('1234567890')).toBe(true);
      expect(validatePhone('123-456-7890')).toBe(true);
      expect(validatePhone('(123) 456-7890')).toBe(true);
    });

    it('rejects invalid phone numbers', () => {
      expect(validatePhone('123')).toBe(false);
      expect(validatePhone('abcdefghij')).toBe(false);
    });
  });

  describe('sanitizeInput', () => {
    it('removes script tags', () => {
      const input = 'Hello <script>alert("xss")</script> World';
      expect(sanitizeInput(input)).toBe('Hello  World');
    });

    it('escapes HTML entities', () => {
      const input = '<div>Test & "quotes"</div>';
      expect(sanitizeInput(input)).toBe('&lt;div&gt;Test &amp; &quot;quotes&quot;&lt;/div&gt;');
    });
  });
});
```

## Integration Testing

### API Route Testing

```typescript
// app/api/__tests__/items.test.ts
import { createMocks } from 'node-mocks-http';
import { GET, POST } from '../items/route';

describe('/api/items', () => {
  describe('GET', () => {
    it('returns list of items', async () => {
      const { req } = createMocks({
        method: 'GET',
      });

      const response = await GET(req as any);
      const json = await response.json();

      expect(response.status).toBe(200);
      expect(json.data).toBeInstanceOf(Array);
    });

    it('supports pagination', async () => {
      const { req } = createMocks({
        method: 'GET',
        query: {
          page: '2',
          limit: '10',
        },
      });

      const response = await GET(req as any);
      const json = await response.json();

      expect(json.pagination.page).toBe(2);
      expect(json.pagination.limit).toBe(10);
    });
  });

  describe('POST', () => {
    it('creates new item', async () => {
      const { req } = createMocks({
        method: 'POST',
        headers: {
          'content-type': 'application/json',
        },
        body: {
          name: 'Test Item',
          description: 'Test Description',
        },
      });

      const response = await POST(req as any);
      const json = await response.json();

      expect(response.status).toBe(201);
      expect(json.data).toHaveProperty('id');
      expect(json.data.name).toBe('Test Item');
    });

    it('validates required fields', async () => {
      const { req } = createMocks({
        method: 'POST',
        body: {
          // Missing required name field
          description: 'Test Description',
        },
      });

      const response = await POST(req as any);
      const json = await response.json();

      expect(response.status).toBe(400);
      expect(json.error).toBe('Validation failed');
    });
  });
});
```

### Database Testing

```typescript
// lib/db/__tests__/queries.test.ts
import { beforeAll, afterAll, beforeEach } from 'vitest';
import { createUser, getUserById, updateUser } from '../queries';
import { resetDatabase } from '../../test/db-helpers';

describe('Database queries', () => {
  beforeAll(async () => {
    // Set up test database
    process.env.DATABASE_URL = process.env.TEST_DATABASE_URL;
  });

  beforeEach(async () => {
    // Reset database before each test
    await resetDatabase();
  });

  afterAll(async () => {
    // Clean up
  });

  describe('createUser', () => {
    it('creates a new user', async () => {
      const userData = {
        email: 'test@example.com',
        username: 'testuser',
        full_name: 'Test User',
      };

      const user = await createUser(userData);

      expect(user).toHaveProperty('id');
      expect(user.email).toBe(userData.email);
      expect(user.username).toBe(userData.username);
    });

    it('enforces unique email constraint', async () => {
      const userData = {
        email: 'duplicate@example.com',
        username: 'user1',
      };

      await createUser(userData);

      await expect(
        createUser({ ...userData, username: 'user2' })
      ).rejects.toThrow('unique constraint');
    });
  });

  describe('getUserById', () => {
    it('retrieves existing user', async () => {
      const created = await createUser({
        email: 'find@example.com',
        username: 'findme',
      });

      const found = await getUserById(created.id);

      expect(found).toEqual(created);
    });

    it('returns null for non-existent user', async () => {
      const user = await getUserById('non-existent-id');
      expect(user).toBeNull();
    });
  });
});
```

## End-to-End Testing

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

### E2E Test Examples

```typescript
// e2e/user-flow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Flow', () => {
  test('completes full user journey', async ({ page }) => {
    // Navigate to homepage
    await page.goto('/');
    
    // Check page loaded
    await expect(page).toHaveTitle(/Welcome/);
    
    // Start flow
    await page.click('text=Get Started');
    
    // Fill form
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="name"]', 'Test User');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for navigation
    await page.waitForURL('/success');
    
    // Verify success page
    await expect(page.locator('h1')).toContainText('Thank You');
  });

  test('handles form validation', async ({ page }) => {
    await page.goto('/form');
    
    // Try to submit empty form
    await page.click('button[type="submit"]');
    
    // Check validation messages
    await expect(page.locator('text=Email is required')).toBeVisible();
    await expect(page.locator('text=Name is required')).toBeVisible();
    
    // Fill invalid email
    await page.fill('input[name="email"]', 'invalid-email');
    await page.click('button[type="submit"]');
    
    // Check email validation
    await expect(page.locator('text=Invalid email format')).toBeVisible();
  });

  test('responsive design', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Check mobile menu
    await expect(page.locator('.mobile-menu')).toBeHidden();
    await page.click('.menu-toggle');
    await expect(page.locator('.mobile-menu')).toBeVisible();
    
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page.locator('.desktop-nav')).toBeVisible();
    await expect(page.locator('.menu-toggle')).toBeHidden();
  });
});
```

### Visual Regression Testing

```typescript
// e2e/visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage screenshot', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });

  test('form states', async ({ page }) => {
    await page.goto('/form');
    
    // Default state
    await expect(page.locator('form')).toHaveScreenshot('form-default.png');
    
    // Focus state
    await page.focus('input[name="email"]');
    await expect(page.locator('form')).toHaveScreenshot('form-focused.png');
    
    // Error state
    await page.click('button[type="submit"]');
    await expect(page.locator('form')).toHaveScreenshot('form-errors.png');
  });
});
```

## API Mocking with MSW

### Setup MSW

```typescript
// mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.get('/api/items', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          { id: '1', name: 'Item 1' },
          { id: '2', name: 'Item 2' },
        ],
      })
    );
  }),

  rest.post('/api/items', async (req, res, ctx) => {
    const body = await req.json();
    
    return res(
      ctx.status(201),
      ctx.json({
        data: {
          id: '3',
          ...body,
        },
      })
    );
  }),
];

// mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### Using MSW in Tests

```typescript
// components/__tests__/ItemList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { server } from '../../mocks/server';
import { rest } from 'msw';
import { ItemList } from '../ItemList';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('ItemList', () => {
  it('displays items from API', async () => {
    render(<ItemList />);
    
    await waitFor(() => {
      expect(screen.getByText('Item 1')).toBeInTheDocument();
      expect(screen.getByText('Item 2')).toBeInTheDocument();
    });
  });

  it('handles API errors', async () => {
    server.use(
      rest.get('/api/items', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ error: 'Server error' }));
      })
    );

    render(<ItemList />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to load items')).toBeInTheDocument();
    });
  });
});
```

## Test Coverage

### Coverage Configuration

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "test:watch": "vitest watch"
  }
}
```

### Coverage Requirements

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
      exclude: [
        'node_modules/',
        'test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData.ts',
      ],
    },
  },
});
```

## Testing Best Practices

### 1. Test Structure

```typescript
// Follow AAA pattern
test('should calculate total price with discount', () => {
  // Arrange
  const items = [
    { price: 100, quantity: 2 },
    { price: 50, quantity: 1 },
  ];
  const discountPercent = 10;

  // Act
  const total = calculateTotal(items, discountPercent);

  // Assert
  expect(total).toBe(225); // (200 + 50) * 0.9
});
```

### 2. Test Data Builders

```typescript
// test/builders/user.builder.ts
export class UserBuilder {
  private user = {
    id: '1',
    email: 'test@example.com',
    username: 'testuser',
    role: 'user',
  };

  withId(id: string) {
    this.user.id = id;
    return this;
  }

  withEmail(email: string) {
    this.user.email = email;
    return this;
  }

  withRole(role: string) {
    this.user.role = role;
    return this;
  }

  build() {
    return { ...this.user };
  }
}

// Usage in tests
const adminUser = new UserBuilder()
  .withRole('admin')
  .withEmail('admin@example.com')
  .build();
```

### 3. Custom Matchers

```typescript
// test/matchers.ts
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () => `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true,
      };
    } else {
      return {
        message: () => `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false,
      };
    }
  },
});

// Usage
expect(value).toBeWithinRange(1, 100);
```

## Testing Checklist

### Before Commit
- [ ] All tests pass locally
- [ ] New features have tests
- [ ] Test coverage meets minimum (80%)
- [ ] No `.only` or `.skip` in tests

### Test Types
- [ ] Unit tests for utilities
- [ ] Component tests for UI
- [ ] Integration tests for APIs
- [ ] E2E tests for critical paths

### Quality Checks
- [ ] Tests are maintainable
- [ ] Tests are isolated
- [ ] Tests are deterministic
- [ ] Tests have clear names

Remember: Good tests enable confident refactoring and catch bugs before users do.