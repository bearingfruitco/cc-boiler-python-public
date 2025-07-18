# Check Work

Quick implementation quality check that leverages existing systems.

## Arguments:
- $ASPECT: all|versions|imports|todos (default: all)

## Why This Command:
- Catch common implementation issues
- Ensure consistency
- Find incomplete work
- Complement existing systems

## Steps:

### Quick All-Around Check

```bash
/check-work

echo "🔍 IMPLEMENTATION CHECK"
echo "====================="
echo ""

# 1. Version Consistency (simple check)
echo "📌 Version Consistency:"
CONFIG_VERSION=$(grep -o '"version":\s*"[^"]*"' .claude/config.json | cut -d'"' -f4)
PACKAGE_VERSION=$(grep -o '"version":\s*"[^"]*"' package.json | cut -d'"' -f4)

if [ "$CONFIG_VERSION" = "$PACKAGE_VERSION" ]; then
  echo "✅ Versions match: $CONFIG_VERSION"
else
  echo "❌ Version mismatch!"
  echo "   .claude/config.json: $CONFIG_VERSION"
  echo "   package.json: $PACKAGE_VERSION"
fi

# 2. Recent Changes (leverage existing change-log)
echo -e "\n📝 Recent Changes:"
echo "Run: /change-log view"
echo "(Your changes are already tracked by change-log)"

# 3. Check for TODOs/FIXMEs
echo -e "\n🚧 Incomplete Work:"
TODO_COUNT=$(grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.tsx" --include="*.py" . 2>/dev/null | grep -v node_modules | wc -l)

if [ $TODO_COUNT -eq 0 ]; then
  echo "✅ No TODOs found"
else
  echo "⚠️  Found $TODO_COUNT TODO/FIXME markers:"
  grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.tsx" --include="*.py" . 2>/dev/null | grep -v node_modules | head -5
  if [ $TODO_COUNT -gt 5 ]; then
    echo "... and $(($TODO_COUNT - 5)) more"
  fi
fi

# 4. Hook Conflicts
echo -e "\n🪝 Hook Integrity:"
DUPLICATE_HOOKS=$(find .claude/hooks -name "*.py" | xargs -I {} basename {} | sed 's/^\([0-9]*\)-.*/\1/' | sort | uniq -d)

if [ -z "$DUPLICATE_HOOKS" ]; then
  echo "✅ No duplicate hook numbers"
else
  echo "❌ Duplicate hook numbers found: $DUPLICATE_HOOKS"
fi

# 5. Import Check (for Python files modified recently)
echo -e "\n📦 Import Validation:"
echo "Checking recently modified Python files..."

# Find Python files modified in last day
RECENT_PY=$(find . -name "*.py" -mtime -1 -not -path "./node_modules/*" -not -path "./.git/*" 2>/dev/null)

if [ -z "$RECENT_PY" ]; then
  echo "No Python files modified recently"
else
  IMPORT_ERRORS=0
  for file in $RECENT_PY; do
    # Basic check for obvious import issues
    if grep -E "from \.\. import" "$file" > /dev/null 2>&1; then
      # Check if parent __init__.py exists
      parent_init="$(dirname $(dirname $file))/__init__.py"
      if [ ! -f "$parent_init" ]; then
        echo "⚠️  Missing __init__.py for imports in $file"
        ((IMPORT_ERRORS++))
      fi
    fi
  done
  
  if [ $IMPORT_ERRORS -eq 0 ]; then
    echo "✅ Import structure looks good"
  fi
fi

# 6. Suggest Next Steps
echo -e "\n💡 NEXT STEPS:"

if [ $TODO_COUNT -gt 0 ]; then
  echo "1. Complete the $TODO_COUNT TODO items"
fi

if [ "$CONFIG_VERSION" != "$PACKAGE_VERSION" ]; then
  echo "2. Sync version numbers across files"
fi

echo "3. Run /change-log sync-docs to update documentation"
echo "4. Use /checkpoint to save your progress"
echo "5. Run /validate-design to check design compliance"

echo -e "\n✨ Check complete! Use existing commands for deeper analysis."
```

### Focused Checks

#### Check Versions Only
```bash
/check-work versions

# Quick version check across all files
grep -H '"version"' .claude/config.json package.json *.json 2>/dev/null | grep -v node_modules
```

#### Check TODOs Only
```bash
/check-work todos

# Find all incomplete work markers with context
grep -rn "TODO\|FIXME\|HACK\|XXX\|INCOMPLETE" \
  --include="*.ts" --include="*.tsx" --include="*.py" --include="*.md" \
  . 2>/dev/null | grep -v node_modules | \
  awk -F: '{print $1 ":" $2 " - " substr($0, index($0,$3))}'
```

#### Check Imports Only
```bash
/check-work imports

# Python import check
echo "🐍 Python Import Check:"
find . -name "*.py" -not -path "./node_modules/*" -exec python3 -m py_compile {} \; 2>&1 | grep -v "node_modules"

# TypeScript import check
echo -e "\n📘 TypeScript Import Check:"
echo "Run: npm run typecheck"
```

## Integration with Existing Tools

This command is intentionally lightweight and leverages:

1. **Change Log** - For tracking what changed
   ```bash
   /change-log view      # See all changes
   /change-log sync-docs # Update docs
   ```

2. **Validation Commands** - For deeper checks
   ```bash
   /validate-design     # Design system compliance
   /lint-check         # Code quality
   /test-runner        # Run tests
   ```

3. **State Management** - For saving work
   ```bash
   /checkpoint         # Save current state
   /sr                # Smart resume
   ```

## Philosophy

This command follows the pattern:
1. **Analyze** - Quick scan for common issues
2. **Recommend** - Suggest existing tools
3. **Revise** - Don't duplicate, integrate

It's a "pre-flight check" that points you to the right tools rather than reimplementing them.

## Examples

```bash
# After making changes
/check-work
> Version mismatch detected
> 3 TODOs found
> Suggests: sync versions, complete TODOs

# Before committing
/check-work
> All checks passed
> Suggests: /change-log add feature "..."

# Quick TODO scan
/check-work todos
> Lists all incomplete items with file:line
```

This complements your existing sophisticated systems without duplicating them!
