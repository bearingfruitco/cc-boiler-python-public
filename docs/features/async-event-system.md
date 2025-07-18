# Async Event System

## Overview

This boilerplate includes a comprehensive async event-driven architecture that ensures non-critical operations (analytics, tracking, webhooks) never block the user experience. This is especially important for lead generation forms where multiple events need to fire when form submissions occur.

## Quick Start

### 1. Basic Event Emission

```typescript
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

// Fire and forget - non-blocking
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
  formId: 'contact-form',
  sessionId: 'abc123',
  data: formData
});
```

### 2. Form Integration

```typescript
import { useLeadFormEvents } from '@/hooks/use-event-system';

export function ContactForm() {
  const { 
    trackFormSubmit, 
    trackSubmissionResult,
    sessionId 
  } = useLeadFormEvents('contact-form');

  const onSubmit = async (data) => {
    // Track submission start (critical)
    const startTime = await trackFormSubmit(data);
    
    try {
      const result = await api.submit(data);
      // Track success (non-blocking)
      trackSubmissionResult(true, startTime);
    } catch (error) {
      // Track failure (non-blocking)
      trackSubmissionResult(false, startTime);
    }
  };
}
```

### 3. Parallel Operations

```typescript
import { parallelSettle } from '@/lib/utils/async-helpers';

// Run multiple operations with timeout protection
const results = await parallelSettle({
  user: fetchUser(),
  preferences: fetchPreferences(),
  permissions: fetchPermissions()
}, {
  timeout: 5000,
  critical: ['user'] // User is required, others optional
});
```

## Architecture

```
User Action → Event Queue → Analytics Bridge → Rudderstack → Destinations
                         ↓
                    Internal Handlers
                    (Webhooks, Logging)
```

## Event Types

### Lead Events
- `lead.form.view` - Form viewed by user
- `lead.form.start` - First interaction with form
- `lead.field.change` - Field value changed
- `lead.form.submit` - Form submission attempted
- `lead.submission.success` - Successful submission
- `lead.submission.error` - Failed submission
- `lead.consent.accepted` - TCPA/GDPR consent given

### Analytics Events
- `analytics.page.view` - Page viewed
- `analytics.user.action` - User performed action
- `analytics.error.track` - Error occurred
- `analytics.conversion` - Conversion tracked

## Loading States

All async operations must show loading states:

```typescript
import { LoadingState, ErrorState } from '@/components/ui/async-states';

function MyComponent() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  if (isLoading) return <LoadingState message="Processing..." />;
  if (error) return <ErrorState error={error} retry={handleRetry} />;
  
  return <YourContent />;
}
```

## Commands

- `/create-event-handler` - Create new event handler with retry logic
- `/prd-async [feature]` - Add async requirements to PRD
- `/validate-async` - Check code for async anti-patterns

## Best Practices

### 1. Never Block on Tracking
```typescript
// ❌ Bad - blocks form submission
await trackToGoogle(data);
await trackToFacebook(data);

// ✅ Good - fire and forget
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
```

### 2. Use Parallel Operations
```typescript
// ❌ Bad - sequential
const user = await fetchUser();
const prefs = await fetchPreferences();

// ✅ Good - parallel
const [user, prefs] = await Promise.all([
  fetchUser(),
  fetchPreferences()
]);
```

### 3. Always Handle Timeouts
```typescript
import { withTimeout } from '@/lib/utils/async-helpers';

// Add timeout to any promise
const result = await withTimeout(
  fetchData(),
  5000,
  'Data fetch timed out'
);
```

### 4. Show Loading States
```typescript
// Every async operation needs user feedback
const [isLoading, setIsLoading] = useState(false);

const handleSubmit = async () => {
  setIsLoading(true);
  try {
    await operation();
  } finally {
    setIsLoading(false);
  }
};
```

## Testing

```typescript
import { waitForEvent, expectEventSequence } from '@/lib/testing/async-test-utils';

// Wait for specific event
const event = await waitForEvent(LEAD_EVENTS.FORM_SUBMIT, 5000);

// Expect sequence of events
await expectEventSequence(
  ['lead.form.start', 'lead.form.submit', 'lead.submission.success'],
  async () => {
    await userSubmitsForm();
  }
);
```

## Configuration

The system initializes automatically in `app/providers.tsx`. No additional setup required.

### Environment Variables
```env
# Rudderstack (required for analytics)
NEXT_PUBLIC_RUDDERSTACK_KEY=your-key
NEXT_PUBLIC_RUDDERSTACK_DATA_PLANE_URL=your-url

# Optional webhook endpoint
NEXT_PUBLIC_LEAD_WEBHOOK_URL=https://your-webhook.com
```

## Monitoring

In development, all events are logged to console. In production, events flow through Rudderstack where you can:
- Monitor event volume
- Track success/failure rates
- Set up alerts
- Debug with event inspector

## Migration

Existing forms continue to work. To add event tracking:

1. Import the hook: `useLeadFormEvents`
2. Replace direct tracking calls with event emissions
3. All tracking becomes non-blocking automatically

---

For more details, see [Event System Architecture](/docs/architecture/event-analytics-alignment.md)
