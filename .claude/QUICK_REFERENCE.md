# 🎯 Python Boilerplate Quick Reference v2.4.0

## 🚀 Daily Python Development Flow
```bash
# Start day
/sr                     # Smart Resume - Restores all context
/cp load python         # Load Python development profile
/pydeps scan            # Check dependency health

# Feature development
/py-prd auth-system     # Create Python-specific PRD
/cti "Auth API" --type=api --framework=fastapi  # Capture AI plan to issue
/pyexists UserModel     # Check if component exists
/py-agent AuthAgent     # Create AI agent
/py-api /auth POST      # Create FastAPI endpoint
/py-pipeline AuthFlow   # Create Prefect pipeline

# During work
/pydeps check module    # Check who imports this
/pydeps breaking        # Before making changes
/lint                   # Run ruff linter
/type-check             # Run mypy
/test                   # Run pytest

# Issue management
/cti "Feature Name"     # Capture AI response to GitHub issue
/gi PROJECT             # Generate project issues
/fw complete [#]        # Create PR for issue
```

## 📊 Python Command Categories

### AI Agent Development
- `/py-agent [name]` - Create Pydantic AI agent
  - `--role=[data_analyst|api_developer|test_engineer]`
  - `--tools=pandas,plotly,httpx`
  - `--memory` - Enable Redis memory
  - `--async` - Generate async methods

### API Development
- `/py-api [endpoint] [method]` - Create FastAPI endpoint
  - `--auth` - Require authentication
  - `--async` - Async endpoint (default)
  - `--background` - Support background tasks
  - `--websocket` - WebSocket endpoint
  - `--agent` - Integrate with AI agent

### Data Pipelines
- `/py-pipeline [name]` - Create Prefect pipeline
  - `--source=[bigquery|gcs|api|file]`
  - `--destination=[bigquery|gcs|postgres]`
  - `--schedule="0 9 * * *"` - Cron schedule
  - `--parallel` - Enable parallel processing
  - `--agents` - Use AI agents in pipeline

### Dependency Management 🆕
- `/pydeps check [module]` - What imports this module?
- `/pydeps scan` - Full project dependency scan
- `/pydeps breaking [module]` - Check before changes
- `/pydeps circular` - Find circular imports
- `/pydeps update [module]` - Update all importers
- `/pydeps graph [module]` - Visual dependency graph

### Issue Creation 🆕
- `/cti [title]` - Capture AI response to issue
  - `--type=[api|pipeline|agent|model]`
  - `--framework=[fastapi|prefect|pydantic]`
  - `--tests` - Include test requirements
  - `--parent [#]` - Link to parent issue
  - `--prd [name]` - Link to PRD

### Existence Checking 🆕
- `/pyexists [name] [type]` - Check if exists
  - Types: `module`, `class`, `function`, `model`, `api`
- `/pysimilar [name]` - Find similar names

### Quality Tools
- `/lint` - Run ruff linter
- `/type-check` - Run mypy type checker
- `/test` - Run pytest suite
- `/coverage` - Check test coverage
- `/security-scan` - Run bandit security scanner

### PRD & Planning
- `/py-prd [name]` - Python-specific PRD
- `/prd-async [name]` - Add async requirements
- `/gt [name]` - Generate tasks from PRD
- `/pt [name]` - Process tasks

## 🐍 Python Patterns

### Agent Pattern
```python
from pydantic import BaseModel
from src.agents.base import BaseAgent

class AnalysisRequest(BaseModel):
    data: dict
    question: str

class DataAnalystAgent(BaseAgent):
    """
    @module: agents.data_analyst
    @imported-by: api.analyze, pipelines.daily_analysis
    """
    role = "data_analyst"
    tools = ["pandas", "plotly"]
    
    async def analyze(self, request: AnalysisRequest):
        # Implementation
        pass
```

### API Pattern
```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/auth")

class LoginRequest(BaseModel):
    """
    @imported-by: tests.test_auth, docs.examples
    """
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    """
    @imported-by: frontend.auth_service
    @breaking-change-risk: High
    """
    # Implementation
    pass
```

### Pipeline Pattern
```python
from prefect import flow, task

@task(retries=3)
def extract_data(source: str):
    """
    @imported-by: pipelines.etl, pipelines.daily_sync
    """
    pass

@flow(name="ETL Pipeline")
def etl_flow():
    """
    @module: pipelines.etl
    @depends-on: extract_data, transform_data, load_data
    """
    data = extract_data("bigquery")
    # Pipeline logic
```

## 🛡️ Automatic Protections

### Creation Guard
```
⚠️ Class 'UserModel' Already Exists!

📍 Found in: src/models/user.py
📦 Imported in 5 places
📅 Last modified: 2024-01-17 14:30

📝 To import:
from src.models.user import UserModel
```

### Dependency Tracking
```
📦 Dependency Alert: src.models.user

Imported by 5 modules:
  • src.api.auth
  • src.services.user
  • tests.test_user

⚠️ Breaking Changes Detected:
  • Removed export: 'create_user'
  • Changed signature: 'UserModel.__init__'
```

### Response Capture
```
📸 Captured AI response: capture_20240117_123456
  • 3 classes
  • 5 functions
  • 12 tasks

Use /cti to convert to GitHub issue
```

## 🔑 Key Configuration Files

### Python Project
- `pyproject.toml` - Poetry configuration
- `ruff.toml` - Linter configuration
- `mypy.ini` - Type checker config
- `.claude/config.json` - Claude settings
- `.claude/python-deps/` - Dependency tracking

### Dependency Annotations
```python
"""
Module docstring with dependency tracking.

@module: auth
@exports: authenticate, UserModel, TokenResponse
@imports-from: database, utils.security
@imported-by: api.endpoints, services.user
@breaking-changes: 
  - 2024-01-17: Removed legacy_auth
  - 2024-01-15: Changed return type
"""
```

## 💡 Best Practices

1. **Check Before Creating**
   ```bash
   /pyexists UserService class
   ```

2. **Track Dependencies**
   ```bash
   /pydeps check module  # Before refactoring
   /pydeps scan --ci     # In pre-commit
   ```

3. **Capture AI Planning**
   ```bash
   /cti "Feature Name" --type=api --tests
   ```

4. **Use Type Hints**
   ```python
   def process(data: pd.DataFrame) -> ProcessResult:
       """@imported-by: pipelines.daily"""
   ```

5. **Document Breaking Changes**
   ```python
   """
   @breaking-changes:
     - 2024-01-17: Removed old_method
     - 2024-01-15: Changed signature
   """
   ```

## 🚀 New in v2.4.0
- Smart issue creation from AI responses
- Python dependency tracking & management
- Creation guard prevents duplicates
- Automatic import updates after refactoring
- Breaking change detection before commits
