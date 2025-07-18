# Create Component with Wireframe - Enhanced

Create a new component with design system validation and optional ASCII wireframe step.

## Usage
```bash
/create-component [type] [name] [options]
/cc [type] [name] [options]

# Options:
--wireframe    # Start with ASCII wireframe
--style=ref    # Use reference image for style
--animate      # Include animation planning
```

## Enhanced Flow with Wireframe

### Step 1: ASCII Wireframe (Optional with --wireframe)

When using `--wireframe`, first generate a quick ASCII layout:

```
┌─────────────────────────────────┐
│ UserProfile Component           │
├─────────────────────────────────┤
│ ┌─────┐  Name: John Doe        │
│ │     │  Role: Developer        │
│ │ IMG │  ─────────────────      │
│ │     │  Bio text here...       │
│ └─────┘  spanning multiple      │
│          lines                  │
├─────────────────────────────────┤
│ [Edit Profile] [Settings]       │
└─────────────────────────────────┘
```

Benefits:
- Validate layout in 1 second
- Agree on structure before coding
- Show interactions (click → sidebar)

### Step 2: Apply Design System

After wireframe approval, generate with our strict rules:
- Font sizes: text-size-[1-4] only
- Font weights: font-regular, font-semibold only
- Spacing: 4px grid (p-1, p-2, p-3, etc.)
- Touch targets: minimum 44px (h-11)

### Step 3: Animation Planning (Optional with --animate)

Define micro-interactions:
```typescript
const animations = {
  hover: {
    trigger: "onMouseEnter",
    duration: "200ms",
    effect: "scale(1.02) + shadow-lg"
  },
  click: {
    trigger: "onClick", 
    duration: "150ms",
    effect: "scale(0.98)"
  }
};
```

### Step 4: Component Generation

Generate the actual component with all constraints applied.

## Examples

### Basic Component
```bash
/cc ui Button
```

### With Wireframe First
```bash
/cc ui Card --wireframe

# Shows ASCII:
┌──────────────────┐
│ ┌────┐           │
│ │IMG │ Title     │
│ └────┘ Subtitle  │
│ Description...   │
│ [Action]         │
└──────────────────┘

# Then generates component
```

### With Animation Planning
```bash
/cc feature ProductCard --animate

# Plans animations:
- Hover: lift with shadow
- Image: lazy load fade-in
- Button: press effect
```

### Complete Flow
```bash
/cc feature Dashboard --wireframe --animate

# 1. ASCII wireframe
# 2. Confirm layout
# 3. Apply design system
# 4. Plan animations
# 5. Generate component
```

## Integration with Existing Commands

Works with:
- `/vd` - Validates generated component
- `/orch` - Can use frontend agent
- Design hooks - Still enforce rules

## Why This Enhancement Works

1. **Faster Iteration** - ASCII in 1 second vs full component in 30 seconds
2. **Better Alignment** - Agree on layout before implementation
3. **Maintains Standards** - Still enforces your design system
4. **Optional** - Only use when helpful

This brings the best of SuperDesign's approach while maintaining your superior design system enforcement.
