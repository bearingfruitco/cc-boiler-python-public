# Async Event-Driven Python Workflow

This guide covers building event-driven Python applications with async patterns.

## Overview

Modern Python applications use async patterns for:
- High-performance APIs
- Concurrent data processing
- Real-time event handling
- Background task processing

## Core Async Architecture

### 1. Event Queue System

```python
from asyncio import Queue
from typing import Dict, Any
import asyncio

class EventQueue:
    def __init__(self):
        self.queue = Queue()
        self.handlers: Dict[str, list] = {}
    
    def register_handler(self, event_type: str, handler):
        """Register an async handler for an event type."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    async def emit(self, event_type: str, data: Any):
        """Emit an event to the queue."""
        await self.queue.put((event_type, data))
    
    async def process_events(self):
        """Process events from the queue."""
        while True:
            event_type, data = await self.queue.get()
            
            if event_type in self.handlers:
                # Run all handlers concurrently
                tasks = [
                    handler(data) 
                    for handler in self.handlers[event_type]
                ]
                await asyncio.gather(*tasks, return_exceptions=True)

# Global event queue
event_queue = EventQueue()
```

### 2. FastAPI with Events

```python
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start event processor
    task = asyncio.create_task(event_queue.process_events())
    yield
    # Cleanup
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.post("/users")
async def create_user(user: UserCreate):
    # Quick database save
    new_user = await save_user(user)
    
    # Emit events for async processing
    await event_queue.emit("user_created", {
        "user_id": new_user.id,
        "email": new_user.email
    })
    
    return {"id": new_user.id, "status": "created"}
```

### 3. Event Handlers

```python
# Register handlers at startup
@event_queue.register_handler("user_created")
async def send_welcome_email(data: dict):
    """Send welcome email asynchronously."""
    user_id = data["user_id"]
    email = data["email"]
    
    try:
        await email_service.send_welcome(email)
        logger.info(f"Welcome email sent to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        # Could retry or send to dead letter queue

@event_queue.register_handler("user_created")
async def update_analytics(data: dict):
    """Update analytics asynchronously."""
    await analytics_service.track_signup(data["user_id"])

@event_queue.register_handler("user_created")
async def sync_to_crm(data: dict):
    """Sync to external CRM."""
    await crm_service.create_contact(data)
```

## Async Patterns

### 1. Fire and Forget Pattern

```python
async def fire_and_forget(coro):
    """Execute coroutine without waiting for result."""
    task = asyncio.create_task(coro)
    
    # Optional: Add error handler
    def handle_task_result(task):
        try:
            task.result()
        except Exception as e:
            logger.error(f"Background task failed: {e}")
    
    task.add_done_callback(handle_task_result)
```

### 2. Batch Processing Pattern

```python
class BatchProcessor:
    def __init__(self, process_func, batch_size=100, interval=5.0):
        self.process_func = process_func
        self.batch_size = batch_size
        self.interval = interval
        self.items = []
        self.lock = asyncio.Lock()
    
    async def add(self, item):
        async with self.lock:
            self.items.append(item)
            if len(self.items) >= self.batch_size:
                await self._process_batch()
    
    async def _process_batch(self):
        async with self.lock:
            if not self.items:
                return
            
            batch = self.items[:self.batch_size]
            self.items = self.items[self.batch_size:]
            
            # Process batch
            await self.process_func(batch)
    
    async def run_periodic(self):
        """Process batches periodically."""
        while True:
            await asyncio.sleep(self.interval)
            await self._process_batch()
```

### 3. Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            if self.failures >= self.failure_threshold:
                self.state = "open"
            
            raise e
```

## Testing Async Events

### 1. Event Testing

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_user_creation_emits_event():
    # Mock event queue
    mock_emit = AsyncMock()
    event_queue.emit = mock_emit
    
    # Create user
    response = await client.post("/users", json={
        "email": "test@example.com",
        "name": "Test User"
    })
    
    assert response.status_code == 200
    
    # Verify event emitted
    mock_emit.assert_called_once()
    call_args = mock_emit.call_args
    assert call_args[0][0] == "user_created"
    assert call_args[0][1]["email"] == "test@example.com"
```

### 2. Handler Testing

```python
@pytest.mark.asyncio
async def test_welcome_email_handler():
    # Mock email service
    email_service.send_welcome = AsyncMock()
    
    # Call handler directly
    await send_welcome_email({
        "user_id": 123,
        "email": "test@example.com"
    })
    
    # Verify email sent
    email_service.send_welcome.assert_called_once_with("test@example.com")
```

## Monitoring Async Operations

### 1. Event Metrics

```python
from prometheus_client import Counter, Histogram

event_counter = Counter(
    'events_total',
    'Total events processed',
    ['event_type', 'status']
)

event_duration = Histogram(
    'event_processing_duration_seconds',
    'Event processing duration',
    ['event_type']
)

async def monitored_handler(event_type: str, handler):
    """Wrap handler with monitoring."""
    async def wrapper(data):
        with event_duration.labels(event_type).time():
            try:
                await handler(data)
                event_counter.labels(event_type, 'success').inc()
            except Exception as e:
                event_counter.labels(event_type, 'failure').inc()
                raise
    
    return wrapper
```

### 2. Health Checks

```python
@app.get("/health/events")
async def event_health():
    """Check event processing health."""
    return {
        "queue_size": event_queue.queue.qsize(),
        "handlers": {
            event_type: len(handlers)
            for event_type, handlers in event_queue.handlers.items()
        },
        "status": "healthy" if event_queue.queue.qsize() < 1000 else "degraded"
    }
```

## Common Async Pitfalls

### 1. Blocking Operations
```python
# ❌ Bad - Blocks event loop
def process_image(path):
    image = Image.open(path)  # Blocking I/O
    # Process...

# ✅ Good - Non-blocking
async def process_image(path):
    loop = asyncio.get_event_loop()
    image = await loop.run_in_executor(None, Image.open, path)
    # Process...
```

### 2. Exception Handling
```python
# ❌ Bad - Swallows exceptions
async def handler(data):
    try:
        await risky_operation(data)
    except:
        pass  # Silent failure

# ✅ Good - Proper handling
async def handler(data):
    try:
        await risky_operation(data)
    except SpecificError as e:
        logger.error(f"Expected error: {e}")
        # Retry or compensate
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        # Alert and investigate
```

### 3. Memory Leaks
```python
# ❌ Bad - Unbounded queue
events = []
async def bad_handler(data):
    events.append(data)  # Grows forever

# ✅ Good - Bounded processing
from collections import deque

events = deque(maxlen=1000)  # Fixed size
async def good_handler(data):
    events.append(data)
```

## Claude Code Commands

### Event-Driven Development
```bash
# Create event handler
/create-event-handler user-registered

# Add async validation
/validate-async

# Test event flow
/test-async-flow user-registration

# Monitor events
/pm events
```

### Debugging Async Code
```bash
# Check event queue
/debug events queue

# Trace event flow
/debug events trace user_created

# Performance analysis
/pm async-profile
```

## Best Practices

1. **Always provide feedback** - Show users their action was received
2. **Set timeouts** - Don't wait forever for async operations
3. **Handle failures gracefully** - Use retry logic and dead letter queues
4. **Monitor everything** - Track queue sizes, processing times, and errors
5. **Test thoroughly** - Include async scenarios in your test suite

Start building event-driven systems with `/py-prd async-service`!
