# Complete Command Decision Guide - When to Use What (v2.5)

## 🎯 Enhanced Visual Decision Tree

```mermaid
graph TD
    Start([🚀 Start Here]) --> SR{Need Context?}
    SR -->|Always YES| SR_CMD[/sr + /tl]
    SR_CMD --> MainFlow{What are you doing?}
    
    MainFlow -->|🆕 New Project| NEW[/init-project or /py-prd]
    MainFlow -->|🐛 Bug Fix| BUG[/bt add → fix → /bt resolve]
    MainFlow -->|✨ Feature| KNOW{Know what to build?}
    MainFlow -->|🔬 Research| RESEARCH[/prp or /think-through]
    
    KNOW -->|YES ✅| CTI[/cti --tests]
    KNOW -->|NO ❓| PRP[/prp-create]
    
    CTI --> TASKS[/gt → /fw start → /pt]
    PRP --> PRPFLOW[/prp-execute → /prp-complete]
    
    style Start fill:#4CAF50,color:#fff
    style SR_CMD fill:#2196F3,color:#fff
    style CTI fill:#8BC34A,color:#fff
    style PRP fill:#FF9800,color:#fff
    style BUG fill:#f44336,color:#fff
```

### Quick Decision Tree (Text Version)
```
Start Here
    ↓
Need to see what you're working on?
    YES → /sr then /tl (ALWAYS start here!)
    NO ↓
    
Is this a new project/product?
    YES → /init-project or /py-prd
    NO ↓
    
Do you know exactly what needs to be done?
    NO → /prp (research needed) or /think-through
    YES ↓
    
Is it a bug or small fix?
    YES → /bt (bug track) or /mt (micro task)
    NO ↓
    
Is it a clear enhancement/feature?
    YES → /cti (capture to issue)
    NO ↓
    
Is it complex with multiple unknowns?
    YES → /prp (progressive research)
    NO → /prd (standard PRD)
```

## 📊 Command Complexity/Time Matrix

```
┌─────────────────────────────────────────────────────────┐
│                  COMPLEXITY vs TIME MATRIX              │
├─────────────────────────────────────────────────────────┤
│         │  < 30min  │  < 2hr   │  < 1day  │   > 1day   │
├─────────┼───────────┼──────────┼──────────┼────────────┤
│ Simple  │    /mt    │   /cti   │   /prd   │     -      │
│ Medium  │    /bt    │   /cti   │   /gt    │   /orch    │
│ Complex │     -     │/think-   │  /orch   │   /prp     │
│         │           │ through  │          │            │
└─────────┴───────────┴──────────┴──────────┴────────────┘
```

## 🔄 Visual Workflow Pipelines

```
📍 TDD Feature Flow (Automatic!)
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│  /cti  │ --> │  /gt   │ --> │  /fw   │ --> │  /pt   │
│--tests │     │ tasks  │     │ start  │     │process │
└────────┘     └────────┘     └────────┘     └────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
 Issue +       Tasks in      Tests auto-    TDD enforced
  Tests        Ledger        generated      completion

🔄 Daily Rhythm
┌─────────────────────────────────────────────────┐
│ Morning: /sr → /tl → /sync-main → pick work    │
│ Coding:  /fw start → /pt → /test → repeat      │
│ Evening: /checkpoint → /tl → handoff notes     │
└─────────────────────────────────────────────────┘
```

## 🗺️ Command Relationship Map

```
                    🎯 Core Commands
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    📝 Planning      🔨 Building      🧪 Quality
        │                 │                 │
    /py-prd           /py-agent         /test
    /prp              /py-api           /lint-fix
    /cti              /py-pipeline      /grade
    /gt               /pt               /verify
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                    📊 Tracking
                    /tl (ledger)
                    /ws (status)
                    /bs (branch)
```

## 🎯 Interactive Decision Helper

```
┌─────────────────────────────────────────────┐
│ QUICK COMMAND SELECTOR                      │
├─────────────────────────────────────────────┤
│ I need to...                               │
│                                             │
│ [✓] See what I'm working on     → /sr /tl  │
│ [ ] Fix a bug                   → /bt      │
│ [ ] Build new feature           → /cti     │
│ [ ] Research complex problem    → /prp     │
│ [ ] Quick 15-min fix           → /mt      │
│ [ ] Check if code exists       → /pyexists │
│ [ ] Run multiple agents        → /orch     │
│ [ ] Save my progress           → /checkpoint│
└─────────────────────────────────────────────┘
```

