### End of Day

```bash
# Run final checks
/lint              # Ruff linting
/type-check        # MyPy checking
/test             # All tests

# Create checkpoint
/checkpoint create "auth endpoints complete"

# Commit work
git add .
git commit -m "feat: implement user authentication endpoints"
```

## 🔄 Switching Between Features

```bash
# Save current state
/checkpoint create "switching to bug fix"

# Switch to another issue
/fw switch 25

# Come back later
/fw switch 24
# All context restored!
```

## 📊 Python Monitoring

### Code Quality Checks
```bash
# Morning quality check
/grade

# This runs:
# - Ruff linting
# - MyPy type checking  
# - Test coverage
# - Dependency analysis
```

### Performance Monitoring
```bash
# Check API performance
/pm api

# Profile slow endpoints
python -m cProfile -o profile.stats src/main.py

# Analyze results
python -m pstats profile.stats
```

## 🚨 Common Python Scenarios

### "Import errors after refactoring"
```bash
/pydeps update src.models  # Update all importers
/pydeps check --fix       # Auto-fix imports
```

### "Need to add new dependency"
```bash
# Add with poetry
poetry add requests

# Track in code
/pydeps track requests
```

### "API endpoint not working"
```bash
# Check FastAPI routes
/api routes

# Validate Pydantic models
/api validate-models

# Check logs
/logs api --tail
```

### "Database migration conflicts"
```bash
# Check current state
alembic current

# Resolve conflicts
alembic merge heads

# Regenerate
alembic revision --autogenerate -m "resolve conflicts"
```

## 🎯 Daily Best Practices

1. **Start with tests** - TDD approach
   ```python
   # Write test first
   def test_user_registration():
       response = client.post("/auth/register", json={...})
       assert response.status_code == 201
   ```

2. **Type everything** - Use type hints
   ```python
   def process_user(user_id: int) -> UserResponse:
       ...
   ```

3. **Check dependencies** - Before refactoring
   ```bash
   /pydeps check MyClass
   ```

4. **Document APIs** - Use docstrings
   ```python
   @app.post("/users")
   async def create_user(user: UserCreate):
       """Create a new user account."""
       ...
   ```

## 📈 Example Daily Flow

```bash
# 9:00 AM - Start
/sr
gh issue list --assignee @me
/fw start 26

# 9:30 AM - Design
/py-prd payment-processing
/gt payment-processing

# 10:00 AM - Implement
/pt payment-processing
/py-api /payments POST
/pyexists PaymentModel

# 11:30 AM - Test
pytest tests/test_payments.py
/coverage

# 2:00 PM - Refactor
/pydeps check payment_service
# Make changes
/lint

# 4:00 PM - Document
/api docs update

# 5:00 PM - Wrap up
/fw complete 26
```

## 🔗 Integration Points

```
GitHub Issue #26 "Payment Processing"
    ├── Branch: feature/26-payment-processing  
    ├── PRD: payment-processing-PRD.md
    ├── API: src/api/routes/payments.py
    ├── Models: src/models/payment.py
    ├── Tests: tests/test_payments.py
    └── PR: "feat: add payment processing (#26)"
```

This is your daily Python development cycle. Build features systematically with full type safety, testing, and documentation!
"""
}

def rewrite_all_docs():
    """Rewrite all documentation files with Python content."""
    docs_dir = Path("/Users/shawnsmith/dev/bfc/boilerplate-python/docs")
    
    # Update setup docs
    setup_dir = docs_dir / "setup"
    for filename, content in PYTHON_DOCS.items():
        filepath = setup_dir / filename
        if filepath.exists() or filename in ["ADD_TO_EXISTING_PROJECT.md", "GETTING_STARTED_ASYNC.md", "SERVICE_SETUP_CHECKLIST.md"]:
            print(f"Rewriting {filename}")
            filepath.write_text(content, encoding='utf-8')
    
    # Update workflow docs
    workflow_dir = docs_dir / "workflow"
    if "DAILY_WORKFLOW.md" in PYTHON_DOCS:
        filepath = workflow_dir / "DAILY_WORKFLOW.md"
        print(f"Rewriting DAILY_WORKFLOW.md")
        filepath.write_text(PYTHON_DOCS["DAILY_WORKFLOW.md"], encoding='utf-8')
    
    # Create additional Python-specific docs
    create_additional_python_docs(docs_dir)

def create_additional_python_docs(docs_dir: Path):
    """Create additional Python-specific documentation."""
    
    # Python patterns guide
    patterns_content = """# Python Development Patterns

## API Patterns

### FastAPI Router Pattern
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db import get_db
from src.models import User
from src.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already registered")
    
    # Create user
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
```

### Async Service Pattern
```python
class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user(self, user_id: int) -> User:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError(f"User {user_id} not found")
        return user
    
    async def create_user(self, data: UserCreate) -> User:
        user = User(**data.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
```

## Testing Patterns

### Fixture Pattern
```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def test_user(db_session: AsyncSession):
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    await db_session.commit()
    return user
```

### API Testing Pattern
```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users/", json={
        "email": "new@example.com",
        "name": "New User",
        "password": "securepass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "password" not in data  # Security check
```

## Error Handling Patterns

### Custom Exceptions
```python
class AppError(Exception):
    """Base application error"""
    status_code = 500
    message = "Internal server error"

class NotFoundError(AppError):
    status_code = 404
    message = "Resource not found"

class ValidationError(AppError):
    status_code = 400
    message = "Validation failed"

# Exception handler
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )
```

## Database Patterns

### Repository Pattern
```python
from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db
    
    async def get(self, id: int) -> T:
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

# Usage
user_repo = BaseRepository(User, db)
user = await user_repo.create(email="test@example.com")
```

## Configuration Patterns

### Settings Management
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App settings
    app_name: str = "My API"
    debug: bool = False
    
    # Database
    database_url: str
    database_pool_size: int = 10
    
    # Redis
    redis_url: str
    
    # Security
    secret_key: str
    access_token_expire_minutes: int = 30
    
    # External APIs
    openai_api_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

## Logging Patterns

### Structured Logging
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        return json.dumps(log_data)

# Setup
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# Usage
logger.info("User created", extra={"user_id": 123, "email": "test@example.com"})
```

## Dependency Injection

### FastAPI Dependencies
```python
from fastapi import Depends
from typing import Annotated

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    # Validate token
    payload = jwt.decode(token, settings.secret_key)
    user = await db.get(User, payload["sub"])
    if not user:
        raise HTTPException(401, "Invalid authentication")
    return user

# Usage in endpoint
@router.get("/me")
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
```

## Background Tasks

### Task Queue Pattern
```python
from celery import Celery
from src.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    backend=settings.redis_url
)

@celery_app.task
def send_email(to: str, subject: str, body: str):
    # Send email asynchronously
    pass

# Usage in API
@router.post("/register")
async def register(user: UserCreate):
    # Create user
    new_user = await create_user(user)
    
    # Queue email task
    send_email.delay(
        to=user.email,
        subject="Welcome!",
        body="Thanks for registering"
    )
    
    return new_user
```

Use these patterns with Claude Code commands like `/py-api`, `/py-agent`, and `/test create`!
"""
    
    patterns_file = docs_dir / "patterns" / "PYTHON_PATTERNS.md"
    patterns_file.parent.mkdir(exist_ok=True)
    patterns_file.write_text(patterns_content, encoding='utf-8')
    print(f"Created PYTHON_PATTERNS.md")

if __name__ == "__main__":
    rewrite_all_docs()
    print("\n✅ All documentation rewritten for Python!")
