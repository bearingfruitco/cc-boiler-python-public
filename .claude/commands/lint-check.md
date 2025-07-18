# Lint Check (Biome Edition)

Run Biome linting and formatting checks on your code.

## Arguments:
- $SCOPE: current|changed|all|fix
- $FILES: specific files or patterns (optional)

## Usage Examples:
```bash
/lint-check current       # Check current file
/lint-check changed       # Check modified files  
/lint-check all          # Check entire project
/lint-check fix          # Auto-fix all issues
/lc changed              # Short alias
```

## Steps:

### Scope: CURRENT
Lint current file being edited:

```bash
# Get current file from context
CURRENT_FILE=$(grep -E "^(Creating|Editing|Working on):" .claude/context/current.md | \
  head -1 | sed 's/.*: //' | sed 's/ .*//')

if [ -f "$CURRENT_FILE" ]; then
  echo "🔍 Checking: $CURRENT_FILE"
  
  # Run Biome check
  pnpm biome check "$CURRENT_FILE"
  
  # If issues found, offer to fix
  if [ $? -ne 0 ]; then
    echo ""
    echo "💡 To auto-fix, run: /lint-check fix $CURRENT_FILE"
  fi
else
  echo "❌ No current file found in context"
fi
```

### Scope: CHANGED
Check all modified files:

```bash
# Get changed files (staged and unstaged)
CHANGED=$(git diff --name-only HEAD; git diff --cached --name-only)
CHANGED=$(echo "$CHANGED" | sort -u | grep -E '\.(jsx?|tsx?|json)$')

if [ -n "$CHANGED" ]; then
  echo "🔍 Checking changed files..."
  echo "$CHANGED" | nl
  echo ""
  
  # Run Biome on changed files
  pnpm biome check $CHANGED
  
  # Show summary
  echo ""
  echo "📊 Summary:"
  echo "Files checked: $(echo "$CHANGED" | wc -l)"
else
  echo "✅ No changed files to check"
fi
```

### Scope: ALL
Check entire project:

```bash
echo "🚀 Running full project lint check..."

# Run Biome on all files
pnpm lint

# Get stats
echo ""
echo "📊 Project Statistics:"
pnpm biome check . --formatter=json | jq -r '
  "Files analyzed: \(.filesAnalyzed)\nIssues found: \(.diagnostics | length)"
'
```

### Scope: FIX
Auto-fix all issues:

```bash
echo "🔧 Auto-fixing issues with Biome..."

# Fix specific files or all
if [ -n "$FILES" ]; then
  pnpm biome check --apply $FILES
  pnpm biome format --write $FILES
else
  # Fix all
  pnpm lint:fix
  pnpm format
fi

echo ""
echo "✅ Auto-fix complete!"
echo "💡 Review changes with: git diff"
```

## Format Check

Check formatting without linting:

```bash
/lint-check format components/

# Just formatting check
pnpm biome format components/

# To apply formatting
pnpm biome format --write components/
```

## CI Mode

Strict checking for CI/pre-commit:

```bash
/lint-check ci

# Run with error on warnings
pnpm biome check . --error-on-warnings

# Exit with error code if issues found
if [ $? -ne 0 ]; then
  echo "❌ CI check failed"
  exit 1
fi
```

## Integration with Git Hooks

Pre-commit hook integration:

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run Biome on staged files
STAGED=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(jsx?|tsx?|json)$')

if [ -n "$STAGED" ]; then
  pnpm biome check --apply $STAGED
  git add $STAGED
fi
```

## Custom Rules

Check for project-specific patterns:

```bash
# Check for console.logs
/lint-check custom no-console

# Uses Biome's built-in rules
pnpm biome check . --rule=suspicious.noConsoleLog=error
```

## Error Explanations

Get detailed explanations for errors:

```bash
/lint-check explain

# Example output:
"""
❌ suspicious.noConsoleLog
   Found console.log statement at line 42
   
   Why this matters:
   - Console logs can expose sensitive data
   - They impact performance in production
   - Use proper logging service instead
   
   Fix: Replace with logger.debug() or remove
"""
```

## Performance

Biome is incredibly fast:

```bash
# Benchmark against ESLint
time pnpm lint              # Biome: ~200ms
time pnpm eslint .          # ESLint: ~3000ms

# 15x faster! ⚡
```

## Configuration

Current Biome rules are in `biome.json`:
- Formatting: 2 spaces, single quotes
- Linting: Recommended + strict rules
- Organizing: Import sorting enabled

## Aliases
- `/lc` - Short for lint-check
- `/lint` - Alternative alias
- `/format` - Just formatting

This ensures code quality with blazing-fast Biome! 🚀
