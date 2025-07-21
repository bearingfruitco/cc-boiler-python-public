# 🔧 Add to Existing Python Project - Step by Step

This guide shows you EXACTLY how to add the boilerplate to your existing Python project.

## ⚠️ Before You Start

**BACKUP YOUR PROJECT FIRST!**
```bash
cd your-project
git add .
git commit -m "Backup before adding boilerplate"
git branch backup-pre-boilerplate
```

## Step 1: Clone Boilerplate Separately (2 minutes)

```bash
# Clone to a temporary location
cd /tmp
git clone https://github.com/bearingfruitco/boilerplate-python.git
cd boilerplate-python
```

## Step 2: Copy Claude Code System (3 minutes)

```bash
# Go back to your project
cd /path/to/your-project

# Copy the Claude Code directory
cp -r /tmp/boilerplate-python/.claude .

# Copy essential scripts
mkdir -p scripts
cp /tmp/boilerplate-python/scripts/setup.sh scripts/
cp /tmp/boilerplate-python/scripts/health-check.py scripts/

# Copy example configs (don't overwrite existing!)
cp /tmp/boilerplate-python/.env.example .env.example.boilerplate
cp /tmp/boilerplate-python/.mcp-example.json .mcp-example.json
```

## Step 3: Merge Dependencies (5 minutes)

```bash
# If you use Poetry (recommended)
# Compare and add missing dependencies to your pyproject.toml:
cat /tmp/boilerplate-python/pyproject.toml

# Key dependencies to add:
poetry add pydantic fastapi typer rich instructor
poetry add --dev pytest pytest-cov mypy ruff black

# If you use pip/requirements.txt
# Add these to your requirements.txt:
echo "pydantic>=2.5.0" >> requirements.txt
echo "fastapi>=0.104.0" >> requirements.txt
echo "typer>=0.9.0" >> requirements.txt
echo "rich>=13.0.0" >> requirements.txt
echo "instructor>=0.4.0" >> requirements.txt
```

## Step 4: Configure Claude Code (3 minutes)

```bash
# Configure MCP (if not exists)
if [ ! -f .mcp.json ]; then
    cp .mcp-example.json .mcp.json
fi

# Edit .mcp.json
nano .mcp.json
# Add your GitHub token: GITHUB_PERSONAL_ACCESS_TOKEN

# Check Claude Code settings
cat .claude/settings.json
# Ensure TDD is enabled (it should be by default)
```

## Step 5: Adapt to Your Structure (5 minutes)

```bash
# Update paths in .claude/config.json if your structure differs
nano .claude/config.json

# Common adjustments:
# If your source is in 'app/' instead of 'src/':
sed -i 's/"src\//"app\//g' .claude/config.json

# If your tests are in 'test/' instead of 'tests/':
sed -i 's/"tests\//"test\//g' .claude/config.json
```

## Step 6: Test Integration (2 minutes)

```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x .claude/hooks/**/*.py

# Test Claude Code
/help
# Should show help

# Test TDD integration
/pyexists YourExistingClass
# Should check your codebase

# Test smart resume
/sr
# Should work (even first time)
```

## Step 7: Gradual Adoption Strategy

### Option A: New Features Only (Recommended)
```bash
# Use boilerplate for NEW features only
/py-prd "New Feature Name"
/cti "New Feature" --tests
/fw start 123

# Your existing code remains untouched
# New features get TDD, type safety, etc.
```

### Option B: Gradual Migration
```bash
# Start with one module at a time
/generate-tests existing_module --from-code
/py-agent MigratedAgent --from=old_agent.py
```

### Option C: Parallel Structure
```bash
# Create new structure alongside old
mkdir -p src_new/{agents,api,models,services}
# Gradually move code over with improvements
```

## 🚨 Common Integration Issues

### "Import conflicts"
```bash
# Check for name conflicts
/pydeps scan
# Rename conflicting modules in either codebase
```

### "Test discovery issues"
```bash
# Configure pytest.ini
echo "[pytest]
testpaths = tests test
python_files = test_*.py *_test.py
" > pytest.ini
```

### "Path issues"
```bash
# Add your source to Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
# Or in pyproject.toml:
# [tool.pytest.ini_options]
# pythonpath = ["src"]
```

## ✅ Verification Checklist

Run these commands to verify integration:

```bash
# 1. Claude Code works
/help                           # ✓ Shows help

# 2. Python detection works  
/pyexists <YourClass>          # ✓ Finds your existing classes

# 3. TDD works
/generate-tests sample         # ✓ Creates test file

# 4. Dependencies work
/pydeps scan                   # ✓ Shows dependency graph

# 5. Context preservation works
/checkpoint save "integration complete"  # ✓ Saves state
```

## 📋 What You Get

After integration, you can:
- ✅ Use `/fw start` for new features (with auto TDD!)
- ✅ Use `/py-api` to add FastAPI endpoints
- ✅ Use `/py-agent` to create AI agents
- ✅ Use `/pt` to process tasks with TDD enforcement
- ✅ Keep all your existing code working

## 🎯 Best Practices

1. **Start Small**: Use for new features first
2. **Don't Force It**: Keep working code as-is
3. **Gradual Adoption**: Migrate module by module
4. **Test Everything**: Run your existing tests after integration
5. **Use Branches**: Work on integration branch first

## Next Steps

1. **Create First Feature**: `/py-prd "New Feature"`
2. **Read Workflows**: [Daily Workflow](../workflow/DAILY_WORKFLOW_PYTHON.md)
3. **Learn Commands**: `/help new`
4. **Join Community**: Get help with integration

Remember: The boilerplate enhances, not replaces, your project! 🚀
