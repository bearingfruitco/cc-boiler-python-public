---
name: prp-complete
aliases: [finish-prp, prp-done]
description: Move completed PRP to archive
category: PRPs
---

# Complete PRP: $ARGUMENTS

## Completion Checklist

### 1. Verify All Tasks Complete
- [ ] All implementation tasks done
- [ ] All validation levels passed
- [ ] Documentation updated
- [ ] Tests passing

### 2. Capture Metrics
```json
{
  "prp": "$ARGUMENTS",
  "success": true,
  "one_pass": true,
  "duration_hours": 2.5,
  "validation_failures": 0,
  "cost_usd": 3.45,
  "confidence_actual": 9,
  "confidence_predicted": 8
}
```

### 3. Archive PRP
```bash
# Move to completed
mv PRPs/active/$ARGUMENTS.md PRPs/completed/$ARGUMENTS_$(date +%Y%m%d).md

# Add completion metadata
echo "Completed: $(date)" >> PRPs/completed/$ARGUMENTS_*.md
```

### 4. Update Related Systems
- Close GitHub issues
- Update project documentation
- Share learnings

### 5. Extract Patterns
- What worked well?
- What gotchas were found?
- What patterns to reuse?

### 6. Update Templates
If this PRP revealed new patterns or gotchas, update the templates:
- PRPs/templates/prp_base_python.md
- PRPs/ai_docs/

## Post-Completion Actions
1. Review execution logs
2. Update confidence scoring
3. Share with team
4. Consider creating similar PRPs
