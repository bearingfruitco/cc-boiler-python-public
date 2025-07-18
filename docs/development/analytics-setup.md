# Analytics Setup Guide

## Overview

This guide covers implementing analytics using RudderStack CDP or similar analytics platforms for comprehensive tracking and attribution.

## Initial Setup

### 1. Install Analytics SDK
```bash
npm install rudder-sdk-js
# or for other platforms
npm install analytics mixpanel segment
```

### 2. Initialize in Layout
```typescript
// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script id="analytics-setup" strategy="afterInteractive">
          {`
            !function(){var e=window.rudderanalytics=window.rudderanalytics||[];
            e.methods=["load","page","track","identify","alias","group","ready","reset",
            "getAnonymousId","setAnonymousId","getUserId","getUserTraits","getGroupId",
            "getGroupTraits","startSession","endSession","getSessionId"];
            e.factory=function(t){return function(){e.push([t].concat(Array.prototype.slice.call(arguments)))}};
            for(var t=0;t<e.methods.length;t++){var r=e.methods[t];e[r]=e.factory(r)}
            e.loadJS=function(e,t){var r=document.createElement("script");r.type="text/javascript",
            r.async=!0,r.src="https://cdn.rudderlabs.com/v1.1/rudder-analytics.min.js";
            var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(r,a)},
            e.loadJS(),
            e.load("${process.env.NEXT_PUBLIC_ANALYTICS_KEY}","${process.env.NEXT_PUBLIC_ANALYTICS_URL}",
            {
              integrations: { All: true },
              logLevel: "${process.env.NODE_ENV === 'production' ? 'error' : 'debug'}"
            })}();
          `}
        </Script>
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 3. TypeScript Types
```typescript
// types/analytics.d.ts
interface Analytics {
  load(writeKey: string, dataPlaneUrl: string, options?: any): void;
  ready(callback: () => void): void;
  identify(userId?: string, traits?: any, options?: any, callback?: () => void): void;
  track(event: string, properties?: any, options?: any, callback?: () => void): void;
  page(category?: string, name?: string, properties?: any, options?: any): void;
  alias(to: string, from?: string, options?: any, callback?: () => void): void;
  group(groupId: string, traits?: any, options?: any, callback?: () => void): void;
  reset(): void;
}

declare global {
  interface Window {
    rudderanalytics: Analytics;
    analytics: Analytics; // For other providers
  }
}
```

## Event Tracking Schema

### Standard Events

```typescript
// lib/analytics/events.ts
export const EVENTS = {
  // Page view events
  PAGE_VIEW: 'Page Viewed',
  
  // User interaction events
  BUTTON_CLICKED: 'Button Clicked',
  LINK_CLICKED: 'Link Clicked',
  FORM_STARTED: 'Form Started',
  FORM_COMPLETED: 'Form Completed',
  
  // Flow events
  FLOW_STARTED: 'Flow Started',
  FLOW_STEP_VIEWED: 'Flow Step Viewed',
  FLOW_COMPLETED: 'Flow Completed',
  
  // Conversion events
  SIGNUP_COMPLETED: 'Signup Completed',
  PURCHASE_COMPLETED: 'Purchase Completed',
  GOAL_ACHIEVED: 'Goal Achieved',
  
  // Error events
  ERROR_OCCURRED: 'Error Occurred',
  API_ERROR: 'API Error',
} as const;

// Event property schemas
export interface PageViewProps {
  page_name: string;
  page_category: string;
  page_path: string;
  referrer?: string;
}

export interface FlowStepProps {
  flow_name: string;
  step_number: number;
  step_name: string;
  step_value?: any;
  time_on_step?: number;
}

export interface ConversionProps {
  conversion_id: string;
  conversion_value?: number;
  conversion_type: string;
  attribution: AttributionData;
}
```

### Analytics Hook Implementation

```typescript
// hooks/useAnalytics.ts
import { useCallback, useEffect, useRef } from 'react';
import { EVENTS } from '@/lib/analytics/events';
import { useTracking } from './useTracking';

