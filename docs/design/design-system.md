# Universal Design System

## Table of Contents
1. [Design Philosophy](#design-philosophy)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [Components](#components)
6. [Icons](#icons)
7. [Animation & Transitions](#animation--transitions)
8. [Mobile Considerations](#mobile-considerations)
9. [Implementation Recommendations](#implementation-recommendations)

---

## Design Philosophy

### Core Principles
- **User Journey**: Guide users through clear, purposeful flows
- **Visual Hierarchy**: Clear distinction between primary, secondary, and tertiary elements
- **Progressive Disclosure**: One decision at a time to reduce cognitive load
- **Trust Building**: Professional yet approachable, clean but not sterile

### User Psychology
- **Color Psychology**: Use color purposefully to guide actions
- **Progress Indication**: Always show where users are in a flow
- **Immediate Feedback**: Visual responses to every interaction
- **Mobile-First**: Thumb-friendly targets, no horizontal scrolling

---

## Color System

### Color Philosophy & Perception

#### Five Guiding Principles for Color Choice

1. **Color is Personal**
   - Avoid pop psychology associations
   - Consider color vision deficiency (~8% of men, ~0.5% of women)
   - Test with accessibility tools

2. **Color is Contextual**
   - Colors mean different things in different contexts
   - Be consistent within your application
   - Test in real-world lighting conditions

3. **Color is Connotative**
   - Colors communicate about the product itself
   - Choose colors that align with your brand values
   - Consider industry expectations

4. **Color is Relational**
   - Color combinations create associations
   - Consider contrast and harmony
   - Use color relationships to guide hierarchy

5. **Color is Cultural**
   - Be aware of cultural color meanings
   - Test with diverse user groups
   - Provide alternatives when needed

#### Mobile-First Color Strategy

**Warm vs Cool Colors:**
- Warm colors (red, orange, yellow) naturally stand out - perfect for CTAs
- Cool colors (blue, green, purple) recede - ideal for backgrounds
- On mobile's limited space, use warm colors sparingly for maximum impact

**60-30-10 Rule for Mobile:**
- **60% Neutral** (white, light gray backgrounds)
- **30% Primary** (text, borders, UI elements)
- **10% Accent** (CTAs, alerts, highlights)

### Primary Palette

```css
/* Primary Brand Colors */
--primary-50: #eff6ff;
--primary-100: #dbeafe;
--primary-200: #bfdbfe;
--primary-300: #93c5fd;
--primary-400: #60a5fa;
--primary-500: #3b82f6;
--primary-600: #2563eb;  /* Main CTA */
--primary-700: #1d4ed8;
--primary-800: #1e40af;
--primary-900: #1e3a8a;

/* Success Colors */
--success-50: #f0fdf4;
--success-100: #dcfce7;
--success-200: #bbf7d0;
--success-300: #86efac;
--success-400: #4ade80;
--success-500: #22c55e;
--success-600: #16a34a;  /* Success primary */
--success-700: #15803d;
--success-800: #166534;
--success-900: #14532d;

/* Warning/Error Colors */
--error-50: #fef2f2;
--error-100: #fee2e2;
--error-200: #fecaca;
--error-300: #fca5a5;
--error-400: #f87171;
--error-500: #ef4444;
--error-600: #dc2626;  /* Error primary */
--error-700: #b91c1c;
--error-800: #991b1b;
--error-900: #7f1d1d;

/* Neutral Colors */
--neutral-50: #f9fafb;
--neutral-100: #f3f4f6;
--neutral-200: #e5e7eb;
--neutral-300: #d1d5db;
--neutral-400: #9ca3af;
--neutral-500: #6b7280;
--neutral-600: #4b5563;
--neutral-700: #374151;
--neutral-800: #1f2937;
--neutral-900: #111827;
```

### Semantic Color Usage

#### Color Distribution Table

| Context | Background (60%) | Text/UI (30%) | Accent (10%) |
|---------|------------------|---------------|--------------|
| Default Screen | neutral-50 | neutral-700 | primary-600 |
| Success State | success-50 | neutral-700 | success-600 |
| Error State | error-50 | neutral-700 | error-600 |
| Interactive | white | neutral-700 | primary-600 |

---

## Typography

### Mobile-First Typography Philosophy

Typography commands 80% of user attention. On mobile, legibility is paramount.

### Simplified Typography System: 4 Sizes, 2 Weights

#### **4 Font Sizes Only**
```css
/* Size 1: Large headings/displays */
--text-size-1: 32px;    /* 8 grid units - Major headers */
--text-size-1-mobile: 28px;  /* Responsive adjustment */

/* Size 2: Subheadings/Important content */
--text-size-2: 24px;    /* 6 grid units - Section headers */
--text-size-2-mobile: 20px;  /* Responsive adjustment */

/* Size 3: Body text (base) */
--text-size-3: 16px;    /* 4 grid units - Default text */
--text-size-3-mobile: 16px;  /* Minimum legible */

/* Size 4: Small text/labels */
--text-size-4: 12px;    /* 3 grid units - Captions, hints */
--text-size-4-mobile: 12px;  /* Minimum size */
```

#### **2 Font Weights Only**
```css
/* Semibold: Headers and emphasis */
--font-semibold: 600;

/* Regular: Body text and general content */
--font-regular: 400;

/* NO OTHER WEIGHTS - This creates visual consistency */
```

### Implementation Examples

```css
/* Headers (Size 1, Semibold) */
.header-primary {
  font-size: var(--text-size-1-mobile);
  font-weight: var(--font-semibold);
  line-height: 1.25;
}

/* Subheadings (Size 2, Semibold) */
.header-secondary {
  font-size: var(--text-size-2-mobile);
  font-weight: var(--font-semibold);
  line-height: 1.375;
}

/* Body text (Size 3, Regular) */
.body-text {
  font-size: var(--text-size-3);
  font-weight: var(--font-regular);
  line-height: 1.5;
}

/* Labels (Size 4, Regular) */
.label-text {
  font-size: var(--text-size-4);
  font-weight: var(--font-regular);
  line-height: 1.5;
  letter-spacing: 0.025em;
}
```

### Font Selection

**Primary Font: Sans-serif**
```css
--font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
             "Helvetica Neue", Arial, sans-serif;
```

---

## Spacing & Layout

### Grid System - The Four Pixel Rule

#### Base Grid: 4px
```css
/* Base unit */
--grid-unit: 4px;

/* Grid multipliers */
--grid-0: 0;                    /* 0px */
--grid-1: calc(1 * 4px);        /* 4px */
--grid-2: calc(2 * 4px);        /* 8px */
--grid-3: calc(3 * 4px);        /* 12px */
--grid-4: calc(4 * 4px);        /* 16px */
--grid-5: calc(5 * 4px);        /* 20px */
--grid-6: calc(6 * 4px);        /* 24px */
--grid-7: calc(7 * 4px);        /* 28px */
--grid-8: calc(8 * 4px);        /* 32px */
--grid-9: calc(9 * 4px);        /* 36px */
--grid-10: calc(10 * 4px);      /* 40px */
--grid-11: calc(11 * 4px);      /* 44px - Min touch target */
--grid-12: calc(12 * 4px);      /* 48px - Preferred touch */
--grid-16: calc(16 * 4px);      /* 64px */
--grid-20: calc(20 * 4px);      /* 80px */
--grid-24: calc(24 * 4px);      /* 96px */
```

#### Spacing Hierarchy

```css
/* Spacing between elements */
--spacing-xs: var(--grid-1);      /* 4px - Icon to text */
--spacing-sm: var(--grid-2);      /* 8px - List items */
--spacing-md: var(--grid-4);      /* 16px - Standard spacing */
--spacing-lg: var(--grid-6);      /* 24px - Between sections */
--spacing-xl: var(--grid-8);      /* 32px - Major sections */
--spacing-2xl: var(--grid-12);    /* 48px - Page sections */
```

### Container Widths
```css
--max-width-xs: 320px;   /* Minimum phone */
--max-width-sm: 384px;   /* Standard phone */
--max-width-md: 448px;   /* Large phone */
--max-width-lg: 512px;   /* Tablet */
--max-width-xl: 640px;   /* Small desktop */
```

### Border Radius
```css
--radius-sm: 4px;        /* 1 grid unit */
--radius-md: 8px;        /* 2 grid units - Default */
--radius-lg: 12px;       /* 3 grid units - Cards */
--radius-xl: 16px;       /* 4 grid units - Large cards */
--radius-2xl: 24px;      /* 6 grid units - Container */
--radius-full: 9999px;   /* Pills, circles */
```

---

## Components

### Component Architecture

#### 2-Layer Architecture
1. **Structure Layer**: HTML structure and state management
2. **Style Layer**: Tailwind CSS utilities following design system

#### Component Principles
- **Single Responsibility**: Each component has one clear purpose
- **Consistent Spacing**: All components use the 4px grid
- **Predictable Behavior**: Similar components behave similarly
- **Mobile-First**: Designed for touch interaction

### Standard Components

#### Button
```jsx
<button className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 
  bg-primary-600 text-white hover:bg-primary-700 transition-all">
  Continue
</button>
```

#### Input
```jsx
<input
  type="text"
  className="w-full h-12 px-4 border-2 border-neutral-200 rounded-xl 
  focus:border-primary-500 focus:outline-none transition-colors"
/>
```

#### Card
```jsx
<div className="bg-white border border-neutral-200 rounded-xl p-4 space-y-3">
  <h3 className="text-size-2 font-semibold">Title</h3>
  <p className="text-size-3 font-regular">Content</p>
</div>
```

---

## Icons

### Icon Library: Lucide React
Chosen for consistency, tree-shaking, and mobile optimization.

### Icon Usage Guidelines
- Default size: w-5 h-5 (20px)
- Always pair with text for accessibility
- Use consistent sizing within contexts
- Match icon color to context

### Common Icons
| Purpose | Icon | Size |
|---------|------|------|
| Navigation | `ChevronRight` | w-5 h-5 |
| Success | `CheckCircle` | w-5 h-5 |
| Error | `AlertCircle` | w-5 h-5 |
| Warning | `AlertTriangle` | w-4 h-4 |
| Close | `X` | w-6 h-6 |
| Menu | `Menu` | w-6 h-6 |

---

## Animation & Transitions

### Timing Functions
```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Standard Transitions
```css
/* Default transition */
transition: all 0.2s ease-out;

/* Color transitions */
transition: background-color 0.2s ease-out, 
            border-color 0.2s ease-out,
            color 0.2s ease-out;

/* Transform transitions */
transition: transform 0.2s ease-out;
```

### Animation Classes
```css
@keyframes fadeIn {
  from { 
    opacity: 0; 
    transform: translateY(10px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
```

---

## Mobile Considerations

### Touch Targets
- Minimum 44x44px (Apple HIG)
- Prefer 48x48px for primary actions
- 8px minimum spacing between targets

### Mobile-Specific Styles
```css
/* Prevent zoom on input focus (iOS) */
input, textarea, select {
  font-size: 16px;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Prevent text selection on buttons */
button {
  -webkit-user-select: none;
  user-select: none;
}
```

### Responsive Breakpoints
```css
--breakpoint-sm: 640px;   /* Larger phones */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Small laptops */
--breakpoint-xl: 1280px;  /* Desktops */
```

---

## Implementation Guidelines

### Component Development Process

1. **Start with Structure**: Define HTML/JSX structure first
2. **Apply Typography**: Use only the 4 sizes and 2 weights
3. **Add Spacing**: Ensure all values divisible by 4
4. **Apply Colors**: Follow 60/30/10 distribution
5. **Test Interaction**: Verify touch targets and states

### Code Review Checklist

- [ ] Typography: Uses only 4 font sizes and 2 font weights
- [ ] Spacing: All values divisible by 4
- [ ] Colors: Follows 60/30/10 distribution
- [ ] Touch targets minimum 44px
- [ ] Text minimum 16px for body content
- [ ] Consistent component patterns

### Common Issues to Flag
- ❌ More than 4 font sizes in use
- ❌ Font weights other than 600 and 400
- ❌ Spacing values not divisible by 4
- ❌ Overuse of accent colors (exceeding 10%)
- ❌ Touch targets under 44px
- ❌ Text under 16px for important content

---

This design system provides a scalable, accessible, and performant foundation for modern web applications. All components are designed for consistency and ease of use.