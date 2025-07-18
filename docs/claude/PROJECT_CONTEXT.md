# FreshSlate Project Context

## Project Type
Financial wellness quiz application with lead generation

## Core Design Rules
1. ONLY 4 font sizes: text-size-1 (32px), text-size-2 (24px), text-size-3 (16px), text-size-4 (12px)
2. ONLY 2 font weights: font-regular (400), font-semibold (600)
3. ALL spacing on 4px grid (p-1, p-2, p-3, p-4, p-6, p-8, p-12, p-16)
4. 60/30/10 color distribution
5. Mobile-first: 44px minimum touch targets (use h-11 or h-12)

## Available Documentation
- Design System: docs/design/design-system.md
- Design Rules Quick Reference: docs/design/design-rules-quick.md
- Components Guide: docs/design/components.md
- API Patterns: docs/technical/api-boilerplate.md
- Auth Guide: docs/development/auth-guide.md
- Data Fetching: docs/guides/data-fetching-guide.md
- State Management: docs/guides/state-management-guide.md
- Database/ORM: docs/guides/database-orm-guide.md
- Claude Code Instructions: docs/guides/claude-code-instructions.md

## Tech Stack
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS (with custom design tokens)
- Supabase (Auth + DB)
- React Query / TanStack Query
- React Hook Form + Zod
- Framer Motion
- Lucide React (icons)
- SWR (alternative to React Query)

## Project Structure
```
/app              # Next.js app directory
  /api           # API routes
    /lib         # API utilities
  /(public)      # Public routes
  /(protected)   # Auth-required routes
/components
  /ui            # Base UI components
  /forms         # Form components
  /layout        # Layout components
  /features      # Feature-specific components
/lib
  /api           # API client
  /db            # Database utilities
  /forms         # Form utilities
  /query         # React Query setup
  /supabase      # Supabase clients
  /utils         # Helper functions
/hooks
  /queries       # React Query hooks
/stores          # Zustand stores
/types           # TypeScript types
```

## Commands Available
Run `/help` to see all available Claude Code commands in the .claude/commands directory:
- /analyze-project - Analyze project structure
- /checkpoint - Save progress checkpoint
- /create-component - Create new component
- /validate-design - Check design system compliance
- /feature-workflow - Start new feature
- /todo - Manage tasks
- /work-status - Current work status

## Design System Compliance
EVERY component must follow these rules:
- ❌ NEVER use: text-sm, text-lg, text-xl, font-bold, p-5, p-7, m-5
- ✅ ALWAYS use: text-size-[1-4], font-regular/semibold, 4px grid spacing

## API Patterns
- All routes use withErrorHandler wrapper
- Validation with Zod schemas
- Consistent error responses
- Type-safe API client

## State Management
- Local state: useState
- Server state: React Query
- Global state: Zustand (sparingly)
- Form state: React Hook Form
- URL state: URLSearchParams
