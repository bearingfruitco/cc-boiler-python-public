---
name: prp-review
aliases: [review-prp, prp-check]
description: Review PRP for completeness and quality
category: PRPs
---

# Review PRP: $ARGUMENTS

Analyze PRP for quality and completeness before execution.

## Review Checklist

### 1. Structure Completeness
- [ ] Metadata section present
- [ ] Goal clearly defined
- [ ] Success criteria measurable
- [ ] All needed context included
- [ ] Known gotchas documented
- [ ] Implementation blueprint detailed
- [ ] Validation loops defined
- [ ] Anti-patterns listed

### 2. Context Quality
```yaml
Documentation:
- [ ] Official docs linked with specific sections
- [ ] Codebase examples referenced
- [ ] AI docs cached and linked

Patterns:
- [ ] Existing patterns identified
- [ ] File paths correct
- [ ] Dependencies listed
```

### 3. Validation Executability
```bash
# Test each validation command
Level 1: ruff check && mypy
Level 2: pytest tests/test_feature.py
Level 3: docker-compose test
Level 4: security scans
```

### 4. Dependency Analysis
```bash
# Check if all dependencies are available
/pydeps check-prp $ARGUMENTS

# Potential breaking changes
/pydeps breaking --prp $ARGUMENTS
```

### 5. Conflict Detection
- [ ] No active PRPs conflict
- [ ] No uncommitted changes in target files
- [ ] No team members working on same files

### 6. Confidence Score Validation
```yaml
Documentation: [X]/2
Pattern Examples: [X]/2  
Gotchas Identified: [X]/2
Test Coverage: [X]/2
Automation Ready: [X]/2
---
Total: [X]/10
```

## Review Output
```
╔══════════════════════════════════════════════════════════╗
║ PRP REVIEW: $ARGUMENTS                                   ║
╠══════════════════════════════════════════════════════════╣
║ Quality Score: 8.5/10                                    ║
║ Ready for Execution: YES                                 ║
╠══════════════════════════════════════════════════════════╣
║ Strengths:                                               ║
║ ✅ Comprehensive context                                 ║
║ ✅ Clear validation gates                                ║
║ ✅ Good pattern examples                                 ║
╠══════════════════════════════════════════════════════════╣
║ Improvements Needed:                                     ║
║ ⚠️  Add load test commands                              ║
║ ⚠️  Include rollback plan                               ║
╠══════════════════════════════════════════════════════════╣
║ Recommendations:                                         ║
║ • Add performance benchmarks                             ║
║ • Cache pandas documentation                             ║
║ • Review similar completed PRPs                          ║
╚══════════════════════════════════════════════════════════╝
```

## Auto-Fix Options
1. Add missing sections
2. Fetch missing documentation
3. Generate validation commands
4. Update confidence score
