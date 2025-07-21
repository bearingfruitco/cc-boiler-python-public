# Python Development Workflows

This document describes the Python-specific workflows available in your boilerplate.

## Quick Reference

| Shortcut | Workflow | Description |
|----------|----------|-------------|
| `/pf` | python-feature | Complete feature development |
| `/pr` | python-refactor | Safe refactoring workflow |
| `/pa` | python-api | Create API endpoint |
| `/pag` | python-agent | Create AI agent |
| `/ppl` | python-pipeline | Create data pipeline |
| `/prpw` | prp-workflow | Complete PRP workflow |
| `/dc` | dependency-check | Dependency analysis |
| `/pq` | python-quality | Code quality checks |
| `/iw` | issue-workflow | GitHub issue creation |
| `/ma` | multi-agent | Multi-agent orchestration |

## Common Workflows

### 1. New Feature Development
```bash
# Start with PRD
/py-prd "User Authentication System"

# Or use the chain
/chain pf
```

### 2. Refactoring Safely
```bash
# Check dependencies before refactoring
/chain pr

# Then update imports
/python-import-updater old.module new.module
```

### 3. Creating APIs
```bash
# FastAPI endpoint creation
/chain pa

# Or directly
/py-api /users POST
```

### 4. AI Agent Development
```bash
# Create Pydantic AI agent
/chain pag

# Or directly
/py-agent DataAnalyst --role=analyst
```

### 5. Quality Assurance
```bash
# Run all quality checks
/chain pq
```

## Hook Integration

These workflows integrate with the following hooks:

- **Creation Guard**: Prevents duplicates before creating
- **Dependency Tracker**: Tracks module dependencies
- **Import Updater**: Updates imports after refactoring
- **Response Capture**: Saves AI implementation plans
- **PRP Progress**: Tracks PRP workflow progress

## Best Practices

1. Always start with a PRD: `/py-prd`
2. Check existence before creating: `/pyexists`
3. Track dependencies: `/pydeps`
4. Use chains for complex workflows: `/chain pf`
5. Capture AI responses: `/cti`
