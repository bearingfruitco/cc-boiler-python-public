# Tech Stack & Versions

## Core Framework Versions

### Frontend
```json
{
  "next": "^15.0.0",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "typescript": "^5.8.0",
  "swr": "^2.2.0",
  "zustand": "^4.5.0"
}
```

### Database & Backend
```json
{
  "@supabase/supabase-js": "^2.39.0",
  "drizzle-orm": "^0.29.0",
  "drizzle-kit": "^0.20.0",
  "@prisma/client": "^5.7.0",
  "prisma": "^5.7.0",
  "postgres": "^3.4.0"
}
```

### Styling & UI
```json
{
  "tailwindcss": "^4.0.0",
  "framer-motion": "^10.16.0",
  "lucide-react": "^0.300.0"
}
```

### Premium UI Components (Optional)
**Note**: These are paid services for marketing/landing pages only. NOT for core application UI.

- **Tailwind UI Plus**: $299 - Marketing components and templates
- **shadcn/ui Pro**: $199 - Premium components and blocks
- **Catalyst UI**: $299 - Application UI kit

**Important**: 
- Your project should have its own design system
- Premium components should be adapted to match your design system
- Never use these component libraries as-is without modification
- Core application components must follow your project's design rules

### Forms & Validation
```json
{
  "react-hook-form": "^7.48.0",
  "@hookform/resolvers": "^3.3.4",
  "zod": "^3.22.0"
}
```

### State Management & Data Fetching
```json
{
  "swr": "^2.2.0",           // Data fetching with caching
  "zustand": "^4.5.0",       // State management
  "immer": "^10.0.3"         // Immutable state updates
}
```

**Why these additions?**
- **SWR**: Handles data fetching, caching, revalidation, and optimistic updates
- **Zustand**: Lightweight state management without the complexity of Context API
- **Immer**: Makes immutable updates easier in Zustand stores

### Analytics & Monitoring
```json
{
  "rudder-sdk-js": "^2.40.0",
  "@sentry/nextjs": "^7.99.0",
  "@vercel/analytics": "^1.1.0"
}
```

### Utilities
```json
{
  "@upstash/redis": "^1.27.0",
  "@tanstack/react-query": "^5.0.0",
  "sharp": "^0.33.0",
  "isomorphic-dompurify": "^2.9.0",
  "pino": "^8.17.0",
  "pino-pretty": "^10.3.0"
}
```

### Development Tools
```json
{
  "@biomejs/biome": "^1.5.0",
  "@playwright/test": "^1.40.0",
  "@testing-library/react": "^14.0.0",
  "@testing-library/jest-dom": "^6.2.0",
  "@testing-library/user-event": "^14.5.2",
  "@types/bun": "^1.0.0",
  "@types/node": "^20.10.0",
  "@types/react": "^18.2.0",
  "@types/react-dom": "^18.2.0",
  "husky": "^8.0.3",
  "prettier": "^3.0.0",
  "vitest": "^1.0.0",
  "webpack-bundle-analyzer": "^4.10.0"
}
```

## Runtime Requirements

### Node.js & Package Managers
```json
{
  "engines": {
    "node": ">=22.0.0",
    "bun": ">=1.0.0"
  },
  "packageManager": "pnpm@9.0.0"
}
```

### Required Services
- **Vercel**: Pro plan minimum for analytics and functions
- **Supabase**: Pro plan for production
- **Upstash Redis**: Pay-as-you-go for rate limiting and caching
- **BetterStack**: For monitoring and alerting
- **Sentry**: For error tracking

## Next.js 15 Specific Features

```typescript
// 1. App Router (not Pages Router)
app/
├── layout.tsx
├── page.tsx
└── api/

// 2. React Server Components by default
// Mark client components explicitly
'use client';

// 3. Server Actions
'use server';

// 4. Partial Prerendering
export const experimental_ppr = true;

// 5. React 19 features
use(); // New use() hook
```

## Environment Variables Required

```bash
# Next.js
NEXT_PUBLIC_APP_URL=

# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Database
DATABASE_URL=
DATABASE_POOL_URL=

# Redis
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=

# Analytics
NEXT_PUBLIC_RUDDERSTACK_KEY=
NEXT_PUBLIC_RUDDERSTACK_URL=

# Monitoring
SENTRY_DSN=
SENTRY_AUTH_TOKEN=
BETTERSTACK_API_KEY=
BETTERSTACK_SOURCE_TOKEN=

# Authentication
AUTH_SECRET=
AUTH_URL=

# Email
RESEND_API_KEY=
EMAIL_FROM=

# External APIs
OPENAI_API_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
```

## Database Stack

### Primary Database
- **Supabase PostgreSQL**: Main database with built-in auth
- **Drizzle ORM**: Type-safe queries and migrations
- **Prisma**: Alternative ORM for specific use cases

### Caching Layer
- **Upstash Redis**: Serverless Redis for caching and rate limiting
- **Vercel KV**: Alternative Redis solution (optional)

### Database Tools
```bash
# Drizzle commands
pnpm db:generate  # Generate SQL migrations
pnpm db:push     # Push schema to database
pnpm db:studio   # Visual database browser

# Prisma commands (if using)
pnpm prisma:generate  # Generate client
pnpm prisma:migrate   # Run migrations
pnpm prisma:studio    # Prisma Studio
```

