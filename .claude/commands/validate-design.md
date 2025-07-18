# Validate Design System Compliance

Comprehensive validation including design system rules, Biome linting, and Bun tests.

## Arguments:
- $SCOPE: current|all|fix
- $TYPE: design|lint|test|all (default: all)

## Usage:
```bash
/validate-design              # Full validation of current file
/validate-design all          # Validate entire project
/validate-design fix          # Auto-fix what's possible
/vd                          # Short alias
```

## Steps:

### 1. Design System Check

```typescript
// Typography violations
const fontSizeViolations = findClasses(/(text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))/g);
const fontWeightViolations = findClasses(/(font-(thin|extralight|light|normal|medium|bold|extrabold|black))/g);

// Spacing violations (non-4px grid)
const spacingViolations = findClasses(/(p|m|gap|space)-(5|7|9|10|11|13|14|15|17|18|19)/g);

// Touch target analysis
const smallTargets = findElements('h-[0-9]+').filter(h => parseInt(h) < 44);

// Color distribution
const backgrounds = countClasses(/bg-(white|gray-50)/g);
const textColors = countClasses(/text-(gray-[67]00)/g);
const accents = countClasses(/(bg|text)-(blue|red|green)-[56]00/g);
```

### 2. Biome Linting

```bash
# Run Biome check on file
if [[ "$TYPE" == "lint" || "$TYPE" == "all" ]]; then
  echo "🔍 Running Biome linting..."
  
  if [[ "$SCOPE" == "current" ]]; then
    pnpm biome check "$CURRENT_FILE"
  else
    pnpm lint
  fi
  
  BIOME_EXIT=$?
fi
```

### 3. Test Validation

```bash
# Run related tests
if [[ "$TYPE" == "test" || "$TYPE" == "all" ]]; then
  echo "🧪 Running tests..."
  
  # Find test file
  TEST_FILE="${CURRENT_FILE%.tsx}.test.tsx"
  
  if [ -f "$TEST_FILE" ]; then
    bun test "$TEST_FILE"
    TEST_EXIT=$?
  else
    echo "⚠️ No test file found"
    TEST_EXIT=1
  fi
fi
```

### 4. Full Validation Report

```markdown
# 📊 Validation Report: ComponentName.tsx

## 🎨 Design System (3 issues)
❌ **Critical Violations:**
- Line 42: `text-sm` → use `text-size-4`
- Line 67: `font-bold` → use `font-semibold`
- Line 89: `p-5` → use `p-4` or `p-6`

⚠️ **Warnings:**
- Touch target on line 34 is only 40px (min: 44px)
- Color distribution: 70/25/5 (target: 60/30/10)

## 🔍 Biome Linting (2 issues)
⚠️ **Warnings:**
- Line 15: noConsoleLog - Remove console.log
- Line 23: noUnusedVariables - 'temp' is declared but never used

## 🧪 Test Coverage
✅ **Tests Passing:** 5/5
📊 **Coverage:** 87% (target: 80%)

## 📋 Summary
- Design: 3 critical, 2 warnings
- Linting: 0 errors, 2 warnings  
- Tests: All passing
- **Status:** ❌ Fix required
```

### 5. Auto-Fix Mode

```bash
if [[ "$SCOPE" == "fix" ]]; then
  echo "🔧 Auto-fixing issues..."
  
  # 1. Fix design system violations
  echo "Fixing design violations..."
  # Run design fix script
  
  # 2. Fix Biome issues
  echo "Running Biome auto-fix..."
  pnpm biome check --apply "$CURRENT_FILE"
  pnpm biome format --write "$CURRENT_FILE"
  
  # 3. Update tests if needed
  echo "Updating tests..."
  # Generate missing tests
  
  echo "✅ Auto-fix complete! Review changes with: git diff"
fi
```

## Integration with Hooks

This command is called by pre-commit hooks:

```python
# .claude/hooks/pre-tool-use/02-design-check.py
# Runs validate-design before file changes
```

## Quick Checks

For specific validation only:

```bash
/vd design     # Only design system
/vd lint       # Only Biome linting  
/vd test       # Only run tests
```

## CI Integration

```bash
# In CI pipeline
/validate-design all --ci

# Fails with exit code 1 if any issues
```

## Performance Metrics

Track validation performance:
```json
{
  "validation-times": {
    "design": "50ms",
    "biome": "200ms",
    "tests": "800ms",
    "total": "1050ms"
  }
}
```

## Auto-fix Mapping

```javascript
const fixes = {
  'text-sm': 'text-size-4',
  'text-base': 'text-size-3',
  'text-lg': 'text-size-2',
  'text-xl': 'text-size-2',
  'text-2xl': 'text-size-1',
  'font-bold': 'font-semibold',
  'font-medium': 'font-semibold',
  'p-5': 'p-6',
  'p-7': 'p-8',
  'h-10': 'h-11' // 40px → 44px
};
```

This ensures comprehensive validation with design system, Biome, and tests! 🚀
