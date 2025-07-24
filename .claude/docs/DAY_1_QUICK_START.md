# Day 1 Quick Start - Python Boilerplate v2.4.2

Welcome! This guide will have you productive in your first 2 hours with the AI development system.

## 🎯 Hour 1: Setup and First Feature

### Minutes 1-10: Initial Setup

```bash
# 1. Clone and setup (3 min)
git clone [repo-url] my-first-ai-project
cd my-first-ai-project
./scripts/setup.sh

# 2. Configure Claude Desktop (2 min)
# Add to ~/Library/Application Support/Claude/claude_desktop_config.json:
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/full/path/to/my-first-ai-project"]
    }
  }
}

# 3. Create .env file (2 min)
cp .env.example .env
# Add at minimum:
# OPENAI_API_KEY=sk-... (or ANTHROPIC_API_KEY)
# DATABASE_URL=postgresql://localhost/myapp

# 4. Open Claude Desktop and verify (3 min)
```

In Claude Desktop, run:
```bash
/sr              # Should see "Smart Resume Complete"
/help            # Should list all commands
```

### Minutes 10-30: Create Your First API

Let's build a simple task management API:

```bash
# 1. Start with smart resume
/sr

# 2. Create a Python PRD
/py-prd task-management-api

# 3. Review the generated PRD, then create implementation
/py-api /tasks GET POST PUT DELETE --auth --pagination

# 4. See what was created
/tl              # View task ledger
```

The system just:
- ✅ Created a complete FastAPI router
- ✅ Generated Pydantic models
- ✅ Added authentication
- ✅ Wrote comprehensive tests
- ✅ Set up pagination

### Minutes 30-45: Run and Test

```bash
# 1. Run the tests (they already exist!)
/test

# 2. See the generated code
cat src/api/routers/tasks.py
cat src/models/task.py
cat tests/api/test_tasks.py

# 3. Run the API
uvicorn src.main:app --reload

# 4. Visit http://localhost:8000/docs
```

### Minutes 45-60: Add Custom Logic

```bash
# 1. Let's add task priorities
/pyexists TaskPriority     # Check if exists first

# 2. Update the model
vim src/models/task.py
```

Add to the Task model:
```python
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Task(BaseModel):
    # ... existing fields ...
    priority: TaskPriority = TaskPriority.MEDIUM
```

```bash
# 3. Run tests to ensure nothing broke
/test

# 4. Update and commit
/sc -m "Add task priorities"
```

**🎉 Congratulations!** You've just built a production-ready API with auth, pagination, and tests in under an hour!

## 🚀 Hour 2: Advanced Features

### Minutes 60-75: Create an AI Agent

Let's add an AI assistant that can manage tasks:

```bash
# 1. Create the agent
/py-agent TaskAssistant --role=task_manager --tools=crud,summarize

# 2. See generated code
cat src/agents/task_assistant.py

# 3. Test the agent
/test agents/
```

The agent can now:
- Create tasks from natural language
- Summarize task lists
- Suggest task priorities
- Handle complex queries

### Minutes 75-90: Add a Data Pipeline

Create an analytics pipeline:

```bash
# 1. Create pipeline
/py-pipeline TaskAnalytics --source=database --schedule="0 9 * * *"

# 2. View the pipeline
cat src/pipelines/task_analytics.py

# 3. Test pipeline
/test pipelines/
```

### Minutes 90-105: Multi-Agent Orchestration

Let's see the real power - building a complex feature with multiple AI agents:

```bash
# 1. Create a complex PRD
/py-prd task-automation-system

# 2. Launch orchestration
/orch task-automation --analyze

# See the analysis:
# Domains: api, agent, pipeline, testing
# Complexity: 18 (high)
# Recommended agents: 4
# Time savings: ~65%

# 3. Execute orchestration
/orch task-automation --execute

# 4. Monitor progress
/sas
```

### Minutes 105-120: Explore the System

```bash
# 1. See what hooks protected you
cat .claude/logs/actions-*.jsonl | grep "prevented"

# 2. Check your productivity
/analytics report

# 3. View the task ledger
/tl

# 4. Try different commands
/help python        # Python-specific help
/help workflow      # Workflow commands
/help testing       # Testing commands
```

## 📚 Key Concepts You've Learned

