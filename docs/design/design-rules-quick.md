# FreshSlate Design Rules for AI Coding

## 🚨 MUST FOLLOW RULES

### 1. Typography: 4 Sizes, 2 Weights ONLY
```css
/* ONLY these font sizes */
text-size-1: 32px (28px mobile)  /* Large headings */
text-size-2: 24px (20px mobile)  /* Subheadings */
text-size-3: 16px                /* Body text */
text-size-4: 12px                /* Small text */

/* ONLY these weights */
font-semibold: 600               /* Headers, CTAs */
font-regular: 400                /* Everything else */
```

### 2. Spacing: 4px Grid System
```css
/* ALL spacing divisible by 4 */
✅ USE: 4px, 8px, 12px, 16px, 20px, 24px, 32px, 48px
❌ AVOID: 5px, 10px, 15px, 18px, 25px, 30px

/* Tailwind mapping */
p-1 = 4px    gap-1 = 4px    m-1 = 4px
p-2 = 8px    gap-2 = 8px    m-2 = 8px
p-3 = 12px   gap-3 = 12px   m-3 = 12px
p-4 = 16px   gap-4 = 16px   m-4 = 16px
p-6 = 24px   gap-6 = 24px   m-6 = 24px
p-8 = 32px   gap-8 = 32px   m-8 = 32px
```

### 3. Color Distribution: 60/30/10 Rule
- **60%** Neutral (white, gray-50 backgrounds)
- **30%** Text/UI (gray-700, borders, icons)
- **10%** Accent (blue CTAs, green success, red warnings)

### 4. Mobile-First Requirements
- Minimum touch targets: **44px** (h-11)
- Preferred touch targets: **48px** (h-12)
- Minimum body text: **16px**
- Adequate spacing between tappable elements

## 🎨 Color Usage

### Semantic Colors
```jsx
/* Income/Positive */
bg-green-50 border-green-300 text-green-700

/* Expenses/Negative */
bg-red-50 border-red-200 text-red-700

/* Primary CTAs */
bg-blue-600 hover:bg-blue-700 text-white

/* Secondary CTAs */
bg-gray-800 hover:bg-gray-900 text-white

/* Disabled */
bg-gray-200 text-gray-400 cursor-not-allowed
```

## 📐 Component Patterns

### Standard Container
```jsx
<div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
  <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-6">
    {/* Content */}
  </div>
</div>
```

### Standard Button
```jsx
<button className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 
  bg-blue-600 text-white hover:bg-blue-700 transition-all">
  Continue
</button>
```

### Standard Input
```jsx
<input
  type="text"
  className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl 
  focus:border-blue-500 focus:outline-none transition-colors"
/>
```

### Standard Card
```jsx
<div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
  {/* Content */}
</div>
```

## ✅ Quick Validation Checklist

Before committing any component:
- [ ] Uses only 4 font sizes?
- [ ] Uses only semibold (600) or regular (400) weights?
- [ ] All spacing divisible by 4?
- [ ] Follows 60/30/10 color distribution?
- [ ] Touch targets at least 44px tall?
- [ ] Body text at least 16px?

## 🚫 Common Violations to Flag

```jsx
/* ❌ WRONG - Too many font sizes */
text-sm text-base text-lg text-xl text-2xl text-3xl

/* ✅ RIGHT - Only 4 sizes */
text-size-1 text-size-2 text-size-3 text-size-4

/* ❌ WRONG - Wrong font weights */
font-light font-medium font-bold

/* ✅ RIGHT - Only 2 weights */
font-regular font-semibold

/* ❌ WRONG - Not on 4px grid */
p-5 gap-7 m-10

/* ✅ RIGHT - On 4px grid */
p-4 gap-6 m-8
```

## 📍 Quick Reference Links

- Full design system: `docs/design-system.md`
- Component examples: See design system Components section
- Animation patterns: See design system Animation section
- For complex questions: Reference the full design system