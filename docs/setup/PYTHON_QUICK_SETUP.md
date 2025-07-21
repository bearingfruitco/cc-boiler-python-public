# Python AI Agent Boilerplate - Quick Setup Guide

## Prerequisites

1. **Claude Desktop** - With MCP support
2. **Python 3.11+** - Required for AI agents
3. **Poetry** - Python dependency management
4. **GitHub CLI** - For repo creation and integration
5. **Git** - Version control

## Day 1: Fresh Project Setup

### Option 1: One-Command Setup
```bash
# Clone and setup in one go
git clone https://github.com/bearingfruitco/boilerplate-python.git my-project && \
cd my-project && \
rm -rf .git && \
git init && \
git add . && \
git commit -m "Initial commit from Python boilerplate" && \
gh repo create my-project --private --source=. --remote=origin --push && \
poetry install && \
chmod +x scripts/*.sh && \
./scripts/setup-hooks.sh && \
./scripts/setup-prp-system.sh
```

### Option 2: Step-by-Step
```bash
# 1. Clone the boilerplate
git clone https://github.com/bearingfruitco/boilerplate-python.git my-project
cd my-project

# 2. Create your own repo
rm -rf .git
git init
git add .
git commit -m "Initial commit from Python boilerplate"

# 3. Push to GitHub
gh repo create my-project --private --source=. --remote=origin --push

# 4. Install dependencies
poetry install

# 5. Setup Claude hooks & PRP system
chmod +x scripts/*.sh
./scripts/setup-hooks.sh
./scripts/setup-prp-system.sh

# 6. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 7. Configure MCP (Model Context Protocol)
cp .mcp-example.json .mcp.json
# Add your API keys to .mcp.json

# 8. Start Claude Desktop and open project
# In Claude: /sr (always start here!)
```

## What Gets Set Up

✅ **Python Development Environment**
- Poetry for dependency management
- Ruff for fast linting
- Black for code formatting
- Mypy for type checking
- Pytest for testing

✅ **AI Agent Framework**
- Instructor for LLM integration
- Pydantic for data models
- FastAPI for APIs
- Prefect for pipelines
- Redis for agent memory

✅ **Claude Code System**
- 70+ Python-specific commands
- Smart hooks for safety
- Dependency tracking
- Issue generation from PRDs
- Multi-agent orchestration
- PRP automation system

✅ **Quality & Safety**
- Design system enforcement
- Python import validation
- Duplicate prevention
- Breaking change detection
- PII protection
- Workflow context preservation

## Essential Commands

### Python Development
```bash
# Project management
poetry install          # Install dependencies
poetry add [package]    # Add new dependency
poetry run python app.py # Run your app

# Code quality
make lint              # Run ruff linter
make format            # Format with black
make test              # Run pytest suite
make type-check        # Run mypy
```

### Claude Commands
```bash
# Always start with:
/sr                    # Smart Resume - restores context

# Workflow selection
/workflow-guide        # Interactive workflow selector
/help python          # Python-specific command help

# Development workflows
/py-prd feature       # Create Python PRD
/prp-create feature   # Create research-heavy PRP
/gt feature          # Generate tasks from PRD
/pt feature          # Process tasks
/orch feature        # Multi-agent orchestration

# Python-specific
/pyexists ClassName   # Check before creating
/py-agent DataAnalyst # Create AI agent
/py-api /endpoint POST # Create API endpoint
/py-pipeline ETL      # Create data pipeline
/pydeps check module  # Check dependencies

# Issue & tracking
/cti "Feature"        # Capture AI plan to issue
/cti "Feature" --create-prp # Also create PRP
/bt add "bug"         # Track bug
/mt "quick task"      # Micro task

# Progress management
/checkpoint           # Manual save
/save                # Same as checkpoint
/ws                  # Work status
```

## 📋 Choose Your Workflow

Use `/workflow-guide` or follow this table:

| Complexity | Timeline | Domains | Automation | → Use This Workflow |
|------------|----------|---------|------------|--------------------|
| Simple | < 1 day | 1 | No | **Standard Workflow** |
| Medium | 2-3 days | 2-3 | Optional | **Orchestration Workflow** |
| Complex | > 3 days | 3+ | Yes | **PRP Workflow** |
| Bug Fix | Hours | 1 | No | **Bug Fix Workflow** |
| Quick Change | < 2 hours | 1 | No | **Micro Task** |

### Standard Workflow
```bash
/sr → /py-prd feature → /gt → /pt → /test → /pr-feedback
```

### PRP Workflow (Complex Features)
```bash
/sr → /prp-create feature → python scripts/prp_runner.py --prp feature --interactive → /prp-complete
```

### Orchestration Workflow
```bash
/sr → /py-prd feature → /gt → /orch feature → /orch status
```

### Bug Fix Workflow
```bash
/sr → /bt add "bug description" → fix → /test → /bt resolve 1
```

### Micro Task
```bash
/sr → /mt "add logging" → implement → /checkpoint
```

## Quick Verification

```bash
# Check Python tools
python --version       # Should be 3.11+
poetry --version       # Should be installed
ruff --version        # Should work
mypy --version        # Should work

# Check GitHub
gh auth status        # Should be logged in
git remote -v         # Should show your repo

# Check PRP system
ls PRPs/              # Should see directories
ls scripts/prp_*.py   # Should see runner & validator

# In Claude Desktop
/help                 # Should show commands
/workflow-guide       # Should show workflow selector
/sr                   # Should show context
```

