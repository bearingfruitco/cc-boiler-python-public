# FreshSlate Monitoring Stack Documentation

## Sentry Error Tracking

**Official Documentation**: https://docs.sentry.io/

### Setup
```typescript
// lib/sentry.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  
  // Performance Monitoring
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
  
  // Session Replay
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  
  // Release tracking
  release: process.env.VERCEL_GIT_COMMIT_SHA,
  
  // Environment
  environment: process.env.VERCEL_ENV || 'development',
  
  // Integrations
  integrations: [
    Sentry.replayIntegration({
      maskAllText: false,
      blockAllMedia: false,
    }),
  ],
  
  // Filtering
  ignoreErrors: [
    // Browser extensions
    'top.GLOBALS',
    // Random network errors
    'Network request failed',
    // Facebook errors
    'fb_xd_fragment',
  ],
  
  beforeSend(event, hint) {
    // Filter out non-app errors
    if (event.exception) {
      const error = hint.originalException;
      // Don't send errors from browser extensions
      if (error?.stack?.includes('chrome-extension://')) {
        return null;
      }
    }
    return event;
  },
});
```

### Error Boundary
```typescript
// app/error.tsx
'use client';

import * as Sentry from '@sentry/nextjs';
import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);
  
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-semibold mb-4">Something went wrong!</h2>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Try again
      </button>
    </div>
  );
}
```

### Custom Error Tracking
```typescript
// lib/tracking/errors.ts
export function trackError(
  error: Error,
  context?: Record<string, any>
) {
  // Add context
  Sentry.withScope((scope) => {
    if (context) {
      Object.entries(context).forEach(([key, value]) => {
        scope.setContext(key, value);
      });
    }
    
    // Add user context if available
    const user = getCurrentUser();
    if (user) {
      scope.setUser({
        id: user.id,
        email: user.email,
      });
    }
    
    // Capture
    Sentry.captureException(error);
  });
  
  // Also log to console in dev
  if (process.env.NODE_ENV === 'development') {
    console.error('Error tracked:', error, context);
  }
}

// Form submission errors
export function trackFormError(
  formName: string,
  error: Error,
  formData?: Record<string, any>
) {
  trackError(error, {
    form: {
      name: formName,
      data: sanitizeFormData(formData),
    },
  });
}

// API errors
export function trackApiError(
  endpoint: string,
  error: Error,
  request?: any
) {
  trackError(error, {
    api: {
      endpoint,
      method: request?.method,
      status: error?.status,
    },
  });
}
```

## BetterStack Uptime Monitoring

**Official Documentation**: https://betterstack.com/docs/uptime/start/

### Setup
```typescript
// lib/betterstack.ts
import { BetterStack } from '@betterstack/node';

const betterstack = new BetterStack({
  apiToken: process.env.BETTERSTACK_TOKEN!,
});

// Heartbeat monitoring
export async function sendHeartbeat(monitor: string) {
  try {
    await fetch(`https://uptime.betterstack.com/api/v1/heartbeat/${monitor}`);
  } catch (error) {
    console.error('Failed to send heartbeat:', error);
  }
}

// Custom incident reporting
export async function reportIncident(
  title: string,
  description: string,
  severity: 'low' | 'medium' | 'high' | 'critical' = 'medium'
) {
  try {
    await betterstack.incidents.create({
      title,
      description,
      severity,
      status: 'investigating',
    });
  } catch (error) {
    console.error('Failed to report incident:', error);
  }
}
```

### Health Check Endpoint
```typescript
// app/api/health/route.ts
import { supabase } from '@/lib/supabase';
import { redis } from '@/lib/redis';

export async function GET() {
  const checks = {
    server: 'ok',
    database: 'unknown',
    redis: 'unknown',
    timestamp: new Date().toISOString(),
  };
  
  try {
    // Check database
    const { error: dbError } = await supabase
      .from('leads')
      .select('count')
      .limit(1);
    checks.database = dbError ? 'error' : 'ok';
    
    // Check Redis
    await redis.ping();
    checks.redis = 'ok';
  } catch (error) {
    // Don't throw, just mark as error
  }
  
  const allHealthy = Object.values(checks)
    .filter(v => typeof v === 'string')
    .every(v => v === 'ok');
  
  return Response.json(checks, {
    status: allHealthy ? 200 : 503,
  });
}
```

### Cron Job Monitoring
```typescript
// app/api/cron/sync-leads/route.ts
import { sendHeartbeat } from '@/lib/betterstack';

export async function GET(request: Request) {
  // Verify cron secret
  const authHeader = request.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }
  
  try {
    // Do the work
    await syncLeads();
    
    // Send heartbeat on success
    await sendHeartbeat(process.env.BETTERSTACK_SYNC_MONITOR!);
    
    return Response.json({ success: true });
  } catch (error) {
    // Report incident on failure
    await reportIncident(
      'Lead Sync Failed',
      `Error: ${error.message}`,
      'high'
    );
    
    throw error;
  }
}
```

## Upstash Redis

**Official Documentation**: https://upstash.com/docs/introduction

### Setup
```typescript
// lib/redis.ts
import { Redis } from '@upstash/redis';

