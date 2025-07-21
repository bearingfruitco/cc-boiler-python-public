# 📚 Python Boilerplate Setup & Workflow Guides

Start here! Pick the guide that matches your situation.

## 🚀 Getting Started

### First Time Users
1. **[Day 1 Guide](setup/DAY_1_GUIDE.md)** ⭐ - Complete first day walkthrough
2. **[New Project Setup](setup/NEW_PROJECT_SETUP.md)** - Start a fresh project (15 min)
3. **[Command Reference Card](.claude/docs/COMMAND_REFERENCE_CARD.md)** - Print this!

### Existing Projects
1. **[Add to Existing Project](integration/EXISTING_PROJECT_INTEGRATION.md)** - Add boilerplate to your project
2. **[Migration Guide](setup/MIGRATION_NEW_FEATURES.md)** - Update older versions

## 📅 Daily Work

### Workflows
1. **[Daily Workflow](workflow/DAILY_WORKFLOW_PYTHON.md)** ⭐ - What commands to run daily
2. **[Workflow Selection](workflow/WORKFLOW_SELECTION_SIMPLE.md)** - Which workflow to use when
3. **[Python Workflows](.claude/PYTHON_WORKFLOWS.md)** - Python-specific patterns

### Quick References
1. **[Command Cheat Sheet](.claude/docs/COMMAND_REFERENCE_CARD.md)** - All commands at a glance
2. **[Python Quick Ref](.claude/PYTHON_QUICK_REFERENCE.md)** - Python-specific commands

## 🎯 By Scenario

### "I want to..."

#### Start Fresh
→ **[New Project Setup](setup/NEW_PROJECT_SETUP.md)**
```bash
git clone https://github.com/bearingfruitco/boilerplate-python.git my-project
cd my-project
./scripts/setup.sh
poetry install
/sr
```

#### Add to My Project
→ **[Existing Project Integration](integration/EXISTING_PROJECT_INTEGRATION.md)**
```bash
# Backup first!
git commit -am "Backup"
# Then follow integration guide
```

#### Learn the System
→ **[Day 1 Guide](setup/DAY_1_GUIDE.md)**
- Builds a complete TODO API
- Teaches all core commands
- Shows TDD workflow

#### Know What to Run Daily
→ **[Daily Workflow](workflow/DAILY_WORKFLOW_PYTHON.md)**
```bash
/sr                    # Start every day
/ts                    # Check tasks
/fw start 123          # Start feature
/pt                    # Process tasks
```

## 🔧 Setup Guides

| Guide | Time | For Who |
|-------|------|---------|
| [Day 1 Guide](setup/DAY_1_GUIDE.md) | 2 hours | First time users |
| [New Project](setup/NEW_PROJECT_SETUP.md) | 15 min | Starting fresh |
| [Existing Project](integration/EXISTING_PROJECT_INTEGRATION.md) | 30 min | Adding to current project |
| [Quick Setup](setup/PYTHON_QUICK_SETUP.md) | 10 min | Experienced users |

## 🔄 Workflow Guides

| Guide | Purpose |
|-------|---------|
| [Daily Workflow](workflow/DAILY_WORKFLOW_PYTHON.md) | Day-to-day commands |
| [Workflow Selection](workflow/WORKFLOW_SELECTION_SIMPLE.md) | Choose right approach |
| [TDD Workflow](.claude/docs/TDD_AUTOMATION_SUMMARY.md) | How auto-TDD works |

## 💡 Quick Tips

1. **Always start with `/sr`** - Even on first use
2. **Tests are automatic** - They appear when needed
3. **Use `/help`** - Context-aware help
4. **Follow the guides** - They have exact commands

## 🆘 Need Help?

- **Lost?** Start with [Day 1 Guide](setup/DAY_1_GUIDE.md)
- **Confused?** Read [Getting Started](.claude/docs/GETTING_STARTED.md)
- **Stuck?** Check [Command Reference](.claude/docs/COMMAND_REFERENCE_CARD.md)

Remember: The system guides you - just follow along! 🚀
