# Extract Style from Reference

Extract design tokens from reference images or URLs to maintain brand consistency.

## Usage
```bash
/extract-style [source]
/es [source]

# Sources:
- Image file path
- Dribbble URL
- Behance URL
- Any website URL
```

## What It Does

1. **Analyzes Reference**
   - Extracts color palette
   - Identifies typography patterns
   - Detects spacing rhythm
   - Notes shadow/border styles

2. **Maps to Design System**
   ```typescript
   // Extracted style mapped to your constraints:
   {
     // Colors (respecting 60/30/10 rule)
     primary: "blue-600",      // 10%
     background: "white",      // 60%
     text: "gray-700",        // 30%
     
     // Typography (mapped to your 4 sizes)
     heading: "text-size-1 font-semibold",
     subheading: "text-size-2 font-semibold",
     body: "text-size-3 font-regular",
     caption: "text-size-4 font-regular",
     
     // Spacing (snapped to 4px grid)
     compact: "p-2 gap-2",
     default: "p-4 gap-4", 
     spacious: "p-6 gap-6",
     
     // Effects
     shadow: "shadow-lg",
     radius: "rounded-xl",
     border: "border-gray-200"
   }
   ```

3. **Generates Style Config**
   - Compatible with Tailwind
   - Enforces your constraints
   - Ready to use in components

## Examples

### From Dribbble Shot
```bash
/extract-style https://dribbble.com/shots/123456

# Output:
Style extracted and mapped to design system:
- Primary: indigo-600 (was #5046E5)
- Text sizes: Maintained 4-tier system
- Spacing: Aligned to 4px grid
- Saved to: styles/extracted-theme.json
```

### From Local Image
```bash
/extract-style ./design-mockup.png

# Analyzes image and creates:
styles/
└── mockup-theme.json
```

### Integration with Component Creation
```bash
# Extract style first
/extract-style https://example.com/beautiful-ui

# Then use in component
/cc ui Card --style=extracted-theme
```

## Why This is Better Than SuperDesign's Approach

1. **Enforces Your Rules** - Maps to YOUR design system, not arbitrary CSS
2. **Maintains Consistency** - Can't break 4 sizes, 2 weights rule
3. **Prevents AI-ish UI** - By starting with real design references
4. **Version Controlled** - Themes saved as JSON files

## Limitations

- Won't extract styles that violate your system
- Automatically snaps to nearest valid values
- Focuses on tokens, not pixel-perfect copying

This gives you the style extraction benefit without compromising your design system integrity.
