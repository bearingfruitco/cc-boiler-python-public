# 🚀 Claude Code Boilerplate System - Entry Point

Welcome to the Claude Code boilerplate system. This document provides quick access to all documentation and key concepts.

## 📚 Documentation Map

### Core Documentation
- **[NEW_CHAT_CONTEXT.md](docs/claude/NEW_CHAT_CONTEXT.md)** - Start here for new sessions
- **[CLAUDE.md](CLAUDE.md)** - AI behavior rules and principles
- **[README.md](README.md)** - Project overview and quick start
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates

### Setup & Installation
- **[DAY_1_COMPLETE_GUIDE.md](docs/setup/DAY_1_COMPLETE_GUIDE.md)** - Complete setup walkthrough
- **[NEW_FEATURES_SETUP.md](docs/setup/NEW_FEATURES_SETUP.md)** - Bug tracking, context profiles, doc cache, stage gates
- **[QUICK_START_NEW_PROJECT.md](docs/setup/QUICK_START_NEW_PROJECT.md)** - Fast project setup
- **[ADD_TO_EXISTING_PROJECT.md](docs/setup/ADD_TO_EXISTING_PROJECT.md)** - Add to existing projects
- **[ENV_SETUP_GUIDE.md](docs/setup/ENV_SETUP_GUIDE.md)** - Environment configuration

### Development Guides
- **[DESIGN_SYSTEM.md](docs/design/design-system.md)** - Design rules and tokens
- **[DESIGN_RULES_QUICK.md](docs/design/design-rules-quick.md)** - Quick design reference
- **[COMPONENTS.md](docs/design/components.md)** - Component patterns
- **[AUTH_GUIDE.md](docs/development/auth-guide.md)** - Authentication setup
- **[DATA_FETCHING_GUIDE.md](docs/guides/data-fetching-guide.md)** - Data patterns
- **[STATE_MANAGEMENT_GUIDE.md](docs/guides/state-management-guide.md)** - State patterns
- **[DATABASE_ORM_GUIDE.md](docs/guides/database-orm-guide.md)** - Database setup

### Technical Documentation
- **[DEPENDENCY_MANAGEMENT.md](docs/technical/DEPENDENCY_MANAGEMENT.md)** - Package tracking
- **[PACKAGE_UPDATES_JAN_2025.md](docs/technical/PACKAGE_UPDATES_JAN_2025.md)** - 2025 updates
- **[PACKAGE_RECOMMENDATIONS.md](docs/technical/PACKAGE_RECOMMENDATIONS.md)** - Additional packages
- **[API_BOILERPLATE.md](docs/technical/api-boilerplate.md)** - API patterns
- **[TESTING_GUIDE.md](docs/guides/testing-guide.md)** - Testing strategies

### Claude-Specific
- **[CLAUDE_CODE_GUIDE.md](docs/claude/CLAUDE_CODE_GUIDE.md)** - Claude Code instructions
- **[AI_AGENT_DOCUMENTATION.md](docs/claude/AI_AGENT_DOCUMENTATION.md)** - AI agent patterns
- **[WORKFLOW_VISUAL_GUIDE.md](docs/claude/WORKFLOW_VISUAL_GUIDE.md)** - Visual workflows
- **[TRUTH_ENFORCEMENT_GUIDE.md](docs/claude/TRUTH_ENFORCEMENT_GUIDE.md)** - Protected values

### Security & Compliance
- **[SECURITY_GUIDE.md](docs/SECURITY_GUIDE.md)** - Security overview
- **[Field Registry README](field-registry/README.md)** - Data field management
- **[COMPLIANCE_GUIDE.md](docs/operations/COMPLIANCE_GUIDE.md)** - Regulatory compliance

### Team & Workflow
- **[COMMIT_CONTROL_GUIDE.md](docs/team/COMMIT_CONTROL_GUIDE.md)** - Git workflow
- **[HANDOFF_GUIDE.md](docs/team/HANDOFF_GUIDE.md)** - Team handoffs
- **[PROJECT_GUIDE.md](docs/workflow/PROJECT_GUIDE.md)** - Project workflow

### Quick References
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command cheat sheet
- **[NEW_PACKAGES_QUICK_REFERENCE.md](docs/technical/NEW_PACKAGES_QUICK_REFERENCE.md)** - Package quick start

## 🎯 Key System Features

### 1. Context Preservation & Management
- **Never lose work** - Auto-saves to GitHub every 60 seconds
- **Smart Resume** - `/sr` restores full context
- **Checkpoint System** - Manual saves with `/checkpoint`
- **Context Profiles** - `/cp` for focused work modes
- **Bug Tracking** - `/bt` persists across sessions
- **Doc Cache** - `/dc` for offline documentation

### 2. Design System (STRICT)
- **4 Font Sizes**: text-size-1 (32px), text-size-2 (24px), text-size-3 (16px), text-size-4 (12px)
- **2 Font Weights**: font-regular (400), font-semibold (600)
- **4px Grid**: ALL spacing divisible by 4
- **Enforced by Hooks**: Violations blocked automatically

### 3. PRD-Driven Development with Stage Gates
```bash
/prd feature-name     # Generate PRD with stage gates
/gt feature-name      # Generate tasks
/pt feature-name      # Process tasks
/sv check 1           # Validate stage completion
/ts                   # Task status
```

### 4. Multi-Agent System
- **9 Specialized Personas**: frontend, backend, security, qa, architect, performance, integrator, data, mentor
- **Parallel Development**: `/orch` coordinates multiple agents
- **3-5x Faster**: For complex features

### 5. Security First
- **Field Registry**: All data fields defined and protected
- **PII Detection**: Automatic blocking of sensitive data
- **Encryption**: Field-level encryption for sensitive data
- **Audit Logging**: Every access tracked

