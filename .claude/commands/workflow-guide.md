---
name: workflow-guide
aliases: [wg, choose-workflow, workflow-help]
description: Interactive guide to choose the right development workflow
category: workflow
---

# Workflow Selection Guide

I'll help you choose the best workflow for your task. Let me ask a few questions:

## 1. Task Complexity Analysis

**How complex is this feature?**
- Simple (< 100 lines, single file) → Score: 1
- Medium (multiple files, < 500 lines) → Score: 2  
- Complex (many files, new architecture) → Score: 3

**How many domains are involved?**
(backend, frontend, data, API, testing, etc.)
- 1 domain → Score: 1
- 2-3 domains → Score: 2
- 4+ domains → Score: 3

**Timeline estimate?**
- < 2 hours → Score: 1
- 1-2 days → Score: 2
- 3+ days → Score: 3

**Need automation/CI integration?**
- No → Score: 0
- Maybe → Score: 1
- Yes → Score: 2

## 2. Workflow Recommendation

Based on total score:

### Score 1-3: Micro Task 🚀
Quick implementation for small changes:
```bash
/sr                    # Resume context
/mt "Add logging"      # Define micro task
# Implement
/checkpoint           # Save progress
```

### Score 4-5: Standard Workflow 📋
Traditional PRD-driven development:
```bash
/sr                    # Resume context
/py-prd feature-name   # Create PRD
/gt feature-name      # Generate tasks
/pt feature-name      # Process tasks
/test-runner          # Run tests
/pr-feedback         # Check PR
```

### Score 6-7: Orchestration Workflow 🎭
Multi-agent parallel execution:
```bash
/sr                    # Resume context
/py-prd feature-name   # Create PRD
/gt feature-name      # Generate tasks

# Option 1: Traditional orchestration (shared filesystem)
/orch feature-name    # Orchestrate agents
/orch status         # Monitor progress

# Option 2: Worktree orchestration (isolated filesystem) - RECOMMENDED
/wt feature1 feature2 feature3  # Create isolated worktrees
/wt-status --monitor           # Monitor all worktrees
/chain mpr                     # Multi-perspective review
/wt-merge feature1            # Merge completed features
```

### Score 8-10: PRP Workflow 🔬
Research-heavy with automation:
```bash
/sr                    # Resume context
/prp-create feature    # Deep research + PRP
python scripts/prp_runner.py --prp feature --interactive
python scripts/prp_validator.py feature
/prp-complete feature
```

### Bug Fix: Special Workflow 🐛
For fixing issues:
```bash
/sr                    # Resume context
/bt add "Bug description"  # Track bug
/py-agent DebugHelper     # Optional: Create debug agent
# Fix the bug
/test-runner             # Verify fix
/bt resolve 1           # Mark resolved
```

## 3. Workflow Features Comparison

| Feature | Micro | Standard | Orchestration | Worktree | PRP |
|---------|-------|----------|---------------|----------|-----|
| Speed | ⚡ Fastest | 🏃 Fast | 🚶 Medium | 🏃 Fast | 🐢 Thorough |
| Documentation | ❌ Minimal | ✅ PRD | ✅ PRD | ✅ PRD | ✅✅ Enhanced PRD |
| Multi-agent | ❌ No | ❌ No | ✅ Yes | ✅ Isolated | ✅ Optional |
| File Conflicts | N/A | N/A | ⚠️ Possible | ✅ None | ✅ None |
| Automation | ❌ No | ❌ No | ✅ Partial | ✅ Partial | ✅✅ Full |
| Best For | Quick fixes | Features | Complex features | Parallel features | Research-heavy |

## 4. Context Preservation

All workflows benefit from:
- `/sr` - Always start here to restore context
- `/checkpoint` or `/save` - Manual progress saves
- Auto-save every 60 seconds via hooks
- GitHub gist backups

## 5. Quality Gates

Each workflow includes quality checks:
- **Micro**: Basic lint + test
- **Standard**: Full test suite
- **Orchestration**: Domain-specific tests
- **PRP**: 4-level validation

## Next Steps

Based on your answers, I recommend: **[Workflow Name]**

Ready to start? Here's your first command:
```bash
/sr  # Always start by resuming context
```

### 🆕 Worktree Workflow (Recommended for Parallel Development)
When you need to develop multiple features simultaneously without conflicts:
```bash
/sr                          # Resume context
/py-prd "multi-feature"      # Create PRD
/gt multi-feature           # Generate tasks
/wt feat1 feat2 feat3       # Create isolated worktrees
/wt-status --monitor        # Monitor progress
/chain mpr                  # Multi-perspective review
/wt-merge feat1            # Merge completed features
```

**Benefits of Worktrees:**
- ✅ No file conflicts between parallel work
- ✅ Each feature on its own branch
- ✅ Can run tests simultaneously
- ✅ Easy rollback (just remove worktree)
- ✅ All hooks and validation work per worktree

## Pro Tips

1. **Not sure?** Start with Standard Workflow
2. **Time pressure?** Use Micro Task
3. **Many moving parts?** Use Orchestration
4. **Need research?** Use PRP
5. **Found a bug?** Use Bug Fix workflow

Remember: You can always upgrade workflows mid-stream:
- Standard → Orchestration: Just run `/orch`
- Standard → PRP: Run `/py-prd --prp`
