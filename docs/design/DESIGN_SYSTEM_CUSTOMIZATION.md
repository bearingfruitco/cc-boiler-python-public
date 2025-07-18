# Customizing or Replacing the Design System

## 🚀 Quick Toggle Commands (NEW!)

```bash
/dmoff    # Turn OFF design system - instant freedom!
/dmon     # Turn ON design system - back to strict mode
/dm       # Check current status
```

That's it! No scripts, no terminal, just instant toggle in Claude Code.

## Overview

The Claude Code Boilerplate enforces a strict design system (4 font sizes, 2 weights, 4px grid) to ensure consistency. However, you may want to:
- Use your own design tokens
- Match an existing design from Figma/screenshots
- Use shadcn/ui, Tailwind UI, or other systems
- Have more flexibility for creative projects

This guide shows you how to customize or disable the design system while maintaining the benefits of the boilerplate.

## Quick Disable (5 seconds)

```bash
# Disable design enforcement entirely
mv .claude/hooks/pre-tool-use/02-design-check.py .claude/hooks/pre-tool-use/02-design-check.py.disabled

# Also disable in CodeRabbit
echo "" > .coderabbit.yaml
```

Now you can use any Tailwind classes or design system you want!

## Option 1: Customize the Existing System

### Modify Design Tokens

Edit `.claude/hooks/config.json`:

```json
{
  "design_system": {
    "enforce": true,
    "auto_fix": false,  // Don't auto-fix, just warn
    "allowed_font_sizes": [
      // Your custom sizes
      "text-xs", "text-sm", "text-base", "text-lg", 
      "text-xl", "text-2xl", "text-3xl", "text-4xl"
    ],
    "allowed_font_weights": [
      // Your weights
      "font-light", "font-normal", "font-medium", 
      "font-semibold", "font-bold"
    ],
    "spacing_grid": null,  // Disable grid enforcement
    "min_touch_target": 40  // Or your preference
  }
}
```

### Update Tailwind Config

Edit `tailwind.config.js` to match your design:

```javascript
module.exports = {
  theme: {
    extend: {
      fontSize: {
        // Your custom scale
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        // ... etc
      },
      colors: {
        // Your brand colors
        'brand': {
          50: '#f0f9ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        }
      }
    }
  }
}
```

## Option 2: Use shadcn/ui

### Step 1: Disable Strict Enforcement

```bash
# Edit .claude/hooks/config.json
{
  "design_system": {
    "enforce": false  // Turn off
  }
}
```

### Step 2: Install shadcn/ui

```bash
# Initialize shadcn/ui
npx shadcn-ui@latest init

# Install components as needed
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add form
```

### Step 3: Update Component Templates

Edit `.claude/templates/boilerplate-templates.md` to use shadcn patterns:

```typescript
// Example Button component with shadcn
import { Button } from "@/components/ui/button"

export function MyComponent() {
  return (
    <Button variant="outline" size="lg">
      Click me
    </Button>
  )
}
```

### Step 4: Update AI Instructions

Add to `CLAUDE.md`:

```markdown
## Design System

We use shadcn/ui components. Always import from @/components/ui/:
- Use Button from "@/components/ui/button"
- Use Card from "@/components/ui/card"
- Follow shadcn/ui patterns and variants
- Use cn() utility for className merging
```

## Option 3: Match External Designs (Figma/Screenshots)

### For Figma Designs

1. Export design tokens from Figma
2. Create a custom config:

```javascript
// lib/design-tokens.js
export const tokens = {
  colors: {
    // From Figma
    primary: '#5B21B6',
    secondary: '#F59E0B',
    // etc
  },
  typography: {
    // From Figma
    'heading-1': {
      fontSize: '48px',
      lineHeight: '56px',
      fontWeight: 700,
    },
    // etc
  }
}
```

3. Generate Tailwind config from tokens:

```javascript
// scripts/generate-tailwind-from-figma.js
const tokens = require('./design-tokens');

// Convert Figma tokens to Tailwind config
// ... conversion logic
```

### For Screenshot Matching

When you need to match a specific design:

```bash
# Tell Claude to analyze and match
"I need to match this design [screenshot]. Please:
1. Identify the design patterns
2. Create matching Tailwind utilities
3. Update our design tokens"

# Claude will create custom utilities like:
.custom-hero-text {
  @apply text-[58px] leading-[1.1] font-[600] tracking-[-0.02em];
}
```

