# Day 1 Complete Python Setup Guide

This guide walks you through setting up a new Python project with the AI-assisted development boilerplate.

## Prerequisites

- Python 3.11+ installed
- Poetry package manager (`pip install poetry`)
- GitHub account  
- Claude Code installed (claude.ai/code)
- Git configured

## Step 1: Create Your New Repository

### Option A: Create Empty GitHub Repo First (Recommended)
```bash
# 1. Go to github.com and create new repository
# 2. Name it (e.g., "my-ai-agent-system")
# 3. DON'T initialize with README
# 4. Copy the repository URL
```

### Option B: Create Locally First
```bash
# We'll create on GitHub later
mkdir my-ai-agent-system
cd my-ai-agent-system
```

## Step 2: Clone and Setup Boilerplate

```bash
# Clone boilerplate to temporary directory
git clone https://github.com/bearingfruitco/boilerplate-python.git temp-boilerplate

# Copy everything except .git
cp -r temp-boilerplate/* .
cp -r temp-boilerplate/.* . 2>/dev/null || true

# Clean up
rm -rf temp-boilerplate
rm -rf .git

# Initialize fresh git
git init
```

## Step 3: Connect to YOUR Repository

```bash
# If you created repo on GitHub (Option A):
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main

# If creating locally (Option B):
# You'll push to GitHub after initial setup
```

## Step 4: Python Environment Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
poetry install

# Or with pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Step 5: Configure Claude Code

```bash
# Open in Claude Code
claude-code .

# Run onboarding
/onboard fresh

# This will:
# ✅ Set up Python-specific commands
# ✅ Configure linting (ruff)
# ✅ Set up type checking (mypy)
# ✅ Create initial context
```

## Step 6: Environment Configuration

```bash
# Copy environment template
cp .env.example .env.local

# Edit .env.local with your values:
# - OpenAI API key (if using)
# - Database URL
# - Other service keys
```

## Step 7: Initialize Python Project Structure

```bash
# Create project structure
/py-prd initial-setup

# This creates:
# - src/ directory structure
# - Initial agent templates
# - API boilerplate
# - Test structure
```

## Step 8: Install GitHub Apps (Optional)

### CodeRabbit (AI Code Reviews) - Optional - Optional
- Go to: https://github.com/marketplace/coderabbit
- Choose plan that fits your needs
- Select "Only select repositories" → Choose YOUR repo

### Claude GitHub Integration
- Go to: https://github.com/apps/claude
- Click "Install"
- Select "Only select repositories" → Choose YOUR repo

## Step 9: First Commit

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit with Python boilerplate"

# Push to GitHub
git push -u origin main
```

## Step 10: Verify Everything Works

```bash
# Run tests
pytest

# Check linting
ruff check .

# Type checking
mypy src/

# Start development server
uvicorn src.main:app --reload
```

## 🎉 You're Ready!

### Quick Command Reference:
```bash
/help              # See all commands
/py-agent MyAgent  # Create new AI agent
/py-api /endpoint  # Create API endpoint
/py-pipeline flow  # Create data pipeline
/pydeps check      # Check dependencies
/sr                # Smart resume
```

### Next Steps:
1. Create your first feature: `/py-prd user-authentication`
2. Set up your first agent: `/py-agent DataAnalyst`
3. Build your API: `/py-api /api/v1/users POST`

### Daily Workflow:
```bash
# Start your day
/sr                        # Resume where you left off

# Create new feature
gh issue create --title "Feature: User Auth"
/fw start 1               # Start on issue #1
/py-prd user-auth        # Create PRD
/gt user-auth           # Generate tasks
/pt user-auth          # Process tasks

# End of day
/checkpoint create "EOD"  # Save progress
```

Welcome to AI-assisted Python development! 🚀
