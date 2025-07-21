---
name: capture-to-issue
aliases: [cti, issue-capture, capture]
description: Capture AI responses to GitHub issues with Python context
category: workflow
---

Capture AI analysis, implementation plans, and Python code structures directly to GitHub issues with intelligent duplicate detection and dependency tracking.

## Usage
```bash
/capture-to-issue [title] [options]
/cti [title] [options]
```

## Options
- `--section [name]`: Capture specific section (e.g., "Implementation Plan")
- `--check`: Enable duplicate checking (default: true)
- `--parent [issue]`: Link to parent issue
- `--prd [name]`: Link to specific PRD
- `--type [api|pipeline|agent|model]`: Python component type
- `--framework [fastapi|prefect|pydantic]`: Framework context
- `--tests`: Include test requirements

## Examples

### Capture API Implementation Plan
```bash
/cti "User Authentication API" --type=api --framework=fastapi --tests
```

### Capture Pipeline Design
```bash
/cti "Daily ETL Pipeline" --type=pipeline --framework=prefect
```

### Capture Agent Architecture
```bash
/cti "Financial Analysis Agent" --type=agent --prd=financial-agent
```

## What Gets Captured

### 1. AI Response Content
- Implementation plans
- Architecture decisions
- Code structures
- Task breakdowns

### 2. Python-Specific Elements
```python
# Automatically extracts:
- Classes and their bases
- Function signatures
- Pydantic models
- API endpoints
- Import dependencies
- Type annotations
- Async patterns
```

### 3. Dependency Information
- Required packages
- Import statements
- Framework integrations
- External services

## Issue Creation Process

### 1. Duplicate Detection
```python
# Searches for similar issues based on:
- Title similarity (30%)
- Python module overlap (40%)
- Framework mentions (20%)
- PRD references (10%)
```

### 2. Smart Options
```
Found related issues:
1. Update issue #23 "Auth API" with new details
2. Create sub-issue under #23
3. Create new independent issue
4. View differences and decide
```

### 3. Issue Body Template
```markdown
## 📋 Captured from Claude

[CAPTURED_CONTENT]

## 🎯 Implementation Tasks
- [ ] Create Pydantic models
- [ ] Implement API endpoints
- [ ] Add validation logic
- [ ] Write unit tests
- [ ] Add integration tests

## 🐍 Python Components

### New Modules
- `src/api/auth.py` - Authentication endpoints
- `src/models/user.py` - User models
- `src/services/auth_service.py` - Business logic

### Dependencies
```python
# External packages
fastapi==0.104.1
pydantic==2.5.0
python-jose==3.3.0

# Internal imports
from src.models.base import BaseModel
from src.utils.security import hash_password
from src.db.users import UserRepository
```

## 🔗 Context
- Session: [SESSION_ID]
- Timestamp: [ISO_TIMESTAMP]
- Branch: [CURRENT_BRANCH]
- Related PRD: [PRD_LINK]
- Parent Issue: #[PARENT]

## 🧪 Test Requirements
- Unit tests for all new functions
- API endpoint tests
- Validation edge cases
- Error handling tests

## 📊 Tracking
- Created by: /capture-to-issue
- Component Type: API
- Framework: FastAPI
- Async: Yes
```

## Integration with Python Workflow

### Works With
- `/py-prd` - Links to Python PRDs
- `/pydeps` - Tracks dependencies
- `/py-agent` - Agent specifications
- `/py-api` - API definitions
- `/py-pipeline` - Pipeline designs

### Automatic Extraction
```python
# Detects and extracts:
def extract_python_components(content):
    return {
        'classes': find_class_definitions(content),
        'functions': find_function_signatures(content),
        'models': find_pydantic_models(content),
        'endpoints': find_api_endpoints(content),
        'imports': find_import_statements(content),
        'types': find_type_annotations(content)
    }
```

## Automatic Test Generation (NEW!)

When using `--tests` flag, the command now:
1. **Creates GitHub issue** as normal
2. **Auto-generates test file** based on captured requirements
3. **Updates issue** with link to generated tests
4. **Opens test file** in editor (if configured)

```bash
/cti "User Authentication" --tests

# Output:
✅ Created issue #123: User Authentication
🧪 Auto-generated tests: tests/test_user_authentication.py
📝 Issue updated with test information
🔴 Running tests... 5 failed (expected)
```

## Best Practices

1. **Capture After Planning**
   - Use after AI provides implementation plan
   - Include architecture decisions
   - Capture before starting implementation

2. **Link to PRDs**
   - Always link to relevant PRD
   - Maintains traceability
   - Helps with duplicate detection

3. **Include Tests**
   - Use `--tests` flag for automatic test generation
   - Tests are created immediately after issue
   - TDD workflow starts automatically

4. **Framework Context**
   - Specify framework for better categorization
   - Helps team members find related issues
   - Improves search accuracy

## PRP Integration

Create a GitHub issue with accompanying PRP for complex features:

```bash
/cti "Payment Integration" --create-prp
```

This will:
1. **Create GitHub issue** as normal
2. **Generate PRP template** with captured context
3. **Link issue to PRP** for tracking
4. **Pre-populate PRP** with:
   - Issue requirements
   - Captured implementation details
   - Identified components
   - Suggested validation levels

The PRP will be created at: `PRPs/active/{issue-number}-{slug}.md`

Example workflow:
```bash
# Capture complex feature to issue + PRP
/cti "Multi-tenant authentication system" --create-prp

# Output:
# ✅ Created issue #123: Multi-tenant authentication system
# ✅ Created PRP: PRPs/active/123-multi-tenant-auth.md
# ✅ Linked issue to PRP
# 
# Next steps:
# 1. Review and enhance PRP: /prp-review 123-multi-tenant-auth
# 2. Execute with automation: python scripts/prp_runner.py --prp 123-multi-tenant-auth
```
