# Integration Setup Guide

This guide covers setup and configuration for all services in our stack.

## 📊 State Management

### Zustand
```typescript
// stores/example-store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface ExampleState {
  count: number;
  user: { name: string; email: string } | null;
  increment: () => void;
  setUser: (user: { name: string; email: string }) => void;
  reset: () => void;
}

export const useExampleStore = create<ExampleState>()(
  devtools(
    persist(
      immer((set) => ({
        count: 0,
        user: null,
        increment: () =>
          set((state) => {
            state.count += 1;
          }),
        setUser: (user) =>
          set((state) => {
            state.user = user;
          }),
        reset: () =>
          set((state) => {
            state.count = 0;
            state.user = null;
          }),
      })),
      {
        name: 'example-store',
      }
    )
  )
);
```

## 🗄️ Database

### Drizzle ORM (Primary)
Already configured in:
- `drizzle.config.ts` - Configuration
- `lib/db/schema.ts` - Schema definitions
- `lib/db/index.ts` - Client setup

Usage example:
```typescript
import { db, users } from '@/lib/db';
import { eq } from 'drizzle-orm';

// Query
const user = await db.select().from(users).where(eq(users.email, 'test@example.com'));

// Insert
await db.insert(users).values({
  email: 'new@example.com',
  name: 'New User',
});

// Update
await db.update(users).set({ name: 'Updated' }).where(eq(users.id, userId));
```

### Prisma (Secondary)
Already configured in:
- `prisma/schema.prisma` - Schema

Usage:
```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Query
const user = await prisma.user.findUnique({
  where: { email: 'test@example.com' },
});
```

## 🔐 Authentication

### Better-Auth (Alternative to Supabase Auth)
```bash
pnpm add better-auth
```

Create `lib/auth/better-auth.ts`:
```typescript
import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { db } from '@/lib/db';

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'postgresql',
  }),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
});
```

### Supabase Auth (Currently Configured)
Already set up in:
- `lib/supabase/client.ts`
- `lib/supabase/server.ts`
- `middleware.ts`

## 📊 Analytics

### RudderStack
Add to `.env.local`:
```env
NEXT_PUBLIC_RUDDERSTACK_KEY=your-write-key
NEXT_PUBLIC_RUDDERSTACK_DATA_PLANE_URL=https://your-dataplane.rudderstack.com
```

Create `lib/analytics/rudderstack.ts`:
```typescript
import { RudderAnalytics } from '@rudderstack/analytics-js';

export const analytics = new RudderAnalytics();

export function initAnalytics() {
  if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_RUDDERSTACK_KEY) {
    analytics.load(
      process.env.NEXT_PUBLIC_RUDDERSTACK_KEY,
      process.env.NEXT_PUBLIC_RUDDERSTACK_DATA_PLANE_URL,
      {
        integrations: { All: true },
        trackLifecycleEvents: true,
      }
    );
  }
}

// Usage
export function trackEvent(event: string, properties?: Record<string, any>) {
  if (typeof window !== 'undefined') {
    analytics.track(event, properties);
  }
}
```

## 🐛 Error Tracking

### Sentry
Already configured in `next.config.js` and package.json.

Create `sentry.client.config.ts`:
```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,
      maskAllInputs: true,
    }),
  ],
});
```

Create `sentry.server.config.ts`:
```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
});
```

Create `sentry.edge.config.ts`:
```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
});
```

## 📈 Monitoring

### BetterStack
Add to `.env.local`:
```env
BETTERSTACK_SOURCE_TOKEN=your-source-token
```

Create `lib/monitoring/betterstack.ts`:
```typescript
export async function logToBetterStack(
  level: 'info' | 'warn' | 'error',
  message: string,
  metadata?: Record<string, any>
) {
  if (!process.env.BETTERSTACK_SOURCE_TOKEN) return;

  try {
    await fetch('https://in.logs.betterstack.com', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.BETTERSTACK_SOURCE_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        level,
        message,
        ...metadata,
        timestamp: new Date().toISOString(),
      }),
    });
  } catch (error) {
    console.error('Failed to log to BetterStack:', error);
  }
}
```

## 💾 Caching

### Upstash Redis
Add to `.env.local`:
```env
UPSTASH_REDIS_REST_URL=your-url
UPSTASH_REDIS_REST_TOKEN=your-token
```

Create `lib/cache/upstash.ts`:
```typescript
import { Redis } from '@upstash/redis';

export const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

// Usage examples
export async function cacheGet<T>(key: string): Promise<T | null> {
  try {
    return await redis.get<T>(key);
  } catch (error) {
    console.error('Cache get error:', error);
    return null;
  }
}

export async function cacheSet(
  key: string,
  value: any,
  ttl?: number
): Promise<void> {
  try {
    if (ttl) {
      await redis.setex(key, ttl, value);
    } else {
      await redis.set(key, value);
    }
  } catch (error) {
    console.error('Cache set error:', error);
  }
}

export async function cacheDelete(key: string): Promise<void> {
  try {
    await redis.del(key);
  } catch (error) {
    console.error('Cache delete error:', error);
  }
}
```

## 🤖 Supabase AI Prompts

For SQL generation with Supabase AI:
```typescript
// Example: Generate migration
const prompt = `
Create a table for storing blog posts with:
- id (UUID, primary key)
- title (required)
- content (text)
- author_id (references users table)
- published (boolean, default false)
- created_at, updated_at timestamps
`;

// Use in Supabase Dashboard SQL Editor with AI assist
```

## 📊 dbt (Data Build Tool)

If using dbt with your data warehouse:

Create `dbt_project.yml`:
```yaml
name: 'your_project'
version: '1.0.0'
config-version: 2

profile: 'default'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["data"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

models:
  your_project:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

Create `profiles.yml`:
```yaml
default:
  outputs:
    dev:
      type: postgres
      host: localhost
      user: your_user
      password: your_password
      port: 5432
      dbname: your_database
      schema: analytics
      threads: 4
  target: dev
```

## 🔧 Environment Variables Summary

Add all these to `.env.local`:
```env
# Database
DATABASE_URL=postgresql://...
DATABASE_DIRECT_URL=postgresql://...

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# Redis (Upstash)
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...

# Analytics (RudderStack)
NEXT_PUBLIC_RUDDERSTACK_KEY=...
NEXT_PUBLIC_RUDDERSTACK_DATA_PLANE_URL=...

# Error Tracking (Sentry)
NEXT_PUBLIC_SENTRY_DSN=...
SENTRY_AUTH_TOKEN=...
SENTRY_ORG=...
SENTRY_PROJECT=...

# Monitoring (BetterStack)
BETTERSTACK_SOURCE_TOKEN=...

# Auth (if using Better-Auth)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# Environment
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 📚 Additional Resources

- [Zustand Docs](https://zustand.docs.pmnd.rs/getting-started/introduction)
- [Drizzle Guides](https://orm.drizzle.team/docs/guides)
- [Prisma Docs](https://www.prisma.io/docs)
- [Sentry Next.js](https://docs.sentry.io/platforms/javascript/guides/nextjs/)
- [Upstash Redis](https://upstash.com/docs/redis/overall/getstarted)
- [RudderStack](https://www.rudderstack.com/docs)
- [Better-Auth](https://www.better-auth.com/docs/introduction)
- [BetterStack](https://betterstack.com/docs/uptime/start/)
- [Supabase AI](https://supabase.com/docs/guides/getting-started/ai-prompts)
- [dbt](https://docs.getdbt.com/docs/introduction)
