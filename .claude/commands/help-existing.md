---
name: help-existing
aliases: [existing-help, drop-in-help]
description: Help for integrating into existing projects
category: help
---

# 🚀 Existing Project Integration Guide

## Quick Start (30 seconds)
```bash
# In your existing Python project:
/chain eps  # OR /analyze-existing
```

This will:
1. Analyze your codebase structure
2. Detect frameworks and patterns
3. Install complete boilerplate system
4. Generate documentation from code
5. Extract tasks from TODOs

## What Gets Installed

### 1. Complete Hook System (35 hooks)
- **Safety**: PII protection, dangerous commands
- **Quality**: Style checks, import validation  
- **Process**: TDD enforcement, evidence language
- **Intelligence**: Pattern learning, auto-orchestration

### 2. All Commands (70+)
- `/py-prd`, `/py-agent`, `/py-api` - Development
- `/test-runner`, `/lint-check` - Quality
- `/task-ledger`, `/process-tasks` - Management
- `/orchestrate-agents` - Multi-agent

### 3. Workflow Automation
- Chains for your project type
- Aliases for quick access
- Permission profiles
- Context management

### 4. Documentation Generation
From your existing code:
- `.claude/product/mission.md` - Inferred purpose
- `.claude/product/roadmap.md` - Progress tracking
- `.claude/product/tech-stack.md` - Detected stack
- `.task-ledger.md` - Extracted TODOs

## Integration Approaches

### Minimal Integration (Observation Mode)
```bash
/analyze-existing --observe
```
- Installs hooks in monitor mode
- No enforcement, just tracking
- Learn patterns before enforcing

### Standard Integration (Recommended)
```bash
/chain eps
```
- Full system with gradual adoption
- Enforces new code only
- Preserves existing patterns

### Full Integration (Clean Slate)
```bash
/analyze-existing --enforce-all
```
- Applies all standards immediately
- Generates refactoring tasks
- Full TDD/PRD workflow

## Framework-Specific Features

### FastAPI Projects
- API endpoint tracking
- Pydantic model generation
- OpenAPI integration
- Async pattern validation

### Django Projects  
- Model/View/Template tracking
- Admin customization support
- Django test runner integration
- Migration tracking

### Data Science Projects
- Jupyter notebook support
- Pipeline tracking (Prefect)
- Experiment logging
- Dataset versioning

### CLI Projects
- Typer/Click integration
- Command tracking
- Help generation
- Distribution support

## Common Scenarios

### "I have partial tests"
```bash
/generate-tests --missing  # Fills gaps
/coverage  # Shows current state
/chain tdd  # Enables TDD workflow
```

### "My code has no documentation"
```bash
/analyze-existing  # Generates from code
/generate-docs  # Creates missing docs
/py-prd --from-existing  # PRDs from features
```

### "I want to add AI agents"
```bash
/py-agent --integrate  # Add to existing code
/test-runner  # Ensure nothing breaks
/grade  # Check integration quality
```

### "Team wants to adopt gradually"
```bash
/analyze-existing --team-mode
# Creates onboarding plan
# Separate profiles per developer
# Gradual standard adoption
```

## Migration Strategies

### Phase 1: Observation (Week 1)
- Install with monitoring only
- Collect metrics
- Learn codebase patterns
- No enforcement

### Phase 2: New Code (Week 2-3)
- Enforce on new files only
- Generate tests for new features
- Start using PRD workflow
- Track in task ledger

### Phase 3: Refactoring (Week 4+)
- Enable full enforcement
- Generate refactoring tasks
- Update existing code
- Complete test coverage

## Troubleshooting

### "Hooks conflict with my tools"
```bash
/config hooks.exclude_tools = ["tool_name"]
```

### "Too many style violations"
```bash
/config python_style.enforce = false  # Disable temporarily
/lint-check --fix  # Fix incrementally
```

### "Can't detect my framework"
```bash
/analyze-existing --framework=custom
# Then define patterns manually
```

## Verification

After integration:
```bash
/sr  # Should load all context
/tl  # Should show extracted tasks  
/roadmap  # Should visualize progress
/test-runner  # Should find all tests
```

## Best Practices

1. **Start with observation** - Let hooks learn first
2. **Review generated docs** - AI might miss context
3. **Customize standards** - Match your team's style
4. **Use chains** - Automate common workflows
5. **Enable gradually** - Don't overwhelm the team

## Getting More Help

- `/help` - General help
- `/workflow-guide` - Personalized workflows
- `/chain eps` - Run full integration
- Check `.claude-integration.md` - Summary of what was installed

Remember: The system adapts to YOUR project, not the other way around!