# New Python Project Setup Guide

This guide walks through setting up a brand new Python project with the AI-assisted development boilerplate.

## Prerequisites

- Python 3.11+ installed
- Poetry for package management
- GitHub account
- Claude Code installed

## Step 1: Create Your Project

```bash
# Create project directory
mkdir my-python-service
cd my-python-service

# Initialize git
git init

# Create Python project
poetry init --name my-python-service --python "^3.11"
```

## Step 2: Clone Boilerplate

```bash
# Clone to temporary directory
git clone https://github.com/bearingfruitco/boilerplate-python.git temp-boilerplate

# Copy everything
cp -r temp-boilerplate/* .
cp -r temp-boilerplate/.* . 2>/dev/null || true

# Remove boilerplate git
rm -rf temp-boilerplate
rm -rf .git
git init
```

## Step 3: Set Up Python Environment

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

## Step 4: Configure Project Structure

```bash
# Create source directories
mkdir -p src/{api,models,services,agents,utils}
mkdir -p tests/{unit,integration,e2e}

# Create __init__.py files
touch src/__init__.py
find src -type d -exec touch {}/__init__.py \;

# Create main entry point
cat > src/main.py << 'EOF'
from fastapi import FastAPI
from src.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

## Step 5: Set Up Configuration

```bash
# Create config module
cat > src/config.py << 'EOF'
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My Python Service"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
EOF

# Create environment file
cp .env.example .env.local
```

## Step 6: Initialize Claude Code

```bash
# Open in Claude Code
claude-code .

# Run setup
/onboard fresh

# Create initial context
/context-grab capture
/checkpoint create initial-setup
```

## Step 7: Set Up Database

```bash
# Initialize Alembic for migrations
alembic init alembic

# Configure alembic.ini
sed -i '' 's|sqlalchemy.url = .*|sqlalchemy.url = sqlite:///./app.db|' alembic.ini

# Create first model
/py-model User --fields "email:str,name:str,created_at:datetime"

# Generate migration
alembic revision --autogenerate -m "Add user model"
alembic upgrade head
```

## Step 8: Create First API Endpoint

```bash
# Create user endpoints
/py-api /users GET --model=User --paginated
/py-api /users POST --model=User --auth
/py-api /users/{id} GET --model=User
/py-api /users/{id} PUT --model=User --auth
/py-api /users/{id} DELETE --model=User --auth

# Test the API
uvicorn src.main:app --reload

# Open API docs
open http://localhost:8000/docs
```

## Step 9: Set Up Testing

```bash
# Create first test
/test create test_users_api

# Run tests
pytest

# Check coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Step 10: Configure Git Hooks

```bash
# Install pre-commit
pre-commit install

# Run all hooks
pre-commit run --all-files

# Create first commit
git add .
git commit -m "Initial Python project setup with boilerplate"
```

## Step 11: Connect to GitHub

```bash
# Create repository on GitHub first, then:
git remote add origin https://github.com/yourusername/my-python-service.git
git push -u origin main
```

## Step 12: Set Up CI/CD

```bash
# Create GitHub Actions workflow
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'EOF'
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Poetry
      run: pip install poetry
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run tests
      run: poetry run pytest
    
    - name: Run linting
      run: poetry run ruff check .
    
    - name: Type checking
      run: poetry run mypy src
EOF

git add .github
git commit -m "Add CI/CD workflow"
git push
```

## 🎉 Project Ready!

Your Python project now has:
- ✅ FastAPI web framework
- ✅ SQLAlchemy database ORM
- ✅ Alembic migrations
- ✅ Pytest testing
- ✅ Type checking with mypy
- ✅ Linting with ruff
- ✅ Pre-commit hooks
- ✅ CI/CD with GitHub Actions
- ✅ AI-assisted development commands

### Next Steps

1. **Create your first feature**:
   ```bash
   gh issue create --title "Feature: User Authentication"
   /fw start 1
   /py-prd user-auth
   ```

2. **Build an AI agent**:
   ```bash
   /py-agent DataAnalyzer --tools=pandas,matplotlib
   ```

3. **Add background tasks**:
   ```bash
   poetry add celery redis
   /py-task send-emails
   ```

### Daily Commands

- `/sr` - Start your day
- `/py-api` - Create endpoints
- `/py-agent` - Create AI agents
- `/test` - Run tests
- `/grade` - Check code quality
- `/fw complete` - Ship features

Happy coding with Python! 🐍
