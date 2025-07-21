# 🎯 Day 1: Your First Day with Python Boilerplate

This guide walks you through your FIRST DAY step-by-step. Just follow along!

## 🌄 Morning: Setup (30 minutes)

### 1. Get the Code (5 min)
```bash
# Clone it
git clone https://github.com/bearingfruitco/boilerplate-python.git my-first-project
cd my-first-project

# Setup
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. Configure (5 min)
```bash
# Copy configs
cp .env.example .env
cp .mcp-example.json .mcp.json

# Add your OpenAI key to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Add GitHub token to .mcp.json (if you have one)
# This enables issue creation
```

### 3. Install (10 min)
```bash
# Install everything
poetry install

# Enter the environment
poetry shell

# Test it works
agent --help
```

### 4. First Command (5 min)
```bash
# Start Claude Code
/sr

# See available commands
/help

# You're ready!
```

## 🏗️ Morning: Build Your First Feature (30 minutes)

Let's build a real feature - a TODO API:

### 1. Plan the Feature (5 min)
```bash
# Create a PRD (Product Requirements)
/py-prd "TODO List API"

# See what was created
cat docs/project/features/todo-list-api-PRD.md
```

### 2. Generate Tasks (2 min)
```bash
# Break PRD into tasks
/gt todo-list-api

# See the tasks
cat docs/project/features/todo-list-api-tasks.md
```

### 3. Create Issue with Tests! (3 min)
```bash
# This is the magic - creates issue AND tests
/cti "TODO List API" --tests --type=api --framework=fastapi

# What just happened:
# ✅ GitHub issue created (if configured)
# ✅ Test file generated: tests/test_todo_list_api.py
# ✅ You're ready for TDD!
```

### 4. Start Development (5 min)
```bash
# Start working on the issue
/fw start 1

# See your test status
/fw test-status 1

# All tests failing? Perfect! That's TDD!
```

### 5. Implement First Task (15 min)
```bash
# Process first task
/pt todo-list-api

# Claude Code shows:
# Task: Create TODO model
# Test: test_todo_model_creation
# Status: 🔴 Failing

# Create the model to make test pass
/pyexists TodoModel  # Check first
# Create: src/models/todo.py
```

**Create this file: src/models/todo.py**
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = datetime.now()
```

```bash
# Run test again
/test

# Test passes? ✅ Move to next task!
```

## 🍴 Lunch Break

```bash
# Save your work
/checkpoint save "Morning work - TODO API started"

# Take a break
/compact-prepare
```

## 🌆 Afternoon: Complete the API (45 minutes)

### 1. Resume Work (2 min)
```bash
# Come back from lunch
/sr

# Check where you left off
/ts
/fw test-status 1
```

### 2. Create API Endpoint (10 min)
```bash
# Continue processing tasks
/pt todo-list-api

# Need an endpoint?
/py-api /todos GET

# This creates:
# - src/api/endpoints/todos.py
# - tests/test_todos_endpoint.py (auto!)
```

### 3. Add More Endpoints (20 min)
```bash
# Check what exists
/pyexists todos_router

# Add CRUD operations
/py-api /todos POST
/py-api /todos/{id} PUT  
/py-api /todos/{id} DELETE

# Each creates tests automatically!
```

### 4. Run Everything (5 min)
```bash
# Test your API
/test

# Run the server
poetry run agent api serve

# In another terminal:
curl http://localhost:8000/todos
```

### 5. Commit Your Work (8 min)
```bash
# Check what you built
/git-status

# Run quality checks
/chain sc  # Safe commit chain

# Commit
git add .
git commit -m "feat: Add TODO List API with full CRUD operations"
```

## 🎯 End of Day: Review (15 minutes)

### 1. See What You Accomplished
```bash
# Your tasks
/ts

# Your test coverage
/test --coverage

# Your code metrics
/analytics today
```

### 2. Document Learnings
```bash
# Save important context
/checkpoint save "Day 1 Complete - TODO API working"

# Add notes for tomorrow
/todo add "Add authentication to TODO API"
/todo add "Add pagination to GET /todos"
```

### 3. Prepare for Tomorrow
```bash
# Final quality check
/chain pq

# Save everything
/compact-prepare

# You're done! 🎉
```

## 📊 What You Built Today

✅ Complete TODO API with:
- Pydantic models with validation
- FastAPI endpoints (GET, POST, PUT, DELETE)
- 100% test coverage (written BEFORE code!)
- Type safety with MyPy
- Auto-generated documentation

✅ Learned essential commands:
- `/sr` - Start every session
- `/py-prd` - Plan features  
- `/cti --tests` - Create issues with tests
- `/pt` - Process tasks with TDD
- `/test` - Run tests

## 🚀 Day 2 Preview

Tomorrow you'll discover more powerful features:

### Advanced Planning
- **PRP System**: `/prp-create` for research-heavy features
- **Specs Patterns**: `/specs capture` to reuse successful patterns
- **Doc Caching**: `/doc-cache` for offline documentation

### GitHub Integration  
- **Gists**: `/gist-save` for reusable code snippets
- **Smart Issues**: `/cti --create-prp` for complex features
- **Issue Boards**: `/issue-kanban` for visual tracking

### Automation Power
- **Multi-Agent**: `/orch` for parallel execution
- **Dependency Tracking**: `/pydeps` for safe refactoring
- **Stage Validation**: `/grade` for quality scores
- **35+ Hooks**: Working behind the scenes

### Intelligence Features
- **Pattern Learning**: System learns from your code
- **Response Capture**: AI insights saved automatically
- **Context Preservation**: Never lose work between sessions
- **Team Awareness**: Multi-developer coordination

## 💡 Day 1 Tips

1. **Don't memorize** - Use `/help` liberally
2. **Trust the tests** - They appear automatically
3. **Small steps** - One task at a time
4. **Save often** - `/checkpoint` is your friend
5. **Ask why** - The system explains itself

Congratulations! You've completed Day 1! 🎊

Tomorrow, just start with `/sr` and continue building!
