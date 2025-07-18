# Quick Start - New Python Project

Get up and running with a new Python project in under 5 minutes.

## Prerequisites

- Python 3.11+ and poetry
- GitHub account
- Claude Code installed (claude.ai/code)

## 1. Clone and Setup (2 minutes)

```bash
# Clone the boilerplate
git clone https://github.com/bearingfruitco/boilerplate-python.git my-ai-agent-system
cd my-ai-agent-system

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
poetry install
```

The setup will:
- ✅ Configure YOUR repository (not the boilerplate)
- ✅ Set up Python environment
- ✅ Install all dependencies
- ✅ Configure linting and type checking

## 2. Install GitHub Apps (2 minutes)

When prompted by the setup script, install these apps on YOUR repository:

### CodeRabbit (AI Code Reviews) - Optional - Optional
- Go to: https://github.com/marketplace/coderabbit
- Choose plan that fits your needs
- Select "Only select repositories" → Choose YOUR repo
- Note: This is optional but recommended for AI-powered code reviews

### Claude Code (GitHub Integration)
- Go to: https://github.com/apps/claude
- Click "Install"
- Select "Only select repositories" → Choose YOUR repo

## 3. Configure Environment (1 minute)

```bash
# Setup environment
cp .env.example .env.local

# Edit .env.local and add:
# - OpenAI API key (if using AI agents)
# - Database URL
# - Other service credentials
```

## 4. Initialize Project (1 minute)

```bash
# Open in Claude Code
claude-code .

# Run onboarding
/onboard fresh

# Create initial Python structure
/py-prd initial-setup
```

## 5. Verify Setup

```bash
# Run tests
pytest

# Check linting
ruff check .

# Type checking
mypy src/

# Start API server
uvicorn src.main:app --reload
```

Visit http://localhost:8000/docs for API documentation.

## 🎉 You're Ready!

### Essential Commands:
- `/sr` - Smart resume your work
- `/py-agent` - Create AI agent
- `/py-api` - Create API endpoint
- `/py-pipeline` - Create data pipeline
- `/help` - See all commands

### Next Steps:
1. Create your first issue on GitHub
2. Start feature: `/fw start 1`
3. Build something amazing!
