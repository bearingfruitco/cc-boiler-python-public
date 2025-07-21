# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# CLAUDE.md - AI Agent Instructions with Hooks Integration

This file contains persistent instructions for Claude Code agents working on this project.
The hooks system enforces many of these rules automatically.

## 🚨 CRITICAL RULES (Enforced by Hooks)

### ALWAYS

1. **ALWAYS test before claiming fixes** - "Actually Works" protocol enforced
2. **ALWAYS use design system tokens** - Only text-size-[1-4], font-regular/semibold
3. **ALWAYS sync before editing** - GitHub pull happens automatically
4. **ALWAYS save work state** - Auto-saves every 60 seconds to GitHub
5. **ALWAYS check team activity** - Conflicts detected in real-time
6. **ALWAYS handle PII server-side** - All sensitive data processing on backend only
7. **ALWAYS encrypt PII fields** - Automatic field-level encryption for sensitive data
8. **ALWAYS audit log PII access** - Every access to sensitive data is logged
9. **ALWAYS use event queue for non-critical ops** - Analytics, tracking, webhooks async
10. **ALWAYS show loading states** - Every async operation needs user feedback

### NEVER

1. **NEVER use forbidden CSS** - text-sm, text-lg, font-bold BLOCKED
2. **NEVER use non-4px spacing** - p-5, m-7, gap-5 BLOCKED
3. **NEVER overwrite team work** - Conflicts warned before they happen
4. **NEVER lose work** - Everything backed up to GitHub gists
5. **NEVER claim "should work"** - Must verify with actual testing
6. **NEVER log PII to console** - Hook blocks console.log with sensitive data
7. **NEVER store PII client-side** - No localStorage/sessionStorage for PII
8. **NEVER put PII in URLs** - No email/phone/SSN in query parameters
9. **NEVER expose raw PII** - Always mask sensitive fields in UI
10. **NEVER skip consent** - TCPA/GDPR consent required for data collection
11. **NEVER block form submission on tracking** - Use async event queue
12. **NEVER use sequential awaits for parallel ops** - Use Promise.all()

## 📋 Core Coding Principles

1. **Test Everything** - The "Actually Works" protocol is enforced
   - Run the code before claiming it's fixed
   - See the actual output with your own observation
   - Check for errors in console/logs
   - Would you bet $100 it works?

2. **Design System Compliance** - Automatically enforced
   - 4 font sizes only (text-size-1 through 4)
   - 2 font weights only (font-regular, font-semibold)
   - 4px spacing grid (all spacing divisible by 4)
   - 60/30/10 color distribution

3. **Evidence-Based Development** - Claims require proof
   - **NEVER say**: "best", "optimal", "faster", "secure" without evidence
   - **ALWAYS say**: "testing shows", "metrics indicate", "benchmarks reveal"
   - **Examples**:
     - ❌ "This is the best approach"
     - ✅ "Testing shows this approach reduces load time by 40%"
     - ❌ "This is more secure"
     - ✅ "Security scan confirms 0 OWASP vulnerabilities"
     - ❌ "Optimized for performance"
     - ✅ "Profiling shows 2x throughput improvement"

4. **Team Collaboration** - Hooks handle coordination
   - Auto-sync with GitHub before edits
   - Warn about conflicts with team members
   - Share knowledge automatically
   - Perfect handoffs via state persistence

## 🤖 CodeRabbit Integration (v2.3.4)

### Dual-AI Development Workflow

You now work with CodeRabbit IDE extension for real-time code review:

**Your Role (Claude Code)**: Generate code fast, implement features
**CodeRabbit's Role**: Review quality, catch bugs, enforce standards

**The Workflow**:
1. You generate code in Cursor
2. CodeRabbit reviews in real-time
3. Fix issues before they reach git
4. Commit clean code
5. `/pr-feedback` for final check

**Benefits**:
- 95% of bugs caught before commit
- Design violations highlighted immediately
- Educational feedback improves coding
- Faster PR approvals (already clean)

## 🚀 Workflow Enhancement (v2.3.1)

### No More "Can I Edit This File?" Interruptions!

