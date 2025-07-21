# Project Knowledge Base

## Project Overview

[Project name and description - what does this application do?]

## Design System Files

1. **docs/design-system.md** - Complete design system documentation
2. **DESIGN_RULES.md** - Quick reference for developers
3. **project-instructions.md** - AI coding assistant commands
4. **project-snippets.json** - VS Code snippets
5. **tailwind-tokens.js** - Design tokens for Tailwind config

## Critical Design Constraints

### 1. Typography: 4 Sizes, 2 Weights ONLY
- **Sizes**: text-size-1 (32px), text-size-2 (24px), text-size-3 (16px), text-size-4 (12px)
- **Weights**: font-regular (400), font-semibold (600)
- **NO OTHER SIZES OR WEIGHTS ALLOWED**

### 2. Spacing: 4px Grid System
- All spacing must be divisible by 4
- Use: 4px, 8px, 12px, 16px, 20px, 24px, 32px, 48px
- Never use: 5px, 10px, 15px, 18px, 25px, 30px, etc.

### 3. Color Distribution: 60/30/10 Rule
- 60% Neutral (backgrounds)
- 30% Text/UI elements
- 10% Accent colors (CTAs, warnings)

### 4. Mobile-First Requirements
- Minimum touch targets: 44px (h-11)
- Preferred touch targets: 48px (h-12)
- Minimum body text: 16px
- Test everything on mobile first

## Component Architecture

### Core Components
1. **Container** - Centered, responsive, proper padding
2. **Cards** - Consistent borders, spacing, shadows
3. **Buttons** - Standard heights, proper touch targets
4. **Forms** - Progressive disclosure, mobile-friendly
5. **Navigation** - Accessible, thumb-friendly

### State Management
- React useState for local state
- Context for global state
- URL params for shareable state
- Session storage for temporary data

## Business Logic

[Link to separate business logic document]

### Core Features
1. [Feature 1 description]
2. [Feature 2 description]
3. [Feature 3 description]

### User Flows
1. [Primary user flow]
2. [Secondary user flow]
3. [Edge cases]

## Technical Patterns

### API Structure
```typescript
// Standard API response format
{
  success: boolean;
  data?: any;
  error?: string;
  metadata?: {
    timestamp: string;
    version: string;
  };
}
```

### Error Handling
- User-friendly error messages
- Proper error logging
- Fallback UI states
- Recovery mechanisms

### Performance Requirements
- Page load < 3s
- Time to Interactive < 5s
- Core Web Vitals passing
- Bundle size < 300KB

## Common Patterns

### Standard Layout
```jsx
<div className="min-h-screen bg-gray-50">
  <div className="max-w-md mx-auto p-4">
    {/* Content */}
  </div>
</div>
```

### Standard Card
```jsx
<div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
  <h3 className="text-size-2 font-semibold">Title</h3>
  <p className="text-size-3 font-regular">Content</p>
</div>
```

### Standard Button
```jsx
<button className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 
  bg-primary-600 text-white hover:bg-primary-700 transition-all">
  Action
</button>
```

## Validation Checklist

Before any code review or commit:
- [ ] Only 4 font sizes used?
- [ ] Only 2 font weights used?
- [ ] All spacing divisible by 4?
- [ ] Following 60/30/10 color rule?
- [ ] Touch targets at least 44px?
- [ ] Works on mobile?

## File Structure

```
project-name/
├── docs/
│   ├── design-system.md
│   ├── DESIGN_RULES.md
│   └── PROJECT_KNOWLEDGE.md
├── components/
│   ├── ui/
│   └── features/
├── lib/
│   ├── utils/
│   └── api/
└── app/
    ├── (public)/
    └── (protected)/
```

## Key Technologies

- **React** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Animations
- **Zod** - Validation
- **React Hook Form** - Form management

## Integration Notes

### When Using External Components
1. Adjust spacing to 4px grid
2. Replace typography with 4-size system
3. Update colors to match semantic system
4. Ensure mobile-first approach

### When Adding New Features
1. Follow existing patterns
2. Maintain design system consistency
3. Test on mobile first
4. Add proper error handling

## Remember

Every design decision should:
1. Improve user experience
2. Maintain consistency
3. Work on mobile
4. Follow the design system
5. Be accessible

The design system is not just about aesthetics—it's about creating a consistent, trustworthy experience that works for all users.