# 🎯 Which Workflow Should I Use?

Simple guide: Pick based on what you're building.

## 🚀 Quick Decision Tree

```
What are you building?
│
├─ Small Feature (< 4 hours)
│  └─ Use: STANDARD WORKFLOW
│
├─ Bug Fix (< 2 hours)
│  └─ Use: BUG FIX WORKFLOW
│
├─ Complex Feature (multiple parts)
│  └─ Is it research-heavy?
│     ├─ Yes → Use: PRP WORKFLOW
│     └─ No  → Use: ORCHESTRATION WORKFLOW
│
└─ Just exploring/learning
   └─ Use: MICRO TASK WORKFLOW
```

## 📋 The Workflows

### 1️⃣ STANDARD WORKFLOW - Most Common
**When**: Regular features, single domain, < 1 day

```bash
/sr                           # Start
/py-prd "Feature Name"        # Plan
/cti "Feature" --tests        # Create issue + tests
/fw start 123                 # Begin (tests ready!)
/pt feature-name              # Work through tasks
/fw complete 123              # Finish
```

### 2️⃣ BUG FIX WORKFLOW - Quick Fixes
**When**: Something's broken, need fast fix

```bash
/sr                           # Start
/bt add "What's broken"       # Track bug
/generate-tests bug-name      # Create failing test
# Fix the code
/test                         # Verify fix
/bt resolve bug_123          # Close bug
```

### 3️⃣ PRP WORKFLOW - Research First
**When**: Complex features, need documentation, external APIs

```bash
/sr                           # Start
/prp-create feature-name      # Deep research phase
/prp-execute feature-name     # Build with validation
/prp-status                   # Check gates
/prp-complete                 # Generate report
```

### 4️⃣ ORCHESTRATION WORKFLOW - Parallel Work
**When**: 10+ tasks, multiple domains, save time

```bash
/sr                           # Start  
/py-prd "Big Feature"         # Plan
/gt big-feature               # Generate tasks
# System says: "Use /orch"
/orch big-feature             # Start agents
/sas                          # Monitor progress
```

### 5️⃣ MICRO TASK WORKFLOW - Quick Wins
**When**: Small improvements, refactoring, experiments

```bash
/sr                           # Start
/mt "Quick task"              # Define micro task
# Do the work
/checkpoint                   # Save
# That's it!
```

## 🎯 Real Examples

### "Add user authentication"
- Multiple components (model, API, middleware)
- Use: **STANDARD WORKFLOW**

### "Fix login button not working"  
- Specific issue, quick fix
- Use: **BUG FIX WORKFLOW**

### "Integrate with Stripe API"
- Needs research, external docs
- Use: **PRP WORKFLOW**

### "Build complete admin dashboard"
- 20+ tasks, frontend + backend
- Use: **ORCHESTRATION WORKFLOW**

### "Update README"
- Simple, quick task
- Use: **MICRO TASK WORKFLOW**

## 📚 Full Feature List by Workflow

### STANDARD WORKFLOW Features
- ✅ PRD creation with domain analysis
- ✅ Automatic TDD with test generation
- ✅ GitHub issue integration
- ✅ Task tracking and verification
- ✅ Component guards (prevent duplicates)
- ✅ Dependency tracking
- ✅ Stage validation
- ✅ All 35+ hooks active

### BUG FIX WORKFLOW Features  
- ✅ Bug tracking with severity
- ✅ Regression test generation
- ✅ Root cause analysis
- ✅ Quick validation
- ✅ Auto import fixes

### PRP WORKFLOW Features
- ✅ Deep research with sub-agents
- ✅ Documentation caching
- ✅ 4-level validation gates
- ✅ Success metrics
- ✅ Pattern capture
- ✅ Automated execution option
- ✅ External API integration

### ORCHESTRATION WORKFLOW Features
- ✅ Automatic complexity analysis
- ✅ Parallel agent execution
- ✅ Task distribution algorithms
- ✅ Progress monitoring
- ✅ 50-70% time savings
- ✅ Smart handoffs
- ✅ Team coordination

### MICRO TASK Features
- ✅ Quick checkpoint/restore
- ✅ Minimal overhead
- ✅ Pattern capture
- ✅ Context preservation

## 💎 Additional Power Features

### Available in ALL Workflows
- **GitHub Gists**: Save/share reusable code
- **Spec Patterns**: Capture/reuse successful patterns  
- **Doc Caching**: Offline documentation access
- **Response Capture**: AI insights saved automatically
- **Knowledge Sharing**: Team learning system
- **Performance Monitoring**: Track improvements
- **Security Scanning**: Automated checks

### Hook System (Always Active)
- 19 Pre-tool hooks (prevent mistakes)
- 13 Post-tool hooks (learning/tracking)
- 4 Notification hooks (team awareness)
- 4 Stop hooks (clean shutdown)

## 💡 Pro Tips

1. **Not sure?** Start with STANDARD - you can always switch
2. **Tasks > 10?** Consider ORCHESTRATION
3. **External API?** Always use PRP
4. **Under 2 hours?** Keep it simple with MICRO TASK

## 🚦 Workflow Commands

```bash
# See all workflows
/help workflows

# Use workflow chains
/chain tdd              # Full TDD workflow
/chain pf               # Python feature
/chain bug              # Bug fix workflow

# Quick shortcuts
/tdd                    # Same as /chain tdd
/pf                     # Same as /chain pf
```

## 📊 Time Estimates

| Workflow | Setup Time | Total Time | Time Saved |
|----------|------------|------------|------------|
| Standard | 5 min | 2-4 hours | Baseline |
| Bug Fix | 2 min | 30-60 min | 30% |
| PRP | 15 min | 4-8 hours | 40% |
| Orchestration | 10 min | 2-3 hours* | 60% |
| Micro Task | 1 min | 15-30 min | 20% |

*For work that would take 6-8 hours sequential

Remember: The right workflow saves time and prevents mistakes! 🚀
