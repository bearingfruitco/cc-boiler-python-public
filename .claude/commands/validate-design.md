---
name: validate-design
aliases: [vd, design-check]
description: Validate design system compliance
category: quality
---

Validate design system compliance for current changes or specified scope.

## Arguments:
- $SCOPE: current|all|[file-path] (default: current)

## Design System Rules Checked:

### Typography (Strict)
- Only text-size-[1-4] allowed
- Only font-regular and font-semibold allowed
- No text-sm, text-lg, text-xl, etc.
- No font-bold, font-medium

### Spacing (4px Grid)
- All spacing must be divisible by 4
- Valid: p-1, p-2, p-3, p-4, p-6, p-8
- Invalid: p-5, p-7, p-10

### Color Distribution
- 60% neutral backgrounds
- 30% text and borders
- 10% primary actions

### Mobile Requirements
- Touch targets >= 44px
- Body text >= 16px
- Max width constraints

## Output Format:
```
Design Validation Results
========================

✅ Passed: 45 files
❌ Failed: 3 files

Violations:
-----------
src/components/Button.tsx:
  Line 23: Invalid font class "font-bold" (use font-semibold)
  Line 45: Invalid spacing "p-5" (use p-4 or p-6)

src/styles/card.css:
  Line 12: Invalid text size "text-sm" (use text-size-3)

Summary:
--------
Typography violations: 2
Spacing violations: 1
Color distribution: Within limits
Mobile compliance: Passed
```

## Integration:
- Used in pre-commit hooks
- Part of PR validation
- Enforced by design-check hook
