# Async Troubleshooting Guide

## Common Issues & Quick Fixes

### 1. Form Submission Feels Slow

**Symptom**: User has to wait for tracking/analytics before seeing success

**Check**: Look for awaited analytics calls
```typescript
// ❌ Problem
await rudderanalytics.track('Form Submitted', data);
await fbq('track', 'Lead');
```

**Fix**: Use event queue
```typescript
// ✅ Solution
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
// All tracking happens async!
```

**Command**: `/validate-async` will find these automatically

### 2. Events Not Firing

**Symptom**: Analytics events missing in Rudderstack/GA

**Check**: Ensure handlers are registered
```typescript
// In app initialization
import '@/lib/events/handlers'; // Must import to register!
```

**Debug**: Check event queue status
```javascript
// Browser console
window.__eventQueue?.getStats()
```

### 3. Form Doesn't Show Loading State

**Symptom**: No feedback during submission

**Check**: Missing loading state
```typescript
// ❌ Problem
const handleSubmit = async (data) => {
  await api.submit(data);
};

// ✅ Solution  
const [isSubmitting, setIsSubmitting] = useState(false);
const handleSubmit = async (data) => {
  setIsSubmitting(true);
  try {
    await api.submit(data);
  } finally {
    setIsSubmitting(false);
  }
};
```

**Command**: `/validate-async` warns about missing states

### 4. Sequential Operations Slow

**Symptom**: Dashboard takes long to load

**Check**: Look for sequential awaits
```typescript
// ❌ Problem (3 seconds total)
const user = await fetchUser();        // 1s
const prefs = await fetchPreferences(); // 1s  
const perms = await fetchPermissions(); // 1s

// ✅ Solution (1 second total)
const [user, prefs, perms] = await Promise.all([
  fetchUser(),
  fetchPreferences(),
  fetchPermissions()
]);
```

**Command**: `/validate-async` suggests parallel operations

### 5. API Call Timeouts

**Symptom**: Form hangs forever on slow network

**Check**: Missing timeout protection
```typescript
// ❌ Problem - No timeout
const response = await fetch('/api/submit', {
  method: 'POST',
  body: JSON.stringify(data)
});

// ✅ Solution - 5s timeout
const response = await fetch('/api/submit', {
  method: 'POST',
  body: JSON.stringify(data),
  signal: AbortSignal.timeout(5000)
});
```

### 6. Event Handler Crashes App

**Symptom**: One failed webhook breaks everything

**Check**: Unhandled errors in handlers
```typescript
// ❌ Problem
eventQueue.on(LEAD_EVENTS.FORM_SUBMIT, async (data) => {
  const result = await riskyOperation(data); // Can throw!
});

// ✅ Solution
eventQueue.on(LEAD_EVENTS.FORM_SUBMIT, async (data) => {
  try {
    const result = await riskyOperation(data);
  } catch (error) {
    console.error('Handler failed:', error);
    // Don't throw - let other handlers run
  }
});
```

### 7. Memory Leaks from Event Listeners

**Symptom**: App slows down over time

**Check**: Component cleanup
```typescript
// ✅ Clean up on unmount
useEffect(() => {
  const handler = (data) => console.log(data);
  eventQueue.on(LEAD_EVENTS.FORM_VIEW, handler);
  
  return () => {
    eventQueue.off(LEAD_EVENTS.FORM_VIEW, handler);
  };
}, []);
```

### 8. Wrong Event Names

**Symptom**: Events fire but Rudderstack shows nothing

**Check**: Event name mapping
```typescript
// Event queue name → Rudderstack name
lead.form.submit → Form Submitted
lead.form.view → Form Viewed
lead.captured → Lead Captured
```

**Use constants**: Always use `LEAD_EVENTS.FORM_SUBMIT`, not strings

## Quick Debug Commands

```bash
# Check for async issues
/validate-async

# Test a form's event flow
/test-async-flow contact-form

# Review async requirements
cat docs/project/features/contact-form-async.md

# Check if handlers are loaded
grep -r "import.*handlers" app/
```

## Browser Console Helpers

```javascript
// See all registered events
window.__eventQueue?.eventNames()

// Check if specific handler exists
window.__eventQueue?.listenerCount('lead.form.submit')

// Enable debug logging
localStorage.setItem('EVENT_QUEUE_DEBUG', 'true')

// See queued events
window.__eventQueue?._queue
```

## Performance Tips

1. **Batch Events**: Group related events
   ```typescript
   eventQueue.emit(LEAD_EVENTS.FORM_COMPLETE, {
     form: data,
     timing: performance.now() - startTime,
     session: getSessionData()
   });
   ```

2. **Debounce Field Changes**: Don't spam events
   ```typescript
   const debouncedTrack = useMemo(
     () => debounce((field, value) => {
       eventQueue.emit(LEAD_EVENTS.FIELD_CHANGE, { field, value });
     }, 500),
     []
   );
   ```

3. **Use Priorities**: Critical events first
   ```typescript
   eventQueue.emit(ANALYTICS_EVENTS.ERROR, error, {
     priority: 'high'
   });
   ```

## When to Ask for Help

If you see:
- Events consistently failing after retries
- Memory usage growing without bound
- Forms taking >5s to submit
- Rudderstack showing no data after 24h

Run these commands and share output:
```bash
/validate-async > async-report.txt
/test-async-flow [form-name] > flow-test.txt
```

Then check with the team - there might be infrastructure issues.