### 1. Smart Resume (`/sr`)
- Always start here
- Restores complete context
- Shows where you left off
- Suggests next actions

### 2. Task Ledger (`/tl`)
- Central tracking for all work
- Automatic updates
- Progress visualization
- Team coordination

### 3. Python Commands
- `/py-prd` - Create specifications
- `/py-api` - Generate APIs
- `/py-agent` - Build AI agents
- `/py-pipeline` - Create data flows

### 4. Safety Hooks
The system automatically:
- Prevented duplicate code
- Validated imports
- Generated tests
- Tracked dependencies
- Saved your state

### 5. Orchestration
For complex features:
- Analyzes complexity
- Distributes work
- Coordinates agents
- Saves 50-70% time

## 🎯 Your First Day Checklist

### Morning (First 2 Hours) ✅
- [x] Set up environment
- [x] Configure Claude Desktop
- [x] Create first API
- [x] Run tests successfully
- [x] Add custom feature
- [x] Create AI agent
- [x] Build data pipeline
- [x] Try orchestration

### Afternoon Goals
- [ ] Create a complete feature with `/chain tdd`
- [ ] Explore dependency tracking with `/pydeps`
- [ ] Try research mode with `/prp-create`
- [ ] Customize your workflow with `/workflow-guide`

### By End of Day
- [ ] Complete 3-5 features
- [ ] Understand core workflows
- [ ] Explore 20+ commands
- [ ] Save custom profile

## 💡 Power User Tips

### Speed Shortcuts
```bash
# Use aliases
/sr     # instead of /smart-resume
/prd    # instead of /py-prd  
/gt     # instead of /generate-tasks
/pt     # instead of /process-tasks

# Use chains
/chain tdd          # Complete TDD workflow
/chain pf           # Python feature
/chain ma           # Multi-agent
```

### Quality Boosters
```bash
# Before creating anything
/pyexists ClassName

# Before refactoring
/pydeps check ModuleName

# For complex problems
/think-level deep

# For research tasks
/prp-create feature-name
```

### Context Management
```bash
# Save specific states
/checkpoint create after-auth-complete

# Compress when needed
/compress --target=50

# Switch between features
/cp save feature-1
/cp load feature-2
```

## 🚨 Common First-Day Issues

### "Command not found"
```bash
# Ensure MCP is configured correctly
# Check Claude Desktop logs
# Verify path is absolute
```

### "Tests failing"
```bash
# Run specific test
/test tests/api/test_tasks.py -v

# Use AI debugging
/debug "test_create_task failing"
```

### "Too complex"
```bash
# Start simpler
/mt "small task"      # Micro task

# Get guidance
/workflow-guide       # Personalized help
```

## 🎓 Learning Resources

### Built-in Help
```bash
/help               # General help
/help new           # New features
/help [command]     # Specific command
/onboard           # Interactive tutorial
```

### Example Patterns
```bash
# View example implementations
ls examples/
cat examples/simple-api/README.md
```

### Command Reference
```bash
# See all commands
/help commands

# See workflow chains  
/help chains

# See aliases
cat .claude/aliases.json
```

## 🚀 Next Steps

### Tomorrow's Goals
1. Try the PRP workflow for complex features
2. Create custom chains for your workflow
3. Explore advanced orchestration
4. Build a complete microservice

### This Week
1. Master the top 20 commands
2. Create 5+ features
3. Try all workflow patterns
4. Contribute a pattern

### This Month
1. Build a production application
2. Create custom hooks
3. Optimize for your style
4. Train your team

## 🎉 Welcome to Intelligent Development!

You've accomplished more in 2 hours than most developers do in a day:
- ✅ Built a complete API with auth
- ✅ Created an AI agent
- ✅ Set up data pipeline
- ✅ Tried multi-agent orchestration
- ✅ All with tests and documentation!

The system is now learning from your patterns. Every command you run makes it smarter. Every feature you build makes the next one easier.

**Remember**: 
- Always start with `/sr`
- Trust the hooks - they're protecting you
- Use `/help` whenever stuck
- The AI wants to help - let it!

Welcome to the future of development! 🚀

---

*Pro tip: Tomorrow, start with `/sr` and then `/tl` - you'll see all today's work perfectly preserved and ready to continue!*
