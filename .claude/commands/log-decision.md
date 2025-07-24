---
name: log-decision
aliases: [decision, arch-decision]
description: Log an architectural decision with context and impact
category: documentation
---

Log architectural decision: $ARGUMENTS

## Check for Breaking Changes
First, analyze if this decision involves breaking changes:

```bash
/pydeps breaking
```

## Decision Entry Format

Add to `.claude/decisions/decisions.md`:

```markdown
## $(date +%Y-%m-%d): $ARGUMENTS

**Decision**: [Refined statement of the decision]

**Context**: [Why is this decision being made now?]

**Alternatives Considered**:
1. [Alternative 1]: [Brief description]
2. [Alternative 2]: [Brief description]
3. [Current approach]: [What we're changing from]

**Rationale**: [Why this choice over alternatives?]

**Impact**:
- Modules affected: [from pydeps check]
- Breaking changes: [yes/no]
- Migration required: [yes/no]
- Test updates needed: [list test files]

**Implementation Notes**:
- [ ] Update imports in affected modules
- [ ] Update tests
- [ ] Update documentation
- [ ] Add migration script (if needed)

**Linked to**:
- Task: [from task ledger]
- Issue: [if created via /cti]
- PRD: [if part of larger feature]
```

## Integration Points

This decision should be referenced in:
1. Related PRDs (update if needed)
2. Task ledger (link decision to tasks)
3. Code comments (reference decision number)

## Follow-up Actions

After logging:
1. If breaking changes: Run `/python-import-updater`
2. If new pattern: Update `.claude/standards/python-patterns.md`
3. If affects tests: Run `/test-runner affected`

Remember: Decisions are immutable once logged. Add amendments rather than editing.