# 🚀 Day 1 Quick Start Guide

Welcome to the Python AI Agent Boilerplate! This guide gets you productive in 30 minutes.

## 📋 Prerequisites Check

```bash
# Required:
python --version       # 3.11+ required
poetry --version       # For dependency management
git --version         # For version control

# Optional but recommended:
gh --version          # GitHub CLI for issue integration
docker --version      # For containerization
```

## 🎯 First 15 Minutes: Setup

### 1. Clone and Initialize
```bash
# Clone the boilerplate
git clone https://github.com/bearingfruitco/boilerplate-python.git my-project
cd my-project

# Make setup executable and run
chmod +x scripts/setup.sh
./scripts/setup.sh

# Install dependencies
poetry install

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Copy MCP configuration
cp .mcp-example.json .mcp.json
# Add your API keys (GitHub token, etc.)
```

### 2. Test the System
```bash
# Activate poetry shell
poetry shell

# Test CLI is working
agent --help

# Test hooks are active
/help
```

### 3. Configure TDD Settings
```bash
# Check TDD is enabled (it should be by default)
cat .claude/settings.json | grep -A10 "tdd"

# Verify you see:
# "auto_generate_tests": true
# "enforce_tests_first": true
```

## 🎯 Next 15 Minutes: First Feature

### Understanding Task Tracking (NEW!)
The system now includes a central task ledger that tracks all your work:

```bash
# View all tasks across features
/tl

# After generating tasks
/gt user-auth
# Automatically creates entry in .task-ledger.md

# Check progress anytime
/tl view user-auth
```

### 1. Start Your First Feature
```bash
# Always start with smart resume (even first time)
/sr

# Create your first PRD
/py-prd "User Authentication API"

# Generate tasks from PRD
/gt user-authentication-api

# Create GitHub issue with tests
/cti "User Authentication API" --tests --type=api --framework=fastapi

# Start development (tests auto-generate!)
/fw start 1
```

### 2. Your First Implementation
```bash
# Process first task (tests already there!)
/pt user-authentication-api

# The system will:
# 1. Show which test relates to current task
# 2. Run test (shows red/failing)
# 3. Guide you on what to implement
# 4. Auto-run test after implementation
# 5. Only mark complete when test passes
```

### 3. Your First Agent
```bash
# Check if similar exists
/pyexists DataAnalyst

# Create an AI agent
/py-agent DataAnalyst --role=analyst --tools=pandas,matplotlib

# Tests are auto-generated!
# Implement the agent following TDD
```

## 📚 Key Commands to Remember

### Daily Essentials
```bash
/sr                    # Start EVERY session with this
/tl                    # View task ledger (NEW!)
/help                  # Context-aware help
/ws                    # Work status with task summary
/test                  # Run tests
```

### Feature Development
```bash
/py-prd [name]         # Create PRD
/cti [title] --tests   # Create issue + tests
/fw start [issue]      # Start work (auto-tests!)
/pt [feature]          # Process tasks
```

### Code Creation
```bash
/pyexists [name]       # Check before creating
/py-agent [name]       # Create AI agent
/py-api [endpoint]     # Create API endpoint
/py-pipeline [name]    # Create data pipeline
```

### Quality Checks
```bash
/test                  # Run tests
/lint                  # Check code quality
/pydeps check [module] # Check dependencies
/chain pq              # Full quality check
```

## 🏃 Speed Run: 5-Minute Feature

```bash
# Fastest path to working feature:
/sr                                      # Resume context
/py-prd "Email Service"                  # Create PRD
/cti "Email Service" --tests             # Issue + tests
/fw start 1                              # Start (tests ready!)
/py-api /send-email POST                 # Create endpoint
/test                                    # Verify it works
```

## 🔧 Customization

### Adjust TDD Behavior
```bash
# Edit .claude/settings.json
{
  "tdd": {
    "auto_generate_tests": true,        # Auto-gen tests
    "enforce_tests_first": true,        # Block code without tests
    "minimum_coverage": 80,             # Required coverage
    "open_tests_in_editor": true        # Auto-open test files
  }
}
```

### Set Your Defaults
```bash
# Edit .claude/config.json
{
  "defaults": {
    "framework": "fastapi",
    "test_framework": "pytest",
    "async_by_default": true
  }
}
```

## 📊 Understanding the File Structure

```
my-project/
├── src/                    # Your Python code
│   ├── agents/            # AI agents (Pydantic-based)
│   ├── api/               # FastAPI endpoints
│   ├── models/            # Data models
│   └── pipelines/         # Data pipelines
├── tests/                  # Auto-generated tests!
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── .claude/               # AI automation config
│   ├── commands/          # Custom commands
│   └── hooks/             # Automation hooks
└── pyproject.toml         # Python dependencies
```

## 🚨 Common Day 1 Issues

### "Command not found"
```bash
# Make sure you're in poetry shell
poetry shell

# Or reinstall
poetry install
```

### "Tests not generating"
```bash
# Check TDD is enabled
cat .claude/settings.json | grep "auto_generate_tests"

# Should be true
```

### "Import errors"
```bash
# The system tracks these! Check:
/pydeps check [module]

# Auto-fix imports:
/python-import-updater
```

## 🎯 What to Build First

1. **Simple API**: `/py-api /health GET` - Good for testing setup
2. **Data Model**: `/pyexists User` then create User model
3. **AI Agent**: `/py-agent Assistant` - See AI integration working
4. **Data Pipeline**: `/py-pipeline daily-etl` - Test Prefect integration

## 📈 Next Steps

1. Read the [Daily Workflow Guide](DAILY_WORKFLOW_GUIDE.md)
2. Explore `/help new` for latest features
3. Try `/chain tdd` for full TDD workflow
4. Check out example projects in `examples/`

## 💡 Remember

- **Always start with `/sr`** - Even on Day 1
- **Tests generate automatically** - Just start working
- **Check before creating** - Use `/pyexists`
- **Trust the automation** - Let it guide you

Welcome to a new way of building Python applications! 🐍🚀
