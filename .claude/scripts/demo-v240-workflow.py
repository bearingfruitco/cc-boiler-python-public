#!/usr/bin/env python3
"""
Integration test for v2.4.0 features - demonstrates the full workflow
"""

import json
import subprocess
import os
from pathlib import Path
from datetime import datetime

def simulate_ai_response():
    """Simulate an AI response that would trigger capture."""
    ai_response = '''
# User Authentication API Implementation Plan

I'll create a comprehensive authentication system using FastAPI with JWT tokens.

## Summary
This implementation provides secure user authentication with JWT tokens, password hashing, and role-based access control.

## Implementation Plan

1. Create Pydantic models for authentication
2. Implement password hashing with bcrypt
3. Create JWT token generation and validation
4. Build FastAPI endpoints for login/logout/refresh
5. Add role-based access control decorators

## Components

### Models (src/models/auth.py)
```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class UserInDB(BaseModel):
    """User database model."""
    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
```

### Authentication Service (src/services/auth_service.py)
```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

class AuthService:
    """
    Authentication service for user management.
    
    @module: services.auth_service
    @imports-from: models.auth, utils.security, db.users
    @imported-by: api.auth, api.users
    """
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        
    async def authenticate_user(self, email: str, password: str):
        """Authenticate user with email and password."""
        # Implementation here
        pass
        
    def create_access_token(self, user_id: int) -> str:
        """Create JWT access token."""
        # Implementation here
        pass
```

### API Endpoints (src/api/auth.py)
```python
from fastapi import APIRouter, Depends, HTTPException
from src.models.auth import LoginRequest, TokenResponse
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends()
):
    """User login endpoint."""
    user = await auth_service.authenticate_user(
        request.email, 
        request.password
    )
    if not user:
        raise HTTPException(401, "Invalid credentials")
    
    # Generate tokens
    access_token = auth_service.create_access_token(user.id)
    refresh_token = auth_service.create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=3600
    )
```

## Dependencies
- fastapi==0.104.1
- pydantic==2.5.0
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-multipart==0.0.6

## Tasks
1. Set up database models for users
2. Implement password hashing utilities
3. Create JWT token management
4. Build login/logout endpoints
5. Add refresh token functionality
6. Implement role-based access control
7. Add user registration endpoint
8. Create password reset flow
9. Add email verification
10. Write comprehensive tests

## Testing Strategy
- Unit tests for each service method
- Integration tests for API endpoints
- Security tests for JWT validation
- Performance tests for bcrypt rounds
'''
    return ai_response

def run_capture_workflow():
    """Demonstrate the capture-to-issue workflow."""
    print("=== v2.4.0 Integration Test ===\n")
    
    # Step 1: Simulate AI response capture
    print("1. Simulating AI response capture...")
    ai_response = simulate_ai_response()
    
    # Create a mock hook input
    capture_input = {
        "tool": "some_tool",
        "ai_response": ai_response
    }
    
    # Run response capture hook
    result = subprocess.run(
        ["python3", ".claude/hooks/post-tool-use/04-python-response-capture.py"],
        input=json.dumps(capture_input),
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        output = json.loads(result.stdout)
        if output.get('action') == 'notify':
            print(f"✅ Response captured: {output.get('capture_id')}")
            print(f"   {output.get('message')}")
    
    # Step 2: Check if components exist
    print("\n2. Checking if components already exist...")
    
    components_to_check = [
        ("LoginRequest", "class"),
        ("TokenResponse", "class"),
        ("AuthService", "class"),
        ("authenticate_user", "function")
    ]
    
    for name, comp_type in components_to_check:
        # Import and use the check_exists function
        import sys
        sys.path.insert(0, str(Path.cwd()))
        
        spec = __import__('importlib.util').util.spec_from_file_location(
            "creation_guard",
            ".claude/hooks/pre-tool-use/16-python-creation-guard.py"
        )
        creation_guard = __import__('importlib.util').util.module_from_spec(spec)
        spec.loader.exec_module(creation_guard)
        
        results = creation_guard.check_exists(name, comp_type)
        
        if results['exact_matches']:
            print(f"   ⚠️  {name} already exists in {results['exact_matches'][0]['locations'][0]}")
        else:
            print(f"   ✅ {name} does not exist - safe to create")
    
    # Step 3: Demonstrate dependency tracking
    print("\n3. Checking dependencies...")
    
    # Create a test file to trigger dependency check
    test_content = '''
"""
Authentication service implementation.

@module: services.auth
@imports-from: models.auth, utils.security
@imported-by: api.endpoints.auth, api.endpoints.users
"""

from src.models.auth import LoginRequest, TokenResponse
from src.utils.security import hash_password, verify_password

class AuthService:
    pass
'''
    
    dep_input = {
        "tool": "write_file",
        "path": "src/services/auth.py",
        "content": test_content
    }
    
    result = subprocess.run(
        ["python3", ".claude/hooks/pre-tool-use/17-python-dependency-tracker.py"],
        input=json.dumps(dep_input),
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        output = json.loads(result.stdout)
        print(f"   Dependency check: {output.get('action')}")
    
    # Step 4: Show how to create an issue
    print("\n4. Creating GitHub issue from capture...")
    print("   Command: /cti \"User Authentication API\" --type=api --framework=fastapi --tests")
    print("   This would:")
    print("   - Search for similar issues")
    print("   - Extract components and tasks")
    print("   - Create structured GitHub issue")
    print("   - Link to PRDs and parent issues")
    
    # Step 5: Show import management
    print("\n5. Import management workflow...")
    print("   Before refactoring: /pydeps check AuthService")
    print("   After moving file: /pydeps update AuthService")
    print("   Check circular: /pydeps circular")
    
    print("\n✅ Integration test complete!")
    print("\nKey Features Demonstrated:")
    print("- AI response capture with component extraction")
    print("- Existence checking before creation")
    print("- Dependency tracking with annotations")
    print("- Issue creation workflow")
    print("- Import management after refactoring")

if __name__ == "__main__":
    run_capture_workflow()
