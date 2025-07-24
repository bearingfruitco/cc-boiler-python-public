# Python Design Patterns Standards
<!-- This complements existing hooks and commands - READ ONLY reference -->

## Agent Architecture Patterns
These patterns are enforced by existing hooks (16-python-creation-guard.py)

### Base Pattern
```python
BaseAgent → SpecializedAgent → ConcreteImplementation
         ↓                    ↓
    AgentMemory          ToolIntegration
```

### Memory Patterns
- Short-term: Last 20 interactions (enforced by BaseAgent)
- Long-term: Redis-backed persistent storage
- Context: Current working state

### Tool Integration Pattern
```python
# Tools declared at class level
tools: List[str] = ["pandas", "plotly", "yfinance"]

# Used via structured method
agent.use_tool("pandas", data=df)
```

## API Design Patterns
These complement py-api command generation

### Router Organization
```
/api
  /routers
    /v1
      /{feature}.py     # Feature-specific endpoints
    /internal
      /admin.py         # Internal only endpoints
  /dependencies.py      # Shared dependencies
  /middleware.py        # Custom middleware
```

### Dependency Injection Pattern
```python
# Always use FastAPI dependencies for:
- Authentication (get_current_user)
- Database sessions (get_db)
- Rate limiting (check_rate_limit)
- Caching (get_cache)
```

## Pipeline Patterns
For use with py-pipeline command

### Prefect Flow Pattern
```python
@flow(name="etl-pipeline")
def main_flow():
    # Extract → Transform → Load
    raw_data = extract_task()
    clean_data = transform_task(raw_data)
    result = load_task(clean_data)
    return result
```

### Error Handling Pattern
- Use Prefect's built-in retry mechanisms
- Log all failures to structured logs
- Send alerts via event queue (non-blocking)

## Testing Patterns
Enforced by 19-test-generation-enforcer.py

### Mock Pattern for LLMs
```python
# Always mock LLM calls
@patch('openai.ChatCompletion.create')
def test_agent_response(mock_llm):
    mock_llm.return_value = {...}
```

### Fixture Organization
```python
# conftest.py structure
- Database fixtures
- Mock LLM fixtures  
- Test data factories
- Authentication fixtures
```

## Event-Driven Patterns
Complements async-patterns hook

### Fire-and-Forget Pattern
```python
# Non-critical operations
eventQueue.emit(EVENTS.ANALYTICS, data)  # Don't await
eventQueue.emit(EVENTS.NOTIFICATION, msg)  # Don't await

# Critical operations
result = await api.save(data)  # Must await
```

### Parallel Processing Pattern
```python
# Good - parallel execution
results = await asyncio.gather(
    fetch_user(id),
    fetch_preferences(id),
    fetch_permissions(id)
)

# Bad - sequential execution
user = await fetch_user(id)
prefs = await fetch_preferences(id)
perms = await fetch_permissions(id)
```

## Security Patterns
Enforced by 07-pii-protection.py

### PII Handling
- Never log PII fields
- Always encrypt at rest
- Use field registry for validation
- Audit all access

### API Security
- Rate limiting on all endpoints
- JWT with short expiration
- Refresh token rotation
- Request signing for webhooks

---

Note: These patterns are automatically enforced by your existing hooks.
This document serves as a reference, not a ruleset.