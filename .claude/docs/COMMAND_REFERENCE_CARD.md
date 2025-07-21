# 📋 Command Reference Card

## 📊 Task Ledger (NEW!)
```bash
/tl                    # View all tasks across project
/tl view [feature]     # View specific feature tasks
/tl update [feature]   # Update task progress
/tl link [f] [#issue]  # Link tasks to GitHub issue
/tl generate           # Generate from existing tasks
```

## 🚀 Daily Essentials
```bash
/sr                    # Smart Resume (ALWAYS start here)
/tl                    # Task ledger overview
/help                  # Context-aware help
/ws                    # Work status (includes tasks)
/checkpoint            # Save state
```

## 🧪 TDD Workflow (Automatic!)
```bash
/fw start 123          # Start issue (tests auto-gen!)
/fw test-status 123    # Check TDD progress
/pt feature-name       # Process tasks (TDD enforced)
/test                  # Run all tests
/cti --tests           # Create issue + tests
```

## 🐍 Python Development
```bash
/py-prd               # Python-specific PRD
/py-agent             # Create AI agent
/py-api               # Create API endpoint  
/py-pipeline          # Create data pipeline
/pyexists             # Check before creating
/pydeps               # Check dependencies
```

## 🔗 Workflow Chains
```bash
/chain tdd    (/tdd)   # Complete TDD workflow
/chain pf     (/pf)    # Python feature
/chain pq     (/pq)    # Python quality
/chain pr     (/pr)    # Python refactor
/chain ma     (/ma)    # Multi-agent
/chain ds     (/ds)    # Daily startup (with ledger)
```

## 📊 Analysis & Tracking
```bash
/bt add/list/resolve   # Bug tracking
/analytics report      # Usage analytics
/performance-monitor   # Performance metrics
/pydeps scan          # Full dependency scan
/grade                # Implementation score
```

## 🛡️ Safety & Context
```bash
/facts                # Show unchangeable truths
/pyexists ClassName   # Check existence
/compress-context     # Optimize tokens
/compact-prepare      # End of session prep
/truth-override       # Override protections
```

## 🚀 Advanced Features
```bash
/orch                 # Multi-agent orchestration
/prp-create           # Research-heavy PRP
/think-through        # Deep analysis
/spawn-agent          # Create sub-agent
/sas                  # Sub-agent status
```

## 🔥 Branch Management (NEW!)
```bash
/bs                   # Branch status
/bsw [branch]         # Switch branches safely
/fs                   # Feature status
/sync-main            # Sync with main branch
```

## 💡 Aliases (Save Typing!)
```bash
/sr    → /smart-resume
/tl    → /task-ledger
/ws    → /work-status
/pt    → /process-tasks
/cti   → /capture-to-issue
/fw    → /feature-workflow
/bt    → /bug-track
/bs    → /branch-status
/bsw   → /branch-switch
/tdd   → /chain tdd
/pf    → /chain python-feature
/pq    → /chain python-quality
```

## 🎯 Command Patterns

### New Feature
```bash
/sr → /py-prd → /cti --tests → /fw start → /pt
```

### Bug Fix  
```bash
/sr → /bt add → /generate-tests → fix → /test → /bt resolve
```

### Complex Feature
```bash
/sr → /prp-create → /prp-execute → /prp-status → /prp-complete
```

### Multi-Agent
```bash
/sr → /py-prd → /gt → /orch → /sas
```

## ⚡ Quick Wins

### "I need to start working"
```bash
/sr → /fw start 123
```

### "Did I create this already?"
```bash
/pyexists ClassName
```

### "What's my progress?"
```bash
/tl → /fw test-status 123
```

### "Run quality checks"
```bash
/chain pq
```

### "Save my work"
```bash
/checkpoint save "milestone"
```

---
Print this and keep it handy! 🎉
