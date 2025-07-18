# 📦 Dependency Management Guide

This guide tracks all dependencies, their latest versions, and installation instructions.

## 🔄 Last Updated: January 2025

> **Note**: Major update completed January 2025 based on comprehensive ecosystem research.
> See [PACKAGE_UPDATES_JAN_2025.md](./PACKAGE_UPDATES_JAN_2025.md) for detailed analysis.

## 📋 Core Dependencies

### Framework & Runtime

| Package | Current | Latest | Docs | Install |
|---------|---------|--------|------|---------|
| **Next.js** | 15.3.5 | [Check](https://www.npmjs.com/package/next) | [Docs](https://nextjs.org/docs) | `pnpm add next@^15.3.5` |
| **React** | 19.1.0 | [Check](https://www.npmjs.com/package/react) | [Docs](https://react.dev/) | `pnpm add react@^19.1.0 react-dom@^19.1.0` |
| **React DOM** | 19.1.0 | [Check](https://www.npmjs.com/package/react-dom) | [Docs](https://react.dev/) | Included above |
| **TypeScript** | 5.8.3 | [Check](https://www.npmjs.com/package/typescript) | [Docs](https://www.typescriptlang.org/) | `pnpm add -D typescript@^5.8.3` |

### Database & ORM

| Package | Current | Latest | Docs | Install |
|---------|---------|--------|------|---------|
| **Supabase** | 2.48.0 | [Check](https://www.npmjs.com/package/@supabase/supabase-js) | [Docs](https://supabase.com/docs) | `pnpm add @supabase/supabase-js @supabase/ssr` |
| **Drizzle ORM** | 0.44.0 | [Check](https://www.npmjs.com/package/drizzle-orm) | [Docs](https://orm.drizzle.team/) | `pnpm add drizzle-orm` |
| **Drizzle Kit** | 0.31.4 | [Check](https://www.npmjs.com/package/drizzle-kit) | [Docs](https://orm.drizzle.team/) | `pnpm add -D drizzle-kit@^0.31.4` |
| **Prisma** | 6.11.1 | [Check](https://www.npmjs.com/package/prisma) | [Docs](https://www.prisma.io/) | `pnpm add -D prisma@^6.11.1 @prisma/client@^6.11.1` |
| **Postgres** | 3.5.0 | [Check](https://www.npmjs.com/package/postgres) | [Docs](https://github.com/porsager/postgres) | `pnpm add postgres@^3.5.0` |
| **Upstash Redis** | 1.35.1 | [Check](https://www.npmjs.com/package/@upstash/redis) | [Docs](https://upstash.com/docs/redis) | `pnpm add @upstash/redis@^1.35.1` |

### State Management & Data Fetching

| Package | Current | Latest | Docs | Install |
|---------|---------|--------|------|---------|
| **TanStack Query** | 5.65.0 | [Check](https://www.npmjs.com/package/@tanstack/react-query) | [Docs](https://tanstack.com/query) | `pnpm add @tanstack/react-query` |
| **SWR** | 2.3.4 | [Check](https://www.npmjs.com/package/swr) | [Docs](https://swr.vercel.app/) | `pnpm add swr@^2.3.4` |
| **Zustand** | 5.0.6 | [Check](https://www.npmjs.com/package/zustand) | [Docs](https://zustand.docs.pmnd.rs/) | `pnpm add zustand@^5.0.6` |
| **Immer** | 10.1.1 | [Check](https://www.npmjs.com/package/immer) | [Docs](https://immerjs.github.io/immer/) | `pnpm add immer@^10.1.1` |

### UI & Styling

| Package | Current | Latest | Docs | Install |
|---------|---------|--------|------|---------|
| **Tailwind CSS** | 4.1.0 | [Check](https://www.npmjs.com/package/tailwindcss) | [Docs](https://tailwindcss.com/) | `pnpm add -D tailwindcss@^4.1.0 @tailwindcss/vite@^4.1.0` |
| **Framer Motion** | 12.23.3 | [Check](https://www.npmjs.com/package/framer-motion) | [Docs](https://motion.dev/) | `pnpm add framer-motion@^12.23.3` |
| **Lucide React** | 0.525.0 | [Check](https://www.npmjs.com/package/lucide-react) | [Docs](https://lucide.dev/) | `pnpm add lucide-react@^0.525.0` |
| **clsx** | 2.1.1 | [Check](https://www.npmjs.com/package/clsx) | - | `pnpm add clsx@^2.1.1` |
| **tailwind-merge** | 3.3.1 | [Check](https://www.npmjs.com/package/tailwind-merge) | - | `pnpm add tailwind-merge@^3.3.1` |

### Forms & Validation

| Package | Current | Latest | Docs | Install |
|---------|---------|--------|------|---------|
| **React Hook Form** | 7.60.0 | [Check](https://www.npmjs.com/package/react-hook-form) | [Docs](https://react-hook-form.com/) | `pnpm add react-hook-form@^7.60.0` |
| **@hookform/resolvers** | 5.1.1 | [Check](https://www.npmjs.com/package/@hookform/resolvers) | - | `pnpm add @hookform/resolvers@^5.1.1` |
| **Zod** | 4.0.5 | [Check](https://www.npmjs.com/package/zod) | [Docs](https://zod.dev/) | `pnpm add zod@^4.0.5` |

### Analytics & Monitoring

| Package | Current | Latest | Docs | Install |
|---------|---------|--------|------|---------|
| **Sentry** | 9.38.0 | [Check](https://www.npmjs.com/package/@sentry/nextjs) | [Docs](https://docs.sentry.io/platforms/javascript/guides/nextjs/) | `pnpm add @sentry/nextjs@^9.38.0` |
| **RudderStack** | 3.21.0 | [Check](https://www.npmjs.com/package/@rudderstack/analytics-js) | [Docs](https://www.rudderstack.com/docs/) | `pnpm add @rudderstack/analytics-js@^3.21.0` |
| **Vercel Analytics** | 1.5.0 | [Check](https://www.npmjs.com/package/@vercel/analytics) | [Docs](https://vercel.com/analytics) | `pnpm add @vercel/analytics@^1.5.0` |
| **Pino** | 9.7.0 | [Check](https://www.npmjs.com/package/pino) | [Docs](https://getpino.io/) | `pnpm add pino@^9.7.0` |
| **Pino Pretty** | 13.0.0 | [Check](https://www.npmjs.com/package/pino-pretty) | - | `pnpm add pino-pretty@^13.0.0` |

### Image & Security

| Package | Current | Latest | Docs | Install |
|---------|---------|--------|------|---------|
| **Sharp** | 0.34.3 | [Check](https://www.npmjs.com/package/sharp) | [Docs](https://sharp.pixelplumbing.com/) | `pnpm add sharp@^0.34.3` |
| **isomorphic-dompurify** | 2.26.0 | [Check](https://www.npmjs.com/package/isomorphic-dompurify) | - | `pnpm add isomorphic-dompurify@^2.26.0` |
| **dotenv** | 17.2.0 | [Check](https://www.npmjs.com/package/dotenv) | - | `pnpm add dotenv@^17.2.0` |

## 🛠️ Development Tools

| Package | Current | Latest | Docs | Install |
|---------|---------|--------|------|---------|
| **Biome** | 2.1.1 | [Check](https://www.npmjs.com/package/@biomejs/biome) | [Docs](https://biomejs.dev/) | `pnpm add -D --save-exact @biomejs/biome@2.1.1` |
| **Vitest** | 3.2.4 | [Check](https://www.npmjs.com/package/vitest) | [Docs](https://vitest.dev/) | `pnpm add -D vitest@^3.2.4` |
| **Playwright** | 1.50.0 | [Check](https://www.npmjs.com/package/@playwright/test) | [Docs](https://playwright.dev/) | `pnpm add -D @playwright/test@^1.50.0` |
| **Husky** | 9.2.0 | [Check](https://www.npmjs.com/package/husky) | [Docs](https://typicode.github.io/husky/) | `pnpm add -D husky@^9.2.0` |
| **Prettier** | 3.4.0 | [Check](https://www.npmjs.com/package/prettier) | [Docs](https://prettier.io/) | `pnpm add -D --save-exact prettier@3.4.0` |
| **Bundle Analyzer** | 4.10.2 | [Check](https://www.npmjs.com/package/webpack-bundle-analyzer) | - | `pnpm add -D webpack-bundle-analyzer@^4.10.2` |

## 📦 Package Managers

| Tool | Version | Install | Docs |
|------|---------|---------|------|
| **pnpm** | 10.0.0 | `npm install -g pnpm@10` | [Docs](https://pnpm.io/) |
| **Bun** | 1.2.18 | `curl -fsSL https://bun.sh/install \| bash` | [Docs](https://bun.sh/) |
| **npm** | Latest | Comes with Node.js | [Docs](https://docs.npmjs.com/) |

## 🔄 Update Commands

### Check for Updates
```bash
# Check outdated packages
pnpm outdated

# Interactive update
pnpm update -i

# Update all to latest
pnpm update --latest
```

### Install All Dependencies
```bash
# Install from package.json
pnpm install

# Install with exact versions
pnpm install --frozen-lockfile
```

### Clean Install
```bash
# Remove node_modules and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## ⚙️ Configuration Notes

### Why Tailwind with Vite?
We use `@tailwindcss/vite` because:
1. **Faster HMR** - Vite's hot module replacement is faster than PostCSS alone
2. **Better DX** - Instant style updates without full page reloads
3. **Next.js 15 Support** - Optimized for App Router and Server Components
4. **Tree Shaking** - Better optimization for production builds

### Package Manager Choice
We use **pnpm** as the primary package manager because:
- **Disk Space** - Shared dependencies save significant space
- **Speed** - Faster installs than npm/yarn
- **Strictness** - Prevents phantom dependencies
- **Monorepo Ready** - Excellent workspace support

### Version Pinning Strategy
- **Exact versions** for: Biome, Prettier (formatting consistency)
- **Caret ranges (^)** for: Most dependencies (get patches/minor updates)
- **Major version locks** for: Critical dependencies (React, Next.js)

## 📝 Maintenance Schedule

1. **Weekly**: Check for security updates
2. **Monthly**: Review and update patch versions
3. **Quarterly**: Evaluate major version updates
4. **Before Deploy**: Run `pnpm audit` for security check

## 🚨 Known Issues

- **React 19**: Some libraries may need updates for full React 19 compatibility
- **Tailwind 4**: Major version with breaking changes from v3
- **Node 22**: Ensure all dependencies support Node 22+

## 📚 Additional Resources

- [Tailwind Plus](https://tailwindcss.com/plus) - Premium components
- [shadcn/ui Pro](https://pro.shadcn.net/) - Pro component library
- [NestJS](https://nestjs.com/) - Alternative backend framework

---

Last verified: January 2025