## 💨 Command Aliases Quick Reference

```
┌──────────────────────────────────┐
│        SPEED SHORTCUTS           │
├──────────────────────────────────┤
│ /sr     = smart-resume          │
│ /tl     = task-ledger           │
│ /fw     = feature-workflow      │
│ /prd    = py-prd                │
│ /gt     = generate-tasks        │
│ /pt     = process-tasks         │
│ /mt     = micro-task            │
│ /orch   = orchestrate-agents    │
│ /bt     = bug-track             │
│ /cti    = capture-to-issue      │
├──────────────────────────────────┤
│ 💡 Pro tip: Use tab completion! │
└──────────────────────────────────┘
```

---

## 📋 Command Categories & When to Use Them

### 0. Essential Daily Commands (NEW SECTION!)

#### `/sr` - Smart Resume ⭐⭐⭐
**When to use:**
- **EVERY TIME YOU START** - No exceptions!
- Resuming after any break
- Switching between projects
- After crashes or disconnects

**What it does:**
- Restores complete context
- Shows task ledger summary
- Displays current branch/issue
- Suggests next actions

**Flow:** `/sr` → see where you are → continue work

#### `/tl` - Task Ledger (NEW!) ⭐⭐
**When to use:**
- View all tasks across project
- Check progress on any feature
- See what's blocked
- Plan your day

**Example usage:**
```bash
/tl                    # View all tasks
/tl view user-auth     # Specific feature
/tl update user-auth   # Update progress
/tl link user-auth 23  # Link to issue
```

**What it shows:**
- All active features
- Progress percentages
- Issue links
- Status (Generated/In Progress/Completed/Blocked)

#### `/ws` - Work Status
**When to use:**
- Check current branch status
- See uncommitted changes
- View team activity
- Get comprehensive overview

**Includes:**
- Task ledger summary
- Git status
- Test results
- Blockers

---

### 1. Starting New Projects

#### `/init-project` - Brand New Project Setup
**When to use:**
- Starting a completely new repository
- Setting up boilerplate for the first time
- Creating initial project structure

**Example scenarios:**
- "I want to build a quiz application"
- "Starting a new SaaS product"
- "Creating a data pipeline project"

**Flow:** `/init-project` → `/gi PROJECT` → `/fw start [issue]`

#### `/py-prd [name]` - Python Project Requirements
**When to use:**
- Defining a new Python feature or system
- Planning a significant component
- Need structured requirements

**Example scenarios:**
- "Build a user authentication system"
- "Create a data processing pipeline"
- "Design an AI agent for customer service"

**Flow:** `/py-prd` → `/gi` → `/gt` → `/fw start`

---

### 2. Capturing Work & Ideas

#### `/cti [title]` - Capture to Issue ⭐
**When to use:**
- Claude gives you a detailed solution/plan
- You have a clear implementation path
- Specific enhancement or fix needed
- Don't want to lose AI recommendations

**Options:**
- `--tests` - Auto-generate tests (recommended!)
- `--type=api|agent|pipeline` - Specify type
- `--framework=fastapi|prefect` - Set framework

**Example scenarios:**
- "Fix these 112 missing fields"
- "Add validation to form inputs"
- "Implement the caching strategy Claude suggested"

**Flow:** `/cti --tests` → `/gt` → `/fw start` → `/pt`

#### `/prp [name]` - Progressive Research Plan
**When to use:**
- Complex problems with unknowns
- Need to research solutions
- Multiple approaches possible
- Multi-day exploration needed

**Example scenarios:**
- "Figure out how to deduplicate leads across sources"
- "Research ML approaches for lead scoring"
- "Design real-time analytics system"

**Flow:** `/prp-create` → `/prp-execute` → `/prp-status` → `/prp-complete`

---

### 3. Breaking Down Work

#### `/gi [PROJECT/feature]` - Generate Issues
**When to use:**
- Have a PRD ready
- Need to create GitHub issues from requirements
- Breaking project into trackable pieces

**Example scenarios:**
- After `/py-prd PROJECT`
- Converting PRD sections to issues
- Creating sprint backlog

