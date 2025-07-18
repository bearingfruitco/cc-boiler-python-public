Create an async event handler for: $ARGUMENTS

Parse arguments:
- Event name or pattern (e.g., 'lead.form.submit' or 'lead.*')
- Handler name (--name=handleLeadSubmit)
- Priority (--priority=normal)
- Timeout (--timeout=5000)
- Retry count (--retry=3)

Steps:

1. Validate event name format:
   - Should follow namespace.category.action pattern
   - Examples: lead.form.submit, analytics.page.view, webhook.send

2. Generate event handler with proper error handling:

```typescript
import { eventQueue } from '@/lib/events';
import { z } from 'zod';

// Define event schema
const $HANDLER_NAME$Schema = z.object({
  // [Generated based on event type]
});

type $HANDLER_NAME$Event = z.infer<typeof $HANDLER_NAME$Schema>;

/**
 * Handler for $EVENT_NAME events
 * Priority: $PRIORITY
 * Timeout: $TIMEOUT$ms
 * Retries: $RETRY
 */
export async function $HANDLER_NAME$(event: $HANDLER_NAME$Event): Promise<void> {
  const startTime = Date.now();
  let lastError: Error | null = null;
  
  // Retry loop
  for (let attempt = 1; attempt <= $RETRY; attempt++) {
    try {
      // Validate event data
      const validatedEvent = $HANDLER_NAME$Schema.parse(event);
      
      // Main handler logic
      await processEvent(validatedEvent);
      
      // Success metrics
      eventQueue.emit('handler.success', {
        handler: '$HANDLER_NAME$',
        duration: Date.now() - startTime,
        attempt,
      });
      
      return;
    } catch (error) {
      lastError = error instanceof Error ? error : new Error('Unknown error');
      
      // Log attempt failure
      console.error(`[$HANDLER_NAME$] Attempt ${attempt}/${$RETRY} failed:`, error);
      
      if (attempt < $RETRY) {
        // Exponential backoff
        const delay = Math.pow(2, attempt) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  // All retries failed
  eventQueue.emit('handler.error', {
    handler: '$HANDLER_NAME$',
    error: lastError?.message,
    attempts: $RETRY,
  });
  
  throw lastError;
}

async function processEvent(event: $HANDLER_NAME$Event): Promise<void> {
  // TODO: Implement event processing logic
  
  // Example: Send to webhook
  if (event.webhookUrl) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), $TIMEOUT);
    
    try {
      const response = await fetch(event.webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Event-Type': '$EVENT_NAME$',
        },
        body: JSON.stringify(event),
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } finally {
      clearTimeout(timeoutId);
    }
  }
}

// Register the handler
eventQueue.on('$EVENT_NAME$', $HANDLER_NAME$);

// Support wildcard patterns
if ('$EVENT_NAME$'.includes('*')) {
  console.log(`Registered wildcard handler for pattern: $EVENT_NAME$`);
}
```

3. Generate tests for the handler:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { eventQueue } from '@/lib/events';
import { $HANDLER_NAME$ } from './$HANDLER_NAME$';

describe('$HANDLER_NAME$', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });
  
  it('should process valid events', async () => {
    const event = {
      // Valid event data
    };
    
    await expect($HANDLER_NAME$(event)).resolves.not.toThrow();
  });
  
  it('should retry on failure', async () => {
    const event = {
      webhookUrl: 'https://example.com/fail',
    };
    
    // Mock fetch to fail twice then succeed
    let attempts = 0;
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      attempts++;
      if (attempts < 3) {
        return Promise.reject(new Error('Network error'));
      }
      return Promise.resolve(new Response('OK'));
    });
    
    await $HANDLER_NAME$(event);
    expect(attempts).toBe(3);
  });
  
  it('should timeout long-running operations', async () => {
    const event = {
      webhookUrl: 'https://example.com/slow',
    };
    
    // Mock fetch to never resolve
    vi.spyOn(global, 'fetch').mockImplementation(() => 
      new Promise(() => {}) // Never resolves
    );
    
    await expect($HANDLER_NAME$(event)).rejects.toThrow();
  });
});
```

4. Generate usage documentation:

```markdown
## $HANDLER_NAME$ Event Handler

Handles events matching: `$EVENT_NAME$`

### Configuration
- **Priority**: $PRIORITY
- **Timeout**: $TIMEOUT$ms
- **Retries**: $RETRY attempts with exponential backoff

### Usage

```typescript
import { eventQueue } from '@/lib/events';

// Fire event
eventQueue.emit('$EVENT_NAME$', {
  // Event data
});

// Fire with options
eventQueue.emit('$EVENT_NAME$', data, {
  priority: 'high',
  timeout: 10000,
});
```

### Error Handling
- Validates event data with Zod schema
- Retries failed operations with backoff
- Emits metrics for monitoring
- Logs detailed error information
```

5. Save files:
   - lib/events/handlers/$HANDLER_NAME$.ts
   - lib/events/handlers/$HANDLER_NAME$.test.ts
   - docs/events/$HANDLER_NAME$.md

6. Update event registry if needed

Important reminders:
- Always validate event data with Zod
- Implement proper timeout handling
- Use exponential backoff for retries
- Emit metrics for monitoring
- Log errors with context
- Handle partial failures gracefully