export function useAnalytics() {
  const tracking = useTracking();
  const startTime = useRef<number>(Date.now());
  const sessionData = useRef({
    session_id: generateSessionId(),
    session_start: new Date().toISOString(),
  });

  // Track page view on mount
  useEffect(() => {
    trackPageView();
  }, []);

  const trackPageView = useCallback((overrides?: any) => {
    if (!window.rudderanalytics) return;

    const properties = {
      page_name: document.title,
      page_path: window.location.pathname,
      page_category: getPageCategory(window.location.pathname),
      referrer: document.referrer,
      ...tracking.params,
      ...sessionData.current,
      ...overrides,
    };

    window.rudderanalytics.page(properties.page_category, properties.page_name, properties);
  }, [tracking.params]);

  const track = useCallback((event: keyof typeof EVENTS, properties?: any) => {
    if (!window.rudderanalytics) return;

    const enrichedProps = {
      ...properties,
      ...tracking.params,
      ...sessionData.current,
      timestamp: new Date().toISOString(),
      time_since_start: Date.now() - startTime.current,
    };

    window.rudderanalytics.track(EVENTS[event], enrichedProps);
    
    // Also send to other platforms if configured
    sendToAdditionalPlatforms(event, enrichedProps);
  }, [tracking.params]);

  const identify = useCallback((userId: string, traits?: any) => {
    if (!window.rudderanalytics) return;

    window.rudderanalytics.identify(userId, {
      ...traits,
      first_seen: new Date().toISOString(),
      ...tracking.params,
    });
  }, [tracking.params]);

  return { track, trackPageView, identify };
}