**Flow:** `/py-prd` → `/gi` → assigns issue numbers

#### `/gt [feature]` - Generate Tasks (ENHANCED!)
**When to use:**
- Have an issue or feature to implement
- Need detailed task breakdown
- Want complexity estimates
- Planning implementation steps

**What's new:**
- ✅ Updates task ledger automatically
- ✅ Shows orchestration recommendations
- ✅ Links to GitHub issues
- ✅ Tracks in `.task-ledger.md`

**Example scenarios:**
- After `/cti` creates an issue
- Before starting complex feature
- Need to see if orchestration helps

**Flow:** `/cti` or `/gi` → `/gt` → check `/tl` → `/pt`

---

### 4. Day-to-Day Development

#### `/fw start [issue#]` - Feature Workflow Start (ENHANCED!)
**When to use:**
- Beginning work on a GitHub issue
- Starting new feature development
- Need branch and context setup

**What's new:**
- ✅ Auto-generates tests if missing
- ✅ Updates task ledger with issue link
- ✅ Enforces branch management rules
- ✅ Shows test status immediately

**Example scenarios:**
- "Start working on issue #17"
- "Begin user auth implementation"

**Flow:** `/fw start` → tests generated → work → `/fw complete`

#### `/fw test-status [issue#]` - Check TDD Progress (NEW!)
**When to use:**
- See which tests are passing/failing
- Check coverage for feature
- Verify TDD compliance

**Shows:**
- Test file location
- Pass/fail count
- Coverage percentage
- Next steps

#### `/pt [feature]` - Process Tasks (ENHANCED!)
**When to use:**
- Have tasks from `/gt`
- Ready to implement
- Working through task list

**What's new:**
- ✅ Updates task ledger progress
- ✅ Shows related test for each task
- ✅ Runs tests automatically
- ✅ Blocks completion until tests pass

**Flow:** `/gt` → `/pt` → see test → implement → test passes → next task

#### `/mt [description]` - Micro Task
**When to use:**
- Quick fixes (< 30 min)
- Small improvements
- One-off tasks
- No issue needed

**Example scenarios:**
- "Fix typo in README"
- "Update dependency version"
- "Add missing docstring"

**Flow:** `/mt` → implement → done

---

### 5. Bug Management

#### `/bt add [description]` - Bug Track
**When to use:**
- Found a bug
- Need to track issues
- Customer reported problem

**Example scenarios:**
- "Import script fails on empty fields"
- "Login timeout too short"
- "Data not saving correctly"

**Flow:** `/bt add` → `/bt assign` → fix → `/bt resolve`

#### `/bt list --open` - View Active Bugs
**When to use:**
- Morning standup
- Sprint planning
- Prioritizing work

---

### 6. Complex Features & Research

#### `/orch [feature]` - Orchestrate Multi-Agent
**When to use:**
- Complex feature (> 4 hours)
- Multiple domains involved
- Can parallelize work
- `/gt` shows orchestration benefit

**Example scenarios:**
- Full CRUD system
- Multi-step data pipeline
- Complex integrations

**Flow:** `/gt` → see orchestration recommendation → `/orch` → `/sas`

#### `/think-through [problem]` - Deep Analysis
**When to use:**
- Need to understand complex problem
- Exploring architecture decisions
- Weighing different approaches

**Example scenarios:**
- "How should we handle authentication?"
- "What's the best database design?"
- "Should we use microservices?"

**Flow:** `/think-through` → `/cti` → `/gt`

---

### 7. Testing & Quality

#### `/generate-tests [feature]` - Test Generation
**When to use:**
- Usually automatic with `/fw start`
- Manual test creation needed
- Adding tests to existing code
- Creating regression tests

**Options:**
- `--type=unit|integration|regression`
- `--source=issue|prd|code`

**Flow:** automatic or `/generate-tests` → `/test`

#### `/test` - Run Tests
**When to use:**
- After implementing features
- Before committing
- Verify changes work

**Options:**
- `--coverage` - Show coverage report
- `--watch` - Watch mode
- `--verbose` - Detailed output

**Flow:** implement → `/test` → `/fw complete`

#### `/lint-fix` or `/lint:fix` - Auto-fix Code Style (NEW!)
**When to use:**
- Before committing
- After major changes
- Fix formatting issues

