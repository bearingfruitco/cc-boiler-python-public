# Troubleshooting Guide

## Overview

This guide helps diagnose and resolve common issues in Next.js applications. Start with the Quick Diagnostics, then move to specific problem areas.

## Quick Diagnostics

### Health Check Script

```bash
#!/bin/bash
# scripts/health-check.sh

echo "🔍 Application Health Check"
echo "=========================="

# Check Node version
echo "✓ Node version: $(node --version)"
if [[ $(node --version) != v22* ]]; then
  echo "  ⚠️  Warning: Node 22+ required"
fi

# Check package manager
echo "✓ Package manager: $(pnpm --version)"

# Check dependencies
echo "✓ Checking dependencies..."
pnpm check

# Check TypeScript
echo "✓ TypeScript check..."
pnpm typecheck

# Check environment variables
echo "✓ Environment variables..."
node scripts/check-env.js

# Check database connection
echo "✓ Database connection..."
node scripts/check-db.js

# Check external services
echo "✓ External services..."
node scripts/check-services.js

echo "=========================="
echo "✅ Health check complete"
```

### Environment Variable Checker

```typescript
// scripts/check-env.js
const required = [
  'DATABASE_URL',
  'NEXT_PUBLIC_API_URL',
  // Add your required env vars
];

const missing = required.filter(key => !process.env[key]);

if (missing.length > 0) {
  console.error('❌ Missing environment variables:');
  missing.forEach(key => console.error(`  - ${key}`));
  process.exit(1);
} else {
  console.log('✅ All required environment variables present');
}
```

## Common Issues & Solutions

### 1. Build Failures

#### TypeScript Errors

**Problem**: `Type error: Property 'X' does not exist on type 'Y'`

**Solution**:
```bash
# Clear TypeScript cache
rm -rf .next
pnpm typecheck

# Regenerate types if using generated types
pnpm generate:types
```

#### Module Resolution Errors

**Problem**: `Module not found: Can't resolve '@/components/...'`

**Solution**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

#### Next.js Build Errors

**Problem**: `Error: Dynamic server usage: headers`

**Solution**:
```typescript
// Mark dynamic routes explicitly
export const dynamic = 'force-dynamic';
// Or use static where possible
export const dynamic = 'force-static';
```

### 2. Runtime Errors

#### Hydration Mismatch

**Problem**: `Error: Hydration failed because the initial UI does not match`

**Common Causes & Solutions**:

```typescript
// ❌ Bad - Date/time differences
<p>Generated at: {new Date().toISOString()}</p>

// ✅ Good - Use consistent values
<p>Generated at: {generatedAt}</p>

// ❌ Bad - Browser-only APIs
<p>Screen width: {window.innerWidth}</p>

// ✅ Good - Use effects
const [width, setWidth] = useState(0);
useEffect(() => {
  setWidth(window.innerWidth);
}, []);
```

#### Client Component Errors

**Problem**: `Error: useRouter only works in Client Components`

**Solution**:
```typescript
// Add 'use client' directive
'use client';

import { useRouter } from 'next/navigation';

export function MyComponent() {
  const router = useRouter();
  // ...
}
```

### 3. Database Issues

#### Connection Errors

**Problem**: `Error: Connection terminated unexpectedly`

**Diagnostics**:
```typescript
// scripts/check-db.js
async function checkDatabase() {
  try {
    // Test your database connection
    const result = await db.query('SELECT 1');
    console.log('✅ Database connection successful');
  } catch (error) {
    console.error('❌ Database connection failed:', error.message);
  }
}

checkDatabase();
```

#### Query Performance

**Problem**: Slow queries

**Solution**:
```sql
-- Check query plan
EXPLAIN ANALYZE 
SELECT * FROM users 
WHERE created_at > NOW() - INTERVAL '7 days';

-- Add missing indexes
CREATE INDEX idx_users_created_at ON users(created_at DESC);
```

### 4. Authentication Issues

#### Invalid API Keys

**Problem**: `Error: Invalid API key`

**Debugging Steps**:
```typescript
// Check API key format
console.log('API Key length:', process.env.API_KEY?.length);
console.log('Starts with:', process.env.API_KEY?.substring(0, 10));

// Verify against service dashboard
```

