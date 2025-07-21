# Playwright MCP Integration Guide for Claude Code

## 🎭 Overview

The Playwright MCP (Model Context Protocol) enables AI agents to control browsers for testing and automation. This guide shows how to integrate it with the Claude Code boilerplate system.

## 🚀 Quick Setup

```bash
# 1. Install Playwright
npm install -D @playwright/test

# 2. Initialize Playwright
npx playwright install

# 3. Set up MCP in Claude Code
/spm  # or /setup-playwright-mcp
```

## 📁 Test Structure

```
tests/
├── browser/
│   ├── auth.spec.ts         # Authentication flows
│   ├── features/            # Feature-specific tests
│   │   ├── posts.spec.ts
│   │   └── profile.spec.ts
│   ├── fixtures/            # Test fixtures
│   │   └── auth.fixture.ts
│   └── helpers/             # Test utilities
│       └── page-objects.ts
```

## 🔧 Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/browser',
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
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## 🎯 Claude Code Commands

### Browser Test Flow Command

The `/btf` command orchestrates browser testing:

```bash
/btf auth          # Test auth feature
/btf profile       # Test profile feature
/btf              # Test current feature
```

This command:
1. Starts the dev server
2. Opens Playwright browser
3. Runs through test scenarios
4. Validates design system compliance
5. Captures screenshots
6. Reports results

## 📝 Test Patterns

### Basic Test Structure

```typescript
// tests/browser/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
  })

  test('should show login form', async ({ page }) => {
    // Check design system compliance
    const heading = page.locator('h2')
    await expect(heading).toHaveClass(/text-size-2/)
    await expect(heading).toHaveClass(/font-semibold/)
    
    // Check form elements
    await expect(page.locator('input[type="email"]')).toBeVisible()
    await expect(page.locator('input[type="password"]')).toBeVisible()
    await expect(page.locator('button[type="submit"]')).toBeVisible()
  })

  test('should login with valid credentials', async ({ page }) => {
    // Fill form
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    
    // Submit
    await page.click('button[type="submit"]')
    
    // Wait for navigation
    await page.waitForURL('/dashboard')
    
    // Verify logged in
    await expect(page.locator('text=Dashboard')).toBeVisible()
  })

  test('should show error with invalid credentials', async ({ page }) => {
    // Fill with invalid data
    await page.fill('input[type="email"]', 'wrong@example.com')
    await page.fill('input[type="password"]', 'wrongpass')
    
    // Submit
    await page.click('button[type="submit"]')
    
    // Check error message
    const error = page.locator('.bg-red-50')
    await expect(error).toBeVisible()
    await expect(error).toContainText('Invalid credentials')
  })
})
```

### Page Object Pattern

```typescript
// tests/browser/helpers/page-objects.ts
import { Page } from '@playwright/test'

export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.fill('input[type="email"]', email)
    await this.page.fill('input[type="password"]', password)
    await this.page.click('button[type="submit"]')
  }

  async getErrorMessage() {
    return this.page.locator('.bg-red-50').textContent()
  }
}

// Usage in test
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('test@example.com', 'password123')
  await page.waitForURL('/dashboard')
})
```

### Design System Validation

```typescript
// tests/browser/helpers/design-validation.ts
import { Page, expect } from '@playwright/test'

export async function validateDesignSystem(page: Page) {
  // Check font sizes
  const headings = await page.locator('h1, h2, h3, h4, h5, h6').all()
  for (const heading of headings) {
    const classes = await heading.getAttribute('class') || ''
    expect(classes).toMatch(/text-size-[1-4]/)
    expect(classes).not.toMatch(/text-(sm|lg|xl|2xl)/)
  }

  // Check font weights
  const textElements = await page.locator('p, span, div, button').all()
  for (const element of textElements) {
    const classes = await element.getAttribute('class') || ''
    if (classes.includes('font-')) {
      expect(classes).toMatch(/font-(regular|semibold)/)
      expect(classes).not.toMatch(/font-(bold|medium|light)/)
    }
  }

  // Check spacing
  const spacedElements = await page.locator('[class*="p-"], [class*="m-"], [class*="gap-"]').all()
  for (const element of spacedElements) {
    const classes = await element.getAttribute('class') || ''
    // Extract spacing values
    const spacingMatch = classes.match(/(p|m|gap)-(\d+)/)
    if (spacingMatch) {
      const value = parseInt(spacingMatch[2])
      expect([1, 2, 3, 4, 6, 8, 12, 16]).toContain(value)
    }
  }

  // Check touch targets
  const buttons = await page.locator('button, a').all()
  for (const button of buttons) {
    const box = await button.boundingBox()
    if (box) {
      expect(box.height).toBeGreaterThanOrEqual(44) // min touch target
    }
  }
}
```