**What it does:**
- Runs Black formatter
- Sorts imports with isort
- Fixes with Ruff
- Updates to standards

---

### 8. Python-Specific Development (NEW SECTION!)

#### `/py-agent [name]` - Create AI Agent
**When to use:**
- Building Pydantic-based agents
- Need structured AI interactions
- Creating specialized processors

**Options:**
- `--role=analyst|developer|reviewer`
- `--tools=pandas,matplotlib,duckdb`
- `--memory=true` (Redis backend)

**Flow:** `/pyexists` → `/py-agent` → tests auto-generated → implement

#### `/py-api [endpoint] [method]` - Create API Endpoint
**When to use:**
- Adding FastAPI endpoints
- Building REST APIs
- Need async handlers

**Example:**
```bash
/py-api /users/profile GET
/py-api /auth/login POST
```

**Flow:** `/pyexists` → `/py-api` → implement → `/test`

#### `/py-pipeline [name]` - Create Data Pipeline
**When to use:**
- Building Prefect workflows
- ETL processes
- Scheduled data tasks

**Flow:** `/py-pipeline` → configure → test → deploy

---

### 9. Code Safety & Dependencies (NEW SECTION!)

#### `/pyexists [name]` - Check Before Creating
**When to use:**
- **ALWAYS** before creating new components
- Prevents duplicates
- Saves time

**Example:**
```bash
/pyexists UserModel
/pyexists DataAnalystAgent
```

#### `/pydeps [action] [module]` - Dependency Management
**When to use:**
- Check what depends on a module
- Find circular dependencies
- Before refactoring

**Actions:**
- `check` - What uses this module
- `circular` - Find circular imports
- `breaking` - Check breaking changes
- `scan` - Full project analysis

**Example:**
```bash
/pydeps check auth
/pydeps circular
```

#### `/python-import-updater [old] [new]` - Update Imports
**When to use:**
- After moving/renaming modules
- Refactoring code structure
- Fixing broken imports

---

### 10. Branch & Feature Management (NEW SECTION!)

#### `/bs` - Branch Status
**When to use:**
- Check current branch info
- See uncommitted changes
- View branch age
- Check for conflicts

#### `/bsw [branch]` - Branch Switch
**When to use:**
- Switch between features
- Change context safely

**What it does:**
- Enforces one active branch
- Requires tests before switch
- Auto-stashes changes
- Updates context

#### `/fs` - Feature Status
**When to use:**
- Check specific feature progress
- See related tasks/tests
- View blockers

#### `/sync-main` - Sync with Main Branch
**When to use:**
- Before starting new work
- Weekly updates
- Before creating PR

---

### 11. Context & State Management

#### `/checkpoint [message]` - Save State
**When to use:**
- After major milestones
- Before risky changes
- End of work session
- Before switching tasks

**Example:**
```bash
/checkpoint "Completed auth module"
/checkpoint "Before refactoring"
```

#### `/context-profile save/load [name]` - Context Profiles
**When to use:**
- Switching between features
- Multiple projects
- Team handoffs

**Example:**
```bash
/context-profile save auth-work
/context-profile load payment-work
```

#### `/compress-context` - Optimize Tokens
**When to use:**
- Long conversations
- Token limit warnings
- Before complex discussions

---

### 12. Quality & Validation

#### `/validate-design` - Check Design Compliance (NEW!)
**When to use:**
- Before committing UI code
- After major changes
- PR preparation

**Checks:**
- Typography rules
- Spacing (4px grid)
- Color distribution
- Mobile compliance

#### `/grade` - Score Implementation
**When to use:**
- After completing feature
- Before PR
- Quality check

**Scores:**
- PRD alignment (0-100%)
- Test coverage
- Code quality
- Documentation

#### `/verify [feature]` - Verify Completion
**When to use:**
- Before marking done
- Final quality check
- PR preparation

**Levels:**
- `--level quick|standard|comprehensive`

---

## 🔄 Common Workflows (Updated)

### Morning Routine
```bash
/sr                  # Always start here
/tl                  # Check all tasks
/bt list --open      # Any bugs?
/sync-main           # Get latest
/fw test-status 23   # Check current work
```

