# Truth Override - Allow Intentional Changes to Established Values

Temporarily override truth enforcement when you need to make intentional changes to established values like API routes, component names, or environment variables.

## Usage

```bash
/truth-override [reason]
/override-facts [reason]
/allow-changes [reason]

# Examples:
/truth-override "Refactoring API v2"
/truth-override "Renaming components to new convention"
/truth-override "Updating environment variables for new auth system"
```

## What It Does

Creates a temporary override that allows changes to established values for 1 hour.

## How It Works

1. **Creates Override File**
   ```json
   {
     "timestamp": "2024-01-15T10:30:00",
     "reason": "Refactoring API v2",
     "user": "current_user",
     "expires": "2024-01-15T11:30:00"
   }
   ```

2. **Truth Enforcer Behavior**
   - Still warns about changes
   - Shows what's being changed
   - Allows the change to proceed
   - Reminds to update all references

3. **Automatic Expiry**
   - Override expires after 1 hour
   - Prevents accidental permanent disable
   - Can be renewed if needed

## Example Workflow

### Refactoring API Routes
```bash
# 1. See current routes
/facts api
> POST /api/auth/login
> GET /api/user/profile

# 2. Enable override
/truth-override "Updating to REST v2 conventions"
> ✅ Truth enforcement override active for 1 hour
> Reason: Updating to REST v2 conventions

# 3. Make changes
# Change /api/auth/login to /api/v2/auth/login
# Truth enforcer will warn but allow

# 4. Update all references
# Update frontend API calls
# Update documentation
# Update tests

# 5. Verify changes
/facts api
> POST /api/v2/auth/login (updated)
> GET /api/v2/user/profile (updated)
```

### Renaming Components
```bash
# Override for component updates
/truth-override "Renaming Button to ActionButton"

# Now you can:
- Rename component files
- Update all imports
- Change prop interfaces
- Update tests
```

## Other Ways to Allow Changes

### 1. Task-Based Override
Include keywords in your task description:
- "refactor"
- "rename" 
- "update api"
- "migrate"
- "breaking change"

Example:
```bash
/todo add "Refactor API routes to v2 structure"
# Truth enforcer detects "refactor" and allows changes
```

### 2. Commit Message Override
Recent commits with refactoring keywords allow changes:
```bash
git commit -m "refactor: Update API routes to v2"
# Truth enforcer sees "refactor:" and allows changes
```

## Safety Features

1. **Time Limited** - Expires after 1 hour
2. **Logged** - All overrides are logged
3. **Warnings Still Show** - You see what's changing
4. **Not Silent** - Still reminds about references

## When to Use

✅ **Good Reasons:**
- API versioning updates
- Component naming conventions
- Database schema migrations
- Environment variable restructuring
- Breaking changes with notice

❌ **Bad Reasons:**
- "Claude is being annoying"
- "Just for this quick fix"
- "I'll update references later"

## Cleanup

Override automatically expires, but to manually remove:
```bash
rm .claude/truth-override.json
```

## Integration with Workflow

```bash
# Full refactoring workflow
/truth-override "API v2 migration"
/facts api                    # Document current state
# Make changes
/facts api                    # Verify new state
# Update all code references
/chain safe-commit           # Validate everything
```

Remember: With great power comes great responsibility. Update ALL references!