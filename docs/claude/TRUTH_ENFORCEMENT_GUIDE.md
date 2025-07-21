# Truth Enforcement - Flexible Protection

## How It Works

The Truth Enforcer protects established values from **accidental** changes while allowing **intentional** refactoring.

## Protection Levels

### 🔴 High Severity (Blocked by default)
- API route changes
- Database schema modifications
- Core configuration changes

### ⚠️ Medium/Low Severity (Warned but allowed)
- Component prop changes
- Non-critical environment variables
- UI text changes

## Allowing Intentional Changes

### Method 1: Task-Based (Automatic)
Include refactoring keywords in your task:
```bash
/todo add "Refactor API routes to v2"
/pt "Migrate auth endpoints"
```

Keywords that allow changes:
- refactor, rename, update api
- migrate, restructure, redesign
- breaking change, api v2, deprecate

### Method 2: Explicit Override (Manual)
```bash
/truth-override "Updating to REST v2 conventions"
# or
/override "Renaming components to new convention"
```

This creates a 1-hour window for changes.

### Method 3: Commit Message
```bash
git commit -m "refactor: Update API structure"
```

Recent commits with "refactor" or "breaking" allow changes.

## Example: Updating API Routes

```bash
# 1. Check current state
/facts api
> POST /api/auth/login (established)

# 2. Enable override (choose one):
/truth-override "API v2 migration"
# OR include in task:
/todo add "Refactor auth API to v2"

# 3. Make changes
# Change /api/auth/login → /api/v2/auth/login
# Hook will warn but allow:
> ⚠️ Changing established API route
> ✅ Proceeding with intentional change
> Remember to update all references!

# 4. Update all references
- Frontend API calls
- Tests
- Documentation

# 5. Verify
/facts api
> POST /api/v2/auth/login (updated)
```

## Smart Detection

The hook is smart about context:

### ✅ Allows automatically:
- When task contains "refactor"
- During active refactoring commits
- With explicit override
- For low-severity changes

### ❌ Blocks automatically:
- Random API route changes
- Accidental deletions
- Typos in established values
- Unexplained modifications

## Best Practices

1. **Use descriptive task names**
   ```bash
   ❌ /pt "Fix stuff"
   ✅ /pt "Refactor auth API to v2 structure"
   ```

2. **Update all references**
   The hook reminds you, but doesn't enforce

3. **Document breaking changes**
   ```bash
   /truth-override "BREAKING: API v2 migration - see MIGRATION.md"
   ```

4. **Clean up after refactoring**
   ```bash
   rm .claude/truth-override.json  # If used manual override
   ```

## Configuration

To adjust protection levels, edit `11-truth-enforcer.py`:

```python
# Line 200: Change severity levels
'severity': 'high'  # Change to 'medium' to warn only

# Line 290: Disable for specific paths
if '/experimental/' in path:
    return  # Skip experimental directories
```

## Summary

- **Prevents**: Accidental changes to established values
- **Allows**: Intentional refactoring with context
- **Flexible**: Multiple ways to override
- **Smart**: Understands refactoring intent
- **Safe**: Time-limited overrides

The goal is to catch mistakes, not prevent legitimate work!