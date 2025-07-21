---
name: prp-create
aliases: [prp-new, create-prp, prp-research]
description: Create a comprehensive PRP with deep research
category: PRPs
---

# Create Comprehensive PRP: $ARGUMENTS

Generate a research-heavy PRP that enables one-pass implementation success.

## Research Phase (Using Sub-Agents)

### 1. Codebase Analysis
/spawn backend "Search for similar patterns to $ARGUMENTS"
/spawn architect "Identify integration points for $ARGUMENTS"
/spawn security "Review security implications of $ARGUMENTS"

### 2. External Research
/spawn research "Find best practices for $ARGUMENTS implementation"
/spawn research "Search documentation for $ARGUMENTS libraries"
/dc cache "Key documentation for $ARGUMENTS"

### 3. Pattern Analysis
- Identify existing patterns to follow
- Note conventions and standards
- Find test patterns to replicate

## PRP Generation

Using template from PRPs/templates/prp_base_python.md:

### Enhanced Sections to Include:

#### All Needed Context
```yaml
- url: [Official documentation]
  why: [Specific sections/methods needed]
- file: [src/similar_feature.py]
  why: [Pattern to follow]
- docfile: [PRPs/ai_docs/cached_doc.md]
  why: [Critical implementation details]
```

#### Known Gotchas
```python
# CRITICAL: Library X requires specific setup
# GOTCHA: This ORM limits batch size to 1000
# WARNING: Async context managers needed here
```

#### Validation Loops (4 Levels)
1. Syntax: `ruff check && mypy`
2. Unit: `pytest tests/test_feature.py`
3. Integration: API/service tests
4. Creative: Load tests, security scans

#### Anti-Patterns
- ❌ Don't create new patterns when existing work
- ❌ Don't skip validation loops
- ❌ Don't ignore type hints

## Output
Save as: PRPs/active/$ARGUMENTS.md

## Confidence Score
Rate 1-10 for one-pass success probability.

## Integration with Existing Workflow
This enhances but doesn't replace:
- Still use `/py-prd` for quick PRDs
- Still use `/gt` and `/pt` for task management
- Add `/prp-execute` for automation when needed