The system now auto-approves safe operations so you can work uninterrupted:

**Auto-Approved Operations:**
- ✅ Reading any file or directory
- ✅ Editing test files (/tests/, *.test.ts, *.spec.js)
- ✅ Running safe commands (npm test, lint, typecheck)
- ✅ Checking file info and searching

**Still Requires Approval:**
- 🔐 Editing production code
- 🔐 Database operations
- 🔐 Git commits and pushes
- 🔐 Installing packages

This means you can start a task, go grab coffee, and come back to completed work instead of permission prompts!

## 🤖 How Hooks Help You

### Pre-Tool-Use Hooks (Before You Edit)
- **00-auto-approve-safe-ops**: Auto-approves read operations and test edits
- **01-collab-sync**: Pulls latest changes automatically
- **02-design-check**: Blocks design violations with auto-fix
- **03-conflict-check**: Warns if team member is editing
- **04-actually-works**: Prevents untested claims
- **08-async-patterns**: Detects async anti-patterns (NEW)
- **08-evidence-language**: Ensures claims have evidence
- **09-auto-persona**: Suggests best persona for task

### Post-Tool-Use Hooks (After You Edit)
- **01-state-save**: Backs up to GitHub every 60 seconds
- **02-metrics**: Tracks design compliance over time

### Notification Hooks (When You Need Input)
- **team-aware**: Shows who's doing what
- **smart-suggest**: Recommends relevant commands

### Stop Hooks (Session End)
- **save-state**: Final backup with summary
- **knowledge-share**: Extracts patterns for team
- **handoff-prep**: Creates handoff documentation

## 📁 Project Structure (Enforced)

```
/app              # Next.js app directory
/components
  /ui            # Base UI components
  /forms         # Form components  
  /layout        # Layout components
  /features      # Feature-specific
/lib
  /api           # API utilities
  /db            # Database utilities
  /events        # Event queue system (NEW)
/hooks           # Custom React hooks
/.claude
  /hooks         # Hook scripts
  /team          # Team coordination
  /commands      # Custom commands
```

## 🔒 Security & Data Protection

### Form Data Handling

1. **Field Registry System**
   - All fields defined in `/field-registry/`
   - Core tracking fields auto-captured
   - PII fields marked and encrypted
   - Compliance rules enforced

2. **Secure Form Creation**
   ```bash
   /create-tracked-form ContactForm --vertical=debt
   ```
   - Generates secure form with tracking
   - PII protection built-in
   - Server-side processing only
   - Audit logging included

3. **Prepopulation Rules**
   - ONLY these fields can be prepopulated from URLs:
     - utm_source, utm_medium, utm_campaign
     - gclid, fbclid, ttclid
     - partner_id, campaign_id
   - NO PII in URLs ever

4. **Data Flow Security**
   ```
   URL Params → Whitelist Check → Sanitization → Form
        ↓                                              ↓
   Block PII                                    Server-Side Only
   ```

5. **Audit Requirements**
   - Every form submission logged
   - PII access tracked
   - Consent recorded
   - Retention policies enforced

## ⚡ Async & Event-Driven Architecture

### Event Queue System

1. **Core Principle**: Don't block the user
   ```typescript
   // ❌ BAD: Blocks form submission
   await trackToGoogle(data);
   await trackToFacebook(data);
   await sendWebhook(data);
   
   // ✅ GOOD: Fire and forget
   eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
   ```

2. **Event Pattern Usage**
   ```typescript
   import { eventQueue, LEAD_EVENTS } from '@/lib/events';
   
   // Critical path (must complete)
   await eventQueue.emit('validation.required', data, { async: false });
   
   // Non-critical (fire and forget)
   eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, data);
   ```

3. **Form Integration**
   ```typescript
   // Use the hook for automatic event tracking
   const { trackFormSubmit, trackSubmissionResult } = useLeadFormEvents('form-name');
   
   const onSubmit = async (data) => {
     const startTime = await trackFormSubmit(data); // Critical
     
     try {
       const result = await api.submit(data); // Critical
       trackSubmissionResult(true, startTime); // Non-blocking
     } catch (error) {
       trackSubmissionResult(false, startTime); // Non-blocking
     }
   };
   ```

