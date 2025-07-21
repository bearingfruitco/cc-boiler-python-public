# Event System & Analytics Alignment

## Overview

The async event system is designed to work seamlessly with your existing analytics infrastructure, particularly Rudderstack. All events flow through a unified pipeline that ensures consistency and proper tracking.

## Architecture

```
User Action → Event Queue → Analytics Bridge → Rudderstack → Destinations
                         ↓                               ↓
                    Internal Handlers              Google Analytics
                    (Webhooks, etc)                Facebook Pixel
                                                   TikTok Pixel
                                                   Data Warehouse
```

## Key Integration Points

### 1. Event Queue → Rudderstack Bridge

The analytics bridge (`lib/analytics/analytics-bridge.ts`) automatically:
- Listens to all `lead.*` events
- Maps internal event names to Rudderstack-friendly names
- Includes all tracking parameters (UTMs, click IDs)
- Maintains session consistency

### 2. Existing Infrastructure Preserved

Your current setup remains unchanged:
- `rudderstack.ts` - Core Rudderstack functions
- `secure-form-handler.ts` - Server-side processing
- Field registry system - PII protection
- All tracking parameters captured server-side

### 3. What's New

The event queue adds:
- **Non-blocking operations** - Tracking never delays form submission
- **Automatic retry logic** - Failed events retry with backoff
- **Parallel processing** - Multiple operations run simultaneously
- **Unified event stream** - All events flow through one pipeline

## Event Flow Example

```typescript
// 1. User submits form
const onSubmit = async (data) => {
  // Critical path - waits for completion
  const result = await api.submitForm(data);
  
  // 2. Fire event (non-blocking)
  eventQueue.emit(LEAD_EVENTS.SUBMISSION_SUCCESS, {
    formId: 'contact-form',
    leadId: result.leadId,
    data: sanitizedData
  });
};

// 3. Analytics bridge catches event
eventQueue.on('lead.submission.success', (event) => {
  // 4. Send to Rudderstack
  rudderanalytics.track('Lead Captured', {
    formId: event.formId,
    leadId: event.leadId,
    ...event.data
  });
});

// 5. Rudderstack handles destinations
// - Sends to Google Analytics
// - Fires Facebook Conversion API
// - Logs to data warehouse
// - Triggers webhooks
```

## Benefits of This Approach

### 1. No Breaking Changes
- Existing Rudderstack setup unchanged
- Current tracking continues working
- Gradual migration possible

### 2. Enhanced Capabilities
- Events can be processed locally before sending
- Retry logic for failed tracking
- Performance metrics on all events
- Debugging via event stream

### 3. Future Flexibility
- Easy to add new event types
- Can process events locally if needed
- A/B testing on event handling
- Real-time event monitoring

## Configuration

### Initialize in App
```typescript
// app/providers.tsx
import { initializeApp } from '@/lib/analytics';

useEffect(() => {
  initializeApp(); // Sets up Rudderstack + event bridge
}, []);
```

### Environment Variables
```env
# Existing Rudderstack config
NEXT_PUBLIC_RUDDERSTACK_KEY=your-key
NEXT_PUBLIC_RUDDERSTACK_DATA_PLANE_URL=your-url

# Optional webhook for leads
NEXT_PUBLIC_LEAD_WEBHOOK_URL=https://your-webhook.com
```

## Event Naming Convention

Internal events use dot notation:
- `lead.form.submit`
- `lead.field.change`
- `analytics.page.view`

These are automatically mapped to Rudderstack conventions:
- `Form Submitted`
- `Form Field Changed`
- `Page Viewed`

## Monitoring & Debugging

### Development Mode
```typescript
// See all events in console
eventQueue.on('*', (event) => {
  console.log('[Event]', event.type, event);
});
```

### Production Monitoring
All events are tracked in Rudderstack, allowing you to:
- Monitor event volume
- Track success/failure rates
- Debug with event inspector
- Set up alerts for anomalies

## Migration Path

### Phase 1: New Forms (Current)
- New forms use `useLeadFormEvents` hook
- Events flow through queue → Rudderstack
- Existing forms continue working

### Phase 2: Update Existing Forms
- Gradually update to use event hooks
- Remove direct `trackEvent` calls
- All tracking becomes non-blocking

### Phase 3: Advanced Features
- Add custom event processors
- Implement event replay
- Build real-time dashboards

## Best Practices

1. **Always use event queue for non-critical operations**
   ```typescript
   // Good
   eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
   
   // Avoid
   await trackEvent('Form Submitted', data);
   ```

2. **Include session ID for journey tracking**
   ```typescript
   const { sessionId } = useLeadFormEvents('form-name');
   ```

3. **Let Rudderstack handle pixel firing**
   - Configure pixels in Rudderstack dashboard
   - Don't fire pixels directly from code
   - Use server-side tracking when possible

4. **Monitor event performance**
   ```typescript
   eventQueue.on(LEAD_EVENTS.PIXEL_FIRE, (event) => {
     if (!event.success) {
       console.error('Pixel failed:', event.error);
     }
   });
   ```

## Summary

The async event system enhances your existing Rudderstack setup without replacing it. All events flow through Rudderstack, maintaining your current tracking while adding:

- Non-blocking performance
- Automatic retries
- Parallel processing
- Better error handling
- Unified event stream

This ensures backward compatibility while providing a foundation for more advanced event-driven features in the future.
