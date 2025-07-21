# FreshSlate Project Knowledge Base

## Project Overview

FreshSlate is a financial wellness quiz application that helps users understand their debt situation and connects them with debt resolution partners. The quiz creates an emotional journey from financial anxiety to hope and action.

## Design System Files

1. **docs/design-system.md** - Complete design system documentation
2. **DESIGN_RULES.md** - Quick reference for developers
3. **claude-code-instructions.md** - AI coding assistant commands
4. **freshslate-snippets.json** - VS Code snippets
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
1. **Quiz Container** - Centered, max-w-md, white background
2. **Quiz Steps** - Single question per screen, clear progression
3. **Input Types** - Sliders, button grids, yes/no choices
4. **Report Cards** - Income (green), expenses (gray), warnings (red)
5. **CTAs** - Primary (blue), income (green), disabled (gray)

### State Management
- React useState for form data
- Step-based navigation
- Validation before progression
- Calculations for financial analysis

## Semantic Color Usage

### Income/Positive
- Background: bg-green-50
- Border: border-green-300
- Text: text-green-700
- Icon: text-green-600

### Expenses/Negative
- Background: bg-red-50
- Border: border-red-200
- Text: text-red-700
- Icon: text-red-600

### Primary Actions
- Background: bg-blue-600
- Hover: hover:bg-blue-700
- Text: text-white

## Animation Patterns

### Micro-interactions (100-200ms)
- Button hovers
- Input focus states
- Ripple effects

### Transitions (300-500ms)
- Step changes
- Card reveals
- Progress updates

### Celebrations (one-time)
- Confetti for positive outcomes
- Success pulses
- Achievement animations

## Common Patterns

### Standard Button
```jsx
<button className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 
  bg-blue-600 text-white hover:bg-blue-700 transition-all">
  Continue
</button>
```

### Standard Card
```jsx
<div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
  <h3 className="text-size-2 font-semibold">Title</h3>
  <p className="text-size-3 font-regular">Content</p>
</div>
```

### Grid Layout (3 columns)
```jsx
<div className="grid grid-cols-3 gap-2">
  {options.map(option => (
    <button key={option} className="h-12 px-3">
      {option}
    </button>
  ))}
</div>
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
freshslate/
├── docs/
│   ├── design-system.md
│   ├── DESIGN_RULES.md
│   └── PROJECT_KNOWLEDGE.md
├── components/
│   ├── quiz/
│   │   ├── QuizContainer.tsx
│   │   ├── QuizStep.tsx
│   │   └── QuizResults.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Card.tsx
│       └── Input.tsx
├── lib/
│   ├── design-tokens.ts
│   └── utils.ts
└── styles/
    └── globals.css
```

## Key Technologies

- **React** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Animations
- **Lucide React** - Icons

## Business Logic

### Debt Calculations
- Minimum payment: 2.5% of balance or $25 (whichever is greater)
- Average APR: 21.5% (current market rate)
- Monthly interest: Balance × (APR/12)

### Financial Health Grades
- **A**: DTI < 20%, positive cash flow
- **B**: DTI 20-36%, manageable
- **C**: DTI 36-43%, concerning
- **D**: DTI 43-50%, critical
- **F**: DTI > 50%, unsustainable

### Recommendations
- Under $5k debt: DIY or consolidation
- Over $25k debt: Professional debt resolution
- Homeowners: Consider HELOC
- Good credit: Balance transfer

## Integration Notes

### When Using Tailwind UI Components
1. Adjust spacing to 4px grid
2. Replace typography with 4-size system
3. Update colors to match semantic system
4. Ensure mobile-first approach

### When Using Shadcn Components
1. Override CSS variables
2. Simplify typography variants
3. Adjust to 4px grid
4. Maintain accessibility features

## Remember

This is a financial product dealing with sensitive user data and emotions. Every design decision should:
1. Build trust
2. Reduce anxiety
3. Provide clear next steps
4. Maintain professionalism
5. Work flawlessly on mobile

The design system is not just about aesthetics—it's about creating a consistent, trustworthy experience that guides users from financial stress to hope and action.