# Next.js 15 API Boilerplate for FreshSlate

## Project Setup

### Base Configuration

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  experimental: {
    // Next.js 15 features
    reactCompiler: true,
    instrumentationHook: true,
    ppr: true, // Partial Prerendering
  },
  
  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },
  
  // Redirects for common patterns
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
    ];
  },
  
  // Image optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.freshslate.com',
      },
    ],
  },
};

export default config;
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## API Route Patterns

### Standard API Route Structure

```typescript
// app/api/v1/leads/route.ts
import { NextRequest } from 'next/server';
import { z } from 'zod';
import { rateLimit } from '@/lib/rate-limit';
import { withAuth } from '@/lib/auth';
import { withError } from '@/lib/error-handler';
import { logger } from '@/lib/logger';

// Request validation
const createLeadSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  phone: z.string().regex(/^\d{10}$/),
  debt_amount: z.number().min(1000).max(1000000),
});

// GET handler
export async function GET(request: NextRequest) {
  return withError(async () => {
    // Check rate limit
    const rateLimitResult = await rateLimit(request);
    if (!rateLimitResult.success) {
      return Response.json(
        { error: 'Too many requests' },
        { status: 429 }
      );
    }
    
    // Parse query params
    const searchParams = request.nextUrl.searchParams;
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '20');
    
    // Fetch data
    const leads = await getLeads({ page, limit });
    
    // Return with cache headers
    return Response.json(
      { data: leads },
      {
        headers: {
          'Cache-Control': 'private, max-age=60',
        },
      }
    );
  });
}

// POST handler
export async function POST(request: NextRequest) {
  return withError(async () => {
    // Parse and validate body
    const body = await request.json();
    const validated = createLeadSchema.parse(body);
    
    // Log the request
    logger.info('Creating lead', {
      email: validated.email,
      source: request.headers.get('referer'),
    });
    
    // Create lead
    const lead = await createLead(validated);
    
    // Return created resource
    return Response.json(
      { data: lead },
      { status: 201 }
    );
  });
}

// OPTIONS handler for CORS
export async function OPTIONS() {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
```

### Error Handler Middleware

```typescript
// lib/error-handler.ts
import { ZodError } from 'zod';
import { logger } from './logger';

export async function withError<T>(
  handler: () => Promise<T>
): Promise<Response> {
  try {
    return await handler();
  } catch (error) {
    // Log error
    logger.error('API Error', { error });
    
    // Handle Zod validation errors
    if (error instanceof ZodError) {
      return Response.json(
        {
          error: 'Validation failed',
          details: error.errors,
        },
        { status: 400 }
      );
    }
    
    // Handle known errors
    if (error instanceof Error) {
      const statusCode = (error as any).statusCode || 500;
      return Response.json(
        {
          error: error.message,
        },
        { status: statusCode }
      );
    }
    
    // Unknown errors
    return Response.json(
      {
        error: 'Internal server error',
      },
      { status: 500 }
    );
  }
}
```

### Rate Limiting

```typescript
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';
import { NextRequest } from 'next/server';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL!,
  token: process.env.UPSTASH_REDIS_TOKEN!,
});

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, '10 s'),
  analytics: true,
});

export async function rateLimit(request: NextRequest) {
  const ip = request.headers.get('x-forwarded-for') ?? 'anonymous';
  return await ratelimit.limit(ip);
}
```

### Logging Setup

```typescript
// lib/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
    },
  },
  redact: ['email', 'phone', 'password'],
});

// Sentry integration
if (process.env.NODE_ENV === 'production') {
  logger.info('Sentry initialized');
}
```

## Middleware

### Global Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Add request ID
  const requestId = crypto.randomUUID();
  const response = NextResponse.next();
  response.headers.set('x-request-id', requestId);
  
  // Add security headers
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  
  // Log request
  console.log({
    requestId,
    method: request.method,
    url: request.url,
    timestamp: new Date().toISOString(),
  });
  
  return response;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
```

## Server Actions (Next.js 15)

```typescript
// app/actions/leads.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';
import { supabase } from '@/lib/supabase';

const leadSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  phone: z.string(),
  debt_amount: z.number(),
});

export async function createLeadAction(data: unknown) {
  try {
    // Validate input
    const validated = leadSchema.parse(data);
    
    // Create lead
    const { data: lead, error } = await supabase
      .from('leads')
      .insert(validated)
      .select()
      .single();
      
    if (error) throw error;
    
    // Revalidate cache
    revalidatePath('/admin/leads');
    
    return { success: true, lead };
  } catch (error) {
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
}
```

## Environment Variables

```bash
# .env.local
NODE_ENV=development

# Database
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# Redis
UPSTASH_REDIS_URL=...
UPSTASH_REDIS_TOKEN=...

# Analytics
RUDDERSTACK_KEY=...
RUDDERSTACK_URL=...

# Error Tracking
SENTRY_DSN=...
BETTERSTACK_TOKEN=...

# External APIs
GOOGLE_TAG_MANAGER_ID=...
FACEBOOK_PIXEL_ID=...

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_CHAT=false
```

## Testing Setup

```typescript
// __tests__/api/leads.test.ts
import { createMocks } from 'node-mocks-http';
import { POST } from '@/app/api/v1/leads/route';

describe('/api/v1/leads', () => {
  it('creates a lead successfully', async () => {
    const { req } = createMocks({
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: {
        name: 'John Doe',
        email: 'john@example.com',
        phone: '1234567890',
        debt_amount: 25000,
      },
    });
    
    const response = await POST(req as any);
    const json = await response.json();
    
    expect(response.status).toBe(201);
    expect(json.data).toHaveProperty('id');
  });
  
  it('validates input data', async () => {
    const { req } = createMocks({
      method: 'POST',
      body: {
        name: 'J', // Too short
        email: 'invalid-email',
        phone: '123', // Too short
      },
    });
    
    const response = await POST(req as any);
    
    expect(response.status).toBe(400);
  });
});
```

## Deployment Configuration

```yaml
# vercel.json
{
  "functions": {
    "app/api/v1/leads/route.ts": {
      "maxDuration": 10
    }
  },
  "crons": [
    {
      "path": "/api/cron/sync-leads",
      "schedule": "0 * * * *"
    }
  ]
}
```

## Performance Monitoring

```typescript
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const { NodeSDK } = await import('@opentelemetry/sdk-node');
    const { getNodeAutoInstrumentations } = await import('@opentelemetry/auto-instrumentations-node');
    const { Resource } = await import('@opentelemetry/resources');
    const { SemanticResourceAttributes } = await import('@opentelemetry/semantic-conventions');
    
    const sdk = new NodeSDK({
      resource: new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: 'freshslate-api',
      }),
      instrumentations: [
        getNodeAutoInstrumentations(),
      ],
    });
    
    sdk.start();
  }
}
```

## Common Utilities

```typescript
// lib/utils/api.ts
export function getBaseUrl() {
  if (typeof window !== 'undefined') return '';
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return `http://localhost:${process.env.PORT ?? 3000}`;
}

export function getApiUrl(path: string) {
  return `${getBaseUrl()}/api/v1${path}`;
}

export async function fetcher<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  
  if (!res.ok) {
    throw new Error(`API Error: ${res.status}`);
  }
  
  return res.json();
}
```