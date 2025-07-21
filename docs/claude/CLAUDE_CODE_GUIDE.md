# 🚀 Claude Code Commands - Complete User Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Daily Workflow](#daily-workflow)
3. [Command Reference](#command-reference)
4. [Common Scenarios](#common-scenarios)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### First Time Setup
```bash
# For new projects
/onboard fresh
/init-project saas-dashboard "YourAppName"

# For existing projects
/onboard existing
/sr  # Smart resume to see current state
```

### Essential Aliases
- `/sr` → Smart Resume (start here every session)
- `/cc` → Create Component
- `/vd` → Validate Design
- `/fw` → Feature Workflow
- `/?` → Help

---

## Daily Workflow

### 🌅 Starting Your Day
```bash
# 1. Resume where you left off
/sr
# Shows: current branch, issue, TODOs, next steps

# 2. Optional: Run morning setup chain
/morning-setup
# Runs: smart-resume → security-check → test-runner
```

### 💻 During Development

#### Creating Components
```bash
# Basic component
/cc ui Button

# With options
/cc form LoginForm --with-tests --with-docs

# Component types:
# - ui: Base components (Button, Card, Input)
# - form: Form components (FormField, ValidationMessage)
# - layout: Layout components (Container, Header)
# - feature: Feature-specific (Dashboard, UserProfile)
```

#### Validating Design System
```bash
# Check current file
/vd

# Check everything
/vd all

# Watch mode (auto-check on save)
/vd --watch
```

#### Managing TODOs
```bash
# Add TODO
/todo add "Implement error handling" high

# View TODOs
/todo list          # Current file
/todo list issue    # Current issue
/todo list all      # Everything

# Complete TODO
/todo update complete todo-001
```

### 🔄 Feature Development

#### Starting a New Feature
```bash
# 1. Start feature from issue
/fw start 23
# Creates: branch, worktree, initial context

# 2. Work on feature
/cc ui ComponentName
/vd
/tr current  # Run tests

# 3. Save progress
/checkpoint create
/todo add "Continue tomorrow"
```

#### Resuming Work
```bash
# Don't know what you were working on?
/work-status list
# Shows all active work with progress

# Resume specific issue
/compact-prepare resume 23
# Restores complete context
```

### 📋 Before Creating PR

#### Pre-PR Checklist
```bash
# Run complete validation chain
/pp  # or /pre-pr
# Runs: validate → test → performance → security

# Or run individually
/vd all                    # Design validation
/tr all                    # All tests
/pm check                  # Performance check
/sc all                    # Security scan
```

#### Complete Feature
```bash
/fw complete 23
# Validates everything and creates PR
```

### 🌙 End of Day
```bash
# Save your progress
/checkpoint create end-of-day
/context-grab capture

# Optional: Generate daily report
/dr  # or /daily-report
```

---

## Command Reference

### 🧠 Context & Resume Commands

#### `/smart-resume` (alias: `/sr`)
**When to use:** First command every session
```bash
/sr         # Auto-detect what you need
/sr quick   # Just show current location
/sr full    # Complete context restoration
```

#### `/context-grab`
**When to use:** Save/restore working context
```bash
/context-grab capture    # Save current context
/context-grab restore    # Restore saved context
/context-grab auto       # Enable auto-capture
```

#### `/checkpoint`
**When to use:** Save progress milestones
```bash
/checkpoint create [name]    # Save checkpoint
/checkpoint restore [name]   # Restore checkpoint
/checkpoint list             # Show all checkpoints
```

### 🛠️ Development Commands

#### `/create-component` (alias: `/cc`)
**When to use:** Creating new components
```bash
/cc ui Button
/cc form ContactForm --with-tests
/cc layout DashboardLayout --with-docs
/cc feature UserProfile --with-tests --with-story
```

#### `/validate-design` (alias: `/vd`)
**When to use:** After any UI changes
```bash
/vd                  # Current file
/vd all              # All files
/vd --watch          # Auto-validate on save
/vd components/ui/*  # Specific path
```

#### `/test-runner` (alias: `/tr`)
**When to use:** Run relevant tests
```bash
/tr current    # Test current file
/tr changed    # Test modified files
/tr related    # Test entire feature
/tr all        # Run all tests
```

### 📊 Tracking Commands

#### `/todo`
**When to use:** Track tasks
```bash
/todo add "Task description" [priority]
/todo list [current|issue|all]
/todo update complete todo-123
/todo sync                      # Sync with GitHub
/todo report                    # Daily TODO report
```

#### `/work-status` (alias: `/ws`)
**When to use:** Find your work
```bash
/ws              # Current work
/ws list         # All active work
/ws find auth    # Search by keyword
/ws last         # Most recent work
```

#### `/issue-kanban`
**When to use:** Visual issue overview
```bash
/issue-kanban          # Show board
/issue-kanban move 23 in-progress
```

### 🔍 Quality Commands

#### `/performance-monitor` (alias: `/pm`)
**When to use:** Check performance
```bash
/pm check      # Quick check
/pm baseline   # Create baseline
/pm compare    # Compare to baseline
/pm report     # Detailed report
```

#### `/security-check` (alias: `/sc`)
**When to use:** Security scanning
```bash
/sc deps       # Check dependencies
/sc secrets    # Scan for secrets
/sc code       # Code vulnerabilities
/sc all        # Everything
```

#### `/error-recovery` (alias: `/er`)
**When to use:** When things break
```bash
/er git        # Git issues
/er build      # Build errors
/er deps       # Dependency problems
/er design     # Design violations
/er all        # Try everything
```

### 🚀 Workflow Commands

#### `/feature-workflow` (alias: `/fw`)
**When to use:** Issue-based development
```bash
/fw start 23      # Start feature
/fw validate 23   # Pre-commit checks
/fw complete 23   # Finish and create PR
```

#### `/compact-prepare`
**When to use:** Handle context compaction
```bash
/compact-prepare prepare    # Save state before compaction
/compact-prepare resume 23  # Restore after compaction
/compact-prepare list       # Show all saved states
```

### 🔧 Setup Commands

#### `/onboard`
**When to use:** Initial setup
```bash
/onboard fresh     # New project
/onboard existing  # Add to existing
/onboard check     # Verify setup
```

#### `/init-project`
**When to use:** Scaffold new project
```bash
/init-project list                    # Show templates
/init-project saas-dashboard "MyApp"  # Use template
/init-project custom "MyApp"          # Custom setup
```

#### `/help` (alias: `/?`)
**When to use:** Learn commands
```bash
/help                     # All commands
/help component           # Search commands
/help create-component    # Specific help
```

### 📈 Analysis Commands

#### `/analytics`
**When to use:** Track productivity
```bash
/analytics report    # Usage report
/analytics insights  # AI suggestions
/analytics export    # Export data
```

#### `/analyze-project`
**When to use:** Understand structure
```bash
/analyze-project           # Full analysis
/analyze-project --summary # Quick overview
```

---

## Common Scenarios

### Scenario: "I don't remember what I was working on"
```bash
/sr              # Smart resume finds everything
# or
/ws list         # Show all active work
/ws last         # Get most recent
```

### Scenario: "Starting work on a new issue"
```bash
/fw start 45     # Creates branch, sets up context
/cc ui Header    # Start creating components
/vd              # Validate as you go
```

### Scenario: "Ready to submit PR"
```bash
/pp              # Run pre-PR checks
# If all pass:
/fw complete 45  # Creates PR
```

### Scenario: "Something is broken"
```bash
/er all          # Try auto-fixes
# If specific:
/er build        # Build errors
/er git          # Git issues
```

### Scenario: "Context was compacted"
```bash
/sr full         # Full restoration
# or if you know the issue:
/compact-prepare resume 45
```

### Scenario: "Need to switch tasks quickly"
```bash
/checkpoint create before-switch
/fw start 50     # Start new task
# Later:
/checkpoint restore before-switch
```

---

## Best Practices

### 1. **Start Every Session with `/sr`**
- Restores context automatically
- Shows what needs attention
- Suggests next actions

### 2. **Use Aliases for Speed**
- `/cc` instead of `/create-component`
- `/vd` instead of `/validate-design`
- `/?` for quick help

### 3. **Create Checkpoints Before**
- Switching tasks
- Major refactors
- End of day
- Context might be lost

### 4. **Run Validation Early and Often**
- `/vd` after creating components
- `/qc` (quick-check) periodically
- `/pp` before any PR

### 5. **Track Everything**
- `/todo add` for any task you think of
- `/checkpoint create` at milestones
- `/analytics report` weekly to improve

### 6. **Use Command Chains**
- `/morning-setup` - Start day right
- `/pre-pr` - Ensure quality
- `/daily-report` - Track progress

---

## Troubleshooting

### "Command not found"
```bash
/help            # See all commands
/onboard check   # Verify setup
```

### "Design validation failing"
```bash
/vd --verbose    # See specific issues
/er design       # Try auto-fix
```

### "Lost context after compaction"
```bash
/sr full         # Restore everything
/context-grab restore
```

### "Tests failing"
```bash
/tr current --debug    # Debug mode
/er test              # Common fixes
```

### "Can't remember issue number"
```bash
/ws list         # Shows all work
/ws find [keyword]    # Search
```

---

## Quick Reference Card

### 🎯 Essential Commands
```bash
/sr              # Resume work
/cc ui [Name]    # Create component  
/vd              # Validate design
/fw start [#]    # Start feature
/fw complete [#] # Finish feature
/?               # Get help
```

### ⚡ Power User
```bash
/pp              # Pre-PR checks
/qc              # Quick check
/morning-setup   # Start day
/daily-report    # End day
/ws              # Find work
/er all          # Fix issues
```

### 💾 Save Progress
```bash
/checkpoint create
/context-grab capture
/todo add "task"
/compact-prepare prepare
```

---

## Remember

1. **You don't need to memorize** - Use `/?` anytime
2. **Commands are smart** - They detect context
3. **Everything is saved** - GitHub backs up your work
4. **Chains save time** - Use `/pp` instead of 4 commands
5. **Context is king** - `/sr` restores everything

Happy coding with Claude Code! 🚀
