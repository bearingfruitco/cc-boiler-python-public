---
name: prp-metrics
aliases: [prp-stats, prp-dashboard]
description: Show PRP success metrics and insights
category: PRPs
---

# PRP Metrics Dashboard

Display comprehensive metrics about PRP usage and effectiveness.

## Metrics Collection

### 1. Success Metrics
```python
metrics = {
    "total_prps": count_files("PRPs/completed/"),
    "success_rate": successful_prps / total_prps,
    "one_pass_rate": one_pass_success / total_prps,
    "avg_confidence_predicted": 7.8,
    "avg_confidence_actual": 8.2,
    "avg_duration_hours": 2.3,
    "avg_cost_usd": 4.50
}
```

### 2. Validation Analysis
```yaml
Validation Failure Points:
  Level 1 (Syntax): 5%
  Level 2 (Unit): 15%
  Level 3 (Integration): 25%
  Level 4 (Security): 10%
  
Most Common Failures:
  - Missing type hints
  - Insufficient test coverage
  - API contract violations
```

### 3. Pattern Reuse
```yaml
Most Reused Patterns:
  1. FastAPI CRUD Router: 12 times
  2. Pydantic Validation: 10 times
  3. Async Service Layer: 8 times
  4. Redis Caching: 7 times
  5. JWT Authentication: 6 times
```

### 4. Time Savings
```yaml
Traditional Development:
  Average: 8.5 hours per feature
  
With PRP:
  Research: 0.5 hours
  PRP Creation: 1.0 hours
  Execution: 2.3 hours
  Total: 3.8 hours
  
Savings: 55% reduction
```

### 5. Cost Analysis
```yaml
Cost per Feature:
  Research Agents: $0.50
  PRP Creation: $1.20
  Execution: $2.80
  Total Average: $4.50
  
ROI: 5.2x (based on developer time saved)
```

## Dashboard Output
```
╔══════════════════════════════════════════════════════════╗
║                    PRP METRICS DASHBOARD                 ║
╠══════════════════════════════════════════════════════════╣
║ OVERVIEW                                                 ║
║ Total PRPs: 42          Success Rate: 92%               ║
║ One-Pass Success: 78%   Avg Duration: 2.3h              ║
║ Avg Cost: $4.50        Time Saved: 55%                 ║
╠══════════════════════════════════════════════════════════╣
║ VALIDATION SUCCESS RATES                                 ║
║ ████████████████████░ Level 1: 95%                     ║
║ ████████████████░░░░░ Level 2: 85%                     ║
║ ████████████░░░░░░░░░ Level 3: 75%                     ║
║ ██████████████████░░░ Level 4: 90%                     ║
╠══════════════════════════════════════════════════════════╣
║ TOP PATTERNS                      │ USAGE               ║
║ FastAPI CRUD Router               │ ████████████ 12     ║
║ Pydantic Validation               │ ██████████░░ 10     ║
║ Async Service Layer               │ ████████░░░░ 8      ║
║ Redis Caching                     │ ███████░░░░░ 7      ║
║ JWT Authentication                │ ██████░░░░░░ 6      ║
╠══════════════════════════════════════════════════════════╣
║ RECENT PRPS                       │ STATUS │ TIME       ║
║ user-authentication               │ ✅     │ 2.1h       ║
║ payment-integration               │ ✅     │ 3.2h       ║
║ data-pipeline-etl                 │ 🔄     │ 1.5h       ║
║ notification-service              │ ✅     │ 2.8h       ║
╚══════════════════════════════════════════════════════════╝
```

## Export Options
1. Save to JSON: `.claude/metrics/prp_metrics.json`
2. Generate report: `docs/prp_metrics_report.md`
3. Send to monitoring: Prometheus/Grafana

## Insights & Recommendations
Based on current metrics:
- Consider creating more agent-specific PRPs
- Update templates with common validation fixes
- Cache more library documentation
- Increase test coverage requirements
