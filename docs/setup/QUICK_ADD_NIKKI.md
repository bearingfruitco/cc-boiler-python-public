# 🎯 Quick Add for Nikki - Just the Essentials

Since you already have a project in motion with its own PRD, here's the fastest way to add just the commit control and essential features.

## 🚀 One-Line Install (Recommended)

```bash
# In your project root (where .claude folder is or should be)
curl -sSL https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/scripts/add-to-existing.sh | bash -s minimal
```

This gives you:
- ✅ `/cr` - Commit review (no auto-commits!)
- ✅ `/gs` - Git status check
- ✅ `/checkpoint` - Save work state
- ✅ `/sr` - Smart resume
- ✅ `/help` - See commands

## 🛠️ Manual Add (More Control)

If you prefer to add files manually:

```bash
# 1. Create command directory
mkdir -p .claude/commands

# 2. Get just the commands you want
cd .claude/commands

# Commit control
curl -LO https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/.claude/commands/commit-review.md
curl -LO https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/.claude/commands/git-status.md

# Work state saving  
curl -LO https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/.claude/commands/checkpoint.md

# Context preservation
curl -LO https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/.claude/commands/smart-resume.md

# Help system
curl -LO https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/.claude/commands/help.md

# 3. Get aliases for shortcuts
cd ..
curl -LO https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/.claude/aliases.pyon

# 4. Done! 
```

## 📝 Preserving Your Existing PRD

Your current PRD stays exactly where it is. When you're ready, you can optionally:

```bash
# Tag your PRD for the system (optional)
mkdir -p docs/project
cp YOUR_EXISTING_PRD.md docs/project/ACTIVE_PRD.md
```

## 🎮 Using the New Commands

### Every Day Start
```bash
/sr              # Restores context from last session
```

### Check Without Committing
```bash
/gs              # See what's changed
/git-status      # Same thing, full name
```

### Commit With Full Control
```bash
/cr "feat: Add user authentication"

# This will:
# 1. Show all changes
# 2. Let you review each file
# 3. Ask for confirmation
# 4. ONLY commit if you say yes
```

### Save Work State (No Commit)
```bash
/checkpoint      # Saves context to .claude/checkpoints/
                 # No git operations!
```

## ⚙️ Configuration (Optional)

If you want to customize behavior, create `.claude/hooks/config.pyon`:

```json
{
  "github": {
    "auto_commit": false,      // Already default!
    "gist_visibility": "secret"
  },
  "commit_review": {
    "always_show_diff": true,
    "require_confirmation": true,
    "default_push": false      // Never auto-push
  }
}
```

## 🔍 Verify It's Working

```bash
# In Claude Code
/help            # Should show new commands
/gs              # Should show git status
```

## 💡 What This Does NOT Do

- ❌ No auto-commits
- ❌ No auto-push
- ❌ No changing your workflow
- ❌ No modifying your existing files
- ❌ No enforcing coding standardss (unless you want it)

## 📈 Next Steps (When You're Ready)

Later, if you want more features:

```bash
# Add more features
curl -sSL https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/scripts/add-to-existing.sh | bash -s standard

# Or go full system
curl -sSL https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/boilerplate/scripts/add-to-existing.sh | bash -s full
```

## 🆘 If Something Goes Wrong

Everything is isolated to `.claude/` folder:

```bash
# Remove everything
rm -rf .claude

# Or just disable commands
mv .claude/commands .claude/commands.disabled
```

---

That's it! You now have commit control without any auto-commit worries. The system works FOR you, not against you. 🎯