#### CORS Errors

**Problem**: `Access to fetch at '...' from origin '...' has been blocked by CORS`

**Solution**:
```typescript
// app/api/route.ts
export async function OPTIONS() {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
```

### 5. Performance Issues

#### Slow Page Load

**Diagnostics**:
```typescript
// Add performance logging
export default function Page() {
  useEffect(() => {
    // Log performance metrics
    const perfData = {
      fcp: performance.timing.responseEnd - performance.timing.fetchStart,
      domLoad: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
      windowLoad: performance.timing.loadEventEnd - performance.timing.navigationStart,
    };
    
    console.log('Performance:', perfData);
    
    // Check for specific issues
    if (perfData.windowLoad > 3000) {
      console.warn('Page load exceeds 3s target');
    }
  }, []);
}
```

#### Memory Leaks

**Detection**:
```typescript
// Chrome DevTools > Memory > Heap Snapshot
// Take snapshot → Perform action → Take snapshot → Compare

// Common leak patterns to check:
// 1. Event listeners not removed
useEffect(() => {
  const handler = () => {};
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler); // Cleanup!
}, []);

// 2. Timers not cleared
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  return () => clearInterval(timer); // Cleanup!
}, []);

// 3. Subscriptions not unsubscribed
useEffect(() => {
  const sub = observable.subscribe();
  return () => sub.unsubscribe(); // Cleanup!
}, []);
```

### 6. Analytics Issues

#### Events Not Firing

**Debugging**:
```typescript
// Enable debug mode
localStorage.setItem('analytics_debug', 'true');
window.location.reload();

// Check in console
window.analytics.track('Test Event', { test: true });

// Verify in Network tab
// Look for requests to your analytics URL
```

#### Attribution Loss

**Problem**: UTM parameters not captured

**Solution**:
```typescript
// Debug attribution capture
const debugAttribution = () => {
  console.log('URL params:', Object.fromEntries(new URLSearchParams(window.location.search)));
  console.log('Session storage:', sessionStorage.getItem('tracking_params'));
  console.log('Cookies:', document.cookie);
};

// Ensure params are captured on mount
useEffect(() => {
  const params = Object.fromEntries(new URLSearchParams(window.location.search));
  if (Object.keys(params).length > 0) {
    sessionStorage.setItem('tracking_params', JSON.stringify(params));
  }
}, []);
```

### 7. Design System Violations

#### Typography Issues

**Problem**: Using incorrect font sizes

**Detection Script**:
```javascript
// Run in browser console
const checkTypography = () => {
  const elements = document.querySelectorAll('*');
  const violations = [];
  
  elements.forEach(el => {
    const classes = el.className.split(' ');
    const textClass = classes.find(c => c.includes('text-') && !c.includes('text-size-'));
    
    if (textClass && !['text-left', 'text-center', 'text-right'].includes(textClass)) {
      violations.push({
        element: el,
        class: textClass,
        suggestion: 'Use text-size-1, text-size-2, text-size-3, or text-size-4'
      });
    }
  });
  
  console.table(violations);
};

checkTypography();
```

#### Spacing Violations

**Detection**:
```javascript
// Check for non-4px grid spacing
const checkSpacing = () => {
  const violations = [];
  const spacingClasses = ['p-', 'px-', 'py-', 'm-', 'mx-', 'my-', 'gap-', 'space-'];
  
  document.querySelectorAll('*').forEach(el => {
    const classes = el.className.split(' ');
    
    classes.forEach(className => {
      spacingClasses.forEach(prefix => {
        if (className.startsWith(prefix)) {
          const value = parseInt(className.replace(prefix, ''));
          const pixels = value * 4;
          
          if (pixels % 4 !== 0) {
            violations.push({
              element: el,
              class: className,
              pixels: pixels,
              suggestion: `Use ${prefix}${Math.round(pixels / 4)}`
            });
          }
        }
      });
    });
  });
  
  console.table(violations);
};

checkSpacing();
```

### 8. Deployment Issues

#### Vercel Build Errors

**Problem**: `Error: Failed to collect page data for /api/...`

