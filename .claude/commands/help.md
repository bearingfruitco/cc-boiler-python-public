# Help - Enhanced Command Reference

Show context-aware help for all commands and workflows.

## Usage

```bash
/help [topic]
/h [topic]     # short alias
/? [topic]     # shorter alias

# Topics: all, new, commands, workflows, aliases, prd, testing, security, context, existing
```

## 🆕 NEW FEATURES (Latest Updates)

### Test-Driven Development (v2.4.1) ✨
- **Automatic Test Generation** - Tests created at workflow trigger points
- **TDD Enforcement** - Can't write code without tests (configurable)
- **Smart Integration** - Tests auto-generate when:
  - Starting work on issue: `/fw start 123`
  - Processing tasks: `/pt feature-name`
  - Creating issue with tests: `/cti "Title" --tests`
- **Test-First Workflows** - `/chain tdd` or `/tdd` for complete TDD flow

### CodeRabbit Integration (v2.3.4)
- **Real-time code review** in Cursor/VSCode IDE
- `/pr-feedback` - Quick PR status check command
- **Dual-AI workflow** - Claude generates, CodeRabbit reviews
- **95% bug catch rate** before code reaches git

### Grove-Inspired Enhancements (v2.3.0)
- **PRD Clarity Linter** - Automatic ambiguity detection in requirements
- `/specs` - Extract and reuse successful specification patterns
- `/prd-tests` - Generate tests from PRD acceptance criteria
- `/grade` - Score implementation alignment with PRD (0-100%)

### Context Management & Optimization (v2.2.0)
- `/context-profile (cp)` - Manage focused context profiles for different work modes
- `/bug-track (bt)` - Persistent bug tracking across sessions
- `/doc-cache (dc)` - Cache external documentation locally
- `/stage-validate (sv)` - Enforce stage completion gates

