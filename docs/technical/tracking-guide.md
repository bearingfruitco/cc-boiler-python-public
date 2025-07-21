# URL Parameter & Cookie Tracking Guide

## Overview

This guide covers capturing marketing attribution data from URLs and cookies for comprehensive tracking.

## URL Parameter Capture

### Standard UTM Parameters
```typescript
// lib/tracking/url-params.ts
export interface UTMParams {
  utm_source?: string;      // e.g., 'facebook', 'google'
  utm_medium?: string;      // e.g., 'cpc', 'social'
  utm_campaign?: string;    // e.g., 'summer-sale-2024'
  utm_term?: string;        // e.g., 'running+shoes'
  utm_content?: string;     // e.g., 'blue-cta-button'
}

// Platform-specific parameters
export interface PlatformParams {
  gclid?: string;          // Google Click ID
  fbclid?: string;         // Facebook Click ID
  ttclid?: string;         // TikTok Click ID
  msclkid?: string;        // Microsoft Click ID
  
  // Custom tracking
  source_id?: string;      // Internal source tracking
  affiliate_id?: string;   // Affiliate partner ID
  creative_id?: string;    // Ad creative identifier
  placement?: string;      // Ad placement
}
```

### Implementation: URL Parameter Hook
```typescript
// hooks/useUrlParams.ts
import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';

export interface TrackingParams extends UTMParams, PlatformParams {
  [key: string]: string | undefined;
}

export function useUrlParams() {
  const searchParams = useSearchParams();
  const [params, setParams] = useState<TrackingParams>({});

  useEffect(() => {
    const urlParams: TrackingParams = {};
    
    // Capture all query parameters
    searchParams.forEach((value, key) => {
      urlParams[key] = value;
    });

    // Store in session for multi-step forms
    if (Object.keys(urlParams).length > 0) {
      sessionStorage.setItem('tracking_params', JSON.stringify(urlParams));
      setParams(urlParams);
    } else {
      // Retrieve from session if no URL params
      const stored = sessionStorage.getItem('tracking_params');
      if (stored) {
        setParams(JSON.parse(stored));
      }
    }
  }, [searchParams]);

  return params;
}
```

### Form Integration
```typescript
// components/TrackedForm.tsx
export function TrackedForm() {
  const trackingParams = useUrlParams();
  
  const onSubmit = async (formData: FormData) => {
    // Include tracking params with form submission
    const payload = {
      ...formData,
      tracking: {
        ...trackingParams,
        page_url: window.location.href,
        referrer: document.referrer,
        timestamp: new Date().toISOString(),
      }
    };
    
    await submitData(payload);
  };
}
```

## Cookie Tracking

### Reading Advertising Platform Cookies
```typescript
// lib/tracking/cookies.ts
export interface AdPlatformCookies {
  _fbp?: string;      // Facebook Browser ID
  _fbc?: string;      // Facebook Click ID
  _ga?: string;       // Google Analytics Client ID
  _gcl_aw?: string;   // Google Ads Click ID
  _ttp?: string;      // TikTok Pixel ID
}

export function getAdCookies(): AdPlatformCookies {
  const cookies: AdPlatformCookies = {};
  
  // Parse document.cookie
  document.cookie.split(';').forEach(cookie => {
    const [name, value] = cookie.trim().split('=');
    
    // Facebook cookies
    if (name === '_fbp') cookies._fbp = value;
    if (name === '_fbc') cookies._fbc = value;
    
    // Google cookies
    if (name === '_ga') cookies._ga = value;
    if (name.startsWith('_gcl_aw')) cookies._gcl_aw = value;
    
    // TikTok cookies
    if (name === '_ttp') cookies._ttp = value;
  });
  
  return cookies;
}

// First-party cookie fallback
export function setFirstPartyCookie(name: string, value: string, days = 30) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  
  document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/;domain=${getDomain()};SameSite=Lax;Secure`;
}

