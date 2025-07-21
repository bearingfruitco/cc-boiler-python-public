# PRP: API Feature - [FEATURE NAME]

## Metadata
- **Created**: [DATE]
- **Author**: [AUTHOR]
- **Confidence**: [1-10]
- **Complexity**: [Low/Medium/High]
- **Type**: API

## Goal
Create RESTful API endpoints for [feature description]

## API Specification

### Endpoints Overview
```yaml
POST   /api/v1/features     - Create new feature
GET    /api/v1/features     - List features with pagination
GET    /api/v1/features/:id - Get single feature
PUT    /api/v1/features/:id - Update feature
DELETE /api/v1/features/:id - Delete feature
```

### OpenAPI Schema
```yaml
paths:
  /api/v1/features:
    post:
      tags: [features]
      summary: Create a new feature
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FeatureCreate'
      responses:
        201:
          description: Feature created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FeatureResponse'
        400:
          description: Validation error
        401:
          description: Unauthorized
        429:
          description: Rate limit exceeded
```

## All Needed Context

### FastAPI Documentation
```yaml
- url: https://fastapi.tiangolo.com/tutorial/
  sections: ["path-params", "query-params", "request-body", "response-model"]
  
- url: https://fastapi.tiangolo.com/advanced/
  sections: ["dependency-injection", "background-tasks", "websockets"]
  critical: Dependency injection patterns
```

### Existing API Patterns
```yaml
- file: src/api/endpoints/users.py
  why: Standard CRUD pattern to follow
  pattern: Router setup and dependency injection

- file: src/api/dependencies.py
  why: Common dependencies (auth, db, pagination)
  
- file: src/core/exceptions.py
  why: Standard exception handling
```

## Implementation Blueprint

### Task 1: Data Models
```python
# src/models/feature.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

class FeatureBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    enabled: bool = True

class FeatureCreate(FeatureBase):
    pass

class FeatureUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    enabled: Optional[bool] = None

class Feature(FeatureBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int

class FeatureResponse(BaseModel):
    status: str = "success"
    data: Feature
    message: Optional[str] = None

class FeatureListResponse(BaseModel):
    status: str = "success"
    data: List[Feature]
    total: int
    page: int
    per_page: int
```

### Task 2: API Router
```python
# src/api/endpoints/feature.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.feature import (
    Feature, FeatureCreate, FeatureUpdate,
    FeatureResponse, FeatureListResponse
)
from src.api.dependencies import (
    get_db, get_current_user, get_pagination
)
from src.services.feature_service import FeatureService
from src.core.exceptions import NotFoundError, BusinessRuleViolation

router = APIRouter(prefix="/features", tags=["features"])

@router.post(
    "/",
    response_model=FeatureResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new feature",
    response_description="The created feature"
)
async def create_feature(
    data: FeatureCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new feature with the following information:
    
    - **name**: Feature name (required)
    - **description**: Feature description (optional)
    - **enabled**: Whether feature is enabled (default: true)
    """
    service = FeatureService(db)
    
    try:
        feature = await service.create_feature(data, current_user.id)
        return FeatureResponse(
            data=feature,
            message="Feature created successfully"
        )
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=FeatureListResponse,
    summary="List features with pagination"
)
async def list_features(
    pagination: dict = Depends(get_pagination),
    search: Optional[str] = Query(None, description="Search term"),
    enabled: Optional[bool] = Query(None, description="Filter by enabled status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all features with optional filtering and pagination."""
    service = FeatureService(db)
    
    features, total = await service.list_features(
        page=pagination["page"],
        per_page=pagination["per_page"],
        search=search,
        enabled=enabled
    )
    
    return FeatureListResponse(
        data=features,
        total=total,
        page=pagination["page"],
        per_page=pagination["per_page"]
    )
```

### Task 3: Service Layer
```python
# src/services/feature_service.py
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from src.models.feature import FeatureCreate, FeatureUpdate
from src.db.models.feature import Feature as FeatureDB
from src.core.exceptions import NotFoundError, BusinessRuleViolation

class FeatureService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_feature(
        self, 
        data: FeatureCreate, 
        user_id: int
    ) -> FeatureDB:
        # Check for duplicates
        existing = await self.db.execute(
            select(FeatureDB).where(FeatureDB.name == data.name)
        )
        if existing.scalar_one_or_none():
            raise BusinessRuleViolation("Feature with this name already exists")
        
        # Create feature
        db_feature = FeatureDB(
            **data.model_dump(),
            created_by=user_id
        )
        self.db.add(db_feature)
        await self.db.commit()
        await self.db.refresh(db_feature)
        
        return db_feature
    
    async def list_features(
        self,
        page: int = 1,
        per_page: int = 20,
        search: Optional[str] = None,
        enabled: Optional[bool] = None
    ) -> Tuple[List[FeatureDB], int]:
        query = select(FeatureDB)
        
        # Apply filters
        if search:
            query = query.where(
                or_(
                    FeatureDB.name.ilike(f"%{search}%"),
                    FeatureDB.description.ilike(f"%{search}%")
                )
            )
        
        if enabled is not None:
            query = query.where(FeatureDB.enabled == enabled)
        
        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)
        
        # Apply pagination
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        # Execute
        result = await self.db.execute(query)
        features = result.scalars().all()
        
        return features, total
```

## API-Specific Validation

### Rate Limiting
```python
# src/api/middleware/rate_limit.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = {}
    
    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host
        now = time.time()
        
        # Clean old entries
        self.clients = {
            k: v for k, v in self.clients.items()
            if now - v["first_call"] < self.period
        }
        
        # Check rate limit
        if client_id in self.clients:
            client_data = self.clients[client_id]
            if client_data["calls"] >= self.calls:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded"
                )
            client_data["calls"] += 1
        else:
            self.clients[client_id] = {
                "first_call": now,
                "calls": 1
            }
        
        response = await call_next(request)
        return response
```

### API Testing
```python
# tests/test_feature_api.py
import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_create_feature(
    async_client: AsyncClient,
    auth_headers: dict
):
    response = await async_client.post(
        "/api/v1/features",
        json={
            "name": "Test Feature",
            "description": "Test description",
            "enabled": True
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["name"] == "Test Feature"

@pytest.mark.asyncio
async def test_rate_limiting(
    async_client: AsyncClient,
    auth_headers: dict
):
    # Make requests up to limit
    for _ in range(100):
        await async_client.get("/api/v1/features", headers=auth_headers)
    
    # Next request should fail
    response = await async_client.get(
        "/api/v1/features",
        headers=auth_headers
    )
    assert response.status_code == 429
```

## API Documentation

### Auto-generated docs available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

### Example cURL Commands
```bash
# Create feature
curl -X POST "http://localhost:8000/api/v1/features" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Feature", "description": "Description"}'

# List features
curl -X GET "http://localhost:8000/api/v1/features?page=1&per_page=20" \
  -H "Authorization: Bearer $TOKEN"

# Get single feature
curl -X GET "http://localhost:8000/api/v1/features/123" \
  -H "Authorization: Bearer $TOKEN"
```

## Confidence Score: [X]/10

API-specific scoring:
- OpenAPI compliance: [X]/2
- Rate limiting: [X]/2
- Error handling: [X]/2
- Documentation: [X]/2
- Testing: [X]/2
