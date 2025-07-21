# File Organization Safety Guide

## ✅ SAFE TO MOVE (Already moved - no dependencies)

### Documentation Files → `docs/` or `.claude/`
- `SYSTEM_OVERVIEW.md` → `docs/`
- `RELEASES.md` → `docs/`
- `RELEASE_SUMMARY_v2.3.6.md` → `docs/releases/`
- `GITHUB_RELEASE_PREP.md` → `docs/releases/`
- `FIX_SUMMARY.md` → `docs/updates/`
- `NEW_CHAT_CONTEXT.md` → `.claude/`
- `QUICK_REFERENCE.md` → `.claude/`
- `UPDATED_SYSTEM_PROMPT.md` → `.claude/docs/`

These are documentation files that are read by humans or accessed directly by path. No code dependencies.

### Test Files → `tests/`
- `test-imports.tsx` → `tests/`
- `test-setup.ts` → `tests/`

These were duplicates or test utilities.

## ❌ MUST STAY IN ROOT (Have dependencies)

### Configuration Files
- `sentry.client.config.ts` - Sentry SDK looks for these in root
- `sentry.edge.config.ts` - Sentry SDK looks for these in root  
- `sentry.server.config.ts` - Sentry SDK looks for these in root
- `next.config.js` - Next.js requires this in root
- `middleware.ts` - Next.js requires this in root
- `tailwind.config.js` - Tailwind looks for this in root
- `tsconfig.json` - TypeScript requires this in root
- `package.json` - npm/pnpm requires this in root
- All other config files (.env.example, biome.json, etc.)

### Important User-Facing Docs
- `README.md` - GitHub shows this on repo homepage
- `CHANGELOG.md` - Standard location for version history
- `CLAUDE.md` - AI agents look for this in root

## 📁 PROPER PROJECT STRUCTURE

```
boilerplate/
├── .claude/              # Claude Code specific files
│   ├── commands/         # Custom commands
│   ├── hooks/           # Pre/post hooks
│   ├── docs/            # Claude-specific docs
│   ├── NEW_CHAT_CONTEXT.md
│   └── QUICK_REFERENCE.md
├── app/                 # Next.js App Router
├── components/          # React components
├── lib/                 # Utilities and libraries
├── docs/               # Project documentation
│   ├── setup/
│   ├── workflow/
│   ├── technical/
│   ├── updates/
│   └── releases/
├── config/             # Additional configs (if needed)
├── tests/              # Test files
└── [root configs]      # All config files stay in root
```

## 🔧 NO ACTION NEEDED

The reorganization script already moved the safe files. The Sentry configs have been moved back to root where they belong. No broken dependencies!