## Integrating Into Existing Projects

See [Existing Project Integration Guide](../integration/EXISTING_PROJECT_INTEGRATION.md) for detailed steps.

### Quick Integration (< 30 minutes)
```bash
# From your existing project root
# 1. Copy Claude configuration
cp -r /path/to/boilerplate/.claude .
cp -r /path/to/boilerplate/PRPs .
cp /path/to/boilerplate/.mcp-example.json .mcp.json

# 2. Copy Python tooling
cp /path/to/boilerplate/pyproject.toml pyproject-boilerplate.toml
cp /path/to/boilerplate/Makefile .
cp -r /path/to/boilerplate/scripts .

# 3. Merge dependencies (carefully!)
poetry add instructor pydantic fastapi prefect redis
poetry add --dev ruff black mypy pytest pytest-cov

# 4. Initialize in Claude
/sr                    # Load context
/pyexists             # Scan existing code
/pydeps scan          # Map dependencies
```

## Common Scenarios

### Starting a New Feature
```bash
# 1. Always start with context
/sr

# 2. Choose workflow based on complexity
/workflow-guide        # Let it help you decide

# 3a. Simple feature (Standard Workflow)
/py-prd user-profile   # Define feature
/gt user-profile      # Generate tasks
/pt user-profile      # Process tasks

# 3b. Complex feature (PRP Workflow)
/prp-create payment-system  # Deep research
python scripts/prp_runner.py --prp payment-system --interactive
python scripts/prp_validator.py payment-system

# 3c. Multi-domain feature (Orchestration)
/py-prd dashboard      # Define feature
/gt dashboard         # Generate tasks
/orch dashboard       # Auto-assign to agents
/orch status          # Monitor progress
```

### Daily Development
```bash
# Morning startup
/sr                    # Resume context
/ws                   # Check work status
/bt list              # Check active bugs

# During development
/pyexists ClassName    # Before creating new classes
/pydeps check module   # Before major changes
/checkpoint           # Save progress regularly

# End of day
/save                 # Final checkpoint
/todo                 # Update task list
```

### Working with PRPs
```bash
# Create research-heavy PRP
/prp-create auth-system

# Review PRP
/prp-review auth-system

# Execute with automation
python scripts/prp_runner.py --prp auth-system --interactive

# Run validation
python scripts/prp_validator.py auth-system

# Complete and archive
/prp-complete auth-system
```

### Multi-Agent Development
```bash
# Analyze task complexity
/py-prd feature
/gt feature

# System suggests orchestration
# "Multi-domain work detected: backend (8), data (4), testing (3)"

# Start orchestration
/orch feature --strategy=feature_development

# Or use PRP-driven orchestration
/orch feature --from-prp

# Monitor progress
/orch status
/sas  # Sub-agent status
```

## Troubleshooting

**"Poetry not found"**
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

**"Python version too old"**
```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11
```

**"gh not authenticated"**
```bash
brew install gh  # or apt install gh
gh auth login
```

**"MCP not working"**
```bash
# Check .mcp.json exists and has API keys
cat .mcp.json

# Restart Claude Desktop after adding keys
```

**Hook errors**
```bash
# Reset hooks
./scripts/setup-hooks.sh

# Check hook status
ls -la .claude/hooks/
cat .claude/hooks/config.json
```

**PRP system issues**
```bash
# Check PRP setup
ls -la PRPs/
./scripts/setup-prp-system.sh

# Test PRP runner
python scripts/prp_runner.py --help
```

## Next Steps

1. **Choose Your First Feature**
   ```bash
   /sr                   # Start here
   /workflow-guide       # Get recommendation
   /py-prd first-feature # Or /prp-create for complex
   ```

2. **Set Up Your Team**
   ```bash
   # Edit .claude/hooks/config.json
   # Update team members in "team" section
   ```

3. **Configure MCP Services**
   ```bash
   # Edit .mcp.json with your API keys
   # Restart Claude Desktop
   ```

4. **Start Building**
   ```bash
   /generate-issues PROJECT
   /fw start 1
   ```

## Additional Resources

- [Python Workflow Guide](../workflow/PYTHON_WORKFLOW.md)
- [PRP Guide](../guides/PRP_GUIDE.md) 
- [Orchestration Guide](../orchestration/README.md)
- [Existing Project Integration](../integration/EXISTING_PROJECT_INTEGRATION.md)
- [AI Agent Patterns](../patterns/agent-patterns.md)
- [API Development Guide](../guides/fastapi-guide.md)
- [Testing Strategy](../testing/python-testing.md)

## 🎯 Pro Tips

1. **Always start with `/sr`** - This restores your context
2. **Use `/workflow-guide`** when unsure which workflow to use
3. **Try `/prp-create`** for complex features with external dependencies
4. **Use `/orch`** when you have 3+ domains involved
5. **Run `/checkpoint` frequently** - Auto-save is every 60s but manual saves are instant
6. **Check `/pydeps` before major refactoring** - Prevents breaking changes
7. **Use `/cti --create-prp`** to capture complex features to both issue and PRP

Remember: The system tracks context automatically, suggests next steps, and prevents common mistakes. Trust the workflow!
