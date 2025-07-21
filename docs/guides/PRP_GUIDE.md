# Complete PRP (Product Requirement Prompt) Guide

## What is a PRP?

A PRP is an enhanced PRD (Product Requirements Document) optimized for AI agents to achieve one-pass implementation success. It combines:
- Traditional requirements documentation
- Comprehensive context and references
- Implementation patterns and gotchas
- Executable validation loops
- Automation capabilities

## PRP vs PRD

| Aspect | PRD (Traditional) | PRP (Enhanced) |
|--------|-------------------|----------------|
| Purpose | Human understanding | AI implementation |
| Context | Business focused | Code focused |
| References | General | Specific files/URLs |
| Validation | Manual QA | Automated loops |
| Execution | Manual coding | Optional automation |

## When to Use Each

### Use `/py-prd` (Traditional) When:
- Quick feature planning
- Exploring requirements
- Team discussion needed
- Simple implementations

### Use `/prp-create` (Enhanced) When:
- Complex features
- Need automation
- Want one-pass success
- Repeating patterns
- CI/CD integration

## Workflow Integration

```mermaid
graph TD
    A[Feature Request] --> B{Complexity?}
    B -->|Simple| C[/py-prd]
    B -->|Complex| D[/prp-create]
    
    C --> E[/gt - Generate Tasks]
    E --> F[/pt - Process Tasks]
    
    D --> G[Deep Research]
    G --> H[PRP Document]
    H --> I{Execution Mode?}
    
    I -->|Manual| F
    I -->|Automated| J[prp_runner.py]
    
    F --> K[Validation]
    J --> K
    K --> L[Complete]
```

## Creating a PRP

### 1. Research Phase
```bash
# Start research-heavy PRP creation
/prp-create payment-integration

# This will:
- Spawn research agents
- Analyze codebase patterns
- Cache documentation
- Identify gotchas
```

### 2. Template Selection
- `prp_base_python.md` - General features
- `prp_api.md` - REST API endpoints
- `prp_agent.md` - AI agents
- `prp_pipeline.md` - Data pipelines

### 3. Key Sections to Complete

#### All Needed Context
```yaml
- url: https://stripe.com/docs/api
  why: Payment processing API reference
  sections: ["charges", "customers", "webhooks"]
  
- file: src/api/billing.py
  why: Existing billing patterns to follow
  
- docfile: PRPs/ai_docs/stripe_webhooks.md
  why: Webhook handling patterns and security
```

#### Known Gotchas
```python
# CRITICAL: Stripe requires TLS 1.2+
# GOTCHA: Webhook signatures expire after 5 minutes
# PATTERN: Always use idempotency keys
```

#### Validation Loops
```bash
# Level 1: Syntax
ruff check && mypy

# Level 2: Unit tests
pytest tests/test_payment.py

# Level 3: Integration
python scripts/test_stripe_integration.py

# Level 4: Security
bandit -r src/payments/
```

### 4. Confidence Scoring

Rate 1-10 based on:
- Documentation completeness (2 points)
- Pattern examples (2 points)
- Gotchas identified (2 points)
- Test coverage (2 points)
- Automation readiness (2 points)

## Executing a PRP

### Manual Execution
```bash
# Traditional workflow still works
/py-prd payment-integration
/gt payment-integration
/pt payment-integration
```

### Automated Execution
```bash
# Interactive mode (recommended for development)
python scripts/prp_runner.py --prp payment-integration --interactive

# Automated mode (for CI/CD)
python scripts/prp_runner.py --prp payment-integration --output-format json

# Streaming mode (for monitoring)
python scripts/prp_runner.py --prp payment-integration --output-format stream-json
```

### CI/CD Integration
```yaml
# .github/workflows/prp-automation.yml
name: Execute PRP
on:
  workflow_dispatch:
    inputs:
      prp_name:
        description: 'PRP to execute'
        required: true

jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
          
      - name: Execute PRP
        run: |
          python scripts/prp_runner.py \
            --prp ${{ github.event.inputs.prp_name }} \
            --output-format json \
            > results.json
            
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: prp-results
          path: results.json
```

## Best Practices

### 1. Research Thoroughly
- Use multiple research agents
- Cache important docs
- Identify ALL gotchas

### 2. Provide Rich Context
- Specific file references
- Exact URL sections
- Real code examples

### 3. Define Clear Validation
- All 4 levels
- Executable commands
- Expected outcomes

### 4. Track Execution
- Save execution logs
- Monitor costs
- Review success rates

## Troubleshooting

### PRP Not Found
```bash
# Check active PRPs
ls PRPs/active/

# Check templates
ls PRPs/templates/
```

### Validation Failures
```bash
# Run validation separately
python scripts/prp_validator.py feature-name

# Check specific level
ruff check src/
pytest tests/test_feature.py -v
```

### Automation Issues
```bash
# Test Claude Code CLI
claude --version

# Check allowed tools
claude --help

# Verify PRP format
python scripts/prp_runner.py --prp test --dry-run
```

## Examples

See `docs/templates/prp_examples/` for complete examples:
- `payment_integration_prp.md`
- `ai_agent_prp.md`
- `data_pipeline_prp.md`

## Integration with Existing Features

### With Orchestration
```bash
# Parse PRP for orchestration
/orch payment-integration --from-prp

# Auto-assigns tasks to agents based on PRP structure
```

### With Issue Tracking
```bash
# Create issue from PRP
/cti "Payment Integration" --from-prp payment-integration

# Links GitHub issue to PRP execution
```

### With Dependency Analysis
```bash
# Analyze PRP dependencies before execution
/pydeps analyze-prp payment-integration

# Shows potential breaking changes
```

## Metrics & Success Tracking

### View PRP Metrics
```bash
# Dashboard
/prp-metrics

# Specific PRP
/prp-status payment-integration
```

### Success Indicators
- One-pass completion: 78%
- Average time: 2.3 hours
- Validation success: 92%
- Cost per feature: $4.50

## Tips for Success

1. **Start Simple**: Use PRPs for complex features first
2. **Iterate**: Improve templates based on failures
3. **Cache Docs**: Build ai_docs library over time
4. **Track Patterns**: Reuse successful patterns
5. **Measure**: Use metrics to improve

## Migration Path

### Week 1: Learn
- Read this guide
- Review example PRPs
- Try `/prp-create` once

### Week 2: Practice
- Create 2-3 PRPs
- Run manual execution
- Review results

### Week 3: Automate
- Try automated execution
- Set up CI/CD
- Track metrics

### Week 4: Optimize
- Update templates
- Share learnings
- Improve process

## Future Enhancements

Coming soon:
- Visual PRP builder
- Auto-pattern extraction
- Cost optimization
- Team collaboration features
