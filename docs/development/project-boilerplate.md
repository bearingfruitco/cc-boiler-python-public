# Universal Project Boilerplate Instructions

## Project Setup

### Initial Context
```
You are building a modern web application using Next.js 15 and TypeScript.

ALWAYS follow these rules:
1. Mobile-first design (test everything on 375px width first)
2. Typography: ONLY 4 sizes (32px, 24px, 16px, 12px) and 2 weights (400, 600)
3. Spacing: ONLY values divisible by 4 (4px, 8px, 12px, 16px, etc.)
4. Colors: 60% neutral, 30% text/UI, 10% accent
5. Performance: Optimize for 3G connections
6. Accessibility: WCAG AA minimum

Tech stack:
- Next.js 15+ with App Router
- TypeScript (strict mode)
- Tailwind CSS
- Framer Motion for animations
- React Hook Form for forms
- Zod for validation
```

### Project Structure Template
```
project-name/
├── app/
│   ├── layout.tsx           # Root layout with analytics
│   ├── page.tsx            # Landing page
│   ├── (public)/           # Public routes
│   │   └── [pages]/
│   └── (protected)/        # Protected routes
│       └── [pages]/
├── components/
│   ├── analytics/
│   │   ├── Analytics.tsx   # Analytics wrapper
│   │   └── Providers.tsx   # Analytics providers
│   ├── forms/
│   │   └── [FormComponents]
│   └── ui/
│       └── [UIComponents]
├── lib/
│   ├── analytics.ts        # Analytics utilities
│   ├── cookies.ts          # Cookie management
│   ├── tracking.ts         # Tracking utilities
│   └── validation.ts       # Validation schemas
└── hooks/
    ├── useAnalytics.ts
    ├── useTracking.ts
    └── [customHooks]
```

### Standard Features Every Project Needs

1. **URL Parameter Capture**
   - UTM parameters (source, medium, campaign, term, content)
   - Custom parameters
   - Persist in session storage
   - Pass to forms

2. **Cookie Management**
   - Read tracking cookies
   - GDPR/CCPA compliant consent
   - First-party cookie fallbacks
   - Cross-domain tracking

3. **Analytics Events**
   - Page views
   - User interactions
   - Form submissions
   - Conversion tracking
   - Error tracking

4. **Form Standards**
   - Progressive data capture
   - Real-time validation
   - Auto-save progress
   - Mobile-optimized inputs

5. **Performance Requirements**
   - LCP < 2.5s
   - FID < 100ms
   - CLS < 0.1
   - Bundle size < 300KB

### Compliance Requirements

1. **Data Privacy**
   - Cookie consent banner
   - Privacy policy link
   - Opt-out mechanisms
   - Data retention policies

2. **Legal Compliance**
   - Required disclosures
   - Terms of service
   - Age verification (if needed)
   - Geographic restrictions

3. **Accessibility**
   - Keyboard navigation
   - Screen reader support
   - Focus indicators
   - Error announcements

### Standard Components to Include

```typescript
// Every project needs these base components:

// 1. Analytics Provider
<AnalyticsProvider
  providers={['rudderstack', 'google', 'facebook']}
  config={analyticsConfig}
>

// 2. Cookie Consent
<CookieConsent
  privacyUrl="/privacy"
  onAccept={handleCookieAccept}
/>

// 3. Data Capture Form
<DataForm
  fields={formFields}
  validation={validationSchema}
  onSubmit={handleSubmit}
/>

// 4. Progress Indicator
<ProgressBar
  current={currentStep}
  total={totalSteps}
  showLabels={false}
/>
```

### Environment Variables Template
```env
# Analytics
NEXT_PUBLIC_ANALYTICS_KEY=
NEXT_PUBLIC_ANALYTICS_URL=

# API Endpoints
NEXT_PUBLIC_API_URL=
API_SECRET_KEY=

# Feature Flags
NEXT_PUBLIC_ENABLE_FEATURE_X=false

# External Services
THIRD_PARTY_API_KEY=
THIRD_PARTY_API_URL=

# Database
DATABASE_URL=
REDIS_URL=

# Monitoring
SENTRY_DSN=
MONITORING_API_KEY=
```

### Testing Checklist

Before deployment, verify:
- [ ] Mobile responsiveness (test on real devices)
- [ ] Form validation and error handling
- [ ] Analytics events firing correctly
- [ ] URL parameters captured
- [ ] Cookie consent working
- [ ] Page load performance
- [ ] Accessibility scan passing
- [ ] Cross-browser compatibility
- [ ] Error tracking configured
- [ ] Success tracking verified

### Performance Optimization

1. **Code Splitting**
   - Dynamic imports for heavy components
   - Route-based splitting
   - Conditional loading

2. **Image Optimization**
   - Next.js Image component
   - Proper sizing and formats
   - Lazy loading

3. **Bundle Optimization**
   - Tree shaking
   - Minification
   - Compression

### Security Considerations

1. **Input Validation**
   - Server-side validation
   - SQL injection prevention
   - XSS protection

2. **Authentication**
   - Secure session management
   - CSRF protection
   - Rate limiting

3. **Data Protection**
   - Encryption at rest
   - Secure transmission
   - PII handling

### Deployment Preparation

1. **Environment Setup**
   - Production variables
   - Staging environment
   - Preview deployments

2. **CI/CD Pipeline**
   - Automated testing
   - Build verification
   - Deployment automation

3. **Monitoring**
   - Error tracking
   - Performance monitoring
   - Uptime checks

### Common Patterns

```typescript
// API Route Pattern
export async function GET/POST(request: NextRequest) {
  try {
    // Validation
    const data = await request.json();
    const validated = schema.parse(data);
    
    // Processing
    const result = await processData(validated);
    
    // Response
    return NextResponse.json({ success: true, data: result });
  } catch (error) {
    return NextResponse.json({ success: false, error: error.message }, { status: 400 });
  }
}

// Form Submission Pattern
const handleSubmit = async (data: FormData) => {
  try {
    // Track attempt
    analytics.track('Form Submitted', { formName });
    
    // Submit
    const result = await api.submit(data);
    
    // Track success
    analytics.track('Form Success', { formName, resultId: result.id });
    
    // Navigate
    router.push('/success');
  } catch (error) {
    // Track error
    analytics.track('Form Error', { formName, error: error.message });
    
    // Show error
    setError(error.message);
  }
};
```

### Getting Started

1. Clone the boilerplate
2. Update project name and description
3. Configure environment variables
4. Customize components for your use case
5. Implement business logic
6. Add project-specific features
7. Test thoroughly
8. Deploy

Remember: This boilerplate provides the foundation. Your project's unique requirements and business logic should be implemented on top of these patterns.