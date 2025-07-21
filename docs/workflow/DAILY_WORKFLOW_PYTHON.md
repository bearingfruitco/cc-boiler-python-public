# 📅 Daily Python Workflow - Simple Commands

This guide shows you EXACTLY what commands to run throughout your day.

## 🌅 Start Your Day (2 minutes)

```bash
# ALWAYS start with this - even if nothing to resume
/sr

# Check what's happening
/ts                    # Your task status
/ws                    # Team work status  
/bt list --open        # Any bugs to fix?

# Quick health check
/test --changed        # Run tests for recent changes
```

## 💼 Working on Features

### Starting New Feature
```bash
# 1. Define what you're building
/py-prd "Payment Processing"

# 2. Break into tasks
/gt payment-processing

# 3. Create issue with tests (magic happens!)
/cti "Payment Processing" --tests --type=api

# 4. Start work (tests ready!)
/fw start 123

# You're ready - tests are waiting!
```

### Continue Existing Feature
```bash
# Resume where you left off
/sr
/fw test-status 123    # See TDD progress
/pt payment-processing # Continue tasks

# System shows:
# - Current task
# - Which test to pass
# - What to implement
```

### Quick Bug Fix
```bash
# 1. Track the bug
/bt add "Login fails with @ symbol"

# 2. Create test that reproduces it
/generate-tests login-bug --regression

# 3. Fix the bug (test guides you)
vim src/auth/login.py

# 4. Verify and close
/test
/bt resolve bug_1234 "Fixed @ symbol handling"
```

## 🏗️ Building Components

### Create API Endpoint
```bash
# Check it doesn't exist
/pyexists UserEndpoint

# Create with tests
/py-api /users POST

# Tests are generated!
# Implement to make them pass
```

### Create AI Agent
```bash
# Check first
/pyexists DataAnalyzer

# Create agent
/py-agent DataAnalyzer --tools=pandas,matplotlib

# Tests ready!
# Follow TDD to implement
```

### Create Data Pipeline
```bash
/py-pipeline daily-report --source=database --destination=s3
# Tests generated for each step!
```

## ✅ Quality Checks

### Before Committing
```bash
# Run the safe commit chain
/chain sc
# Or manually:
/test                  # All tests pass?
/lint                  # Code formatted?
/pydeps circular       # No circular imports?
```

### Quick Quality Check
```bash
# Just check current work
/chain qc
# Does: lint + test current file
```

### Full Project Check
```bash
# Complete quality check
/chain pq
# Does: lint + test + deps + security
```

## 🔄 Context Management

### Switching Tasks
```bash
# Save current work
/checkpoint save "payment feature WIP"

# Switch context  
/context-profile save "payment-work"
/context-profile load "user-auth-work"

# Resume other task
/sr
```

### Taking a Break
```bash
# Quick break (< 1 hour)
/checkpoint
# Just saves state

# Longer break (lunch, meetings)
/compact-prepare
# Optimizes context for later
```

### End of Day
```bash
# Review what you did
/ts                    # Task status
/analytics today       # Your metrics

# Save everything
/checkpoint save "EOD $(date +%Y-%m-%d)"
/compact-prepare

# Check nothing left uncommitted
/git-status
```

## 🚀 Power Workflows

### Complex Feature (Use Orchestration)
```bash
# Let AI analyze complexity
/gt big-feature
# System: "15 tasks across 3 domains, suggest: /orch"

# Use multi-agent
/orch big-feature --strategy=feature_development
/sas                   # Monitor progress
```

### Research-Heavy Feature
```bash
# Use PRP for deep research
/prp-create ai-integration
/prp-execute ai-integration
/prp-status            # Track validation
```

### Full TDD Feature
```bash
# Complete TDD workflow
/chain tdd
# Or shortcut:
/tdd
```

## 🆘 When Things Go Wrong

### "I lost my context"
```bash
/sr                    # Recovers everything
/checkpoint list       # See all saves
```

### "Are tests up to date?"
```bash
/fw test-status 123    # For specific feature
/test --coverage       # Overall coverage
```

### "What depends on this?"
```bash
/pydeps check module_name
/pydeps breaking module_name
```

### "Did I already create this?"
```bash
/pyexists ClassName
/pysimilar ClassName   # Find similar names
```

## 📊 Tracking Progress

### Throughout the Day
```bash
/ts                    # Task status (often)
/fw test-status        # TDD progress
/performance-monitor   # Speed metrics
```

### Weekly Review
```bash
/analytics week        # Your productivity
/prp-metrics          # Feature success rate
/bug-track stats      # Bug trends
```

## 💡 Daily Tips

1. **Start with `/sr`** - Always, even first thing
2. **Use aliases** - `/ts` not `/task-status`
3. **Trust auto-tests** - They appear when needed
4. **Checkpoint often** - After completing anything significant
5. **Use chains** - `/tdd` `/pq` `/sc` for common workflows

## 🎯 Advanced Features You Should Use

### Research & Documentation
```bash
# Research before building
/research "Best practices for payment processing"

# Cache external docs
/doc-cache cache "https://stripe.com/docs"
/doc-cache search "webhooks"

# Capture successful patterns
/specs capture "Payment Flow"
/specs list payment
```

### GitHub Integration
```bash
# Save reusable code as gists
/gist-save "auth_middleware.py" --desc="JWT middleware"
/gist-list auth
/gist-apply auth_middleware

# Smart issue management
/cti "Feature" --tests --create-prp  # Issue + Tests + PRP!
/issue-kanban                         # Visual board
```

### Multi-Agent Orchestration
```bash
# Let system analyze complexity
/gt big-feature
# If system suggests orchestration:
/orch big-feature --strategy=feature_development
/sas                                  # Monitor agents
/orchestration-stats                  # See time saved
```

### Dependency Intelligence
```bash
# Before refactoring
/pydeps check module_name             # What uses this?
/pydeps breaking module_name          # What might break?
/pydeps circular                      # Find circular imports
/pydeps scan                          # Full dependency graph
```

### Stage Validation & Grading
```bash
# Ensure quality gates
/stage-validate check 1               # Foundation complete?
/stage-validate require 2             # Enforce completion
/grade feature-name                   # PRD alignment score
```

Remember: The system guides you - let it! 🚀
