# Daily Workflow Guide - Python Boilerplate v2.4.2

This guide shows real daily workflows for maximum productivity with the AI development system.

## 🌅 Morning Routine (5 minutes)

### Start Your Day Right

```bash
# 1. Load context and see where you are
/sr

# 2. Check task progress
/tl

# 3. Review any overnight changes
/gs

# 4. Run morning chain (optional)
/chain morning-setup
```

### What You'll See
```
📍 You Are Here
Branch: feature/23-user-auth
Issue: #23
Progress: 7/10 tasks (70%)

📋 Active Tasks
- [ ] Add integration tests
- [ ] Update documentation
- [ ] Security review

🎯 Suggested Next Steps
1. Continue with 3 remaining tasks: /pt user-auth
2. Fix failing test: pytest tests/test_auth.py::test_refresh -v
```

## 💼 Common Daily Workflows

### 1. Continuing Yesterday's Feature

```bash
# Resume exactly where you left off
/sr

# Check task status
/tl view current-feature

# Continue implementation
/pt current-feature

# After making changes
/test --related    # Test only affected code
/grade            # Check quality
```

**Time: 2-4 hours for typical feature completion**

### 2. Starting a New Feature

```bash
# Start fresh
/sr

# Create feature specification
/py-prd notification-system

# Generate tasks and issue
/cti "Email Notification System" --tests

# Begin work (tests already exist!)
/fw start 124

# Start implementing
/pt notification-system
```

**Time: 30 minutes to full setup with tests**

### 3. Quick Bug Fix

```bash
# Load context
/sr

# Create micro task
/mt "fix password validation bug"

# Make the fix
vim src/auth/validators.py

# Verify fix
/test auth/validators
/sc    # Safe commit
```

**Time: 15-30 minutes including tests**

### 4. Code Review Preparation

```bash
# Prepare for PR
/chain pre-pr

# This runs:
# - Design validation
# - All tests
# - Security checks
# - Performance analysis

# Fix any issues, then
/commit-review
```

**Time: 10-15 minutes**

### 5. Research & Complex Feature

```bash
# Start research-heavy feature
/prp-create payment-gateway

# Let system research
/prp-execute

# Review findings
/prp-status

# Implement with confidence
/prp-complete
```

**Time: 1-2 days for complex integrations**

## 🚀 Productivity Workflows

### Multi-Agent Development (For Complex Features)

```bash
# When to use: Feature touches 3+ domains
# Time savings: 50-70%

# 1. Create comprehensive PRD
/py-prd social-media-integration

# 2. Launch orchestration
/orch social-media --strategy=feature_development

# 3. Monitor progress
/sas
/orchestration-view

# 4. Integrate results
/orch integrate
```

### TDD Speed Run

```bash
# Enforced TDD workflow
/chain tdd

# Automatically:
# 1. Creates PRD
# 2. Generates all tests
# 3. Shows failing tests
# 4. Guides implementation
# 5. Validates coverage
```

### Dependency Analysis Before Refactoring

```bash
# Before changing core components
/pydeps check UserModel
/pydeps breaking UserModel

# See impact analysis
⚠️ UserModel is used by:
- api/auth.py (5 references)
- services/user.py (12 references)
- tests/test_user.py (8 references)

# Safe refactoring approach
/chain python-refactor
```

## 📋 Task Management Workflows

### Daily Task Review

```bash
# See all tasks across features
/tl

# Filter views
/tl view --in-progress     # Active work
/tl view --blocked         # Needs attention
/tl view --ready           # Can start

# Update progress
/tl update feature-name
```

### Sprint Planning

```bash
# Generate sprint tasks
/task-board

# Assign work
/assign-tasks @teammate feature-name

# Track velocity
/analytics sprint-velocity
```

### End-of-Day Wrap-up

```bash
# Save current state
/checkpoint create end-of-day

# Generate summary
/work-status

# Prepare handoff
/chain context-maintenance

# Final commit
/sc -m "EOD: Updated auth validation"
```

## 🔄 Context Management Workflows

### Switching Between Features

```bash
# Save current feature state
/cp save feature-auth

# Switch branch (auto-stash enabled)
/bsw feature/124-notifications

# Load new context
/sr

# When returning
/bsw feature/123-auth
/cp load feature-auth
```

### Managing Large Contexts

```bash
# Check token usage
/analytics token-usage

# Compress intelligently
/compress --focus="current task"

# Archive completed work
/checkpoint create pre-archive
/compress --archive-completed
```

### Team Collaboration

```bash
# Before pushing
/chain safe-commit

# Share context
/cp share feature-auth

# After pulling
/sr
/sync-main
```

## 🛠️ Development Patterns

### API Endpoint Creation