## 💻 Tech Stack

### Core Framework
- **Next.js 15.3.5** - App Router + Turbopack
- **React 19.1.0** - Latest React
- **TypeScript 5.8.3** - Strict mode
- **Tailwind CSS 4.1.0** - Custom design tokens

### Database & Auth
- **Supabase** - Auth + PostgreSQL
- **Drizzle ORM 0.44.0** - Type-safe ORM
- **Auth.js v5** - Authentication standard
- **Prisma 6.11.1** - Alternative ORM

### State & Data
- **TanStack Query 5.65.0** - Server state
- **Zustand 5.0.6** - Client state
- **SWR 2.3.4** - Data fetching alternative
- **Zod 4.0.5** - Validation

### Developer Experience
- **Turbopack** - 76.7% faster dev builds
- **Biome 2.1.1** - 15x faster than ESLint
- **Vitest 3.2.4** - Fast unit testing
- **Playwright** - E2E testing
- **MSW 2.7.0** - API mocking

### UI Components
- **Radix UI** - Headless primitives
- **Lucide React 0.525.0** - Icons
- **Framer Motion 12.23.3** - Animations
- **React Hook Form 7.60.0** - Forms

### Monitoring & Analytics
- **Sentry** - Error tracking
- **RudderStack** - Analytics
- **Vercel Analytics** - Performance

## 🛠️ MCP Integrations

Currently configured in `.mcp.json`:
- **GitHub** - Version control integration
- **Supabase** - Database operations
- **Puppeteer** - Browser automation
- **Brave Search** - Web search
- **Context7** - Library documentation
- **Prisma** - Database management
- **Sentry** - Error tracking

Additional MCPs available (disabled by default):
- Browserbase, Stagehand - Advanced browser automation
- Cloudflare - Observability & bindings
- Upstash - Redis caching
- Bright Data - Web scraping
- dbt - Data transformation

## 📦 Package Management

### Package Managers
- **pnpm 10.0.0** - Primary (enforced)
- **Bun 1.2.18** - Alternative runtime
- **npm** - Fallback only

### Key Dependencies Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [React 19 Docs](https://react.dev/reference/react)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Drizzle ORM Docs](https://orm.drizzle.team/docs)
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Zustand Docs](https://zustand.docs.pmnd.rs)
- [Vitest Docs](https://vitest.dev/guide/)
- [Playwright Docs](https://playwright.dev/docs/intro)

## 🚀 Quick Start Commands

```bash
# Start new session
/sr                    # Smart resume - ALWAYS FIRST!

# Development
/cc ComponentName      # Create component
/vd                    # Validate design
/fw start 123         # Start GitHub issue

# PRD Workflow (Enhanced)
/prd feature-name     # Create PRD with documentation requirements
/research-docs "tech1, tech2"  # Research documentation (NEW)
/gt feature-name      # Generate tasks
/pt feature-name      # Process tasks phase by phase
/compress-context     # Optimize tokens when needed
/compact-prepare      # Save state to GitHub

# Multi-Agent
/orch feature-name    # Orchestrate agents

# Safety
/facts                # Show protected values
/exists Component     # Check before creating
/chain safe-commit    # Validate before commit

# Help
/help                 # Show all commands
/help new            # Latest features
```

## 📋 Evaluation: OpenRouter & Pydantic

### OpenRouter
**Recommendation: NOT NEEDED** ❌

Reasons:
- Your boilerplate is for web applications, not AI/LLM integration
- OpenRouter is for routing LLM API calls (GPT-4, Claude, etc.)
- Would add unnecessary complexity for most projects
- Can be added project-specifically when needed

### Pydantic
**Recommendation: NOT NEEDED** ❌

Reasons:
- Pydantic is Python-specific for data validation
- Your boilerplate uses TypeScript with Zod for validation
- Zod (already included) provides the same functionality for TypeScript
- Would require Python runtime which conflicts with your JS/TS stack

## 🚀 PRP System Enhancement (Based on Analysis)

### Your Current Strengths
- ✅ 90+ commands (vs their ~4)
- ✅ Design system enforcement
- ✅ Security-first with field registry
- ✅ GitHub integration
- ✅ 9 specialized personas

### Key Enhancements Added
Based on analysis of other PRP systems, I've enhanced yours with:

1. **Documentation Research Phase** 
   - Added to PRD template (section 8)
   - New `/research-docs` command for multi-agent doc scraping
   - Focus on official documentation only

2. **Context Management** (You already had this!)
   - `/compress-context` - Optimizes tokens (existing)
   - `/compact-prepare` - Saves to GitHub (existing)
   - Their system uses these between phases, which is smart

3. **Phase-Based PRD Structure**
   - Enhanced PRD template with clear phases
   - Phase 1: Foundation/skeleton
   - Phase 2: Core features/production ready
   - Phase 3: Polish and optimization

### What Makes Your System Better
- **Comprehensive hooks** for safety and enforcement
- **Field registry** for security
- **90+ specialized commands** vs basic 4
- **GitHub integration** throughout workflow
- **Design system enforcement** automatic

### MCP-Related Dependencies
**Current Status: ADEQUATE** ✅

Your `.mcp.json` properly configures MCP servers. The actual MCP packages are installed globally via `npx` when needed, not as project dependencies. This is the correct approach.

## 🎯 Summary

Your boilerplate is well-architected with:
- ✅ Comprehensive documentation structure
- ✅ Proper MCP integration setup
- ✅ Right validation library (Zod for TypeScript)
- ✅ Lean philosophy (no unnecessary packages)
- ✅ Enhanced PRP system combining best of both approaches

The main valuable additions from their system were:
- Emphasis on documentation research before coding
- Using context management commands between phases
- Clear phase-based execution

All of these are now part of your enhanced system without breaking anything.
