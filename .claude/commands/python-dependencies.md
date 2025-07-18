---
name: python-dependencies
aliases: [pydeps, py-deps, deps-py]
description: Track and manage Python module dependencies
category: python
---

Lightweight dependency tracking for Python projects using docstring annotations and import analysis. Prevents breaking changes and circular dependencies.

## Usage
```bash
/pydeps [action] [module] [options]
```

## Actions

### Check Dependencies
```bash
/pydeps check module_name      # What imports this module?
/pydeps check src.api.auth     # Full module path
/pydeps check UserModel        # Class/function name
```

### Scan Project
```bash
/pydeps scan                   # Full project scan
/pydeps scan --update          # Update all annotations
/pydeps scan --ci              # CI mode (fail on issues)
```

### Breaking Change Detection
```bash
/pydeps breaking module_name   # Check before changes
/pydeps breaking --preview     # See what would break
```

### Other Actions
```bash
/pydeps circular               # Find circular imports
/pydeps update module_name     # Update all importers
/pydeps graph module_name      # Visual dependency graph
```

## Annotation Format

### Module Level
```python
"""
User authentication module.

@module: auth
@exports: authenticate, create_user, UserModel
@imports-from: database, utils.security, models.base
@imported-by: api.endpoints, services.user, tests.test_auth
@breaking-changes: 2024-01-15 - Removed legacy_auth function
"""
```

### Class Level
```python
class UserModel(BaseModel):
    """
    User data model.
    
    @imported-by: api.auth, services.user, serializers.user
    @depends-on: BaseModel, EmailStr, SecretStr
    @interface-stable: True
    """
```

### Function Level
```python
async def process_data(
    data: pd.DataFrame,
    config: ProcessConfig
) -> ProcessResult:
    """
    Process data with configuration.
    
    @imported-by: pipelines.daily_etl, pipelines.hourly_etl
    @breaking-change-risk: High (return type critical)
    @async: True
    """
```

## Dependency Detection

### Import Patterns Detected
```python
# Direct imports
import module
from module import Class, function

# Relative imports
from . import sibling
from ..parent import something

# Dynamic imports
importlib.import_module('module')

# Type annotation imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from module import Type
```

### Dependency Graph Structure
```json
{
  "src.models.user": {
    "exports": ["UserModel", "UserRole", "UserStatus"],
    "imports": ["pydantic", "enum", "datetime"],
    "imported_by": [
      "src.api.auth",
      "src.services.user",
      "src.db.repositories.user"
    ],
    "change_risk": "high",
    "last_modified": "2024-01-17",
    "breaking_changes": []
  }
}
```

## Breaking Change Detection

### What's Detected
1. **Removed exports** - Functions/classes no longer available
2. **Signature changes** - Different parameters or return types
3. **Type changes** - Modified type annotations
4. **Async changes** - Sync → async or vice versa
5. **Required parameters** - New required args added

### Alert Example
```
⚠️ Breaking Change Alert: src.models.user

This module is imported by 5 other modules:
  • src.api.auth (3 imports)
  • src.services.user (2 imports)  
  • src.db.repositories.user (1 import)
  • tests.test_user (4 imports)
  • src.serializers.user (1 import)

🚨 Breaking Changes Detected:
  • Removed export: 'create_user' (used by api.auth)
  • Changed signature: 'UserModel.__init__' (added required field)
  • Type change: 'user_id' from int to UUID

Suggested Actions:
  1. /pydeps update src.models.user - Update importers
  2. Review changes in: api.auth, services.user
  3. Run tests: pytest tests/test_user.py
```

## Integration with Python Tools

### pytest Integration
```python
# Automatically generated test
def test_imports_still_work():
    """Test that all imports in dependency graph resolve."""
    for module, deps in dependency_graph.items():
        for imp in deps['imports']:
            try:
                importlib.import_module(imp)
            except ImportError:
                pytest.fail(f"{module} cannot import {imp}")
```

### mypy Integration
```bash
# Check type compatibility after changes
/pydeps check UserModel --mypy
```

### Ruff Integration
```bash
# Update imports to match new structure
/pydeps update module --fix-imports
```

## Circular Dependency Detection

### Detection Output
```
🔄 Circular Dependencies Found:

Cycle 1:
  src.models.user → src.services.auth → src.models.user
  
  Breaking points:
  1. Move 'authenticate' to src.services.user
  2. Extract interface to src.interfaces.auth
  
Cycle 2:
  src.api.endpoints → src.db.queries → src.api.utils → src.api.endpoints
  
  Severity: High (affects 8 modules)
```

## Configuration

### .claude/config.json
```json
{
  "python_dependencies": {
    "scan_on_save": true,
    "update_annotations": true,
    "check_circular": true,
    "alert_threshold": 3,
    "track_test_deps": true,
    "ignore_patterns": ["*_test.py", "migrations/*"],
    "framework_specific": {
      "django": ["models", "views", "serializers"],
      "fastapi": ["routers", "dependencies", "models"],
      "prefect": ["flows", "tasks", "blocks"]
    }
  }
}
```

## Best Practices

1. **Regular Scans**
   ```bash
   # Add to pre-commit
   /pydeps scan --ci
   ```

2. **Before Refactoring**
   ```bash
   /pydeps check MyClass
   /pydeps breaking MyClass --preview
   ```

3. **Document Breaking Changes**
   ```python
   """
   @breaking-changes:
     - 2024-01-17: Removed legacy_method
     - 2024-01-15: Changed return type to List[User]
   """
   ```

4. **Use Type Annotations**
   - Helps detect signature changes
   - Improves breaking change detection
   - Better IDE support
