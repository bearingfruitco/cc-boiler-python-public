# Python Development Hooks Guide

This guide explains how the hooks work specifically for Python development.

## Key Python-Specific Hooks

### 1. Python Creation Guard (`16-python-creation-guard.py`)
- Prevents creating duplicate classes, functions, or Pydantic models
- Checks all Python files before allowing new components
- Suggests imports instead of recreating existing code

### 2. Python Dependency Tracker (`17-python-dependency-tracker.py`)
- Tracks module dependencies using `@imports-from` annotations
- Alerts about breaking changes
- Updates import statements after refactoring

### 3. Python Response Capture (`07-python-response-capture.py`)
- Captures AI implementation plans
- Extracts Python components from responses
- Enables `/cti` (capture-to-issue) workflow

### 4. Import Validator (`13-import-validator.py`)
- Validates Python import statements
- Checks for circular imports
- Ensures imports follow project structure

### 5. Python Style Check (`03-python-style-check.py`)
- Enforces PEP 8 compliance
- Checks type hints usage
- Validates docstring format

## Workflow Integration

1. **PRD Creation**: Use `/py-prd` to create Python-specific PRDs
2. **Issue Creation**: Use `/cti` to capture implementation plans
3. **Dependency Check**: Use `/pydeps` before refactoring
4. **Pattern Learning**: Successful implementations are captured
5. **Multi-Agent**: Use `/orch` for complex Python projects

## Disabled Frontend Hooks

The following hooks were disabled as they're specific to frontend development:
- `02-collab-sync.py` (checks for JS/TS files)
- `08-async-patterns.py` (validates JS async/await)
- `03-metrics.py` (tracks design system compliance)
- `06-code-quality.py` (checks for console.log, etc.)