4. **Loading States Required**
   ```typescript
   // Every async operation needs feedback
   import { LoadingState, ErrorState } from '@/components/ui/async-states';
   
   if (isLoading) return <LoadingState message="Processing..." />;
   if (error) return <ErrorState error={error} retry={handleRetry} />;
   ```

5. **Parallel Operations**
   ```typescript
   // ✅ Load independent data in parallel
   const [user, preferences, permissions] = await Promise.all([
     fetchUser(id),
     fetchPreferences(id),
     fetchPermissions(id)
   ]);
   
   // ❌ Don't await sequentially
   const user = await fetchUser(id);
   const preferences = await fetchPreferences(id);
   ```

6. **Timeout Protection**
   ```typescript
   // All external calls need timeouts
   const controller = new AbortController();
   const timeoutId = setTimeout(() => controller.abort(), 5000);
   
   try {
     const response = await fetch(url, { signal: controller.signal });
   } finally {
     clearTimeout(timeoutId);
   }
   ```

### Event Types

- **Lead Events**: Form interactions, submissions, tracking
- **Analytics Events**: Page views, actions, conversions
- **System Events**: Errors, performance, monitoring

### Commands for Async

- `/create-event-handler` - Create event handler with retry logic
- `/prd-async` - Add async requirements to PRD
- `/validate-async` - Check async pattern compliance
- `/test-async-flow` - Test event chains

## 🧪 Testing Requirements

Before saying "fixed" or "should work":

1. **For UI Changes**
   - Actually render the component
   - Click buttons/interact with it
   - Check browser console for errors
   - Verify responsive behavior

2. **For API Changes**
   - Make the actual API call
   - Verify response format
   - Check error handling
   - Test edge cases

3. **For Logic Changes**
   - Run the specific scenario
   - Log intermediate values
   - Verify expected output
   - Test failure paths

4. **For Async Operations**
   - Test timeout scenarios
   - Verify loading states
   - Check error recovery
   - Test parallel execution

## 📝 Documentation (Auto-Generated)

The hooks system automatically documents:
- Component patterns (when created)
- Bug fixes and solutions (when solved)
- Design compliance metrics
- Team knowledge base

Manual documentation still needed for:
- Business logic decisions
- Architecture changes
- API documentation
- Feature specifications

## 📚 Research Management System (NEW v2.3.5)

