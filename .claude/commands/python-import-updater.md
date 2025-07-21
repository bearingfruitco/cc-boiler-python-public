---
name: python-import-updater
aliases: [pyimports, update-imports, fix-imports]
description: Update Python imports after refactoring or moving files
category: python
---

Automatically update import statements across your codebase after moving, renaming, or refactoring Python modules. Prevents broken imports and maintains consistency.

## Usage
```bash
/python-import-updater [old_path] [new_path]
/pyimports [old_module] [new_module]
/update-imports --check
/fix-imports --auto
```

## Common Scenarios

### After Moving a Module
```bash
# Moved src/utils/auth.py to src/auth/core.py
/python-import-updater src.utils.auth src.auth.core

# Updates all imports:
# from src.utils.auth import login → from src.auth.core import login
# import src.utils.auth → import src.auth.core
```

### After Renaming a Class
```bash
# Renamed UserModel to User
/pyimports UserModel User --type=class

# Updates:
# from models import UserModel → from models import User
# isinstance(obj, UserModel) → isinstance(obj, User)
```

### After Splitting a Module
```bash
# Split src/models.py into src/models/user.py and src/models/post.py
/python-import-updater --split src.models "src.models.user:User,UserProfile src.models.post:Post,Comment"
```

## Features

### 1. Import Detection
- Direct imports: `import module`
- From imports: `from module import name`
- Aliased imports: `import module as alias`
- Relative imports: `from . import module`
- Dynamic imports: `__import__('module')`

### 2. Update Types
- Module moves/renames
- Class/function moves
- Package restructuring
- Namespace changes
- Import consolidation

### 3. Safety Features
- Dry run mode (default)
- Backup creation
- Git integration
- Rollback support

## Options

### Check Mode (Default)
```bash
/python-import-updater --check
# Shows what would be updated without making changes

Output:
📊 Import Update Preview
Found 12 files with imports to update:

src/api/auth.py:
  Line 3: from src.utils.auth import login
  → from src.auth.core import login

src/services/user.py:
  Line 8: import src.utils.auth as auth_utils
  → import src.auth.core as auth_utils

[10 more files...]

Run with --apply to make changes
```

### Apply Changes
```bash
/python-import-updater src.utils.auth src.auth.core --apply

✅ Updated 12 files
📁 Backup created: .claude/backups/imports_20240117_143022/
```

### Auto-Fix All Issues
```bash
/fix-imports --auto

🔍 Scanning for broken imports...
Found 3 broken imports:
  - src.old_module (not found)
  - src.utils.deleted_func (not found)
  - src.models.OldModel (not found)

🔧 Attempting auto-fix...
  ✅ Fixed: src.old_module → src.new_module
  ✅ Fixed: src.utils.deleted_func → src.helpers.new_func
  ❌ Cannot fix: src.models.OldModel (no match found)

2/3 imports fixed automatically
```

## Advanced Usage

### Batch Updates
```bash
# Update multiple modules at once
/python-import-updater --batch << EOF
src.old.module1 → src.new.module1
src.old.module2 → src.new.module2
src.utils.helper → src.core.utilities.helper
EOF
```

### With Git Integration
```bash
# Commit import updates separately
/python-import-updater src.old src.new --git-commit

✅ Updated 8 files
📝 Committed: "refactor: Update imports after moving src.old to src.new"
```

### Import Optimization
```bash
# Consolidate and organize imports
/python-import-updater --optimize

Before:
  from src.models import User
  from src.models import Post
  from src.models import Comment
  import src.utils
  from src.utils import format_date

After:
  from src.models import User, Post, Comment
  from src.utils import format_date
```

## Integration with Other Commands

### After Moving Files
```bash
# Move file
mv src/utils/auth.py src/auth/core.py

# Update imports
/python-import-updater src.utils.auth src.auth.core --apply
```

### With Dependency Tracking
```bash
# Check dependencies first
/pydeps breaking src.utils.auth

# If safe, proceed with update
/python-import-updater src.utils.auth src.auth.core --apply
```

### In Refactoring Workflow
```bash
# 1. Check what uses the module
/pydeps check UserModel

# 2. Move/rename
mv src/models/user_model.py src/models/user.py

# 3. Update imports
/python-import-updater src.models.user_model src.models.user --apply

# 4. Run tests
/test
```

## Configuration

In `.claude/config.json`:
```json
{
  "import_updater": {
    "auto_backup": true,
    "check_tests": true,
    "update_strings": false,
    "update_comments": false,
    "git_commit": false,
    "exclude_patterns": [
      "*.pyc",
      "__pycache__",
      ".venv"
    ]
  }
}
```

## Error Handling

### Common Issues

1. **Ambiguous Imports**
```
⚠️ Ambiguous import found:
  from models import User
  
Could refer to:
  - src.models.user.User
  - src.legacy.models.User
  
Please specify: /python-import-updater models.User src.models.user.User
```

2. **Circular Imports**
```
❌ Circular import detected:
  src.models.user imports src.services.user_service
  src.services.user_service imports src.models.user
  
Consider refactoring to break the cycle.
```

3. **Missing Dependencies**
```
⚠️ Import not found in project:
  from external_lib import something
  
This appears to be an external dependency. No update needed.
```

## Best Practices

1. **Always Check First**
   ```bash
   /python-import-updater --check
   # Review changes before applying
   ```

2. **Update Tests Too**
   ```bash
   /python-import-updater src.old src.new --include-tests
   ```

3. **Use Git Branches**
   ```bash
   git checkout -b refactor/update-imports
   /python-import-updater src.old src.new --apply
   git commit -am "Update imports after refactoring"
   ```

4. **Document Module Moves**
   ```python
   """
   Module moved from src.utils.auth to src.auth.core
   Update imports with: /python-import-updater src.utils.auth src.auth.core
   """
   ```