export const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

// Type-safe wrapper
export const cache = {
  async get<T>(key: string): Promise<T | null> {
    return await redis.get(key);
  },
  
  async set(key: string, value: any, ex?: number): Promise<void> {
    if (ex) {
      await redis.setex(key, ex, value);
    } else {
      await redis.set(key, value);
    }
  },
  
  async delete(key: string): Promise<void> {
    await redis.del(key);
  },
  
  async increment(key: string): Promise<number> {
    return await redis.incr(key);
  },
};
```

### Caching Patterns
```typescript
// lib/cache/patterns.ts

// Cache aside pattern
export async function getCachedData<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl = 3600 // 1 hour default
): Promise<T> {
  // Try cache first
  const cached = await cache.get<T>(key);
  if (cached) return cached;
  
  // Fetch fresh data
  const fresh = await fetcher();
  
  // Cache it
  await cache.set(key, fresh, ttl);
  
  return fresh;
}

// Cache invalidation
export async function invalidateCache(pattern: string) {
  const keys = await redis.keys(pattern);
  if (keys.length > 0) {
    await redis.del(...keys);
  }
}

// Distributed lock
export async function withLock<T>(
  key: string,
  fn: () => Promise<T>,
  timeout = 5000
): Promise<T> {
  const lockKey = `lock:${key}`;
  const lockValue = Math.random().toString(36);
  
  // Try to acquire lock
  const acquired = await redis.set(
    lockKey,
    lockValue,
    'NX',
    'PX',
    timeout
  );
  
  if (!acquired) {
    throw new Error('Could not acquire lock');
  }
  
  try {
    return await fn();
  } finally {
    // Release lock if we still own it
    const current = await redis.get(lockKey);
    if (current === lockValue) {
      await redis.del(lockKey);
    }
  }
}
```

### Session Management
```typescript
// lib/sessions.ts
export async function createSession(data: any): Promise<string> {
  const sessionId = crypto.randomUUID();
  const key = `session:${sessionId}`;
  
  await redis.setex(
    key,
    3600 * 24, // 24 hours
    JSON.stringify(data)
  );
  
  return sessionId;
}

export async function getSession(sessionId: string): Promise<any | null> {
  const key = `session:${sessionId}`;
  const data = await redis.get(key);
  
  if (!data) return null;
  
  // Extend TTL on access
  await redis.expire(key, 3600 * 24);
  
  return JSON.parse(data);
}
```

## Google Tag Manager

### Setup
```typescript
// components/GoogleTagManager.tsx
'use client';

import { useEffect } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import Script from 'next/script';

declare global {
  interface Window {
    dataLayer: any[];
  }
}

export function GoogleTagManager() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  
  // Track page views
  useEffect(() => {
    if (typeof window !== 'undefined' && window.dataLayer) {
      window.dataLayer.push({
        event: 'page_view',
        page_path: pathname,
        page_search: searchParams.toString(),
      });
    }
  }, [pathname, searchParams]);
  
  return (
    <>
      {/* Google Tag Manager */}
      <Script
        id="gtm-script"
        strategy="afterInteractive"
        dangerouslySetInnerHTML={{
          __html: `
            (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer','${process.env.NEXT_PUBLIC_GTM_ID}');
          `,
        }}
      />
      
      {/* Google Tag Manager (noscript) */}
      <noscript>
        <iframe
          src={`https://www.googletagmanager.com/ns.html?id=${process.env.NEXT_PUBLIC_GTM_ID}`}
          height="0"
          width="0"
          style={{ display: 'none', visibility: 'hidden' }}
        />
      </noscript>
    </>
  );
}
```

### Data Layer Events
```typescript
// lib/gtm/events.ts
export function pushDataLayer(data: Record<string, any>) {
  if (typeof window !== 'undefined' && window.dataLayer) {
    window.dataLayer.push(data);
  }
}

// Lead events
export function trackLeadEvent(
  eventName: string,
  leadData: any
) {
  pushDataLayer({
    event: eventName,
    lead_id: leadData.id,
    debt_amount: leadData.debt_amount,
    state: leadData.state,
    qualification_status: leadData.qualification_status,
    timestamp: new Date().toISOString(),
  });
}

// Enhanced Ecommerce
export function trackConversion(
  transactionId: string,
  value: number,
  items: any[]
) {
  pushDataLayer({
    event: 'purchase',
    ecommerce: {
      transaction_id: transactionId,
      value: value,
      currency: 'USD',
      items: items,
    },
  });
}

