# Project AI Assistant Knowledge Base

## About This Project

[Project description - what does this application do?]

## Core Concepts

### 1. User Journey Flow
```
User Journey:
Landing Page → Interactive Flow → Data Capture → Processing → Results
```

### 2. Key Metrics
- **Conversion Rate**: Completions / Page views
- **Engagement Rate**: Interactions / Sessions
- **Completion Rate**: Successful submissions / Started
- **Performance**: Page load times, Core Web Vitals

### 3. Technology Stack
- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind CSS
- **Analytics**: RudderStack CDP, Custom attribution
- **Forms**: React Hook Form + Zod validation
- **Animation**: Framer Motion
- **Deployment**: Vercel
- **Database**: Supabase (PostgreSQL)

## Common Implementation Tasks

### Creating a New Page
```typescript
// Standard page structure
app/
├── [page-name]/
│   ├── page.tsx          // Main page
│   ├── components/       // Page-specific components
│   └── layout.tsx        // Optional layout
```

### Implementing Data Capture
```typescript
// Always include these core fields
interface UserData {
  // Required
  id: string;
  email: string;
  createdAt: Date;
  
  // Attribution (automatic)
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  referrer?: string;
  
  // Compliance
  consent: boolean;
  ip_address: string;
  timestamp: string;
}
```

### Analytics Implementation
```typescript
// Track these events minimum
track('Page Viewed', { page_name, page_path });
track('Flow Started', { flow_type });
track('Flow Completed', { completion_status });
track('Data Captured', { record_id });
track('Action Taken', { action_type });
```

## Design System Rules

### Typography (4 Sizes, 2 Weights)
```css
text-size-1: 32px;  /* Headings */
text-size-2: 24px;  /* Subheadings */
text-size-3: 16px;  /* Body */
text-size-4: 12px;  /* Small */

font-regular: 400;
font-semibold: 600;
```

### Spacing (4px Grid)
```css
✅ Use: 4px, 8px, 12px, 16px, 24px, 32px, 48px
❌ Avoid: 5px, 10px, 15px, 18px, 25px, 30px
```

### Colors (60/30/10 Rule)
- 60% Neutral (backgrounds)
- 30% Text/UI elements  
- 10% Accent (CTAs, alerts)

## API Patterns

### Data Submission
```typescript
POST /api/submissions
{
  "data": { ...userInput },
  "attribution": { utm_*, referrer },
  "consent": { agreed: true, timestamp }
}

Response:
{
  "id": "uuid",
  "status": "success|error",
  "data": { ...processedData }
}
```

### State Management
```typescript
// Use URL params for state persistence
/flow?step=1&data=encoded

// Or session storage for sensitive data
sessionStorage.setItem('flow_progress', JSON.stringify(state));
```

## Common Patterns

### Progressive Disclosure
```typescript
// Step 1: Low-friction data
const step1Fields = ['basicInfo'];

// Step 2: Detailed data  
const step2Fields = ['additionalInfo'];

// Step 3: Contact info (only if needed)
const step3Fields = ['email', 'phone'];
```

### Mobile-First Implementation
```typescript
// Always test at 375px width first
// Minimum touch targets: 44px
// Use thumb-friendly bottom navigation
// Single column layouts preferred
```

### Error Handling
```typescript
try {
  const result = await submitData(data);
  track('Success', result);
} catch (error) {
  track('Error', { 
    error: error.message,
    context: sanitize(data) 
  });
  showUserFriendlyError();
}
```

## Compliance Requirements

### Consent Management
```jsx
<label className="flex items-start gap-3">
  <input type="checkbox" required />
  <span className="text-size-4 text-gray-600">
    By clicking submit, you agree to our terms and conditions
    and privacy policy.
  </span>
</label>
```

### Required Elements
- Privacy Policy link
- Terms of Service link
- Cookie consent (if applicable)
- Data processing disclosure

## Testing Checklist

Before deploying any feature:
```
□ Mobile responsive (375px minimum)
□ Forms validate properly
□ Analytics events fire
□ Attribution captured
□ Error handling works
□ Page speed < 3s
□ Accessibility scan passes
□ Legal requirements met
□ Consent functioning
□ Success tracking works
```

## Debugging Tips

### Check Attribution
```javascript
// In browser console
console.log(sessionStorage.getItem('tracking_params'));
console.log(document.cookie);
```

### Verify Analytics
```javascript
// Enable debug mode
localStorage.setItem('analytics_debug', 'true');
window.location.reload();
```

### Test Form Submission
```javascript
// Bypass validation for testing
document.querySelector('form').noValidate = true;
```

## Common Mistakes to Avoid

1. **Using wrong typography**: Only 4 sizes, 2 weights
2. **Breaking the grid**: All spacing divisible by 4
3. **Forgetting attribution**: Always capture URL params
4. **Missing analytics**: Track every significant action
5. **Poor mobile UX**: Test on real devices
6. **Slow page load**: Optimize images and bundles
7. **Complex forms**: Progressive capture is better
8. **No error handling**: Users need feedback
9. **Missing compliance**: Check legal requirements
10. **Not testing**: Always QA before launch

## Quick Reference

### File Locations
- Design system: `docs/design/design-system.md`
- Components: `components/ui/`
- Analytics: `lib/analytics.ts`
- Forms: `components/forms/`
- API routes: `app/api/`

### Environment Variables
```env
NEXT_PUBLIC_ANALYTICS_KEY=
NEXT_PUBLIC_API_URL=
DATABASE_URL=
```

### Useful Commands
```bash
# Create new page
npm run create:page [name]

# Test mobile view
npm run dev -- --host

# Check bundle size
npm run analyze

# Run tests
npm test
```

---

When building features, always prioritize:
1. **User Experience**: Every element should have purpose
2. **Performance**: Fast loads increase engagement
3. **Mobile UX**: Most traffic is mobile
4. **Analytics**: Track everything for optimization
5. **Accessibility**: Build for everyone