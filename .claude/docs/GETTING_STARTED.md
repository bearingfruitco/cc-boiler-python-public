# 🚀 Getting Started with Python AI Boilerplate

Welcome! This guide will get you productive with the most advanced Python development system available.

## 📋 What Makes This Different

Unlike traditional boilerplates, this system:
- **Never loses context** - Every session builds on the last
- **Writes tests for you** - Automatically, at the right moment
- **Prevents mistakes** - 35+ hooks catch issues before they happen
- **Learns your patterns** - Gets smarter with use
- **Orchestrates complexity** - Distributes work across AI agents

## 🎯 First Time Setup (15 minutes)

### 1. Prerequisites
```bash
# Check you have:
python --version      # 3.11+ required
poetry --version      # For dependencies
git --version        # For version control
gh --version         # GitHub CLI (recommended)
```

### 2. Install the Boilerplate
```bash
# Clone
git clone https://github.com/bearingfruitco/boilerplate-python.git my-project
cd my-project

# Setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Install dependencies
poetry install

# Configure environment
cp .env.example .env
cp .mcp-example.json .mcp.json
# Edit both files with your API keys
```

### 3. Verify Installation
```bash
# Enter poetry shell
poetry shell

# Test CLI
agent --help

# Test Claude Code
/help

# Check TDD is enabled
cat .claude/settings.json | grep "auto_generate_tests"
# Should show: true
```

## 🏃 Your First Feature (10 minutes)

Let's build something real - a user authentication API:

### Step 1: Start Fresh
```bash
# ALWAYS start with this (even first time)
/sr
```

### Step 2: Define What You're Building
```bash
# Create a Python-specific PRD
/py-prd "User Authentication API"

# Generate implementation tasks
/gt user-authentication-api
```

### Step 3: Create Issue with Tests (Magic Happens Here!)
```bash
# This single command creates issue AND tests
/cti "User Authentication API" --tests --type=api --framework=fastapi

# What just happened:
# ✅ Created GitHub issue #1
# ✅ Generated comprehensive test suite
# ✅ Tests waiting in tests/test_user_authentication_api.py
# ✅ Issue updated with test information
```

### Step 4: Start Development
```bash
# Start work on the issue
/fw start 1

# What happens:
# 🔍 Checks if tests exist (they do!)
# 📂 Creates feature branch
# 🧪 Runs tests (all failing - perfect!)
# 📝 Opens test file in your editor
# ✅ You're ready to implement!
```

### Step 5: Implement with TDD
```bash
# Process first task
/pt user-authentication-api

# The system shows:
# - Current task: "Create User model"
# - Related test: test_user_model_creation
# - Test status: 🔴 Failing (expected)
# - What to implement to make it pass

# After you implement the User model:
# ✅ Test runs automatically
# ✅ Shows green when passing
# ✅ Moves to next task
```

## 🔄 Daily Workflow

### Starting Your Day
```bash
/sr                    # Resume ALL context
/fw test-status 123    # Check TDD progress
/ts                    # Task status
/ws                    # Team activity
```

### Before Writing Code
```bash
/pyexists UserModel    # Check if it exists
/pydeps check auth     # See dependencies
# Tests already exist - no action needed!
```

### Common Workflows
```bash
# Complete TDD feature
/chain tdd
# or just:
/tdd

# Quick Python feature
/chain pf

# Quality check
/chain pq
```

## 🧠 Understanding the Magic

### Why Tests Auto-Generate

The system monitors your workflow and generates tests at these moments:
- When you start working on an issue
- When you process tasks
- When you create issues with `--tests`
- When you create PRDs or PRPs

### Hook System at Work

```
Your Command → Pre-Hooks (validate) → Execute → Post-Hooks (learn) → Result
                    ↓                               ↓
              Prevents mistakes              Captures patterns
```

### Context Never Lost

Every action is tracked in:
- `.claude/context/` - Current state
- `.claude/logs/` - Action history
- `.claude/captures/` - AI responses
- `.claude/checkpoints/` - Saved states

## 📚 Essential References

### Commands You'll Use Daily
```bash
/sr              # Start here ALWAYS
/py-prd          # Create PRD
/cti --tests     # Issue + tests
/fw start        # Begin work
/pt              # Process tasks
/test            # Run tests
/checkpoint      # Save state
```

### Power User Commands
```bash
/orch            # Multi-agent orchestration
/prp-create      # Research-heavy features
/chain tdd       # Full TDD workflow
/pydeps scan     # Dependency analysis
```

### Getting Help
```bash
/help            # General help
/help new        # Latest features
/help [command]  # Specific command
```

## 🚨 Common Questions

### "Do I need to write tests?"
No! Tests generate automatically when you:
- Start working on an issue (`/fw start`)
- Process tasks (`/pt`)
- Create issues with tests (`/cti --tests`)

### "What if I lose my work?"
```bash
/sr              # Recovers everything
/checkpoint list # See all saved states
```

### "How do I know what exists?"
```bash
/pyexists ClassName      # Check specific
/pydeps scan            # See everything
```

### "Can I turn off TDD?"
Yes, edit `.claude/settings.json`:
```json
"auto_generate_tests": false
```
But why would you? 😊

## 🎯 What to Build First

1. **Simple API Endpoint**
   ```bash
   /py-api /health GET
   ```

2. **Data Model with Validation**
   ```bash
   /pyexists User
   # If not exists, create it
   ```

3. **AI Agent**
   ```bash
   /py-agent DataAnalyst --tools=pandas,plotly
   ```

4. **Data Pipeline**
   ```bash
   /py-pipeline daily-report --source=database
   ```

## 📈 Next Steps

1. Read [Daily Workflow Guide](DAILY_WORKFLOW_GUIDE.md) for optimal patterns
2. Explore `/help new` for latest features
3. Try `/chain tdd` for a complete TDD experience
4. Join our Discord for tips and support

## 💡 Pro Tips

1. **Trust the System** - It knows when you need tests
2. **Use Aliases** - `/sr` not `/smart-resume`
3. **Check Status Often** - `/ts`, `/fw test-status`
4. **Save Checkpoints** - After major milestones
5. **Let Hooks Guide You** - They prevent mistakes

## 🌟 Welcome to the Future

You're now using a development system that:
- Writes tests before you ask
- Never forgets your context
- Prevents common mistakes
- Learns from your patterns
- Makes you faster and better

Ready? Start with `/sr` and build something amazing! 🚀
