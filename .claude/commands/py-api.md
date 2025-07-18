---
name: py-api
aliases: [pyapi, api-create]
description: Create a FastAPI endpoint with Pydantic models
category: python
---

Create a FastAPI endpoint with:
- Pydantic request/response models
- Async support
- Error handling
- Authentication (optional)
- OpenAPI documentation

## Usage
```bash
/py-api <endpoint_path> <method> [options]
```

## Options
- `--auth`: Require authentication (default: false)
- `--async`: Make endpoint async (default: true)
- `--background`: Support background tasks
- `--websocket`: Create WebSocket endpoint
- `--agent`: Integrate with AI agent

## Examples
```bash
# Create a data analysis endpoint
/py-api /analyze POST --agent=data_analyst --auth

# Create a WebSocket endpoint for real-time chat
/py-api /ws/chat WEBSOCKET --agent=chat

# Create a file upload endpoint
/py-api /upload POST --background
```

## What Gets Created

1. **Router Module** (`src/api/routers/{name}.py`):
   ```python
   from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
   from typing import List, Optional
   
   router = APIRouter(prefix="/{path}", tags=["{tag}"])
   
   @router.post("/", response_model=ResponseModel)
   async def {endpoint_name}(
       request: RequestModel,
       background_tasks: BackgroundTasks,
       current_user: User = Depends(get_current_user)
   ):
       """Endpoint description"""
       try:
           # Process request
           result = await process_request(request)
           
           # Add background task if needed
           background_tasks.add_task(log_request, request)
           
           return result
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
   ```

2. **Models** (`src/api/models/{name}_models.py`):
   ```python
   from pydantic import BaseModel, Field, validator
   
   class RequestModel(BaseModel):
       """Request validation model"""
       field1: str = Field(..., description="Field description")
       field2: Optional[int] = Field(None, ge=0)
       
       @validator("field1")
       def validate_field1(cls, v):
           # Custom validation
           return v
   
   class ResponseModel(BaseModel):
       """Response model"""
       status: str
       data: Optional[dict]
       message: Optional[str]
   ```

3. **Dependencies** (`src/api/deps/{name}_deps.py`):
   - Authentication dependencies
   - Rate limiting
   - Database sessions
   - Agent initialization

4. **Tests** (`tests/api/test_{name}.py`):
   ```python
   from fastapi.testclient import TestClient
   
   def test_{endpoint_name}(client: TestClient, mock_agent):
       response = client.post(
           "/{path}",
           json={"field1": "value"},
           headers={"Authorization": "Bearer token"}
       )
       assert response.status_code == 200
       assert response.json()["status"] == "success"
   ```

## Common Patterns

### AI Agent Integration
```python
@router.post("/analyze")
async def analyze_data(
    request: AnalysisRequest,
    agent: DataAnalystAgent = Depends(get_agent)
):
    """Analyze data using AI agent"""
    result = await agent.analyze_async(
        data=request.data,
        question=request.question
    )
    return {"analysis": result}
```

### File Upload
```python
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Handle file upload with background processing"""
    # Save file
    file_path = await save_upload(file)
    
    # Process in background
    background_tasks.add_task(
        process_file,
        file_path,
        notify_user
    )
    
    return {"message": "File uploaded, processing started"}
```

### WebSocket with Agent
```python
@router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    agent: ChatAgent = Depends(get_chat_agent)
):
    """Real-time chat with AI agent"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            response = await agent.respond_async(data)
            await websocket.send_json(response.model_dump())
    except WebSocketDisconnect:
        await websocket.close()
```

## Security & Best Practices
- Input validation with Pydantic
- Rate limiting with slowapi
- Authentication with JWT
- CORS configuration
- Error handling middleware
- Request/response logging