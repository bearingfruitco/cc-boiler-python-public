---
name: python-exists-check
aliases: [pyexists, py-check, pysimilar]
description: Check if Python components exist before creating
category: python
---

Check if Python modules, classes, functions, or models already exist before creating new ones. Prevents duplicate work and shows where components are used.

## Usage
```bash
/pyexists [name] [type]
/py-check [name] [type]
/pysimilar [name]
```

## Types
- `module` - Python module/file
- `class` - Class definition
- `function` - Function definition
- `model` - Pydantic model
- `api` - API endpoint
- `any` - Search all types (default)

## Examples

### Check if Class Exists
```bash
/pyexists UserModel class
/pyexists FastAPIUser model
```

### Check if Function Exists
```bash
/pyexists authenticate function
/pyexists process_data any
```

### Find Similar Names
```bash
/pysimilar UserAuth
/pysimilar DataProcessor
```

## Output Format

### Exact Match Found
```
⚠️ Class 'UserModel' Already Exists!

📍 Found in 2 location(s):
  • src/models/user.py
  • src/models/base.py

📦 Imported in 5 places:
  • src/api/auth.py:12
    from src.models.user import UserModel
  • src/services/user.py:8
    from src.models import UserModel
  • tests/test_user.py:3
    from src.models.user import UserModel

📅 Last modified: 2024-01-17 14:30

🔧 Options:
1. Import and use existing component (recommended)
2. Extend existing component with new functionality
3. Create with different name
4. Override (requires confirmation)

📝 To import:
from src.models.user import UserModel
```

### Similar Names Found
```
ℹ️ No exact match for 'UserAuth', but found similar:

  • UserAuthenticator (85% match)
  • UserAuthService (82% match)
  • AuthUser (80% match)

Consider using one of these instead.
```

### No Match
```
✅ 'NewComponent' does not exist. Safe to create!
```

## Advanced Features

### Check with Context
```bash
# Check in specific module
/pyexists src.api.auth.authenticate function

# Check with inheritance
/pyexists MyModel --base=BaseModel
```

### Batch Check
```bash
# Check multiple components
/pyexists "UserModel, UserService, UserRepo" class
```

### Integration with Creation Commands
When using `/py-agent`, `/py-api`, or `/py-pipeline`, existence checking happens automatically:

```bash
/py-agent DataAnalyst
# Automatically checks if DataAnalyst agent exists

/py-api /users POST
# Checks if endpoint already defined
```

## What Gets Checked

### 1. Direct Definitions
- Class definitions: `class Name:`
- Function definitions: `def name():`
- Async functions: `async def name():`
- Constants: `NAME = value`

### 2. Imports
- Where component is imported
- How it's imported (direct, from, as)
- Import aliases used

### 3. Type Annotations
- Used in function signatures
- Used in class attributes
- Used in type hints

### 4. String References
- Django model references
- SQLAlchemy relationships
- Configuration strings

## Configuration

Configure in `.claude/config.json`:
```json
{
  "creation_guard": {
    "enabled": true,
    "check_modules": true,
    "check_classes": true,
    "check_functions": true,
    "check_models": true,
    "check_api_routes": true,
    "suggest_alternatives": true,
    "similarity_threshold": 0.8,
    "ignore_private": true,
    "ignore_tests": false
  }
}
```

## Best Practices

1. **Always Check First**
   ```bash
   /pyexists UserService class
   # Before: /py-agent UserService
   ```

2. **Use Specific Types**
   ```bash
   /pyexists process_data function  # Better
   /pyexists process_data any       # Slower
   ```

3. **Check Similar Names**
   ```bash
   /pysimilar AuthManager
   # Finds: AuthenticationManager, AuthorizationManager
   ```

4. **Review Imports**
   - See where component is used
   - Understand dependencies
   - Avoid breaking changes
