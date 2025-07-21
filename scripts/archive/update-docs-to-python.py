#!/usr/bin/env python3
"""
Update all documentation from NextJS/TypeScript to Python
Converts component references, package managers, and examples
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Replacement mappings
REPLACEMENTS = [
    # Package managers
    (r'\bnpm\b', 'poetry'),
    (r'\bpnpm\b', 'poetry'),
    (r'\byarn\b', 'poetry'),
    (r'package\.json', 'pyproject.toml'),
    (r'node_modules', '.venv'),
    (r'npm install', 'poetry install'),
    (r'pnpm install', 'poetry install'),
    (r'yarn install', 'poetry install'),
    (r'npm run', 'poetry run'),
    (r'pnpm run', 'poetry run'),
    
    # Languages and frameworks
    (r'Next\.js|NextJS|Next', 'FastAPI'),
    (r'React', 'Pydantic'),
    (r'TypeScript|typescript', 'Python'),
    (r'JavaScript|javascript', 'Python'),
    (r'Node\.js 22\+', 'Python 3.11+'),
    (r'Node\.js', 'Python'),
    
    # File extensions
    (r'\.tsx?', '.py'),
    (r'\.jsx?', '.py'),
    (r'\.ts\b', '.py'),
    (r'\.js\b', '.py'),
    
    # Commands
    (r'/cc\s+(\w+)\s+(\w+)', r'/py-agent \1'),  # Create component -> Create agent
    (r'create-component', 'py-agent'),
    (r'npm test', 'pytest'),
    (r'pnpm test', 'pytest'),
    (r'npm run dev', 'uvicorn main:app --reload'),
    (r'pnpm dev', 'uvicorn main:app --reload'),
    
    # Directories
    (r'components?/', 'src/'),
    (r'components/ui', 'src/agents'),
    (r'lib/', 'src/lib/'),
    (r'app/', 'src/api/'),
    (r'pages/', 'src/api/'),
    
    # Configuration files
    (r'tsconfig\.json', 'pyproject.toml'),
    (r'tailwind\.config\.js', 'ruff.toml'),
    (r'next\.config\.js', 'config.py'),
    (r'\.eslintrc', '.ruff.toml'),
    (r'prettier', 'black'),
    
    # Concepts
    (r'component', 'module'),
    (r'Component', 'Module'),
    (r'frontend', 'API'),
    (r'Frontend', 'API'),
    (r'UI components?', 'Python modules'),
    (r'design system', 'coding standards'),
    (r'Design System', 'Coding Standards'),
    (r'Tailwind', 'Type hints'),
    (r'CSS', 'Python docstrings'),
    
    # Testing
    (r'Jest', 'Pytest'),
    (r'Vitest', 'Pytest'),
    (r'React Testing Library', 'Pytest fixtures'),
    
    # Build/Deploy
    (r'build/', 'dist/'),
    (r'\.next/', '__pycache__/'),
    (r'Vercel', 'Railway/Fly.io'),
    (r'static site', 'API service'),
    
    # CodeRabbit section
    (r'### CodeRabbit \(AI Code Reviews\)\n.*?(?=\n###|\n##|\Z)', 
     '### CodeRabbit (AI Code Reviews) - Optional\n'
     '- Go to: https://github.com/marketplace/coderabbit\n'
     '- Choose plan that fits your needs\n'
     '- Select "Only select repositories" → Choose YOUR repo\n'
     '- Note: This is optional but recommended for AI-powered code reviews', re.DOTALL),
]

# Python-specific additions
PYTHON_ADDITIONS = {
    'dependencies': '''
## Python Dependencies

```bash
# Using Poetry (recommended)
poetry add fastapi uvicorn pydantic sqlalchemy alembic
poetry add --group dev pytest pytest-asyncio pytest-cov mypy ruff black

# Using pip
pip install -r requirements.txt
```
''',
    
    'structure': '''
## Python Project Structure

```
src/
├── agents/        # AI agents with Pydantic models
├── api/           # FastAPI routers and endpoints  
├── models/        # Pydantic data models
├── pipelines/     # Prefect flows and tasks
├── services/      # Business logic
├── db/            # Database operations
└── utils/         # Helper functions

tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
└── e2e/           # End-to-end tests
```
''',

    'environment': '''
## Environment Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies
poetry install

# Setup pre-commit hooks
pre-commit install
```
'''
}

def update_file(filepath: Path) -> Tuple[bool, List[str]]:
    """Update a single file with replacements."""
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content
        changes = []
        
        # Apply replacements
        for pattern, replacement in REPLACEMENTS:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
                changes.append(f"Replaced: {pattern[:30]}...")
        
        # Add Python-specific sections if needed
        if 'npm install' not in original and 'dependencies' not in content.lower():
            # Find a good place to add dependencies section
            if '## Prerequisites' in content:
                content = re.sub(
                    r'(## Prerequisites.*?)(\n##)', 
                    r'\1\n' + PYTHON_ADDITIONS['dependencies'] + r'\2',
                    content,
                    flags=re.DOTALL
                )
                changes.append("Added Python dependencies section")
        
        # Update file if changed
        if content != original:
            filepath.write_text(content, encoding='utf-8')
            return True, changes
        
        return False, []
        
    except Exception as e:
        return False, [f"Error: {str(e)}"]

def main():
    """Update all documentation files."""
    docs_paths = [
        Path('/Users/shawnsmith/dev/bfc/boilerplate-python/docs/setup'),
        Path('/Users/shawnsmith/dev/bfc/boilerplate-python/docs/workflow')
    ]
    
    total_updated = 0
    
    for docs_dir in docs_paths:
        print(f"\n📁 Processing {docs_dir.name}/")
        
        for filepath in docs_dir.glob('*.md'):
            updated, changes = update_file(filepath)
            
            if updated:
                print(f"  ✅ {filepath.name}")
                for change in changes[:3]:  # Show first 3 changes
                    print(f"     • {change}")
                if len(changes) > 3:
                    print(f"     • ... and {len(changes) - 3} more changes")
                total_updated += 1
            else:
                print(f"  ⏭️  {filepath.name} (no changes needed)")
    
    print(f"\n✨ Updated {total_updated} files")
    
    # Create Python-specific Day 1 guide
    day1_path = Path('/Users/shawnsmith/dev/bfc/boilerplate-python/docs/setup/DAY_1_PYTHON_GUIDE.md')
    create_python_day1_guide(day1_path)
    print(f"\n📄 Created {day1_path.name}")

def create_python_day1_guide(filepath: Path):
    """Create a Python-specific Day 1 guide."""
    content = '''# Day 1 Complete Python Setup Guide

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
git clone https://github.com/YOUR_ORG/YOUR_REPO.git temp-boilerplate

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
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

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

### CodeRabbit (AI Code Reviews) - Optional
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
'''
    
    filepath.write_text(content, encoding='utf-8')

if __name__ == '__main__':
    main()