// Custom dimensions
export function setUserProperties(properties: Record<string, any>) {
  pushDataLayer({
    event: 'user_properties',
    user_properties: properties,
  });
}
```

## Cloudflare Workers

**Official Documentation**: https://developers.cloudflare.com/

### Worker Script
```typescript
// workers/api-proxy/index.ts
export interface Env {
  SUPABASE_URL: string;
  SUPABASE_SERVICE_KEY: string;
  RATE_LIMITER: DurableObjectNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Add CORS headers
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }
    
    // Rate limiting
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const rateLimiterId = env.RATE_LIMITER.idFromName(ip);
    const rateLimiter = env.RATE_LIMITER.get(rateLimiterId);
    
    const allowed = await rateLimiter.fetch(request).then(r => r.json());
    if (!allowed) {
      return new Response('Too Many Requests', { status: 429 });
    }
    
    // Proxy to Supabase
    const url = new URL(request.url);
    url.hostname = new URL(env.SUPABASE_URL).hostname;
    
    const proxyRequest = new Request(url, request);
    proxyRequest.headers.set('apikey', env.SUPABASE_SERVICE_KEY);
    
    return fetch(proxyRequest);
  },
};

// Rate limiter Durable Object
export class RateLimiter {
  state: DurableObjectState;
  
  constructor(state: DurableObjectState) {
    this.state = state;
  }
  
  async fetch(request: Request): Promise<Response> {
    const now = Date.now();
    const minute = Math.floor(now / 60000);
    
    const key = `requests:${minute}`;
    const count = (await this.state.storage.get<number>(key)) || 0;
    
    if (count >= 100) { // 100 requests per minute
      return Response.json(false);
    }
    
    await this.state.storage.put(key, count + 1);
    await this.state.storage.setAlarm(now + 60000); // Clean up after 1 minute
    
    return Response.json(true);
  }
  
  async alarm() {
    // Clean up old entries
    const now = Date.now();
    const currentMinute = Math.floor(now / 60000);
    
    const keys = await this.state.storage.list();
    for (const [key] of keys) {
      const minute = parseInt(key.split(':')[1]);
      if (minute < currentMinute - 1) {
        await this.state.storage.delete(key);
      }
    }
  }
}
```

### BigQuery Integration
```typescript
// lib/bigquery.ts
import { BigQuery } from '@google-cloud/bigquery';

const bigquery = new BigQuery({
  projectId: process.env.GOOGLE_CLOUD_PROJECT,
  keyFilename: process.env.GOOGLE_CLOUD_KEYFILE,
});

const dataset = bigquery.dataset('freshslate_analytics');

export async function insertLeadEvent(event: any) {
  const table = dataset.table('lead_events');
  
  await table.insert({
    event_id: crypto.randomUUID(),
    event_name: event.name,
    lead_id: event.lead_id,
    properties: JSON.stringify(event.properties),
    created_at: new Date().toISOString(),
  });
}

export async function queryLeadMetrics(startDate: Date, endDate: Date) {
  const query = `
    SELECT
      DATE(created_at) as date,
      COUNT(DISTINCT lead_id) as leads,
      SUM(CAST(JSON_EXTRACT_SCALAR(properties, '$.debt_amount') AS NUMERIC)) as total_debt,
      AVG(CAST(JSON_EXTRACT_SCALAR(properties, '$.debt_amount') AS NUMERIC)) as avg_debt
    FROM \`${process.env.GOOGLE_CLOUD_PROJECT}.freshslate_analytics.lead_events\`
    WHERE created_at BETWEEN @startDate AND @endDate
      AND event_name = 'lead_created'
    GROUP BY date
    ORDER BY date DESC
  `;
  
  const [rows] = await bigquery.query({
    query,
    params: { startDate, endDate },
  });
  
  return rows;
}
```

## Complete Monitoring Setup Checklist

```markdown
## Monitoring Checklist

### Error Tracking (Sentry)
- [ ] Install Sentry SDK
- [ ] Configure for client and server
- [ ] Set up error boundaries
- [ ] Add custom context
- [ ] Configure release tracking
- [ ] Set up alerts

### Uptime Monitoring (BetterStack)
- [ ] Create monitors for each endpoint
- [ ] Set up health check endpoint
- [ ] Configure heartbeat monitors
- [ ] Set up incident workflows
- [ ] Create status page

### Caching (Upstash Redis)
- [ ] Set up Redis client
- [ ] Implement caching patterns
- [ ] Add session management
- [ ] Configure rate limiting
- [ ] Set up cache invalidation

### Analytics (GTM + BigQuery)
- [ ] Install GTM container
- [ ] Configure data layer
- [ ] Set up conversion tracking
- [ ] Stream to BigQuery
- [ ] Create dashboards

### Performance (Cloudflare)
- [ ] Deploy Workers for API proxy
- [ ] Set up rate limiting
- [ ] Configure caching rules
- [ ] Enable analytics
```