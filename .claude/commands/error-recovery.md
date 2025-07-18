# Error Recovery

Recover from common development errors and issues.

## Arguments:
- $TYPE: git|build|test|design|deps|all
- $ACTION: diagnose|fix|rollback

## Why This Command:
- Quick recovery from common issues
- Maintains context during fixes
- Prevents work loss
- Reduces debugging time

## Steps:

### Type: GIT
Handle git-related issues:

```bash
# Diagnose
/error-recovery git diagnose
> "Detached HEAD detected"
> "3 uncommitted files at risk"
> "Suggested: /error-recovery git fix"

# Fix common issues
case "$ISSUE" in
  "detached-head")
    git checkout -b temp-recovery-$(date +%s)
    echo "✅ Created recovery branch"
    ;;
  "merge-conflict")
    echo "Conflicts in:"
    git diff --name-only --diff-filter=U
    echo "Run: git mergetool"
    ;;
  "large-file")
    git reset HEAD~1
    echo "Use: git lfs track '*.psd'"
    ;;
esac
```

### Type: BUILD
Fix build errors:

```bash
# Common Next.js issues
"Module not found" -> npm install
"Type error" -> Run tsc --noEmit
"Build failed" -> Clear cache and retry

# Auto-fix attempt
rm -rf .next node_modules
npm install
npm run build
```

### Type: DESIGN
Fix design violations:

```bash
# Auto-fix common violations
find . -name "*.tsx" -type f -exec sed -i '' \
  -e 's/text-sm/text-size-3/g' \
  -e 's/text-lg/text-size-2/g' \
  -e 's/font-bold/font-semibold/g' \
  -e 's/p-5/p-4/g' \
  {} \;

echo "✅ Fixed common violations"
echo "Run: /validate-design"
```

### Type: DEPS
Fix dependency issues:

```bash
# Clear all caches
rm -rf node_modules .next .turbo
rm package-lock.json pnpm-lock.yaml

# Reinstall
pnpm install --force

# Verify
pnpm run typecheck
```

### Emergency Rollback
When all else fails:

```bash
# Save current state
/checkpoint create emergency-$(date +%s)

# Find last working commit
LAST_GOOD=$(git log --format="%h %s" -20 | \
  grep -E "(feat|fix|chore)" | head -1 | cut -d' ' -f1)

# Create recovery branch
git checkout -b recovery-$(date +%s) $LAST_GOOD

echo "✅ Rolled back to: $LAST_GOOD"
echo "Lost work saved in checkpoint"
```

## Integration:
- Captures context before any fixes
- Updates context after resolution
- Links to relevant documentation
- Suggests preventive measures