```bash
# Morning: Design
/py-prd order-management

# Generate endpoint
/py-api /orders CRUD --auth --pagination

# Customize
vim src/api/routers/orders.py

# Test immediately
/test api/orders

# Add to documentation
/generate-docs api
```

### Agent Development Workflow

```bash
# Create agent spec
/py-prd customer-support-agent

# Generate agent
/py-agent SupportBot --tools=zendesk,slack

# Implement conversation logic
vim src/agents/support_bot.py

# Test conversations
/test agents/support --fixtures=conversations

# Deploy
/cloud-deploy agent support-bot
```

### Pipeline Creation

```bash
# Design data flow
/py-prd daily-analytics-pipeline

# Generate pipeline
/py-pipeline AnalyticsETL --schedule="0 2 * * *"

# Add transformations
vim src/pipelines/analytics_etl.py

# Test with sample data
/test pipelines/analytics --sample-data

# Monitor
/pipeline-monitor analytics-etl
```

## 🎯 Advanced Daily Workflows

### Deep Problem Solving

```bash
# Enhance AI reasoning
/think-level deep

# Analyze complex issue
/think-through "optimize query performance"

# Get implementation plan
/cti "Query Optimization" --detailed

# Execute with guidance
/pt query-optimization
```

### Performance Optimization

```bash
# Profile current performance
/performance-monitor baseline

# Make optimizations
# ... code changes ...

# Compare results
/performance-monitor compare

# Generate report
/analytics performance-report
```

### Security Audit

```bash
# Run security check
/security-check all

# Fix critical issues
/process-tasks security-critical

# Verify fixes
/security-check verify

# Document changes
/log-decision "security-improvements"
```

## 💡 Daily Productivity Tips

### Time Savers

1. **Use Chains**: `/chain tdd` vs manual commands (save 10-15 min)
2. **Trust Auto-staging**: Let hooks handle git (save 5 min/hour)
3. **Batch Similar Tasks**: `/pt --type=tests` (save 20 min)
4. **Let AI Debug**: `/think-level deep && /debug` (save 30 min)

### Quality Boosters

1. **Check First**: `/pyexists` before creating (prevent rework)
2. **Test Continuously**: `/test --watch` in another terminal
3. **Grade Often**: `/grade` after major changes
4. **Document Decisions**: `/log-decision` for future reference

### Context Optimization

1. **Compress Regularly**: Every 2-3 hours
2. **Checkpoint Milestones**: Before major changes
3. **Profile Switching**: For multiple features
4. **Clean Commits**: `/sc` for automatic formatting

## 📊 Daily Metrics

Track your productivity:

```bash
# End of day metrics
/analytics daily-summary

# Shows:
- Tasks completed: 12
- Test coverage: 87%
- Tokens saved: 45%
- Time saved: 2.5 hours
- Code quality: A+
```

## 🌙 End of Day Routine

```bash
# 1. Checkpoint current state
/checkpoint create eod-$(date +%Y%m%d)

# 2. Update task ledger
/tl update all

# 3. Generate summary
/work-status report

# 4. Prepare for tomorrow
/todo add "Review PR feedback"
/todo add "Start notification feature"

# 5. Clean up
/chain context-maintenance
```

## 🚨 Common Daily Scenarios

### "I broke something!"
```bash
/error-recovery recent
/checkpoint restore last-working
/test --failed-only
```

### "Too many conflicts"
```bash
/sync-main --strategy=theirs
/conflict-check
/merge-assist
```

### "Lost track of tasks"
```bash
/tl rebuild
/work-status detailed
/suggest-next
```

### "Need to onboard teammate"
```bash
/team-setup add @teammate
/cp share onboarding
/generate-docs quickstart
```

## 🎉 Daily Success Checklist

- [ ] Started with `/sr` ✓
- [ ] Checked task ledger ✓
- [ ] Used appropriate workflow ✓
- [ ] Ran tests frequently ✓
- [ ] Compressed context ✓
- [ ] Saved checkpoints ✓
- [ ] Updated documentation ✓
- [ ] Clean commits ✓

## 📈 Leveling Up Daily

### Week 1: Build Habits
- Always start with `/sr`
- Use `/tl` for task tracking
- Trust the test automation

### Week 2: Increase Speed
- Master workflow chains
- Try multi-agent mode
- Use thinking levels

### Month 1: Peak Performance
- Create custom workflows
- Optimize token usage
- Contribute patterns

Remember: **The system learns from your patterns**. The more consistently you use it, the more it adapts to your style!

---

*Pro tip: Pin your 5 most-used commands to muscle memory. Most developers use `/sr`, `/tl`, `/pt`, `/test`, and `/sc` dozens of times daily.*
