# Getting Started with Grove Enhancements

Quick guide to start using the new specification-driven features inspired by Sean Grove's talk.

## 🚀 Quick Start

### 1. Enable PRD Clarity Linting (Already On!)
The PRD linter is enabled by default. Next time you create or edit a PRD:

```bash
/prd user-authentication
```

You'll see:
```
🔍 PRD CLARITY CHECK
⚠️ Line 23: "fast" - Specify concrete performance metrics
   Suggestions:
   → Response time < 200ms
   → Page load < 3 seconds
```

### 2. Try the Pattern Library

After completing a feature:
```bash
# Extract pattern from successful implementation
/specs extract --from-feature auth-system

# See available patterns
/specs list

# Apply to new feature
/specs apply auth-jwt --to payment-system
```

### 3. Generate Tests from PRD

```bash
# After writing PRD with acceptance criteria
/prd-tests auth-system

# This creates:
# - tests/features/auth-system/auth.test.py
# - tests/features/auth-system/auth.e2e.py
```

### 4. Check Implementation Alignment

```bash
# Grade current implementation
/grade

# Or specific feature
/sv grade --feature auth-system
```

## 📝 Best Practices

### Writing Better PRDs
With the clarity linter, focus on:
- **Specific metrics** instead of adjectives
- **Measurable criteria** instead of opinions
- **Concrete examples** instead of abstractions

Bad:
```markdown
The system should be fast and user-friendly
```

Good:
```markdown
The system must respond within 200ms for 95% of requests
Users complete registration in under 3 clicks
```

### Building Your Pattern Library
1. Complete features normally
2. When tests pass and it works well:
   ```bash
   /specs extract --from-feature [name]
   ```
3. Patterns auto-tagged and indexed
4. Reuse on similar features

### Test-Driven from PRD
1. Write clear acceptance criteria
2. Generate tests: `/prd-tests [feature]`
3. Tests fail initially (red)
4. Implement until tests pass (green)
5. Grade alignment: `/grade`

## 🎯 Workflow Integration

### Enhanced Daily Flow
```bash
# Morning
/sr                        # Resume context
/grade                     # Check yesterday's alignment

# Starting feature
/prd auth --lint           # Create PRD with linting
/prd-tests auth            # Generate test suite
/specs search auth         # Find similar patterns
/specs apply auth-pattern  # Apply if found

# During development
/pt auth                   # Work through tasks
[tests auto-run]           # See progress

# Completing feature
/grade                     # Check alignment
/specs extract --from-feature auth  # Save pattern
/fw complete               # Create PR
```

## ⚙️ Configuration

### Adjust Linting Strictness
```json
// .claude/config.pyon
{
  "grove_enhancements": {
    "prd_linter": {
      "blocking": true,  // Make it blocking
      "custom_terms": ["blazing-fast", "next-gen"]
    }
  }
}
```

### Set Grading Thresholds
```json
{
  "implementation_grading": {
    "min_grade": 0.90,  // Require 90% alignment
    "block_pr": true    // Block PR if below
  }
}
```

## 🔍 Troubleshooting

### Linter Too Strict?
- Set `blocking: false` in config
- Focus on requirements sections only
- Add terms to `custom_terms` if needed

### Pattern Not Extracting?
- Ensure feature has tests
- Complete at least one full feature first
- Check `.claude/specs/patterns/` directory

### Tests Not Generating?
- PRD needs clear acceptance criteria
- Use bullet points for each criterion
- Include success conditions

### Grade Too Low?
- Check uncovered acceptance criteria
- Run `/prd-tests` to ensure test coverage
- Use `/vd` to fix design issues

## 📚 Learn More

- [Full Documentation](GROVE_ENHANCEMENTS.md)
- [Grove's Talk](https://www.youtube.com/watch?v=8rABwKRsec4)
- [Example PRD with Clear Criteria](../examples/CLEAR_PRD_EXAMPLE.md)

## 💡 Philosophy Reminder

> "The person who communicates most effectively is the most valuable programmer." - Sean Grove

These tools help you communicate intent clearly through specifications, making your PRDs the true "source code" of your application.
