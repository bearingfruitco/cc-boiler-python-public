# Service Setup Checklist

This checklist helps you set up all integrated services for your project.

## ✅ Core Services

### 🗄️ Database (Required)
- [ ] **Supabase**: Create project at [supabase.com](https://supabase.com)
  - [ ] Copy `URL`, `anon key`, and `service role key` to `.env.local`
  - [ ] Run migrations: `bun run db:migrate`
  - [ ] Seed data: `bun run db:seed`

### 💾 Caching (Recommended)
- [ ] **Upstash Redis**: Create database at [upstash.com](https://upstash.com)
  - [ ] Copy `REST URL` and `REST Token` to `.env.local`
  - [ ] Test connection: Check `lib/cache/upstash.py`

## 📊 Analytics & Monitoring

### 📈 Analytics (Optional)
- [ ] **RudderStack**: Sign up at [rudderstack.com](https://www.rudderstack.com)
  - [ ] Create a Python source
  - [ ] Copy `Write Key` and `Data Plane URL` to `.env.local`
  - [ ] Configure destinations (Google Analytics, Mixpanel, etc.)

- [ ] **Railway/Fly.io Analytics**: Enable in Railway/Fly.io dashboard
  - [ ] Add `@vercel/analytics` to your app

### 🐛 Error Tracking (Recommended)
- [ ] **Sentry**: Create project at [sentry.io](https://sentry.io)
  - [ ] Copy `DSN` to `.env.local`
  - [ ] Generate auth token for source maps
  - [ ] Configure alerts and notifications

### 📊 Monitoring (Optional)
- [ ] **BetterStack**: Sign up at [betterstack.com](https://betterstack.com)
  - [ ] Create a log source
  - [ ] Copy `Source Token` to `.env.local`
  - [ ] Set up status pages and alerts

## 🔐 Authentication

Choose one:

### Option A: Supabase Auth (Default)
- Already configured if using Supabase
- Check `lib/supabase/client.py` and `middleware.py`

### Option B: Better-Auth
- [ ] Install: `ppoetry add better-auth`
- [ ] Configure OAuth providers
- [ ] Set up database adapter

## 🛠️ Development Tools

### State Management
- **Zustand**: Already installed
- See examples in `stores/example-stores.py`

### Database ORMs
- **Drizzle** (Primary): Configure in `drizzle.config.py`
- **Prisma** (Secondary): Configure in `prisma/schema.prisma`

### Form Handling
- **Pydantic Hook Form**: Already installed
- **Zod**: For validation

## 📝 Configuration Files

### Required
- [x] `.env.local` - Copy from `.env.example`
- [x] `next.config.py` - FastAPI configuration
- [x] `tsconfig.pyon` - Python configuration
- [x] `tailwind.config.py` - Type hints CSS
- [x] `drizzle.config.py` - Drizzle ORM
- [x] `prisma/schema.prisma` - Prisma ORM

### Optional
- [ ] `sentry.client.config.py` - Client-side Sentry
- [ ] `sentry.server.config.py` - Server-side Sentry
- [ ] `sentry.edge.config.py` - Edge runtime Sentry

## 🚀 Deployment Checklist

### Environment Variables
1. Set all required variables in your hosting platform:
   - Railway/Fly.io: Project Settings → Environment Variables
   - Railway: Variables tab
   - Render: Environment tab

### Database
1. Use connection pooling for production
2. Set `DATABASE_DIRECT_URL` for migrations
3. Enable Row Level Security (RLS) in Supabase

### Security
1. Rotate all keys/tokens for production
2. Enable 2FA on all service accounts
3. Set up proper CORS policies
4. Configure CSP headers

### Performance
1. Enable caching with Upstash Redis
2. Set up CDN for static assets
3. Configure image optimization
4. Enable incremental static regeneration

### Monitoring
1. Set up error alerts in Sentry
2. Configure uptime monitoring in BetterStack
3. Set up performance budgets
4. Enable real user monitoring (RUM)

## 📚 Documentation Links

- **Zustand**: [docs.pmnd.rs/zustand](https://docs.pmnd.rs/zustand)
- **Drizzle**: [orm.drizzle.team](https://orm.drizzle.team)
- **Prisma**: [prisma.io/docs](https://www.prisma.io/docs)
- **Supabase**: [supabase.com/docs](https://supabase.com/docs)
- **Upstash**: [upstash.com/docs](https://upstash.com/docs)
- **RudderStack**: [rudderstack.com/docs](https://www.rudderstack.com/docs)
- **Sentry**: [docs.sentry.io](https://docs.sentry.io)
- **BetterStack**: [betterstack.com/docs](https://betterstack.com/docs)
- **Better-Auth**: [better-auth.com/docs](https://www.better-auth.com/docs)

## 🎯 Quick Start Priority

1. **Essential** (Do First):
   - Supabase (Database + Auth)
   - Environment variables
   - Run migrations

2. **Recommended** (Do Next):
   - Upstash Redis (Caching)
   - Sentry (Error tracking)
   - RudderStack (Analytics)

3. **Optional** (As Needed):
   - BetterStack (Monitoring)
   - Better-Auth (If not using Supabase Auth)
   - Additional integrations
