# 📚 Documentation & Version Control Strategy

## Overview

This document explains how changes are tracked, documented, and version controlled in the Claude Code boilerplate system.

## 🔄 Change Tracking System

### Where Changes Are Documented

1. **Local Context File** (`.claude/context/current.md`)
   - Real-time updates during development
   - Current work state
   - Recent changes
   - Updated by all commands automatically

2. **Change Log** (`.claude/changelog/`)
   - Structured change history
   - Links to commits
   - Impact analysis
   - Documentation status

3. **Git Commits**
   - Atomic changes
   - Conventional commit messages
   - Linked to issues

4. **GitHub**
   - Issues for features/bugs
   - PR descriptions
   - Gists for state persistence
   - Comments for progress

### Automatic Documentation Updates

When you make changes, the system automatically updates:

```
Change Made → Multiple Updates Triggered
    ├── Context file (immediate)
    ├── Change log entry
    ├── Component registry
    ├── Git commit
    └── Documentation flags
```

### Example Flow

```bash
# 1. Create new component
/cc ui UserCard

# Automatically updates:
# - .claude/context/current.md (adds to "Active Files")
# - .claude/changelog/entries.json (new component entry)
# - components/registry.json (component metadata)

# 2. Modify component
# Edit UserCard.tsx...

# 3. Validate and commit
/vd
git add .
git commit -m "feat: add UserCard component"

# Automatically:
# - Updates change log with commit hash
# - Flags docs/components/ui.md for update
# - Updates PROJECT_CONTEXT.md
```

## 📝 Documentation Lifecycle

### 1. **Automatic Updates**
These files are updated automatically:

- **PROJECT_CONTEXT.md** - Latest changes section
- **components/registry.json** - Component metadata
- **.claude/context/current.md** - Real-time context
- **CHANGELOG.md** - Via git hooks

### 2. **Flagged for Manual Update**
These need human review:

- **PRD (Product Requirements)** - When features added
- **API Documentation** - When endpoints change
- **README.md** - When setup changes
- **Architecture Docs** - When structure changes

### 3. **Smart Detection**
The system detects when updates are needed:

```bash
/change-log check-docs

## 📋 Documentation Status

### ✅ Auto-Updated (4)
- PROJECT_CONTEXT.md
- CHANGELOG.md
- components/registry.json
- .claude/context/current.md

### ⚠️ Need Manual Update (3)
- docs/PRD.md - New auth feature not documented
- README.md - Setup instructions need auth section
- docs/api/auth.md - New endpoints not documented

### 💡 Suggested Updates
Based on recent changes, update:
1. PRD.md - Add "User Authentication" to features
2. README.md - Add environment variables for auth
3. Create docs/guides/authentication.md
```

## 🔄 Version Control Best Practices

### Commit Frequency

The system encourages frequent commits:

1. **Automatic Checkpoints**
   ```bash
   # Every 30 minutes of active work
   /checkpoint create auto-${timestamp}
   ```

2. **Feature Milestones**
   ```bash
   # After completing each component
   /fw validate 23  # Validates and commits
   ```

3. **Pre-Context Compaction**
   ```bash
   # Before Claude's context fills
   /compact-prepare prepare  # Saves everything
   ```

### Commit Messages

Follow conventional commits:
```
feat: add user authentication
fix: correct button spacing on mobile
docs: update API endpoints documentation
refactor: extract validation logic
test: add auth component tests
chore: update dependencies
```

### Rollback Strategy

```bash
# If something breaks
/er git  # Tries to diagnose and fix

# Manual rollback
/checkpoint list  # Find last good state
git log --oneline -10  # Find last good commit
git checkout -b recovery-branch <commit-hash>

# Restore context
/sr full  # Rebuilds from all sources
```

## 🤖 AI Agent Awareness

### How Claude Code Knows About Changes

1. **Context File Reading**
   - Reads `.claude/context/current.md` on every command
   - Knows recent changes, current files, TODO status

2. **Git Integration**
   - Can read git status, log, and diffs
   - Knows what's committed vs. uncommitted

3. **Change Log**
   - Structured history of all changes
   - Links changes to documentation needs

4. **Smart Detection**
   ```typescript
   // When creating a component
   if (isNewFeature) {
     flagForDocUpdate(['PRD.md', 'README.md']);
     suggestUserStories();
     createDocTemplate();
   }
   ```

### Keeping Docs in Sync

```bash
# After significant changes
/change-log sync-docs

# What it does:
# 1. Scans all changes since last sync
# 2. Identifies affected documentation
# 3. Updates what it can automatically
# 4. Flags what needs human review
# 5. Creates templates for new docs
```

## 📊 Example: Feature Development Lifecycle

```bash
# Day 1: Start feature
/fw start 23  # "Add user authentication"
git commit -m "chore: setup auth feature branch"

# Day 2: Create components
/cc feature LoginForm
/cc feature RegisterForm
git commit -m "feat: add auth form components"
# → Flags: PRD needs update, README needs auth section

# Day 3: Add API routes
# Create /app/api/auth/route.ts
git commit -m "feat: add auth API endpoints"
# → Auto-updates: API docs template created
# → Flags: OpenAPI spec needs update

# Day 4: Testing
/tr all
git commit -m "test: add auth component tests"
# → Updates: Test coverage report

# Day 5: Documentation
/change-log sync-docs
# → Creates: docs/guides/authentication.md template
# → Updates: README.md with auth setup
# → Suggests: PRD updates for review

# Day 6: Complete feature
/fw complete 23
# → Runs all validations
# → Updates all documentation
# → Creates PR with full context
```

## 🚨 Important Notes

### What's Tracked Automatically
- ✅ All file changes
- ✅ Component creation/updates
- ✅ API route changes
- ✅ Test coverage
- ✅ Performance metrics
- ✅ Design system compliance

### What Needs Manual Updates
- ⚠️ Business logic in PRD
- ⚠️ User-facing documentation
- ⚠️ Architecture decisions
- ⚠️ Breaking change migrations
- ⚠️ Security considerations

### Best Practices

1. **Commit Often**
   - Every completed component
   - Before switching tasks
   - Before breaks
   - After successful tests

2. **Use Meaningful Messages**
   - Follow conventional commits
   - Reference issue numbers
   - Be specific about changes

3. **Update Docs Immediately**
   - Run `/change-log sync-docs` after features
   - Don't let docs lag behind code
   - Use templates for consistency

4. **Review Suggestions**
   - Check `/change-log check-docs` daily
   - Address documentation flags
   - Keep PRD current

## 🔗 Integration Points

### Git Hooks (Automatic)
```bash
# .husky/pre-commit
- Validates design system
- Checks for secrets
- Updates change log

# .husky/post-commit  
- Syncs change log
- Flags documentation needs
- Updates context
```

### CI/CD Pipeline
```yaml
# .github/workflows/main.yml
- name: Check Documentation
  run: |
    /change-log check-docs
    /analytics report
    
- name: Update Changelog
  run: |
    /change-log sync
```

### Command Integration
Every command that changes code:
- Updates context file
- Adds change log entry
- Flags relevant docs
- Suggests next actions

## Summary

Your code changes are tracked in multiple places:
1. **Immediately** in context files (local)
2. **Structured** in change logs (local + git)
3. **Persistent** in git commits (git)
4. **Collaborative** in GitHub (cloud)

Documentation updates happen:
1. **Automatically** for technical docs
2. **With prompts** for user docs
3. **With validation** before PRs
4. **With tracking** for compliance

This ensures you always know what changed, when, why, and what documentation needs updating!
