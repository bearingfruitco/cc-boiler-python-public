Validate async patterns in: $ARGUMENTS

Analyze the specified file or directory for async pattern compliance.

Steps:

1. Parse arguments:
   - File or directory path
   - Specific patterns to check (--pattern=all|loading|error|timeout)
   - Fix mode (--fix)

2. Run async pattern checks:

   a. **Loading State Coverage**
      - Find all async operations (await, fetch, api calls)
      - Verify matching loading states exist
      - Check loading UI components

   b. **Error Handling**
      - Async functions have try/catch
      - Promise chains have .catch()
      - Error boundaries for components

   c. **Timeout Protection**
      - API calls use AbortController
      - Or use apiClient with timeout
      - Reasonable timeout values

   d. **Event Queue Usage**
      - Non-critical operations use eventQueue
      - No await on tracking/analytics
      - Proper event naming

   e. **Parallel Optimization**
      - Sequential awaits that could be parallel
      - Promise.all() for independent operations
      - Proper dependency ordering

3. Generate validation report:

```
🔍 Async Pattern Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 File: $FILEPATH

✅ PASSED (X/Y checks)
━━━━━━━━━━━━━━━━━━━━
✓ Loading states: All async operations covered
✓ Error handling: Try/catch blocks present
✓ Event queue: Non-critical ops non-blocking

⚠️  WARNINGS (X issues)
━━━━━━━━━━━━━━━━━━━━
⚠️  Line 45: Sequential awaits could be parallel
   await fetchUser();
   await fetchPreferences();
   
   Fix: const [user, prefs] = await Promise.all([
     fetchUser(),
     fetchPreferences()
   ]);

⚠️  Line 78: Missing timeout on fetch
   const response = await fetch(url);
   
   Fix: Use apiClient or AbortController

❌ ERRORS (X issues)
━━━━━━━━━━━━━━━━━━━━
❌ Line 23: No error handling for async function
   async function submitForm(data) {
     const result = await api.post('/submit', data);
   }
   
   Fix: Add try/catch block

❌ Line 67: Blocking form submission with tracking
   onSubmit={async (data) => {
     await sendToGoogle(data);
     await sendToFacebook(data);
   }}
   
   Fix: Use eventQueue.emit() instead

📊 Summary
━━━━━━━━━━━━━━━━━━━━
Total Checks: Y
Passed: X
Warnings: X
Errors: X
Score: X/100

📝 Recommendations
━━━━━━━━━━━━━━━━━━━━
1. Add useLeadFormEvents hook for tracking
2. Implement global error boundary
3. Set up performance monitoring
4. Use React.Suspense for code splitting
```

4. If --fix mode is enabled:
   - Apply automatic fixes where safe
   - Add missing loading states
   - Wrap in try/catch blocks
   - Convert to eventQueue usage
   - Show diff of changes

5. Integration checks:
   - Verify eventQueue is imported
   - Check for event handler registration
   - Validate event naming conventions

6. Generate fix script if issues found:

```typescript
// async-fixes.ts
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

// Fix 1: Replace blocking tracking
// Before: await trackAnalytics(data);
// After:
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);

// Fix 2: Add loading states
const [isLoading, setIsLoading] = useState(false);

// Fix 3: Add error boundaries
<ErrorBoundary fallback={<ErrorState />}>
  <AsyncComponent />
</ErrorBoundary>
```

Output files:
- .claude/validation/async-report-$TIMESTAMP.md
- .claude/validation/async-fixes-$TIMESTAMP.ts (if fixes needed)

Exit codes:
- 0: All checks passed
- 1: Warnings only
- 2: Errors found