function getDomain() {
  // Extract root domain for cross-subdomain tracking
  const hostname = window.location.hostname;
  const parts = hostname.split('.');
  if (parts.length > 2) {
    return `.${parts.slice(-2).join('.')}`;
  }
  return hostname;
}
```

### Cookie Consent Management
```typescript
// components/CookieConsent.tsx
export function CookieConsent() {
  const [consent, setConsent] = useState<boolean | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('cookie_consent');
    if (saved) {
      setConsent(saved === 'true');
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('cookie_consent', 'true');
    setConsent(true);
    
    // Initialize tracking only after consent
    initializeTracking();
  };

  const handleDecline = () => {
    localStorage.setItem('cookie_consent', 'false');
    setConsent(false);
    
    // Use cookieless tracking
    initializeCookielessTracking();
  };

  if (consent !== null) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg p-4">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <p className="text-size-3 text-gray-700">
          We use cookies to improve your experience and understand how you found us. 
        </p>
        <div className="flex gap-2">
          <button onClick={handleDecline} className="px-4 py-2 text-gray-600">
            Decline
          </button>
          <button onClick={handleAccept} className="px-4 py-2 bg-blue-600 text-white rounded">
            Accept
          </button>
        </div>
      </div>
    </div>
  );
}
```

## Complete Tracking Implementation

### Analytics Context Provider
```typescript
// components/TrackingProvider.tsx
export function TrackingProvider({ children }: { children: React.ReactNode }) {
  const urlParams = useUrlParams();
  const [cookies, setCookies] = useState<AdPlatformCookies>({});
  const [sessionId] = useState(() => generateSessionId());

  useEffect(() => {
    const consent = localStorage.getItem('cookie_consent');
    if (consent === 'true') {
      setCookies(getAdCookies());
    }
  }, []);

  const trackEvent = useCallback((eventName: string, properties?: any) => {
    const eventData = {
      event: eventName,
      properties: {
        ...properties,
        ...urlParams,
        ...cookies,
        session_id: sessionId,
        timestamp: new Date().toISOString(),
      }
    };

    // Send to analytics platform
    if (window.analytics) {
      window.analytics.track(eventName, eventData.properties);
    }

    // Send to other platforms
    sendToAdPlatforms(eventData);
  }, [urlParams, cookies, sessionId]);

  return (
    <TrackingContext.Provider value={{ trackEvent, urlParams, cookies }}>
      {children}
    </TrackingContext.Provider>
  );
}
```

### Attribution Example
```typescript
// Complete submission with full attribution
const submitData = async (formData: DataFormData) => {
  const attribution = {
    // Form data
    ...formData,
    
    // URL parameters
    utm_source: urlParams.utm_source,
    utm_medium: urlParams.utm_medium,
    utm_campaign: urlParams.utm_campaign,
    gclid: urlParams.gclid,
    fbclid: urlParams.fbclid,
    
    // Cookie data
    fb_browser_id: cookies._fbp,
    fb_click_id: cookies._fbc,
    ga_client_id: cookies._ga,
    google_click_id: cookies._gcl_aw,
    
    // Session data
    landing_page: sessionStorage.getItem('landing_page'),
    referrer: sessionStorage.getItem('referrer'),
    session_id: sessionId,
    
    // Technical data
    user_agent: navigator.userAgent,
    screen_resolution: `${window.screen.width}x${window.screen.height}`,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  };

  await fetch('/api/submissions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(attribution),
  });
};
```

## Privacy & Compliance

### Required Disclosures
```jsx
// components/PrivacyNotice.tsx
<div className="text-size-4 text-gray-500 mt-4">
  <p>
    By submitting this form, you consent to our use of cookies and tracking
    technologies to improve your experience and analyze site usage.
  </p>
  <p className="mt-2">
    We track how you found us to improve our services. See our{' '}
    <a href="/privacy" className="text-blue-600 underline">Privacy Policy</a>.
  </p>
</div>
```

### GDPR/CCPA Compliance
```typescript
// lib/privacy.ts
export function deleteUserData(identifier: string) {
  // Clear cookies
  document.cookie.split(';').forEach(cookie => {
    const [name] = cookie.trim().split('=');
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
  });
  
  // Clear storage
  localStorage.removeItem('cookie_consent');
  sessionStorage.clear();
  
  // Request backend deletion
  return fetch('/api/privacy/delete', {
    method: 'POST',
    body: JSON.stringify({ identifier }),
  });
}
```

## Testing Attribution

### URL Parameter Test Cases
```
# Basic UTM test
https://example.com/?utm_source=facebook&utm_medium=cpc&utm_campaign=summer-sale

# With platform IDs
https://example.com/?gclid=123456&utm_source=google&utm_medium=cpc

# Multiple parameters
https://example.com/?fbclid=789&utm_source=facebook&utm_medium=social&creative_id=blue-cta
```

### Cookie Testing
```javascript
// Console commands for testing
// Set test cookies
document.cookie = "_fbp=fb.1.123456789.987654321;path=/";
document.cookie = "_ga=GA1.2.123456789.987654321;path=/";

// Verify capture
console.log(getAdCookies());
```

## Common Issues & Solutions

1. **Cross-domain tracking**: Use first-party cookies with root domain
2. **Safari ITP**: Implement server-side tracking as fallback
3. **Ad blockers**: Use first-party endpoints, not third-party scripts
4. **GDPR compliance**: Always get consent before setting cookies
5. **Attribution windows**: Store first touch and last touch separately

## Server-Side Tracking

```typescript
// app/api/track/route.ts
export async function POST(request: NextRequest) {
  const data = await request.json();
  
  // Get server-side data
  const serverData = {
    ip: request.headers.get('x-forwarded-for'),
    userAgent: request.headers.get('user-agent'),
    timestamp: new Date().toISOString(),
  };
  
  // Merge with client data
  const event = {
    ...data,
    ...serverData,
  };
  
  // Send to analytics platforms
  await sendToAnalytics(event);
  
  return Response.json({ success: true });
}
```