**Solution**:
```typescript
// Ensure API routes export named functions
export async function GET() { /* ... */ }
export async function POST() { /* ... */ }

// Not: export default function handler() { /* ... */ }
```

#### Environment Variable Issues

**Problem**: Variables not available in production

**Checklist**:
1. Add to hosting platform dashboard
2. Prefix with `NEXT_PUBLIC_` for client-side
3. Redeploy after adding
4. Check in multiple environments

```bash
# Verify in production
curl https://your-app.vercel.app/api/health
```

### 9. Mobile-Specific Issues

#### Touch Target Size

**Testing**:
```javascript
// Check touch target sizes
const checkTouchTargets = () => {
  const interactive = document.querySelectorAll('button, a, input, select, textarea');
  const small = [];
  
  interactive.forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.height < 44 || rect.width < 44) {
      small.push({
        element: el.tagName,
        text: el.textContent?.substring(0, 20),
        height: rect.height,
        width: rect.width
      });
    }
  });
  
  if (small.length > 0) {
    console.warn('Touch targets below 44px:');
    console.table(small);
  }
};

checkTouchTargets();
```

#### Viewport Issues

**Problem**: Horizontal scroll on mobile

**Debugging**:
```css
/* Add temporarily to find culprit */
* {
  outline: 1px solid red;
}

/* Common fixes */
html, body {
  overflow-x: hidden;
  max-width: 100vw;
}

/* Check for elements exceeding viewport */
.container {
  width: 100%;
  max-width: 100%;
  padding: 0 1rem;
}
```

## Debugging Tools

### Browser Extensions

1. **React Developer Tools**
   - Component tree inspection
   - Props/state debugging
   - Performance profiling

2. **Tailwind CSS IntelliSense**
   - Class name validation
   - Autocomplete

3. **Lighthouse**
   - Performance audits
   - Accessibility checks

### CLI Tools

```bash
# Debug Next.js build
DEBUG=* pnpm build

# Analyze bundle
ANALYZE=true pnpm build

# Check for outdated packages
pnpm outdated

# Audit dependencies
pnpm audit
```

### Custom Debug Components

```typescript
// components/DebugInfo.tsx
'use client';

export function DebugInfo() {
  if (process.env.NODE_ENV === 'production') return null;
  
  return (
    <div className="fixed bottom-0 right-0 bg-black text-white p-2 text-xs">
      <div>Viewport: {window.innerWidth}x{window.innerHeight}</div>
      <div>Route: {window.location.pathname}</div>
      <div>Env: {process.env.NODE_ENV}</div>
    </div>
  );
}
```

## Error Logging & Monitoring

### Structured Logging

```typescript
// lib/logger.ts
export const logger = {
  error: (message: string, error: any, context?: any) => {
    console.error(`[ERROR] ${message}`, {
      error: error?.message || error,
      stack: error?.stack,
      context,
      timestamp: new Date().toISOString(),
      url: typeof window !== 'undefined' ? window.location.href : 'server',
    });
    
    // Send to monitoring service
    if (typeof window !== 'undefined' && window.sentry) {
      window.sentry.captureException(error, { extra: context });
    }
  },
  
  warn: (message: string, context?: any) => {
    console.warn(`[WARN] ${message}`, context);
  },
  
  info: (message: string, context?: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[INFO] ${message}`, context);
    }
  },
};
```

## Getting Help

### Before Asking for Help

1. Check error messages carefully
2. Search existing issues on GitHub
3. Try the quick diagnostics
4. Isolate the problem (minimal reproduction)
5. Collect relevant logs

### Information to Provide

```markdown
## Issue Template

**Environment:**
- OS: [e.g., macOS 14.0]
- Node: [run `node --version`]
- pnpm: [run `pnpm --version`]
- Browser: [e.g., Chrome 120]

**Description:**
[Clear description of the issue]

**Steps to Reproduce:**
1. ...
2. ...

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Messages:**
```
[Paste full error messages]
```

**Code Sample:**
```typescript
// Minimal code that reproduces the issue
```

**Additional Context:**
[Screenshots, logs, etc.]
```

Remember: Most issues have been encountered before. Check documentation, search issues, and use the debugging tools before escalating.