### Simple Fix
```bash
/bt add "Import fails on null values"
/generate-tests import-null-fix --type=regression
# fix the bug
/test
/bt resolve [id]
```

### Feature from AI Suggestion
```bash
# Claude suggests implementation
/cti "Add caching layer to API" --tests
/gt caching-layer
/tl view caching-layer    # See in ledger
/fw start [issue#]
/pt caching-layer
/test
/fw complete [issue#]
```

### New Feature (Known Requirements)
```bash
/py-prd user-notifications
/gi user-notifications
/gt notification-system
/tl                       # Check ledger updated
/fw start [issue#]
/pt notification-system
/test
/fw complete [issue#]
```

### Complex Feature (Unknown Approach)
```bash
/prp lead-deduplication
/prp-execute
# ... research and experimentation ...
/prp-status
/prp-complete
/cti "Implement fuzzy matching dedup" --tests
/gt lead-dedup
/orch lead-dedup --agents=3
/sas                      # Monitor agents
```

### Brand New Project
```bash
/init-project
/gi PROJECT
/fw start 1
/gt [first-feature]
/pt [first-feature]
```

### Python Component Creation
```bash
/pyexists EmailService    # Check first!
/py-agent EmailAgent --role=processor --tools=smtp,templates
# Tests auto-generated
/pt email-agent
/test
```

### Safe Refactoring
```bash
/pydeps check user_model  # See dependencies
/checkpoint "Before refactor"
/pyexists NewUserModel
# refactor code
/python-import-updater user_model new_user_model
/test
/pydeps circular          # Verify no issues
```

---

## 💡 Decision Helpers

### Use CTI When:
- ✅ Solution is clear
- ✅ Implementation path known
- ✅ Scope is defined
- ✅ No research needed
- ✅ Claude gave you a plan
- ✅ **Always use --tests flag!**

### Use PRP When:
- ❓ Multiple unknowns
- ❓ Need to research options
- ❓ Complex architecture decisions
- ❓ Integration challenges
- ❓ "Figure out how to..."

### Use PRD When:
- 📋 New feature/component
- 📋 Need requirements doc
- 📋 Multiple stakeholders
- 📋 Want issues generated

### Use MT When:
- ⚡ Quick fix needed
- ⚡ No issue required
- ⚡ < 30 minutes work
- ⚡ Obvious solution

### Check Task Ledger When:
- 📊 Need overview of all work
- 📊 Planning your day
- 📊 Checking team progress
- 📊 Finding what to work on

---

## 🎯 Essential Daily Habits

1. **Always Start With:** `/sr` → `/tl`
2. **Before Creating:** `/pyexists [name]`
3. **Before Switching:** `/checkpoint` → `/bsw`
4. **Before Committing:** `/test` → `/lint-fix` → `/validate-design`
5. **End of Day:** `/tl` → `/checkpoint "EOD"`

---

## 🚀 Workflow Chains (Shortcuts)

Save time with predefined chains:

```bash
/chain tdd     (/tdd)    # Full TDD workflow
/chain pf      (/pf)     # Python feature
/chain pq      (/pq)     # Python quality check
/chain pr      (/pr)     # Python refactor
/chain ds      (/ds)     # Daily startup
/chain fc      (/fc)     # Feature complete
```

---

## 📊 Your Current Situation

For your LeadProsper import enhancement:
- ✅ You correctly used `/cti` because Claude analyzed and provided a clear plan
- ✅ Next: `/gt leadprosper-import-fix` or `/gt issue-17`
- ✅ Check: `/tl view leadprosper-import-fix` to see in ledger
- ✅ Then: `/fw start 17` (tests will auto-generate!)
- ✅ Finally: `/pt leadprosper-import-fix` (TDD enforced)

The task ledger will track your progress automatically!

---

## 🆕 New in v2.5

1. **Task Ledger** - Central task tracking
2. **Branch Management** - Safe switching
3. **Auto Test Generation** - TDD by default
4. **Python Commands** - Agent/API/Pipeline creation
5. **Dependency Tracking** - Know what uses what
6. **Design Validation** - UI compliance
7. **Import Management** - Safe refactoring
8. **Enhanced Suggestions** - Next steps always shown

Remember: The system now tracks EVERYTHING automatically. Focus on building, not bookkeeping!