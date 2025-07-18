# Boilerplate Error Fixes Documentation

## Common Errors and Solutions

### 1. Missing Module: recursive-copy

**Error**: `Cannot find module '../lib/recursive-copy'`

**Solution**: Install as dev dependency
```bash
pnpm add -D recursive-copy
```

### 2. Analytics Store Missing Methods

**Error**: `Property 'initialize' does not exist on type 'AnalyticsStore'`

**Fixed by**: Updated `/stores/analytics-store.ts` with complete implementation including:
- `initialize()` - Initialize analytics SDK
- `trackPageView()` - Track page views
- `trackConversion()` - Track conversions
- Event queue integration for non-blocking tracking

### 3. Form Store Missing Methods

**Error**: `Property 'updateField' does not exist on type`

**Fixed by**: Created `/stores/form-store.ts` with:
- `updateFormField()` - Update single field
- `updateMultipleFields()` - Update multiple fields
- `trackFieldInteraction()` - Track field events
- Event queue integration for field tracking

### 4. UI Component Import Errors

**Error**: `Cannot find module '@/components/ui/button'`

**Fixed by**: Created re-export file `/components/ui/button.tsx`
```typescript
export { Button } from './button-component';
```

### 5. CSS File Location

**Error**: `File does not exist: app/globals.css`

**Fixed by**: 
- Copied `styles/globals.css` to `app/globals.css`
- Updated import in `app/layout.tsx`

### 6. Lead Form Component Updates

**Fixed**: Updated `/components/forms/example-lead-form.tsx` to:
- Use correct store methods
- Integrate event tracking hooks
- Follow async patterns
- Track form interactions properly

## Architecture Patterns

### Event-Driven Analytics
```typescript
// Non-blocking tracking
eventQueue.emit('analytics.track', {
  event: 'Form Submit',
  properties: { formId: 'lead-form' }
});
```

### Form Event Tracking
```typescript
const { trackFormSubmit, trackSubmissionResult } = useLeadFormEvents('form-id');

const onSubmit = async (data) => {
  const startTime = await trackFormSubmit(data);
  try {
    await api.submit(data);
    trackSubmissionResult(true, startTime);
  } catch (error) {
    trackSubmissionResult(false, startTime);
  }
};
```

### Store Pattern
All stores follow this pattern:
```typescript
interface Store {
  // State
  data: any;
  
  // Actions
  updateData: (data: any) => void;
  
  // Event integration
  trackAction: (action: string) => void;
}
```

## Running the Fix Script

```bash
# Make executable
chmod +x scripts/fix-errors.sh

# Run fixes
./scripts/fix-errors.sh
```

## Verification

After applying fixes:
```bash
# Check types
pnpm typecheck

# Run linter
pnpm lint

# Start dev server
pnpm dev
```

## Design System Compliance

Remember the boilerplate enforces:
- Font sizes: `text-size-[1-4]` only
- Font weights: `font-regular`, `font-semibold` only
- Spacing: 4px grid (p-1, p-2, p-3, p-4, p-6, p-8)
- Touch targets: minimum 44px (h-11)

## Event Queue Benefits

1. **Non-blocking**: Analytics never slow down forms
2. **Retry logic**: Failed events retry automatically
3. **Timeout protection**: All calls have 5s timeout
4. **Priority handling**: Critical events process first

## Next Steps

1. Run the fix script
2. Verify no TypeScript errors remain
3. Test form submission flow
4. Check analytics tracking
5. Deploy with confidence
