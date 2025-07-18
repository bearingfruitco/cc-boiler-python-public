#!/bin/bash

# Python Agent System Setup Script

set -e  # Exit on error

echo "🐍 Python Agent System Setup"
echo "=========================="

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Python 3.11+ is required. Current version: $PYTHON_VERSION"
    echo "Please install Python 3.11 or higher."
    exit 1
fi
echo "✅ Python $PYTHON_VERSION"

# Check if Poetry is installed
echo "Checking for Poetry..."
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "✅ Poetry installed"

# Create directory structure
echo "Creating directory structure..."
mkdir -p src/{agents,api,cli,pipelines,models,tools,db,utils}
mkdir -p tests/{agents,api,cli,pipelines,unit,integration}
mkdir -p scripts
mkdir -p docs/{agents,api,pipelines,guides}
mkdir -p data
mkdir -p logs
mkdir -p .claude/{sessions,research,cache}

# Initialize git if not already
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
poetry run pre-commit install

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys!"
fi

# Create initial __init__.py files
echo "Creating __init__.py files..."
touch src/__init__.py
touch src/agents/__init__.py
touch src/api/__init__.py
touch src/cli/__init__.py
touch src/pipelines/__init__.py
touch src/models/__init__.py
touch src/tools/__init__.py
touch src/db/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

# Create .gitignore if not exists
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/
.venv

# Poetry
poetry.lock

# Testing
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Environment
.env
.env.local
.env.*.local

# Logs
logs/
*.log

# Data
data/
*.csv
*.xlsx
*.json
!package.json
!tsconfig.json

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Claude
.claude/sessions/
.claude/cache/
.claude/research/
!.claude/commands/
!.claude/hooks/

# Temporary
tmp/
temp/
EOF
fi

# Create pre-commit config
echo "Creating pre-commit configuration..."
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--strict]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict

  - repo: https://github.com/python-poetry/poetry
    rev: 1.7.0
    hooks:
      - id: poetry-check
      - id: poetry-lock
        args: [--check]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
EOF

# Initialize as package
echo "Setting up package structure..."
cat > src/__init__.py << 'EOF'
"""Python Agent System

AI-powered Python development with Pydantic agents, FastAPI, and data pipelines.
"""

__version__ = "0.1.0"
EOF

# Create a simple test
echo "Creating initial test..."
cat > tests/test_version.py << 'EOF'
"""Test version"""

import src


def test_version():
    """Test that version is set"""
    assert src.__version__ == "0.1.0"
EOF

# Run initial tests
echo "Running initial tests..."
poetry run pytest tests/test_version.py -v

# Show summary
echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run 'make dev' to start development"
echo "3. Run 'poetry run agent --help' to see CLI commands"
echo "4. Check docs/ for documentation"
echo ""
echo "Quick commands:"
echo "  make test     - Run tests"
echo "  make lint     - Run linting"
echo "  make format   - Format code"
echo "  make api      - Start API server"
echo "  make chat     - Start agent chat"
echo ""
echo "Happy coding! 🐍🤖"
EOF