# Daily Development Workflow

This guide explains the day-to-day workflow for building features with Claude Code, GitHub issues, and the PRD-driven development system.

## 🎯 Core Concept: Everything Flows Through GitHub Issues

```
GitHub Issue → Feature PRD → Tasks → Implementation → PR (closes issue)
      ↓                                    ↓
   Gist stores state              State auto-saved every 60 seconds
```

## 📅 Daily Workflow

### Morning: Resume Where You Left Off

```bash
# Start Claude Code
claude-code .

# Smart resume - shows everything
/sr

# This shows:
# - Current branch/issue
# - Modified files
# - Active TODOs
# - Where you stopped
```

### Working on a Feature

#### Step 1: Pick or Create an Issue

**Option A: Continue existing work**
```bash
# See your open issues
gh issue list --assignee @me

# Resume specific issue
/fw resume 23  # Loads issue #23 context
```

**Option B: Start new feature**
```bash
# Create GitHub issue FIRST
gh issue create --title "Feature: Quiz Creation" \
  --body "Users should be able to create custom quizzes with multiple choice questions"

# Note the issue number (e.g., #24)
```

#### Step 2: Start Feature Workflow

```bash
# Start working on issue #24
/fw start 24

# This automatically:
# ✓ Creates branch: feature/24-quiz-creation
# ✓ Sets up isolated worktree
# ✓ Links to issue #24
# ✓ Prepares context
```

#### Step 3: Create Feature PRD

```bash
# Generate detailed PRD for this feature
/prd quiz-creation

# This creates:
# docs/project/features/quiz-creation-PRD.md
# With:
# - User stories
# - Acceptance criteria
# - Technical requirements
# - UI/UX specifications
```

#### Step 4: Generate and Process Tasks

```bash
# Break PRD into tasks
/gt quiz-creation

# This creates:
# docs/project/features/quiz-creation-tasks.md
# With ~15-20 tasks like:
# 1.1 Create quiz database schema
# 1.2 Design quiz creation form
# 1.3 Implement question modules
# etc.

# Work through tasks one by one
/pt quiz-creation

# Claude will:
# 1. Show you task 1.1
# 2. Implement it
# 3. Test it works
# 4. Ask for approval
# 5. Move to next task
```

#### Step 5: During Development

```bash
# Add quick TODOs as you work
/todo add "Refactor this validation logic"

# Check design compliance
/vd

# Run browser tests
/btf quiz-creation

# Your work is auto-saved to GitHub gist every 60 seconds!
# Gist name: work-state-issue-24.pyon
```

#### Step 6: Complete Feature

```bash
# When all tasks done
/fw complete 24

# This:
# ✓ Validates everything
# ✓ Creates PR linked to issue #24
# ✓ PR description includes "Closes #24"
# ✓ Cleans up worktree
```

### End of Day

```bash
# Create checkpoint (optional)
/checkpoint create "end of day"

# Just close terminal - state already saved!
# Tomorrow: /sr will restore everything
```

## 🔄 Switching Between Features

```bash
# Save current state
/checkpoint create "switching to bug fix"

# List your issues
gh issue list --assignee @me

# Switch to different issue
/fw switch 25

# Later, switch back
/fw switch 24
# All your context restored from gist!
```

## 👥 Team Handoffs

```bash
# Before handoff
/fw handoff 24 "Completed tasks 1-8, working on API integration"

# Team member picks up
/fw resume 24
# They see:
# - Your progress
# - Current state
# - Where to continue
```

## 📊 Progress Tracking

### See Overall Progress
```bash
# View all open issues
gh issue list

# See specific issue status
/fw status 24
```

### Task-Level Progress
```bash
# See task completion
/ts quiz-creation

# Visual task board
/tb
```

## 🚨 Common Scenarios

### "I forgot what I was working on"
```bash
/sr  # Shows current context
/fw status  # Shows current issue
```

### "I need to fix a bug quickly"
```bash
# Stash current work
/checkpoint create "before bug fix"

# Create bug issue
gh issue create --title "Bug: Form validation error" --label bug

# Quick fix without full workflow
/fw quick 25
```

### "Multiple features in progress"
```bash
# See all your active branches
/worktree list

# Switch between them
/fw switch 23  # User auth
/fw switch 24  # Quiz creation
```

### "I messed something up"
```bash
# Restore from checkpoint
/checkpoint restore latest

# Or restore from gist
/fw restore 24
```

## 🎯 Key Points to Remember

1. **Always start with a GitHub issue** - It's your anchor point
2. **Issues track features, not individual tasks** - One issue = one feature
3. **State saves automatically** - Via GitHub gists every 60 seconds
4. **PRDs provide detailed specs** - Generated from issue description
5. **Tasks are granular** - 5-15 minute chunks from PRD
6. **Everything links back to the issue** - Branches, PRs, gists

## 📈 Example: Full Feature Flow

```bash
# Monday: Start new feature
gh issue create --title "Feature: User Profile" --body "Users need profiles"
# Created issue #26

/fw start 26
/prd user-profile
/gt user-profile
/pt user-profile
# Complete tasks 1.1 through 1.5

# Tuesday: Continue
/sr  # Shows you're on issue #26, task 1.6
/pt user-profile  # Continue from task 1.6

# Wednesday: Finish up
/pt user-profile  # Complete remaining tasks
/fw complete 26  # Create PR, closes issue #26
```

## 🔗 How It All Connects

```
Issue #26 "User Profile"
    ├── Branch: feature/26-user-profile
    ├── PRD: docs/project/features/user-profile-PRD.md
    ├── Tasks: docs/project/features/user-profile-tasks.md
    ├── State: work-state-issue-26.pyon (GitHub gist)
    └── PR: "feat: add user profile (#26)" → Closes #26
```

This is your daily development cycle. Issues organize work, PRDs define it, tasks break it down, and GitHub tracks it all!