### Authentication Fixture

```typescript
// tests/browser/fixtures/auth.fixture.ts
import { test as base } from '@playwright/test'
import { createClient } from '@supabase/supabase-js'

type AuthFixture = {
  authenticatedPage: Page
  testUser: {
    email: string
    password: string
    id: string
  }
}

export const test = base.extend<AuthFixture>({
  testUser: async ({}, use) => {
    // Create test user
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    )

    const email = `test-${Date.now()}@example.com`
    const password = 'testpass123'

    const { data: { user } } = await supabase.auth.admin.createUser({
      email,
      password,
      email_confirm: true,
    })

    await use({ email, password, id: user!.id })

    // Cleanup
    await supabase.auth.admin.deleteUser(user!.id)
  },

  authenticatedPage: async ({ page, testUser }, use) => {
    // Login
    await page.goto('/login')
    await page.fill('input[type="email"]', testUser.email)
    await page.fill('input[type="password"]', testUser.password)
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard')

    await use(page)
  },
})
```

## 🤖 MCP Browser Control

### Available Commands in Tests

```typescript
// When using Playwright MCP in Claude Code
test('interactive browser test', async ({ page }) => {
  // Navigate
  await page.goto('/features/posts')
  
  // Take screenshot for analysis
  await page.screenshot({ path: 'posts-page.png' })
  
  // Get page structure
  const snapshot = await page.accessibility.snapshot()
  console.log('Page structure:', snapshot)
  
  // Interactive debugging
  await page.pause() // Opens Playwright Inspector
})
```

### Claude Code Browser Commands

```bash
# Browser navigation
/browser-navigate https://localhost:3000
/browser-back
/browser-forward

# Interaction
/browser-click "Login button"
/browser-type "email field" "test@example.com"
/browser-select "role dropdown" "admin"

# Analysis
/browser-snapshot          # Get page structure
/browser-screenshot        # Capture screenshot
/browser-get-text         # Extract text content

# Debugging
/browser-console          # Get console logs
/browser-wait 2           # Wait 2 seconds
```

## 🧪 Test Scenarios

### PRD-Based Test Generation

```typescript
// tests/browser/features/user-profile.spec.ts
// Generated from PRD: User Profile Feature

import { test, expect } from '@playwright/test'
import { validateDesignSystem } from '../helpers/design-validation'

test.describe('User Profile - PRD Requirements', () => {
  // Requirement 1: Users can view their profile
  test('should display user profile information', async ({ page }) => {
    // Given: User is logged in
    await page.goto('/profile')
    
    // Then: Profile information is visible
    await expect(page.locator('h1')).toContainText('My Profile')
    await expect(page.locator('[data-testid="user-email"]')).toBeVisible()
    await expect(page.locator('[data-testid="user-name"]')).toBeVisible()
    
    // And: Design system is followed
    await validateDesignSystem(page)
  })

  // Requirement 2: Users can edit their profile
  test('should allow profile editing', async ({ page }) => {
    await page.goto('/profile')
    
    // When: User clicks edit
    await page.click('button:has-text("Edit Profile")')
    
    // Then: Edit form appears
    await expect(page.locator('form[data-testid="profile-form"]')).toBeVisible()
    
    // When: User updates name
    await page.fill('input[name="name"]', 'New Name')
    await page.click('button:has-text("Save")')
    
    // Then: Changes are saved
    await expect(page.locator('[data-testid="user-name"]')).toContainText('New Name')
    await expect(page.locator('.bg-green-50')).toContainText('Profile updated')
  })

  // Edge Case: Network failure
  test('should handle network errors gracefully', async ({ page }) => {
    // Simulate offline
    await page.context().setOffline(true)
    
    await page.goto('/profile')
    await page.click('button:has-text("Edit Profile")')
    await page.fill('input[name="name"]', 'New Name')
    await page.click('button:has-text("Save")')
    
    // Should show error
    await expect(page.locator('.bg-red-50')).toContainText('Connection failed')
    
    // Restore connection
    await page.context().setOffline(false)
  })
})
```

### Mobile Testing

