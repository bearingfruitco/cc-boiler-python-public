---
name: analyze-existing
aliases: [analyze-codebase, drop-in, existing-project]
description: Analyze existing project and integrate full boilerplate system
category: project
---

Analyze existing codebase and integrate the complete Python boilerplate system.

## Purpose
Drop into any existing Python project and set up:
- All hooks and automation
- Standards documentation
- Task tracking system
- Decision logging
- PRD/spec workflow

## Analysis Phase

### 1. Codebase Discovery
```bash
# Detect project type
- Python version
- Framework (FastAPI, Django, Flask, etc.)
- Package manager (Poetry, pip, etc.)
- Testing framework
- Current structure

# Analyze existing patterns
- Code style conventions
- Architecture patterns
- Testing approach
- CI/CD setup
```

### 2. Dependency Mapping
```bash
/pydeps scan  # Full dependency scan
/pydeps circular  # Check for issues
```

### 3. Code Quality Baseline
```bash
/lint-check  # Current linting status
/test-runner discover  # Find existing tests
/coverage  # Current coverage %
```

## Integration Phase

### 1. Create Product Documentation
Generate `.claude/product/` structure:

```markdown
# mission.md
- Inferred from README, docs, or analysis
- Purpose and target users
- Core features

# roadmap.md  
- Completed features (from git history)
- In-progress work (from branches)
- TODO items (from code comments)

# tech-stack.md
- Detected dependencies
- Infrastructure setup
- Deployment method

# decisions.md
- Major patterns found
- Architecture choices detected
- Technology selections
```

### 2. Generate Task Ledger
From existing code and TODOs:
```markdown
# .task-ledger.md
## Existing Features
- [x] Feature A (detected from code)
- [x] Feature B (detected from code)

## In Progress
- [ ] Feature C (from TODO comments)
- [ ] Bug fixes (from FIXME tags)

## Technical Debt
- [ ] Refactoring needs
- [ ] Test coverage gaps
```

### 3. Install Full System
```bash
# Copy all hooks
cp -r ~/.claude/hooks .claude/hooks/

# Generate settings.json
Generate from template with all hooks registered

# Copy commands
cp -r ~/.claude/commands .claude/commands/

# Set up chains
cp ~/.claude/chains.json .claude/

# Configure for this project
- Update project-config.json
- Set Python-specific settings
- Enable all automations
```

### 4. Extract Standards
From existing code patterns:
```python
# Detect and document:
- Naming conventions used
- Import organization
- Error handling patterns
- Testing patterns
- API design patterns
```

### 5. Migration Plan
```markdown
# MIGRATION_PLAN.md
## Phase 1: Non-Breaking Integration
- Install hooks (monitoring only)
- Document existing patterns
- Set up task tracking

## Phase 2: Gradual Enhancement  
- Enable style enforcement
- Add missing tests
- Implement PRD workflow

## Phase 3: Full Adoption
- Enforce all standards
- Complete test coverage
- Multi-agent ready
```

## Workflow Integration

After analysis, set up chains for this project type:

### For FastAPI Projects
```json
{
  "api-endpoint": ["py-prd", "py-api", "test-runner"],
  "api-refactor": ["pydeps check", "log-decision", "refactor"]
}
```

### For CLI Projects
```json
{
  "cli-command": ["py-prd", "typer-command", "test-runner"],
  "cli-enhance": ["analyze-usage", "improve-help", "test"]
}
```

### For Data Projects
```json
{
  "pipeline": ["py-prd", "py-pipeline", "test-runner"],
  "etl-fix": ["check-data-flow", "fix-pipeline", "validate"]
}
```

## Output Structure
```
existing-project/
├── .claude/
│   ├── product/
│   │   ├── mission.md (generated)
│   │   ├── roadmap.md (generated)
│   │   ├── tech-stack.md (detected)
│   │   └── decisions.md (inferred)
│   ├── hooks/ (all 35 hooks)
│   ├── commands/ (all 70+ commands)
│   ├── settings.json (configured)
│   ├── chains.json (customized)
│   ├── project-config.json
│   └── MIGRATION_PLAN.md
├── .task-ledger.md (generated)
└── .claude-integration.md (summary)
```

## Post-Integration Commands

Once integrated:
```bash
/sr  # Loads all context
/tl  # View extracted tasks
/roadmap  # See project progress
/help existing  # Get specific guidance
```

## Smart Detection Features

1. **Framework Detection**
   - FastAPI: Look for `FastAPI()` app
   - Django: Look for `settings.py`
   - Flask: Look for `Flask(__name__)`
   - Prefect: Look for `@flow` decorators

2. **Pattern Recognition**
   - Async patterns → Event-driven setup
   - Class-based → OOP standards
   - Functional → FP standards

3. **Test Framework**
   - pytest → pytest commands
   - unittest → unittest adapters
   - No tests → TDD setup plan

4. **Documentation**
   - Existing docs → Preserve and enhance
   - No docs → Generate from code
   - Partial docs → Fill gaps

This ensures smooth integration into ANY existing Python project!