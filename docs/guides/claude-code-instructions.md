# Claude Code Instructions for FreshSlate

## Initial Setup Message

```
I'm working on FreshSlate, a financial wellness quiz application. 

CRITICAL: You must follow the design system in docs/design-system.md and DESIGN_RULES.md exactly. 

Key constraints:
1. ONLY 4 font sizes (text-size-1 through text-size-4) and 2 weights (regular 400, semibold 600)
2. ALL spacing must be divisible by 4 (use 4px grid)
3. Follow 60/30/10 color rule (60% neutral, 30% text/UI, 10% accent)
4. Mobile-first: minimum 44px touch targets, 16px body text

When you violate any of these rules, I need you to flag it immediately and fix it.
```

## Custom Commands

### 1. Component Creation

```
Command: /create-quiz-component [component-name]

Create a new quiz component following FreshSlate design system:
- Use standard container pattern from DESIGN_RULES.md
- Implement with 4px grid spacing
- Only use the 4 approved font sizes and 2 weights
- Follow 60/30/10 color distribution
- Include proper TypeScript types
- Add subtle animations from design system
- Make it mobile-first with 44px+ touch targets
```

### 2. Design System Validation

```
Command: /validate-design-system

Review the current file against DESIGN_RULES.md and flag:
1. Any font-size not in our 4-size system
2. Any font-weight other than 400 or 600
3. Any spacing not divisible by 4
4. Color distribution violations (should be ~60/30/10)
5. Touch targets under 44px
6. Text under 16px for important content

Provide a report with:
- ❌ Violations found
- ✅ Suggested fixes
- 📍 Line numbers
```

### 3. Convert to FreshSlate Style

```
Command: /convert-to-freshslate

Take the selected code and convert it to follow FreshSlate design system:
1. Replace all font sizes with our 4-size system
2. Replace all font weights with regular/semibold only
3. Adjust all spacing to 4px grid
4. Update colors to match our semantic color system
5. Ensure mobile-first approach
6. Add proper transitions/animations
```

### 4. Create Marketing Component

```
Command: /create-marketing-component [type]

Create a marketing component (hero/features/testimonial/cta) that:
- Follows FreshSlate design system strictly
- Uses emotional color coding (green=positive, red=warning, blue=action)
- Implements 60/30/10 color distribution
- Includes appropriate animations
- Is optimized for conversion
- Works perfectly on mobile
```

### 5. Implement Animation

```
Command: /add-animation [subtle|medium|celebratory]

Add appropriate animation to the selected component:
- Subtle: hover states, micro-interactions (100-200ms)
- Medium: transitions, reveals (300-500ms)  
- Celebratory: confetti, success states (one-time)

Follow animation guidelines from design-system.md
Ensure 60fps performance on mobile
```

## Validation Snippets

### Typography Check
```
Command: /check-typography

Scan for:
- font-size classes not in: text-size-1, text-size-2, text-size-3, text-size-4
- font-weight classes not in: font-regular, font-semibold
- Any inline styles setting font properties
- Text smaller than 16px for body content
```

### Spacing Check
```
Command: /check-spacing

Scan for:
- Padding/margin/gap values not divisible by 4
- Common violations: p-5, m-7, gap-10, space-y-5
- Inline styles with pixel values not on grid
- Suggest nearest 4px grid value
```

### Color Balance Check
```
Command: /check-color-balance

Analyze color distribution:
- Count background/neutral colors (should be ~60%)
- Count text/border colors (should be ~30%)
- Count accent colors (should be ~10%)
- Flag if accent colors are overused
```

## Quick Fixes

### Fix All Typography
```
Command: /fix-typography

Automatically:
- Replace text-sm → text-size-4 (12px)
- Replace text-base → text-size-3 (16px)
- Replace text-lg/text-xl → text-size-2 (24px)
- Replace text-2xl/text-3xl → text-size-1 (32px)
- Replace font-medium/font-bold → font-semibold
- Replace font-light/font-thin → font-regular
```

### Fix All Spacing
```
Command: /fix-spacing

Automatically adjust to 4px grid:
- p-5 → p-4 (20px → 16px)
- p-7 → p-6 (28px → 24px)
- gap-5 → gap-4 (20px → 16px)
- m-10 → m-8 (40px → 32px)
```

## Component Templates

### Quiz Step Template
```
Command: /template-quiz-step

Generate a new quiz step with:
- Standard container and spacing
- Question using text-size-2 font-semibold
- Helper text using text-size-3 font-regular
- Input component (slider/buttons/select)
- Continue button (h-12 for 48px touch target)
- Proper mobile padding (p-4 = 16px)
```

### Report Card Template
```
Command: /template-report-card [type: income|expense|warning|success]

Generate a report card with:
- Appropriate semantic colors
- Icon (w-5 h-5) with proper color
- Title (text-size-2 font-semibold)
- Content (text-size-3 font-regular)
- Proper spacing (p-4 with space-y-3)
```

## Integration Examples

### With Tailwind UI Component
```
Command: /integrate-tailwind-ui

When pasting a Tailwind UI component:
1. Adjust all spacing to our 4px grid
2. Replace their typography with our 4-size system
3. Update colors to match our 60/30/10 distribution
4. Ensure mobile-first approach
5. Add our standard animations
```

### With Shadcn Component
```
Command: /integrate-shadcn

When adding a shadcn/ui component:
1. Override their CSS variables with our design tokens
2. Adjust typography to 4 sizes, 2 weights
3. Update spacing to 4px grid
4. Maintain their accessibility features
5. Style according to our color system
```

## Debugging Commands

### Show Design Violations
```
Command: /show-violations

Highlight in the editor:
- 🔴 Critical violations (wrong typography, broken grid)
- 🟡 Warnings (color balance off, small touch targets)
- 🔵 Suggestions (could use better animation, spacing)
```

### Generate Design Report
```
Command: /design-report

Create a markdown report showing:
- Typography usage statistics
- Spacing compliance percentage
- Color distribution analysis
- Mobile-first compliance
- Suggestions for improvement
```

## Remember

Always reference:
- `DESIGN_RULES.md` for quick checks
- `docs/design-system.md` for detailed patterns
- Component examples for implementation
- Animation guidelines for interactions

The goal is consistent, beautiful, mobile-first UI that follows our strict design system!