```typescript
// tests/browser/mobile.spec.ts
import { test, expect, devices } from '@playwright/test'

test.use(devices['iPhone 13'])

test.describe('Mobile Experience', () => {
  test('should have proper touch targets', async ({ page }) => {
    await page.goto('/')
    
    // Get all buttons
    const buttons = await page.locator('button').all()
    
    for (const button of buttons) {
      const box = await button.boundingBox()
      expect(box?.height).toBeGreaterThanOrEqual(44)
    }
  })

  test('should have readable text', async ({ page }) => {
    await page.goto('/')
    
    // Check body text size
    const bodyText = await page.locator('p').first()
    const fontSize = await bodyText.evaluate(el => 
      window.getComputedStyle(el).fontSize
    )
    expect(parseInt(fontSize)).toBeGreaterThanOrEqual(16)
  })

  test('should handle mobile navigation', async ({ page }) => {
    await page.goto('/')
    
    // Mobile menu should be visible
    await expect(page.locator('[data-testid="mobile-menu-button"]')).toBeVisible()
    
    // Desktop menu should be hidden
    await expect(page.locator('[data-testid="desktop-menu"]')).toBeHidden()
  })
})
```

## 🔍 Debugging & Troubleshooting

### Debug Mode

```typescript
// Run with debug mode
test('debug test', async ({ page }) => {
  // Slow down actions
  await page.setDefaultTimeout(60000)
  
  // Open inspector
  await page.pause()
  
  // Take screenshots at each step
  await page.screenshot({ path: 'step1.png' })
  await page.click('button')
  await page.screenshot({ path: 'step2.png' })
})
```

### Console Monitoring

```typescript
test('monitor console', async ({ page }) => {
  // Capture console messages
  const messages: string[] = []
  page.on('console', msg => messages.push(msg.text()))
  
  // Capture errors
  const errors: Error[] = []
  page.on('pageerror', error => errors.push(error))
  
  await page.goto('/dashboard')
  
  // Assert no errors
  expect(errors).toHaveLength(0)
  
  // Check for warnings
  const warnings = messages.filter(m => m.includes('Warning'))
  expect(warnings).toHaveLength(0)
})
```

### Network Monitoring

```typescript
test('monitor network', async ({ page }) => {
  // Track API calls
  const apiCalls: string[] = []
  
  page.on('request', request => {
    if (request.url().includes('/api/')) {
      apiCalls.push(`${request.method()} ${request.url()}`)
    }
  })
  
  page.on('response', response => {
    if (response.url().includes('/api/') && !response.ok()) {
      console.error(`API Error: ${response.status()} ${response.url()}`)
    }
  })
  
  await page.goto('/dashboard')
  
  // Verify expected API calls
  expect(apiCalls).toContain('GET http://localhost:3000/api/user')
})
```

## 📊 Performance Testing

```typescript
// tests/browser/performance.spec.ts
test('should load quickly', async ({ page }) => {
  const metrics = await page.evaluate(() => {
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
    return {
      domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
      loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
    }
  })
  
  expect(metrics.domContentLoaded).toBeLessThan(3000) // 3 seconds
  expect(metrics.loadComplete).toBeLessThan(5000) // 5 seconds
})
```

## 🎓 Best Practices

1. **Use data-testid attributes**
   ```tsx
   <button data-testid="submit-button">Submit</button>
   ```

2. **Create reusable test helpers**
   ```typescript
   export async function loginAsUser(page: Page, email: string, password: string) {
     await page.goto('/login')
     await page.fill('input[type="email"]', email)
     await page.fill('input[type="password"]', password)
     await page.click('button[type="submit"]')
     await page.waitForURL('/dashboard')
   }
   ```

3. **Test user flows, not implementation**
   ```typescript
   // Good: Tests user behavior
   test('user can complete purchase', async ({ page }) => {
     await addItemToCart(page, 'Product 1')
     await proceedToCheckout(page)
     await fillPaymentDetails(page)
     await confirmPurchase(page)
     await expect(page.locator('.order-success')).toBeVisible()
   })
   ```

4. **Always validate design system**
   ```typescript
   afterEach(async ({ page }) => {
     await validateDesignSystem(page)
   })
   ```

## 🚀 CI/CD Integration

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
      - name: Run Playwright tests
        run: npx playwright test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## 🎯 Remember

- Always test with the design system in mind
- Use the `/btf` command for quick browser testing
- Validate both desktop and mobile experiences
- Test edge cases and error states
- Keep tests focused on user behavior
- Use Page Object pattern for complex pages