When you create analysis/planning documents:
- **Hook detects research docs** automatically
- **Checks for existing similar docs** to prevent duplicates  
- **Updates existing research** instead of creating new versions
- **Organizes in .claude/research/** not project root
- **Manual context inclusion** to prevent overload

**Workflow:**
```bash
# Create analysis doc: ./auth-analysis.md
# Hook detects and prompts

# Review pending docs
/research review

# If updating existing:
> Update existing document (merge changes)
# Intelligently merges based on doc type

# Search later
/research search "authentication"

# Add to context when needed
/research context add "auth analysis" --summary
```

**Benefits:**
- No more auth-v1, auth-v2, auth-final versions
- One living document per topic
- Clean project root
- Searchable knowledge base

## 🚀 Command Enhancements

Your commands are enhanced by hooks:
- `/cc` - Validates design before creating
- `/vd` - Uses accumulated metrics
- `/checkpoint` - Auto-saves to GitHub
- `/sr` - Shows team activity
- `/fw` - Coordinates with team
- `/research` - Manage internal research docs (NEW)

## ⚡ Quick Reminders

1. **You're not alone** - Another agent may be working too
2. **Design rules are enforced** - Don't fight the system
3. **Work is auto-saved** - Focus on coding, not backing up
4. **Testing is required** - "Should work" gets flagged
5. **Knowledge is shared** - Your solutions help the team
6. **Events are async** - Don't block the user experience

## 🎯 The Bottom Line

The hooks system handles the mechanics so you can focus on solving problems.
But remember:

- **Untested code is just a guess**
- **Design consistency matters**
- **Team coordination prevents waste**
- **Every session teaches something**
- **User experience is paramount**

Work with the system, not against it. The hooks are there to help you succeed.

---

*Remember: The user describing a bug for the third time isn't thinking "this AI is trying hard." They're thinking "why am I wasting my time with this tool?"*

## 🛠️ Development Commands

### Essential Commands to Run

```bash
# Development
pnpm dev              # Start development server with Turbopack
pnpm build            # Production build
pnpm start            # Start production server

# Testing & Quality
pnpm lint             # Run Biome linter
pnpm lint:fix         # Fix linting issues
pnpm typecheck        # TypeScript type checking
pnpm test             # Run unit tests with Vitest
pnpm test:watch       # Watch mode for tests
pnpm test:e2e         # Run E2E tests with Playwright
pnpm test:coverage    # Generate test coverage report

# Database (Drizzle - Primary ORM)
pnpm db:generate      # Generate migrations
pnpm db:push          # Push schema changes
pnpm db:studio        # Open Drizzle Studio

# Database (Prisma - Alternative)
pnpm prisma:generate  # Generate Prisma client
pnpm prisma:studio    # Open Prisma Studio
pnpm prisma:migrate   # Run migrations

# Analysis & Health
pnpm analyze          # Bundle analysis
pnpm check:all        # Run all checks (lint, typecheck, test)
pnpm check:health     # Health check script
```

### Running a Single Test
```bash
# Run specific test file
pnpm vitest path/to/test.spec.ts

# Run tests matching pattern
pnpm vitest -t "test name pattern"

# Debug test
pnpm vitest --inspect path/to/test.spec.ts
```

## 🚀 Essential Custom Commands

**ALWAYS start with:**
```bash
/sr    # Smart Resume - restores context from previous sessions
```

### Core Workflow Commands
- `/sr` - Smart Resume (ALWAYS run first)
- `/cp` - Context Profile (load/save work contexts)
- `/bt` - Bug Track (persistent bug tracking)
- `/fw` - Feature Workflow (start/complete GitHub issues)
- `/checkpoint` - Manual save progress to GitHub gist
- `/pr-feedback` - Quick PR status check (NEW in v2.3.4)

### PRD-Driven Development
- `/prd` - Create Product Requirements Document
- `/prd-tests` - Generate tests from PRD acceptance criteria
- `/prd-async` - Add async requirements to PRD (NEW)
- `/grade` - Score implementation alignment with PRD (0-100%)
- `/specs` - Extract and reuse successful patterns

### Development Helpers
- `/cc` - Create Component (enforces design system)
- `/ctf` - Create Tracked Form (with PII protection)
- `/create-event-handler` - Create async event handler (NEW)
- `/dc` - Doc Cache (cache external documentation)
- `/sv` - Stage Validate (enforce completion gates)
- `/orch` - Orchestrate (multi-agent task assignment)

### Quality Assurance
- `/vd` - Validate Design (check compliance)
- `/validate-async` - Validate async patterns (NEW)
- `/facts` - Find And Check Tailwind Styles
- `/research-docs` - Fetch and cache documentation

## 🏗️ Architecture Overview

### Tech Stack
- **Next.js 15.3.5** with App Router, Turbopack, PPR
- **React 19.1.0** with Server Components
- **TypeScript 5.8.3** in strict mode
- **Tailwind CSS v4.1.0** with strict design tokens
- **Supabase** for auth and database
- **Drizzle ORM** (primary) + Prisma (alternative)
- **SWR** + **TanStack Query** for data fetching
- **Zustand** for client state
- **Biome** for linting/formatting (replaces ESLint/Prettier)
- **Event Queue** for async operations (NEW)

### Key Directories
```
/app                  # Next.js App Router
  /api               # API routes with standardized handlers
/components          # UI components following design system
  /ui               # Base components (button, input, etc.)
  /forms            # Form components with tracking
  /layout           # Layout components
/lib                 # Core utilities
  /api              # API client utilities
  /db               # Database schema (Drizzle)
  /events           # Event queue system (NEW)
  /security         # PII encryption, audit logging
  /monitoring       # Sentry, Better Stack integration
/hooks               # Custom React hooks
/stores              # Zustand state stores
/field-registry      # Form field definitions with compliance
/.claude             # AI system configuration
  /commands         # 90+ custom commands
  /hooks            # Automation hooks
  /profiles         # Context profiles
  /specs            # Pattern library
```

## 🔄 PRD-Driven Development Workflow

1. **Project Idea** → Create PROJECT PRD
2. **Project PRD** → Generate GitHub Issues
3. **GitHub Issue** → Create FEATURE PRD
4. **Feature PRD** → Add async requirements
5. **Async PRD** → Generate implementation tasks
6. **Tasks** → Write code with design enforcement
7. **Code** → Grade against PRD (must score >80%)
8. **Approved** → Create PR
9. **PR Merged** → Deploy

### PRD Quality Enforcement
- Clarity linting catches vague language
- Measurable acceptance criteria required
- Async requirements documented
- Test cases generated from criteria
- Implementation graded objectively

## 🎯 Key Development Patterns

### Form Creation with Tracking
```bash
# Create a secure form with built-in tracking
/ctf ContactForm --vertical=debt

# This generates:
# - Form component with PII protection
# - Event tracking hooks
# - Server-side submission handler
# - Field-level encryption
# - Audit logging
# - TCPA/GDPR consent
```

### Component Creation
```bash
# Create component following design system
/cc Button --variant=primary

# Automatically:
# - Enforces design tokens
# - Adds to pattern library
# - Includes accessibility
```

### Bug Tracking Across Sessions
```bash
/bt add "User can't submit form"    # Track new bug
/bt list                           # See all active bugs
/bt resolve 1                      # Mark as fixed
# Bugs persist across sessions!
```

### CodeRabbit Integration
```bash
# Real-time in Cursor IDE
# Write code → See issues → Fix immediately

# For complex fixes:
# 1. Copy CodeRabbit suggestion
# 2. Paste to Claude: "Apply this fix: [suggestion]"
# 3. Claude implements the fix

# Final check before merge:
/pr-feedback
```

## 🔐 Security Patterns

### PII Handling
- All PII fields defined in `/field-registry/`
- Automatic encryption at field level
- Server-side processing only
- Audit log every access
- Never in URLs, console, or client storage

### Secure Data Flow
```
URL → Whitelist → Sanitize → Form → Server → Encrypt → Database
                                       ↓
                                  Audit Log
```

## 💡 Pro Tips

0. **CodeRabbit Workflow** - Let it review as you code:
   - See issues in Problems panel
   - One-click fix simple issues
   - Copy complex fixes to Claude
   - Commit only clean code

1. **Context Profiles** - Save work contexts:
   ```bash
   /cp save frontend-work    # Save current context
   /cp load frontend-work    # Restore later
   ```

2. **Stage Gates** - Enforce quality:
   ```bash
   /sv check                # Check current stage
   /sv require              # Block until complete
   ```

3. **Pattern Extraction** - Reuse success:
   ```bash
   /specs extract          # After successful implementation
   /specs apply           # Use in new features
   ```

4. **Multi-Agent Work** - Delegate tasks:
   ```bash
   /orch "Build user dashboard"
   # Automatically assigns to appropriate agents
   ```

5. **Documentation Caching** - Work offline:
   ```bash
   /dc add https://docs.example.com
   /dc search "authentication"
   ```

## 🚨 Common Pitfalls to Avoid

1. **Don't skip `/sr`** - Always restore context first
2. **Don't fight the hooks** - They're there to help
3. **Don't claim without testing** - "Should work" is flagged
4. **Don't ignore stage gates** - Quality checkpoints matter
5. **Don't forget to grade** - PRD alignment is measured
6. **Don't ignore CodeRabbit** - Fix issues before commit
7. **Don't commit without review** - Let CodeRabbit check first
8. **Don't block on tracking** - Use event queue for async

## 📊 Success Metrics

Your work is automatically tracked:
- Design system compliance score
- PRD alignment percentage
- Bug resolution rate
- Test coverage
- Performance benchmarks
- Event processing metrics

Aim for:
- 100% design compliance
- >80% PRD alignment
- <24hr bug resolution
- >80% test coverage
- <100ms event processing