### Truth & Existence Commands
- `/facts [category]` - Show established project values that cannot be changed
- `/exists [name]` - Check if component/function/route already exists
- `/truth` - Alias for /facts (see what's established)
- `/check` - Alias for /exists

### Field Registry Generation
- `/field-generate schemas` - Generate Zod validation from registry
- `/field-generate factories` - Generate test data factories
- `/field-generate masking` - Generate PII masking functions
- `/fg [type]` - Short alias for field-generate

### New Safety Chains
- `/chain safe-commit` - Validate before committing (facts → design → lint → test)
- `/chain field-sync` - Regenerate all field-based code
- `/chain pre-component` - Check before creating components

## 📚 Command Categories

### 1. Context & State Management
```bash
/smart-resume (sr)         # Restore full context
/checkpoint (cp)           # Save current state
/context-profile (cp)      # NEW: Manage context profiles
/context-grab (cg)         # Capture working context
/compress-context          # Reduce token usage
/compact-prepare          # Prepare for session end
```

### 2. PRD & Task Workflow
```bash
/create-prd (prd)         # Generate Product Requirements (with clarity linting)
/prd-tests                # NEW: Generate tests from acceptance criteria
/generate-tasks (gt)      # Break PRD into tasks
/process-tasks (pt)       # Work through tasks
/stage-validate (sv)      # Validate stage completion
/grade                    # NEW: Grade implementation vs PRD
/task-status (ts)         # View progress
/task-board (tb)          # Visual task view
/verify-task (vt)         # Confirm completion
```

### 3. Development Commands
```bash
/create-component (cc)    # Create validated component
/validate-design (vd)     # Check design compliance
/create-tracked-form (ctf) # Secure form with tracking
/bug-track (bt)           # Track bugs persistently
/exists [name]            # Check before creating
/facts [category]         # Show established values
/specs                    # NEW: Specification pattern library
```

### 4. Documentation & Research
```bash
/research-docs            # Research documentation
/doc-cache (dc)           # NEW: Cache docs locally
/generate-docs            # Generate project docs
```

### 5. Testing & Quality
```bash
/browser-test-flow (btf)  # Browser automation tests
/test-runner (tr)         # Run unit tests
/lint-check (lc)          # Biome linting
/audit-form-security (afs) # Security audit
```

### 6. Team & Collaboration
```bash
/feature-workflow (fw)    # GitHub issue workflow
/pr-feedback              # NEW: Quick PR status check
/work-status (ws)         # Team activity
/todo (td)                # Task management
/change-log               # Recent changes
```

### 7. Security & Compliance
```bash
/security-check (sc)      # Security audit
/audit-form-security      # Form security check
/field-generate           # Generate from registry
/facts env                # Show environment vars
```

### 8. Multi-Agent Orchestration
```bash
/orchestrate-agents (orch) # Start multi-agent work
/spawn-agent (spawn)      # Create specialized agent
/persona (p)              # Switch persona mode
/sub-agent-status (sas)   # Check agent progress
```

## 🔄 Enhanced Workflows

### Starting New Feature (With New Commands)
```bash
# 1. Create issue & set context
gh issue create --title "User Dashboard"
/context-profile create "dashboard-work"

# 2. Start feature
/fw start 23

# 3. Check what exists
/facts                    # See constraints
/exists Dashboard         # Check if exists

# 4. Create PRD & cache docs
/prd user-dashboard
/doc-cache cache "React Dashboard patterns"

# 5. Generate and process tasks
/gt user-dashboard
/pt user-dashboard

# 6. Stage validation
/stage-validate check 1   # Validate foundation

# 7. Safe development
/chain pre-component      # Before creating
/cc feature Dashboard     # Create component
/bug-track add "Issue with props" # Track any bugs

# 8. Complete stage
/stage-validate require 1 # Ensure stage complete
/chain safe-commit       # Before committing

# 9. Check PR status
/pr-feedback             # Quick status check

# 10. Complete feature
/btf dashboard
/fw complete 23
```

### Context-Aware Development
```bash
# Morning with profiles
/sr                              # Resume context
/context-profile load "auth-work" # Load focused context
/bug-track list --open           # Check open bugs
/stage-validate status           # Check progress

# Switching contexts
/context-profile save "auth-work"
/context-profile load "frontend-ui"

# Working with cached docs
/doc-cache search "useEffect"
/doc-cache show "React hooks" --section "useEffect"
```

### Bug Tracking Workflow
```bash
# When error occurs
/bug-track add "Render issue in AuthForm"

# During development  
/bug-track list --file AuthForm
/bug-track update bug_1234 --tag "props"

# When fixing
/bug-track resolve bug_1234 "Fixed prop types"
```

## 💡 Enhanced Command Aliases

### Grove Enhancements
- `specs` → spec-patterns
- `patterns` → spec-patterns
- `prd-tests` → prd-generate-tests
- `gen-tests` → prd-generate-tests
- `grade` → stage-validate-grade
- `alignment` → stage-validate-grade

### Context Management
- `cp` → context-profile
- `bt` → bug-track
- `dc` → doc-cache
- `sv` → stage-validate

### Most Used
- `sr` → smart-resume
- `cc` → create-component
- `vd` → validate-design
- `fw` → feature-workflow
- `prd` → create-prd
- `gt` → generate-tasks
- `pt` → process-tasks

### Safety Aliases
- `truth` → facts
- `check` → exists
- `fg` → field-generate
- `sc` → safe-commit (chain)
- `fs` → field-sync (chain)
- `pc` → pre-component (chain)

## 🛡️ Automatic Protections

### What Hooks Prevent (No Action Needed)
1. **Design violations** - Wrong CSS classes blocked
2. **PII exposure** - No sensitive data in logs
3. **Hydration errors** - SSR issues caught
4. **Import mistakes** - Path errors fixed
5. **Truth violations** - Can't change established values
6. **Accidental deletions** - Warnings before removal

## 📊 Quick Reference Card

```
CONTEXT MANAGEMENT      DAILY ESSENTIALS        STAGE CONTROL
/cp load frontend      /sr    - resume         /sv check 1
/bt list               /facts - constraints    /sv require 2
/dc search "hooks"     /ts    - tasks         /sv status

PRD WORKFLOW           TESTING                 FIELD REGISTRY
/prd   - create PRD    /btf - browser test    /fg schemas
/gt    - gen tasks     /tr  - unit test       /fg factories  
/pt    - process       /afs - security        /fg masking
/sv    - validate      /bt  - track bugs      
```

## 🚀 Getting More Help

```bash
/help workflows          # Detailed workflow guides
/help aliases           # All command shortcuts
/help new               # Latest features only
/help context           # Context management guide
/help [command]         # Specific command help
```

The system prevents common mistakes automatically - focus on building!