## API Architecture

### REST API Routes
```typescript
// app/api/v1/[resource]/route.ts
export async function GET(request: NextRequest) {}
export async function POST(request: NextRequest) {}
export async function PUT(request: NextRequest) {}
export async function DELETE(request: NextRequest) {}
```

### Server Actions
```typescript
// app/actions/[action].ts
'use server';
export async function actionName() {}
```

### tRPC (Optional)
```json
{
  "@trpc/server": "^10.0.0",
  "@trpc/client": "^10.0.0",
  "@trpc/react-query": "^10.0.0"
}
```

## Authentication Options

### 1. Supabase Auth (Recommended)
- Built-in with Supabase
- Social logins supported
- Row Level Security integration

### 2. Better-Auth (Alternative)
```json
{
  "better-auth": "^1.0.0"
}
```

### 3. NextAuth.js (Legacy)
```json
{
  "next-auth": "^5.0.0-beta"
}
```

## Testing Stack

### Unit & Integration Tests
- **Bun Test**: Built-in test runner
- **Vitest**: Alternative test runner
- **Testing Library**: React component testing

### E2E Tests
- **Playwright**: Cross-browser testing
- **Cypress**: Alternative E2E framework

### Test Commands
```bash
pnpm test         # Run all tests
pnpm test:unit    # Unit tests only
pnpm test:e2e     # E2E tests
pnpm test:watch   # Watch mode
```

## Build & Deployment

### Build Tools
- **Turbopack**: Next.js 15 bundler (faster than Webpack)
- **SWC**: Rust-based compiler
- **PostCSS**: For Tailwind processing

### CI/CD Pipeline
- **GitHub Actions**: Primary CI/CD
- **Vercel**: Automatic deployments
- **Changesets**: Version management

### Performance Monitoring
- **Vercel Analytics**: Core Web Vitals
- **Sentry Performance**: Transaction monitoring
- **BetterStack**: Uptime monitoring

## Development Workflow

### Code Quality
```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --apply .",
    "format": "biome format --write .",
    "typecheck": "tsc --noEmit"
  }
}
```

### Git Hooks
- **Husky**: Pre-commit hooks
- **lint-staged**: Run linters on staged files
- **commitlint**: Enforce commit conventions

### IDE Setup
- **VS Code**: Recommended editor
- **Biome Extension**: For linting/formatting
- **Tailwind CSS IntelliSense**: For Tailwind
- **Prisma Extension**: For database

## Security Features

### Built-in Security
- **CSRF Protection**: Next.js built-in
- **CSP Headers**: Content Security Policy
- **Rate Limiting**: Via Upstash Redis
- **Input Validation**: Zod schemas

### Additional Security
```json
{
  "helmet": "^7.0.0",
  "jose": "^5.0.0",
  "bcryptjs": "^2.4.3"
}
```

## Performance Optimizations

### Image Optimization
- **Sharp**: Next.js image optimization
- **Cloudinary**: External image service (optional)

### Bundle Optimization
- **Dynamic Imports**: Code splitting
- **Tree Shaking**: Remove unused code
- **Minification**: Automatic in production

### Caching Strategy
- **ISR**: Incremental Static Regeneration
- **PPR**: Partial Prerendering (experimental)
- **SWR**: Client-side caching
- **Redis**: Server-side caching

## MCP (Model Context Protocol) Tools

Always available in Claude:
- **Supabase MCP**: Database queries and management
- **GitHub MCP**: Repository access and file operations
- **Memory MCP**: Persistent context storage

```typescript
// When using MCP tools, always specify:
// @mcp-tool: supabase
// @mcp-tool: github
```

## Project Structure

```
project-root/
├── app/                  # Next.js 15 App Router
│   ├── (public)/        # Public routes
│   ├── (protected)/     # Auth required routes
│   └── api/             # API routes
├── components/          # React components
│   ├── ui/             # Base UI components
│   └── features/       # Feature components
├── stores/             # Zustand stores (NEW)
├── hooks/              # Custom hooks
│   ├── queries/        # SWR query hooks (NEW)
│   └── mutations/      # SWR mutation hooks (NEW)
├── lib/                # Utilities
├── types/              # TypeScript types
├── public/             # Static assets
└── tests/              # Test files
```

## Quick Start Commands

```bash
# Setup
pnpm install
cp .env.example .env.local

# Development
pnpm dev

# Database
pnpm db:push
pnpm db:studio

# Testing
pnpm test
pnpm test:e2e

# Production
pnpm build
pnpm start
```

## Version Update Strategy

- **Weekly**: Security patches
- **Monthly**: Minor updates
- **Quarterly**: Major updates (with testing)
- **LTS Policy**: Stay on LTS versions when possible

## Breaking Changes to Watch

### Next.js 15
- App Router is default
- Server Components by default
- New caching behavior
- Turbopack improvements

### React 19
- New hooks (use, useFormStatus)
- Improved Server Components
- Better Suspense

### Tailwind CSS 4
- New engine (Oxide)
- Lightning CSS integration
- Faster builds

## Migration Notes

When updating from older versions:
1. Test in staging first
2. Check breaking changes
3. Update types
4. Run full test suite
5. Monitor errors post-deploy