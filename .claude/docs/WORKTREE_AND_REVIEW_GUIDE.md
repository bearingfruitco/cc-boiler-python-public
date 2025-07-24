# Git Worktree & Multi-Perspective Review Integration

## 🎉 Installation Complete!

Your Python boilerplate now includes Kieran-inspired enhancements for parallel development and comprehensive code reviews.

## 🌳 Git Worktrees - True Parallel Development

### Quick Start
```bash
# Create worktrees for parallel features
/worktree-parallel auth payment ui

# Or use the short alias
/wt auth payment ui --tasks "implement auth" "add payments" "refactor UI"

# Monitor all worktrees
/wt-status --monitor

# Review and merge
/wt-review auth
/wt-merge auth
```

### Key Commands
- `/worktree-parallel` (aliases: `/wt`, `/worktree`) - Create parallel worktrees
- `/wt-status` (alias: `/wts`) - Monitor worktree progress  
- `/wt-list` (alias: `/wtl`) - List active worktrees
- `/wt-review [name]` - Review changes in worktree
- `/wt-merge [name]` - Merge worktree to main
- `/wt-clean` - Remove completed worktrees

### Integration with Existing Workflow
```bash
# Traditional parallel (shared filesystem - conflict risk)
/orchestrate-agents "build three features"

# NEW: Worktree parallel (isolated - no conflicts!)
/wt-orchestrate "build three features"

# Or use the chain
/chain worktree-feature "user management"
```

### Benefits
- ✅ **No file conflicts** - Each agent works in isolation
- ✅ **Clean git history** - Separate branches per feature  
- ✅ **Parallel testing** - Run tests simultaneously
- ✅ **Easy rollback** - Just remove the worktree
- ✅ **All hooks work** - Design validation, TDD, etc. per worktree

## 👁️ Multi-Perspective Reviews

### Quick Start
```bash
# Review current changes from multiple angles
/chain multi-perspective-review

# Or use the alias
/chain mpr

# Review a specific PR
/chain pr-multi-review
```

### Review Perspectives
1. **🔒 Security** - OWASP vulnerabilities, auth issues, data exposure
2. **⚡ Performance** - N+1 queries, memory leaks, optimization
3. **📊 Code Quality** - Patterns, coverage, technical debt
4. **💼 Business Logic** - Requirements, edge cases, data integrity
5. **🎨 UX/Accessibility** - Error states, WCAG compliance

### Custom Perspectives
```bash
# Configure specific review focus
/review-perspectives security performance

# Or use alias
/rp --focus "SQL injection" "query optimization"
```

## 🔗 Workflow Integration

### Example: Multi-Feature Development
```bash
# 1. Start fresh
/sr

# 2. Create PRD for multiple features  
/prd "user system: auth, profiles, settings"

# 3. Generate tasks
/gt user-system

# 4. Execute in parallel worktrees
/wt auth profile settings

# 5. Monitor progress
/wt-status --monitor

# 6. Multi-perspective review
/chain mpr

# 7. Merge completed features
/wt-merge auth
/wt-merge profile
/wt-merge settings
```

### New Chains Available
- `worktree-setup` (alias: `wts`) - Validate before worktrees
- `worktree-execute` (alias: `wte`) - Run parallel worktrees
- `worktree-merge` (alias: `wtm`) - Safe merge process
- `multi-perspective-review` (alias: `mpr`) - Parallel reviews
- `pr-multi-review` (alias: `pmr`) - PR + perspectives

## 📋 Best Practices

### For Worktrees
1. **One feature per worktree** - Keep changes focused
2. **Clear naming** - Use descriptive names
3. **Regular sync** - Pull main into worktrees
4. **Clean up** - Remove after merging

### For Reviews  
1. **Review early** - Before PR creation
2. **Focus perspectives** - Use relevant reviewers
3. **Address systematically** - Work through feedback
4. **Learn patterns** - Update perspectives based on findings

## 🚀 Advanced Usage

### Worktree + Multi-Agent + Reviews
```bash
# Ultimate parallel workflow
/prd "e-commerce: cart, checkout, inventory"
/gt e-commerce
/wt cart checkout inventory
/chain mpr  # Review all worktrees
/wt-merge --all --after-review
```

### AppleScript Integration
The system includes AppleScript automation for macOS:
- Opens worktrees in new Terminal windows
- Starts Claude Code with task context
- Shows monitoring dashboard
- Sends completion notifications

## 🔧 Under the Hood

### New Files Added
- Commands: `worktree-*.md`, `review-perspectives.md`
- Scripts: `worktree_manager.py`, `worktree_applescript.py`  
- Hook: `24-worktree-integration.py`
- Chains: 6 new workflow chains

### How It Works
1. **Worktrees** use git's built-in worktree feature
2. Each worktree gets its own `.claude` configuration
3. Hooks detect worktree context automatically
4. Task Ledger tracks progress per worktree
5. Reviews spawn specialized sub-agents

## 💡 Tips

1. **Start small** - Try with 2 features first
2. **Use monitoring** - `/wt-status --monitor` is your friend
3. **Trust the isolation** - No more "file changed by another process"
4. **Combine approaches** - Worktrees + orchestration = 🚀

## 🐛 Troubleshooting

**"Worktree already exists"**
```bash
/wt-list  # See what exists
/wt-clean  # Remove old worktrees
```

**"Can't merge - conflicts"**
```bash
/wt-review feature-name  # See changes
git pull origin main  # Update base
/wt-merge feature-name --resolve
```

**"Reviews taking too long"**
```bash
/rp security performance  # Limit perspectives
/compress --aggressive  # Reduce context
```

---

Ready to develop features in parallel without conflicts? Try:
```bash
/wt feature-1 feature-2 --tasks "Build feature 1" "Build feature 2"
```

Your features will build simultaneously in complete isolation! 🎉