## Option 4: Flexible Creative Mode

For projects that need maximum flexibility:

### 1. Create a "Creative Mode" Config

```bash
# .claude/config-creative.json
{
  "design_system": {
    "enforce": false
  },
  "hooks": {
    "pre-tool-use": [
      // Only keep critical hooks
      {
        "script": "07-pii-protection.py",
        "enabled": true
      }
    ]
  }
}
```

### 2. Switch Modes with Commands

Create `.claude/commands/creative-mode.md`:

```markdown
---
command: creative-mode
alias: [cm, flex]
---

# Creative Mode Toggle

Switches between strict and creative modes.

## Usage
- `/creative-mode on` - Disable design restrictions
- `/creative-mode off` - Re-enable strict mode

## Implementation
```bash
if [ "$1" = "on" ]; then
  cp .claude/config-creative.json .claude/config.json
  echo "🎨 Creative mode enabled - design freely!"
else
  cp .claude/config-strict.json .claude/config.json
  echo "📐 Strict mode enabled - design system enforced"
fi
```
```

## Option 5: Hybrid Approach (Recommended)

Keep the structure but add flexibility:

### 1. Core System + Extensions

```json
// .claude/hooks/config.json
{
  "design_system": {
    "enforce": true,
    "strict_paths": ["components/ui/", "app/"],  // Enforce here
    "flexible_paths": ["app/marketing/", "app/landing/"],  // Flexible here
    "allowed_font_sizes": [
      // Core system
      "text-size-1", "text-size-2", "text-size-3", "text-size-4",
      // Extensions for special cases
      "text-[58px]", "text-[72px]"  // Custom values allowed
    ]
  }
}
```

### 2. Component Variants

```typescript
// Allow both strict and flexible variants
export function Heading({ 
  variant = 'strict',
  className,
  children 
}: {
  variant?: 'strict' | 'creative'
  className?: string
  children: React.ReactNode
}) {
  if (variant === 'creative') {
    // Full flexibility
    return <h1 className={className}>{children}</h1>
  }
  
  // Strict system
  return <h1 className="text-size-1 font-semibold">{children}</h1>
}
```

## Fallback Options

If you disable the design system, you can use:

### 1. **Standard Tailwind CSS**
- All utilities available
- No restrictions
- Use Tailwind UI components

### 2. **shadcn/ui** (Recommended)
- Beautiful components
- Highly customizable
- Great DX with TypeScript

### 3. **Custom CSS/CSS Modules**
```css
/* styles/custom.module.css */
.heroTitle {
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 800;
  letter-spacing: -0.02em;
}
```

### 4. **CSS-in-JS** (Emotion/Stitches)
```typescript
import { styled } from '@emotion/styled'

const HeroTitle = styled.h1`
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 800;
`
```

## Migration Path

To migrate from strict to flexible:

```bash
# 1. Backup current config
cp .claude/hooks/config.json .claude/hooks/config-strict.json

# 2. Disable enforcement
# Edit config.json: "enforce": false

# 3. Update your components gradually
# The old classes still work!

# 4. Update AI instructions
# Add your new patterns to CLAUDE.md
```

## Best Practices

### When to Keep Strict Mode
- Team projects needing consistency
- Design system already defined
- Accessibility is critical
- Building a component library

### When to Use Flexible Mode
- Creative/marketing pages
- Matching external designs
- Rapid prototyping
- Personal projects

### Hybrid Recommendations
1. Keep strict mode for core UI components
2. Allow flexibility in:
   - Landing pages
   - Marketing sections
   - Blog/content areas
   - Experimental features

## Commands for Design Work

```bash
# Analyze a design
/analyze-design [screenshot/figma]

# Generate matching utilities
/match-design [url]

# Switch modes
/creative-mode on
/strict-mode on

# Check current mode
/design-status
```

## Conclusion

The boilerplate's design system is a starting point, not a prison. You can:
- Disable it completely (5 seconds)
- Customize it to match your needs
- Use shadcn/ui or any other system
- Create hybrid approaches
- Switch modes per context

The key is maintaining the OTHER benefits:
- Command system
- PRD workflow  
- Context persistence
- Team coordination
- Security features

The design system is just one hook - everything else still works perfectly!
