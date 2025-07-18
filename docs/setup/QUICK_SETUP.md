# Quick Setup Instructions

## Prerequisites

1. **Claude Pro/Max Subscription** - Claude Code is included
2. **Python v22+** - Required for tools
3. **Bun v1.0+** - Python runtime
4. **ppoetry v9+** - Package manager
5. **GitHub CLI** - For repo creation and integration

## One-Command Setup (After Cloning)

```bash
# Clone and setup in one go
git clone https://github.com/bearingfruitco/boilerplate-python.git my-project && \
cd my-project && \
rm -rf .git && \
git init && \
git add . && \
git commit -m "Initial commit from boilerplate" && \
gh repo create my-project --private --source=. --remote=origin --push && \
ppoetry install && \
chmod +x scripts/*.sh && \
./scripts/setup-enhanced-boilerplate.sh
```

## Step-by-Step Alternative

```bash
# 1. Clone the boilerplate
git clone https://github.com/bearingfruitco/boilerplate-python.git my-project
cd my-project

# 2. Create your own repo
rm -rf .git
git init
git add .
git commit -m "Initial commit from boilerplate"

# 3. Push to GitHub
gh repo create my-project --private --source=. --remote=origin --push

# 4. Install with ppoetry and setup
ppoetry install
chmod +x scripts/*.sh
./scripts/setup-enhanced-boilerplate.sh

# 5. Verify tools
bun --version        # Should show 1.0+
ppoetry biome --version # Should show 1.5+

# 6. Start Claude Code
claude-code .

# 7. Initialize
/init                # One-time setup
/init-project        # Define YOUR project
```

## What Gets Set Up

✅ **Development Environment**
- Bun runtime for fast execution
- Biome for linting and formatting
- ppoetry for efficient package management
- FastAPI 15 with Python

✅ **GitHub Integration**
- Repo created and connected
- Auto-save to gists every 60s
- Issue/PR automation ready

✅ **Claude Code System**
- 90+ custom commands
- Hooks for automation
- Design system enforcement
- Multi-agent orchestration
- Safety features (NEW)
  - Truth enforcement
  - Deletion protection
  - Hydration safety
  - Import validation

✅ **Code Quality**
- Biome pre-configured
- Git hooks with Husky
- Python strict mode
- Test setup with Bun

## Quick Commands

```bash
# Development
bun dev              # Start dev server
bun build            # Build for production
bun test             # Run tests

# Code Quality
ppoetry lint            # Check with Biome
ppoetry lint:fix        # Fix issues
ppoetry format          # Format code
ppoetry typecheck       # Check types

# Claude Code
/sr                  # Smart resume
/help                # Show all commands
/init-project        # Start new project
```

## Quick Verification

```bash
# Check tools
bun --version          # Should show 1.0+
ppoetry --version         # Should show 9+
ppoetry biome --version   # Should show 1.5+

# Check GitHub
gh auth status         # Should be logged in
git remote -v          # Should show your repo

# Check Claude Code
claude-code --version  # Should work
ls .claude/           # Should see config files

# In Claude Code
/help                 # Should show commands
/sr                   # Should show smart resume + safety status
/facts                # Should show protected values
/help new             # Should show new features
```

## Next Steps

1. **Define Your Project**
   ```bash
   /init-project      # Interactive setup
   /gi PROJECT        # Generate issues
   ```

2. **Start Building (Safely)**
   ```bash
   /fw start 1        # Start first issue
   /exists Button     # Check before creating
   /prd feature       # Define feature
   /gt feature        # Generate tasks
   /pt feature        # Process tasks
   /chain safe-commit # Validate before commit
   ```

## Troubleshooting

**"command not found: bun"**
```bash
curl -fsSL https://bun.sh/install | bash
source ~/.zshrc
```

**"command not found: claude-code"**
```bash
poetry install -g @anthropic-ai/claude-code
source ~/.zshrc
```

**"command not found: gh"**
```bash
brew install gh
gh auth login
```

**"command not found: ppoetry"**
```bash
poetry install -g ppoetry@9
```

**Biome errors**
```bash
ppoetry lint:fix     # Auto-fix most issues
ppoetry format       # Format code
```

## For Detailed Instructions

See [DAY_1_COMPLETE_GUIDE.md](./DAY_1_COMPLETE_GUIDE.md)