// Helper functions
function generateSessionId() {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function getPageCategory(path: string) {
  if (path === '/') return 'home';
  const category = path.split('/')[1];
  return category || 'other';
}

function sendToAdditionalPlatforms(event: string, properties: any) {
  // Send to Facebook Pixel if configured
  if (window.fbq) {
    window.fbq('trackCustom', event, properties);
  }
  
  // Send to Google Analytics if configured
  if (window.gtag) {
    window.gtag('event', event, properties);
  }
}
```

## Flow Tracking Example

```typescript
// components/MultiStepFlow.tsx
export function MultiStepFlow() {
  const { track } = useAnalytics();
  const [currentStep, setCurrentStep] = useState(1);
  const [flowData, setFlowData] = useState({});
  const stepStartTime = useRef(Date.now());

  // Track flow start
  useEffect(() => {
    track('FLOW_STARTED', {
      flow_name: 'user_onboarding',
      total_steps: TOTAL_STEPS,
    });
  }, []);

  // Track step views
  useEffect(() => {
    track('FLOW_STEP_VIEWED', {
      flow_name: 'user_onboarding',
      step_number: currentStep,
      step_name: getStepName(currentStep),
    });
    stepStartTime.current = Date.now();
  }, [currentStep]);

  const handleStepComplete = (stepData: any) => {
    const timeOnStep = Date.now() - stepStartTime.current;
    
    track('FORM_COMPLETED', {
      form_name: `step_${currentStep}`,
      time_to_complete: timeOnStep,
      field_count: Object.keys(stepData).length,
    });

    setFlowData({ ...flowData, [`step_${currentStep}`]: stepData });
    
    if (currentStep === TOTAL_STEPS) {
      completeFlow();
    } else {
      setCurrentStep(currentStep + 1);
    }
  };

  const completeFlow = () => {
    track('FLOW_COMPLETED', {
      flow_name: 'user_onboarding',
      completion_time: Date.now() - startTime.current,
      steps_data: flowData,
    });
  };
}
```

## Form Tracking with Attribution

```typescript
// components/TrackedForm.tsx
export function TrackedForm() {
  const { track, identify } = useAnalytics();
  const { params: attribution } = useTracking();
  
  const onSubmit = async (data: FormData) => {
    try {
      // Track form submission
      track('FORM_COMPLETED', {
        form_name: 'contact_form',
        fields_submitted: Object.keys(data),
      });

      // Full attribution data
      const submissionData = {
        ...data,
        attribution: {
          // URL params
          ...attribution,
          
          // Session data
          landing_page: sessionStorage.getItem('landing_page'),
          referrer: sessionStorage.getItem('original_referrer'),
          
          // Technical data
          user_agent: navigator.userAgent,
          screen_resolution: `${window.screen.width}x${window.screen.height}`,
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        },
        
        // Timestamps
        submitted_at: new Date().toISOString(),
      };

      // Submit to API
      const response = await submitForm(submissionData);
      
      // Identify user
      if (response.userId) {
        identify(response.userId, {
          email: data.email,
          name: data.name,
        });
      }

      // Track conversion
      track('GOAL_ACHIEVED', {
        goal_type: 'form_submission',
        goal_value: response.value,
      });
      
    } catch (error) {
      track('ERROR_OCCURRED', {
        error_type: 'form_submission',
        error_message: error.message,
        form_name: 'contact_form',
      });
    }
  };
}
```

## Destination Configuration Examples

### Facebook Conversions API
```javascript
// analytics-config.js
{
  "facebook_pixel": {
    "pixelId": "YOUR_PIXEL_ID",
    "eventsToEvents": [
      {
        "from": "Signup Completed",
        "to": "Lead"
      },
      {
        "from": "Purchase Completed", 
        "to": "Purchase"
      }
    ],
    "useNativeSDK": true,
    "enableServerSideAPI": true,
    "accessToken": "YOUR_ACCESS_TOKEN"
  }
}
```

### Google Analytics 4
```javascript
{
  "google_analytics_4": {
    "measurementId": "G-XXXXXXXXXX",
    "extendPageViewParams": true,
    "includeSearchParams": true,
    "serverSideTracking": {
      "enabled": true,
      "apiSecret": "YOUR_API_SECRET"
    }
  }
}
```

## Testing & Debugging

### Debug Mode
```typescript
// lib/analytics/debug.ts
export function enableAnalyticsDebug() {
  if (typeof window === 'undefined') return;
  
  // Log all analytics calls
  const methods = ['track', 'page', 'identify', 'group', 'alias'];
  
  methods.forEach(method => {
    const original = window.rudderanalytics[method];
    window.rudderanalytics[method] = function(...args) {
      console.log(`[Analytics] ${method}:`, ...args);
      return original.apply(this, args);
    };
  });
  
  // Enable in localStorage
  localStorage.setItem('analytics_debug', 'true');
}
```

### Validation Function
```typescript
// lib/analytics/validation.ts
export function validateEventData(event: string, properties: any) {
  const errors: string[] = [];
  
  // Check required fields
  if (!properties.session_id) errors.push('Missing session_id');
  if (!properties.timestamp) errors.push('Missing timestamp');
  
  // Validate data types
  if (properties.value && typeof properties.value !== 'number') {
    errors.push('Value must be a number');
  }
  
  if (errors.length > 0) {
    console.error('[Analytics Validation]', errors);
    return false;
  }
  
  return true;
}
```

## Best Practices

1. **Always include session_id** for journey tracking
2. **Enrich events** with attribution data
3. **Use consistent naming** (snake_case for properties)
4. **Track errors** for debugging
5. **Test in staging** before production
6. **Monitor data quality** in analytics dashboard
7. **Set up alerts** for critical events
8. **Document custom events** for team

## Common Issues

1. **Events not firing**: Check if analytics library is loaded
2. **Missing attribution**: Ensure URL params are captured
3. **Duplicate events**: Use debouncing for rapid actions
4. **Data discrepancies**: Verify destination mappings
5. **Performance impact**: Batch events when possible

## Privacy Compliance

```typescript
// components/AnalyticsConsent.tsx
export function AnalyticsConsent() {
  const [consent, setConsent] = useState<boolean | null>(null);
  
  const handleConsent = (given: boolean) => {
    setConsent(given);
    localStorage.setItem('analytics_consent', given.toString());
    
    if (given) {
      // Initialize analytics
      window.rudderanalytics.load(
        process.env.NEXT_PUBLIC_ANALYTICS_KEY!,
        process.env.NEXT_PUBLIC_ANALYTICS_URL!
      );
    } else {
      // Disable tracking
      window.rudderanalytics.reset();
    }
  };
  
  if (consent !== null) return null;
  
  return (
    <div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <p>We use analytics to improve your experience.</p>
        <div className="flex gap-2">
          <button onClick={() => handleConsent(false)}>Decline</button>
          <button onClick={() => handleConsent(true)}>Accept</button>
        </div>
      </div>
    </div>
  );
}
```