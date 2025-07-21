# Next.js 15 API Boilerplate

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
        hostname: 'cdn.example.com',
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
// app/api/v1/items/route.ts
import { NextRequest } from 'next/server';
import { z } from 'zod';
import { rateLimit } from '@/lib/rate-limit';
import { withAuth } from '@/lib/auth';
import { withError } from '@/lib/error-handler';
import { logger } from '@/lib/logger';

// Request validation
const createItemSchema = z.object({
  name: z.string().min(2).max(100),
  description: z.string().optional(),
  metadata: z.record(z.unknown()).optional(),
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
    const items = await getItems({ page, limit });
    
    // Return with cache headers
    return Response.json(
      { data: items },
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
    const validated = createItemSchema.parse(body);
    
    // Log the request
    logger.info('Creating item', {
      name: validated.name,
      source: request.headers.get('referer'),
    });
    
    // Create item
    const item = await createItem(validated);
    
    // Return created resource
    return Response.json(
      { data: item },
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
// app/actions/items.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';
import { db } from '@/lib/db';

const itemSchema = z.object({
  name: z.string().min(2),
  description: z.string().optional(),
});

export async function createItemAction(data: unknown) {
  try {
    // Validate input
    const validated = itemSchema.parse(data);
    
    // Create item
    const { data: item, error } = await db
      .from('items')
      .insert(validated)
      .select()
      .single();
      
    if (error) throw error;
    
    // Revalidate cache
    revalidatePath('/items');
    
    return { success: true, item };
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

# Redis
UPSTASH_REDIS_URL=...
UPSTASH_REDIS_TOKEN=...

# Analytics
ANALYTICS_KEY=...
ANALYTICS_URL=...

# Error Tracking
SENTRY_DSN=...

# External APIs
EXTERNAL_API_KEY=...
EXTERNAL_API_URL=...

# Feature Flags
NEXT_PUBLIC_ENABLE_FEATURE_X=true
```

## Testing Setup

```typescript
// __tests__/api/items.test.ts
import { createMocks } from 'node-mocks-http';
import { POST } from '@/app/api/v1/items/route';

describe('/api/v1/items', () => {
  it('creates an item successfully', async () => {
    const { req } = createMocks({
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: {
        name: 'Test Item',
        description: 'Test Description',
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
        name: 'A', // Too short
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
    "app/api/v1/*/route.ts": {
      "maxDuration": 10
    }
  },
  "crons": [
    {
      "path": "/api/cron/cleanup",
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
        [SemanticResourceAttributes.SERVICE_NAME]: 'api-service',
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

## API Documentation

```typescript
// app/api/v1/docs/route.ts
export async function GET() {
  const documentation = {
    version: '1.0.0',
    endpoints: [
      {
        path: '/api/v1/items',
        methods: ['GET', 'POST'],
        description: 'Manage items',
      },
      // Add more endpoints
    ],
  };
  
  return Response.json(documentation);
}
```