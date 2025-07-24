---
name: review-perspectives
aliases: [rp, multi-review]
description: Configure multi-perspective review for current context
category: review
---

# Multi-Perspective Review Configuration

Define review perspectives for parallel analysis using specialized agents.

## Usage

```bash
# Use default perspectives
/review-perspectives default

# Custom perspectives for specific needs
/review-perspectives security performance business

# With specific concerns
/rp --focus "OWASP top 10" "database queries" "requirement compliance"

# Review current PR from multiple angles
/rp --pr

# Review specific files
/rp --files "src/api/*" --perspectives security performance
```

## Default Perspectives

### 1. Security Review Agent
**Focus Areas:**
- Authentication/authorization flaws
- Data exposure risks  
- XSS/CSRF vulnerabilities
- SQL injection risks
- Dependency vulnerabilities
- PII handling
- Encryption usage

**Trigger Prompt:**
```
Review this code from a security perspective. Think like a paranoid security engineer.
Focus on OWASP vulnerabilities, auth bypasses, data exposure, and injection risks.
Be specific about attack vectors and provide remediation suggestions.
```

### 2. Performance Review Agent
**Focus Areas:**
- N+1 query patterns
- Memory leaks
- Unnecessary re-renders
- Bundle size impact
- Database query optimization
- Caching opportunities
- Async/await usage

**Trigger Prompt:**
```
Review this code for performance implications. Think like a performance engineer.
Look for N+1 queries, memory leaks, unnecessary computations, and optimization opportunities.
Quantify performance impacts where possible.
```

### 3. Code Quality Review Agent
**Focus Areas:**
- Design pattern consistency
- Test coverage gaps
- Documentation completeness
- Technical debt
- Code duplication
- Complexity metrics
- Python best practices

**Trigger Prompt:**
```
Review this code for quality and maintainability. Think like a senior engineer.
Check pattern consistency, test coverage, documentation, and technical debt.
Suggest refactoring opportunities.
```

### 4. Business Logic Review Agent
**Focus Areas:**
- Requirement compliance
- Edge case handling
- Data integrity
- Business rule validation
- Error handling
- User experience impact
- Feature completeness

**Trigger Prompt:**
```
Review this code from a business perspective. Think like a product owner.
Verify requirement compliance, edge case handling, and business rule implementation.
Flag any gaps between intent and implementation.
```

### 5. UX/Accessibility Review Agent
**Focus Areas:**
- Error state handling
- Loading states
- Mobile responsiveness
- Accessibility compliance
- User feedback
- Progress indicators
- Help text

**Trigger Prompt:**
```
Review this code for UX and accessibility. Think like a UX engineer.
Check error handling, loading states, accessibility, and user feedback mechanisms.
Ensure WCAG compliance where applicable.
```

## Integration with PR Workflow

```bash
# Standard single-perspective review
/pr-feedback

# Multi-perspective review
/chain multi-perspective-review

# Or combined with PR context
/chain pr-multi-review
```

## Custom Perspective Definition

Create custom review perspectives:

```bash
# Define a database-focused review
/rp --define "database-expert" \
    --focus "Query optimization, indexing, migrations" \
    --prompt "Review like a DBA focusing on database performance"

# Define a compliance review
/rp --define "compliance-officer" \
    --focus "GDPR, HIPAA, data retention" \
    --prompt "Review for regulatory compliance"
```

## Output Format

Reviews are synthesized into a comprehensive report:

```markdown
# Multi-Perspective Review Summary

## 🔒 Security Review
- **Critical**: SQL injection risk in user input
- **High**: Missing auth check on admin endpoint
- **Medium**: Weak password requirements

## ⚡ Performance Review  
- **Critical**: N+1 query in user listing
- **High**: Missing database index
- **Low**: Unnecessary re-renders

## 📊 Code Quality Review
- **High**: Missing test coverage (45%)
- **Medium**: Complex function needs refactoring
- **Low**: Inconsistent naming convention

## 💼 Business Logic Review
- **Critical**: Edge case not handled
- **Medium**: Business rule incomplete

## 🎨 UX/Accessibility Review
- **High**: Missing error states
- **Medium**: No loading indicators
```

## Automated Fixes

When possible, agents suggest or implement fixes:

```bash
# Review and auto-fix where safe
/rp --auto-fix safe

# Generate fix PRs for each perspective
/rp --generate-fixes
```

## Integration with Existing Hooks

Multi-perspective reviews integrate with:
- Task Ledger tracking
- PR feedback system
- Test generation
- Design validation
- Metrics collection

## Best Practices

1. **Run early**: Before PR creation
2. **Focus reviews**: Use relevant perspectives
3. **Iterate**: Address feedback systematically
4. **Document**: Capture decisions from reviews
5. **Learn**: Update perspectives based on findings
