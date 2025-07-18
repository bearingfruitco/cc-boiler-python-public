# Getting Started with Async Event System (v2.3.6)

## Quick Start for Lead Generation Forms

### 1. Create a Tracked Form

```bash
/create-tracked-form LeadCaptureForm --vertical=debt --compliance=tcpa
```

This generates a complete form with:
- ✅ Automatic event tracking (non-blocking)
- ✅ Loading states for submission
- ✅ Timeout protection (5s default)
- ✅ Error handling with retry
- ✅ Rudderstack integration built-in

### 2. Understanding What Gets Generated

The command creates:

**Form Module** (`src/forms/LeadCaptureForm.pyx`):
```typescript
export function LeadCaptureForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { trackFormSubmit, trackSubmissionResult } = useLeadFormEvents('lead-capture');
  
  const onSubmit = async (data) => {
    setIsSubmitting(true);
    
    try {
      // Track start (returns timestamp for duration tracking)
      const startTime = await trackFormSubmit(data);
      
      // Critical path - user waits for this
      const result = await api.submitLead(data);
      
      // Fire all tracking events (non-blocking)
      eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
        formId: 'lead-capture',
        leadId: result.id,
        ...data
      });
      
      // Track success (calculates duration automatically)
      trackSubmissionResult(true, startTime);
      
    } catch (error) {
      // Track failure
      trackSubmissionResult(false, Date.now(), { error });
    } finally {
      setIsSubmitting(false);
    }
  };
}
```

**What's Different from Traditional Forms?**

Traditional approach (blocks user):
```typescript
// ❌ User waits for ALL of these
await api.submitForm(data);
await analytics.track('Form Submit');
await fbPixel.track('Lead');
await sendWebhook(data);
await logToDatadog(data);
// Finally show success... 5+ seconds later!
```

New async approach (instant feedback):
```typescript
// ✅ User only waits for this
await api.submitForm(data);

// Everything else happens in background
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
// Show success immediately!
```

### 3. How Events Flow to Rudderstack

The event system automatically bridges to your existing Rudderstack setup:

```
Your Code:
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, { formId: 'contact', email: 'user@example.com' })
                           ↓
Event Queue:
Processes handlers asynchronously with retry logic
                           ↓
Rudderstack Bridge:
rudderanalytics.track('Form Submitted', { form_id: 'contact', email: 'user@example.com' })
                           ↓
Your Destinations:
Google Analytics, Facebook Pixel, Webhooks, etc.
```

### 4. Adding Custom Event Handlers

Need to add a new tracking pixel or webhook?

```bash
/create-event-handler new-pixel
```

This generates (`lib/events/handlers/new-pixel.py`):
```typescript
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

eventQueue.on(LEAD_EVENTS.FORM_SUBMIT, async (data) => {
  try {
    // Your pixel/webhook logic here
    await fetch('https://pixel.example.com/track', {
      method: 'POST',
      body: JSON.stringify(data),
      signal: AbortSignal.timeout(3000), // 3s timeout
    });
  } catch (error) {
    // Log but don't throw - other handlers continue
    console.error('Pixel failed:', error);
  }
});
```

### 5. Testing Your Async Flow

```bash
/test-async-flow lead-capture-form
```

This will:
1. Submit a test form
2. Verify the API call completes
3. Check all events were emitted
4. Confirm handlers executed
5. Measure total time
6. Report any blocking operations

### 6. Common Patterns

#### Pattern 1: Field Change Tracking (Debounced)
```typescript
const debouncedTrack = useMemo(
  () => debounce((field: string, value: string) => {
    eventQueue.emit(LEAD_EVENTS.FIELD_CHANGE, { 
      formId: 'contact',
      field, 
      value: value.length // Don't send actual value!
    });
  }, 500),
  []
);

<input onChange={(e) => debouncedTrack('email', e.target.value)} />
```

#### Pattern 2: Multi-Step Form Tracking
```typescript
const trackStepComplete = (step: number) => {
  eventQueue.emit(LEAD_EVENTS.FORM_STEP_COMPLETE, {
    formId: 'multi-step',
    step,
    totalSteps: 3,
    timeOnStep: Date.now() - stepStartTime
  });
};
```

#### Pattern 3: Abandonment Tracking
```typescript
useEffect(() => {
  const handleBeforeUnload = () => {
    if (formData.email && !isSubmitted) {
      // Fire and forget - don't block navigation
      eventQueue.emit(LEAD_EVENTS.FORM_ABANDONED, {
        formId: 'contact',
        completedFields: Object.keys(formData).length
      });
    }
  };
  
  window.addEventListener('beforeunload', handleBeforeUnload);
  return () => window.removeEventListener('beforeunload', handleBeforeUnload);
}, [formData, isSubmitted]);
```

### 7. Monitoring & Debugging

In browser console:
```javascript
// See all registered events
window.__eventQueue?.eventNames()
// Output: ['lead.form.submit', 'lead.form.view', ...]

// Check handler count
window.__eventQueue?.listenerCount('lead.form.submit')
// Output: 3 (rudderstack, pixel, webhook)

// Enable debug logging
localStorage.setItem('EVENT_QUEUE_DEBUG', 'true')
// Now see all events in console

// Check queue status
window.__eventQueue?.getStats()
// Output: { processed: 42, queued: 0, failed: 1 }
```

### 8. Best Practices Summary

**DO:**
- ✅ Use event queue for all non-critical operations
- ✅ Show loading states during submission
- ✅ Add timeout protection to all external calls
- ✅ Handle errors gracefully (don't crash other handlers)
- ✅ Use constants for event names
- ✅ Clean up listeners on unmount

**DON'T:**
- ❌ Await analytics/tracking calls
- ❌ Block form submission for pixels
- ❌ Use sequential awaits for parallel operations
- ❌ Forget error boundaries in handlers
- ❌ Log sensitive data in events

### 9. Quick Reference

| Command | Purpose |
|---------|---------|
| `/create-tracked-form` | Generate form with tracking |
| `/create-event-handler` | Add new event handler |
| `/prd-async` | Document async requirements |
| `/validate-async` | Check for anti-patterns |
| `/test-async-flow` | Test complete event chain |

### 10. Next Steps

1. Create your first tracked form with `/create-tracked-form`
2. Add async requirements to PRDs with `/prd-async`
3. Validate existing code with `/validate-async`
4. Monitor events in browser console
5. Check Rudderstack for tracking data

The async event system ensures your forms are fast, reliable, and never block the user experience. Happy coding! ⚡
