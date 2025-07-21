# Daily Workflow Guide - Python Boilerplate v2.4.1

This guide shows you exactly which commands to use and when, ensuring you never lose context and make the most of the system.

## 🌅 Starting Your Day

```bash
# ALWAYS start with:
/sr                    # Smart Resume - restores EVERYTHING from last session

# Check what's pending:
/tl                    # Task Ledger - shows ALL tasks across features (NEW!)
/ws                    # Work status - includes task summary
/bt list --open        # Bug track - any open bugs
```

## 🎯 Command Flow by Scenario

### 1. Starting a New Feature

```bash
# Step 1: Create PRD and plan
/py-prd "User Authentication"              # Creates PRD with Python specifics

# Step 2: Generate tasks
/gt user-authentication                    # Breaks PRD into tasks

# Step 3: Create GitHub issue (with auto tests!)
/cti "User Authentication" --tests         # Creates issue + generates tests

# Step 4: Start development
/fw start 123                              # Tests auto-generated from issue!

# You're now ready with:
# ✅ Branch created
# ✅ Tests written
# ✅ Issue linked
# ✅ Context saved
```

### 2. Working on Existing Issue

```bash
# Start work (tests auto-generate if missing)
/fw start 123                              

# Check test status
/fw test-status 123                        # Shows which tests are failing

# Process tasks (TDD enforced)
/pt user-authentication                    # Won't let you code without tests!

# After each implementation:
# - Tests run automatically
# - Can't mark complete until tests pass
```

### 3. Complex Feature with Research

```bash
# Step 1: Create PRP (includes research phase)
/prp-create payment-integration            

# Step 2: Execute with validation
/prp-execute payment-integration           # Runs research + implementation

# Step 3: Check progress
/prp-status payment-integration            # Shows validation gates

# Step 4: Complete
/prp-complete payment-integration          # Generates metrics
```

### 4. Quick Bug Fix

```bash
# Track the bug
/bt add "Login fails with special chars"   

# Create test that reproduces bug
/generate-tests login-bug --type=regression

# Fix and validate
/test                                      # Run tests
/bt resolve bug_1234 "Fixed special chars"
```

### 5. Multi-Agent Complex Feature

```bash
# Analyze if orchestration would help
/gt user-dashboard                         # Generate tasks
# System analyzes: "15 tasks across backend/frontend/data"
# Suggests: /orch user-dashboard --agents=4

# Start orchestration
/orch user-dashboard --strategy=feature_development

# Monitor progress
/sas                                       # Sub-agent status
```

## 📋 Essential Command Chains

```bash
# Complete feature development (PRD → Tests → Code → Validate)
/chain tdd
# or shortcut:
/tdd

# Python feature workflow
/chain pf
# or shortcut:
/pf

# Quick quality check
/chain pq
# Does: lint → test → circular deps → security
```

## 🛡️ Context Preservation Commands

### Save Context Regularly
```bash
# After completing major work:
/checkpoint save "Completed auth module"    

# Before switching tasks:
/context-profile save "auth-work"          
/context-profile load "payment-work"       

# End of day:
/compact-prepare                           # Prepares handoff
```

### Never Lose Work
```bash
# If something goes wrong:
/er                    # Error recovery
/sr                    # Smart resume - gets you back to where you were

# Check what changed:
/git-status            # See all changes
/pyexists UserModel    # Check if something exists before recreating
/pydeps check auth     # See what depends on your module
```

## 🔄 Workflow Patterns

### Morning Routine
```bash
/sr                    # Resume context
/tl                    # View task ledger (NEW!)
/chain ds              # Daily startup (includes ledger)
/fw test-status 123    # Check TDD progress on current issue
```

### Before Writing Code
```bash
/pyexists ClassName    # Check if it exists
/pysimilar ClassName   # Find similar names
/pydeps check module   # Check dependencies
# Tests are auto-generated, no manual step needed!
```

### After Writing Code
```bash
# Tests run automatically via hooks
# But you can manually run:
/test                  # Run all tests
/lint                  # Check code quality
/pydeps circular       # Check for circular imports
```

### Before Committing
```bash
/chain sc              # Safe commit chain
# or manually:
/facts all             # Check constraints
/test                  # Run tests
/lint                  # Fix formatting
```

### End of Day
```bash
/bt list --open        # Review open bugs
/tl                    # Task ledger overview (NEW!)
/checkpoint save "EOD" # Save state
/compact-prepare       # Prepare handoff
```

## 🚨 Common Scenarios

### "I lost my context"
```bash
/sr                    # Restores everything
```

### "Did I already create this?"
```bash
/pyexists UserService  # Check before creating
```

### "What depends on this module?"
```bash
/pydeps check auth     # Shows all dependents
```

### "I need to refactor safely"
```bash
/chain pr              # Python refactor chain
# Does: deps check → exists check → backup → import update
```

### "Are my tests up to date?"
```bash
/fw test-status 123    # Check specific feature
/test                  # Run all tests
```

## 📊 Progress Tracking

```bash
# Task level:
/tl                    # Task ledger - ALL tasks (NEW!)
/tl view [feature]     # Specific feature tasks
/tb                    # Task board (visual)

# Feature level:
/fw test-status 123    # TDD progress
/prp-status feature    # PRP validation gates

# Project level:
/pydeps scan           # Full dependency analysis
/test --coverage       # Coverage report
```

## 🎯 Key Principles

1. **Always Start with `/sr`** - Never lose context
2. **Tests Generate Automatically** - Just start working
3. **Check Before Creating** - Use `/pyexists`
4. **Save Checkpoints** - After major work
5. **Use Chains** - They enforce best practices

## 🔧 Configuration Check

```bash
# Verify TDD is enabled:
cat .claude/settings.json | grep -A10 "tdd"

# Should show:
"auto_generate_tests": true
"enforce_tests_first": true
```

## 💡 Pro Tips

1. **Trust the Automation** - Tests will be there when needed
2. **Use Aliases** - `/sr` instead of `/smart-resume`
3. **Chain Commands** - `/tdd` for complete workflows
4. **Check Status Often** - `/ts`, `/ws`, `/fw test-status`
5. **Save Context** - Checkpoint after completing modules

Remember: The system is designed to preserve context and enforce quality. Let it guide you!
