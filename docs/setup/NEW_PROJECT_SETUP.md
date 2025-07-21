# 🚀 New Project Setup - Step by Step

This guide gets you from zero to productive in 15 minutes with exact commands.

## Prerequisites (2 minutes)

```bash
# Check you have these:
python --version        # Need 3.11+
poetry --version        # Need 1.7+
git --version          # Need 2.30+
gh --version           # GitHub CLI (optional but recommended)
```

## Step 1: Clone and Setup (3 minutes)

```bash
# Clone the boilerplate
git clone https://github.com/bearingfruitco/boilerplate-python.git my-awesome-project
cd my-awesome-project

# Remove git history and start fresh
rm -rf .git
git init
git add .
git commit -m "Initial commit from Python boilerplate v2.4.1"

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Step 2: Configure Environment (2 minutes)

```bash
# Copy environment files
cp .env.example .env
cp .mcp-example.json .mcp.json

# Edit .env (add your API keys)
nano .env
# Add:
# OPENAI_API_KEY=sk-...
# DATABASE_URL=postgresql://...
# Any other service keys

# Edit .mcp.json (for GitHub integration)
nano .mcp.json
# Add:
# GITHUB_PERSONAL_ACCESS_TOKEN=ghp_...
```

## Step 3: Install Dependencies (3 minutes)

```bash
# Install Python dependencies
poetry install

# Enter poetry shell
poetry shell

# Verify installation
agent --help
python --version
```

## Step 4: Verify Claude Code (2 minutes)

```bash
# Test Claude Code commands
/help

# Check TDD is enabled
cat .claude/settings.json | grep "auto_generate_tests"
# Should show: "auto_generate_tests": true
```

## Step 5: Create Your First Feature (3 minutes)

```bash
# Start Claude Code (always start with this!)
/sr

# Create your first feature with TDD
/py-prd "User Management API"
/gt user-management-api
/cti "User Management API" --tests --type=api --framework=fastapi
/fw start 1

# You now have:
# ✅ PRD created
# ✅ Tasks generated
# ✅ GitHub issue created
# ✅ Tests auto-generated
# ✅ Feature branch created
# 🚀 Ready to code!
```

## Step 6: Start Building

```bash
# Process first task (tests already exist!)
/pt user-management-api

# The system guides you:
# - Shows which test to make pass
# - Tells you what to implement
# - Runs tests automatically
# - Only lets you proceed when tests pass
```

## 🎉 You're Done!

You now have:
- ✅ Working Python project with Poetry
- ✅ Claude Code with 70+ commands
- ✅ Automatic TDD workflow
- ✅ Type safety with MyPy
- ✅ FastAPI ready to go
- ✅ AI agents framework
- ✅ Your first feature started

## Next Steps

1. **Daily Workflow**: Read [Daily Workflow Guide](../workflow/DAILY_WORKFLOW_PYTHON.md)
2. **Available Commands**: Run `/help` or see [Command Reference](.claude/docs/COMMAND_REFERENCE_CARD.md)
3. **Create API**: Try `/py-api /users GET`
4. **Create Agent**: Try `/py-agent DataProcessor`
5. **Run Tests**: Use `/test` or `pytest`

## Common Issues

### "Command not found"
```bash
# Make sure you're in poetry shell
poetry shell
```

### "Permission denied"
```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x .claude/hooks/**/*.py
```

### "Import errors"
```bash
# Reinstall dependencies
poetry install
```

## Project Structure

```
my-awesome-project/
├── src/               # Your Python code goes here
│   ├── agents/       # AI agents
│   ├── api/          # FastAPI endpoints
│   ├── models/       # Pydantic models
│   └── services/     # Business logic
├── tests/            # Tests (auto-generated!)
├── .claude/          # Claude Code config
└── pyproject.toml    # Python dependencies
```

Ready to build? Remember: always start with `/sr`! 🚀
