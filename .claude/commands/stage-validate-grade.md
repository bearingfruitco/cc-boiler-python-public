# Stage Validate Grade

Grade implementation against original PRD specifications using Grove's deliberative alignment concept.

## Arguments:
- $FEATURE: Feature name or current
- $OPTIONS: --verbose --export --against-prd

## Usage:

```bash
/sv grade --feature auth-system
/sv grade --current
/sv grade --feature checkout --export
```

## What It Does:

Analyzes implementation and scores alignment with PRD:
1. Functional requirements completion
2. Test coverage of acceptance criteria
3. Design system compliance
4. Performance target achievement
5. Security requirement adherence

## Grading Process:

### 1. Parse PRD Requirements
```typescript
interface PRDRequirements {
  functional: RequirementItem[];
  performance: PerformanceTarget[];
  security: SecurityRequirement[];
  design: DesignSpecification[];
  acceptance: AcceptanceCriterion[];
}
```

### 2. Analyze Implementation
- Check which requirements have code
- Map tests to acceptance criteria
- Verify performance metrics
- Audit security compliance

### 3. Calculate Scores
```typescript
interface GradeReport {
  overall: number; // 0-100
  breakdown: {
    functional: ScoreDetail;
    testing: ScoreDetail;
    design: ScoreDetail;
    performance: ScoreDetail;
    security: ScoreDetail;
  };
  missing: MissingItem[];
  improvements: Suggestion[];
}
```

## Example Output:

```
=== IMPLEMENTATION GRADE: B+ (87%) ===

📊 Overall Alignment with PRD: 87/100

✅ Functional Requirements: 95% (19/20 complete)
   ✓ User registration with email
   ✓ Password reset flow
   ✓ Session management
   ✗ Social login integration (missing)

✅ Test Coverage: 82% (41/50 criteria)
   Unit tests: 90% (27/30)
   Integration: 78% (11/14)
   E2E tests: 50% (3/6)
   
   Uncovered criteria:
   - "Session persists for 24 hours"
   - "Handles concurrent login attempts"
   - "Accessibility: keyboard navigation"

⚠️ Design Compliance: 85%
   Issues found:
   - LoginForm.tsx:45 - Using text-sm (use text-size-4)
   - RegisterForm.tsx:82 - Using p-5 (use p-4 or p-6)
   - 2 components missing mobile responsiveness

✅ Performance Targets: 91%
   ✓ API response: 180ms avg (target: <200ms)
   ✓ Bundle size: 245KB (target: <250KB)
   ⚠️ LCP: 2.8s (target: <2.5s)
   ✓ Memory usage: 42MB (target: <50MB)

✅ Security Requirements: 100%
   ✓ Passwords hashed with bcrypt
   ✓ Rate limiting implemented
   ✓ CSRF protection active
   ✓ Input sanitization complete

📋 MISSING IMPLEMENTATIONS:
1. Social login integration (PRD section 3.2)
2. Remember me functionality (PRD section 3.4)
3. Admin user management (PRD section 4.1)

🎯 IMPROVEMENT SUGGESTIONS:
1. Add E2E tests for critical paths
   Command: /prd generate-tests auth --type=e2e

2. Fix design violations
   Command: /vd --fix

3. Optimize LCP for better performance
   Focus: Lazy load heavy components

4. Complete missing features
   Next: /pt auth-system --resume

📈 GRADE HISTORY:
- Current: B+ (87%)
- 2 days ago: B (83%)
- 1 week ago: C+ (78%)

🏆 READY FOR STAGE COMPLETION: NO
Required grade: 90%
Gap: 3%

Focus on: E2E test coverage + missing features
```

## Detailed Scoring:

### Functional Requirements (40% weight)
- Each requirement: equal weight
- Partial credit for incomplete
- Extra credit for enhancements

### Test Coverage (25% weight)
- Acceptance criteria coverage
- Edge case handling
- Error scenario testing

### Design Compliance (15% weight)
- Typography rules
- Spacing grid
- Component patterns
- Responsive design

### Performance (10% weight)
- Response times
- Bundle size
- Memory usage
- Core Web Vitals

### Security (10% weight)
- Authentication security
- Data protection
- Input validation
- Audit logging

## Integration Features:

### 1. Continuous Grading
```bash
# Auto-grade during workflow
/fw complete 24 --grade-first
```

### 2. Grade Tracking
```json
// .claude/grades/auth-system.json
{
  "feature": "auth-system",
  "grades": [
    {
      "date": "2024-01-15",
      "score": 87,
      "commit": "abc123",
      "details": {...}
    }
  ]
}
```

### 3. Export Report
```bash
/sv grade --export
```
Generates: `reports/grade-auth-system-2024-01-15.md`

### 4. PR Integration
Grade report automatically added to PR description

## Configuration:

```json
// .claude/config.json
{
  "grove_enhancements": {
    "implementation_grading": {
      "enabled": true,
      "min_grade": 85,
      "block_pr": false,
      "weights": {
        "functional": 0.4,
        "testing": 0.25,
        "design": 0.15,
        "performance": 0.1,
        "security": 0.1
      },
      "grade_on": ["complete", "checkpoint"],
      "export_reports": true
    }
  }
}
```

## Grade Thresholds:

- **A+ (98-100%)**: Exceeds all requirements
- **A (93-97%)**: Meets all requirements  
- **B+ (87-92%)**: Minor gaps
- **B (83-86%)**: Some missing pieces
- **C+ (78-82%)**: Significant gaps
- **C (73-77%)**: Major work needed
- **F (<73%)**: Does not meet PRD

## CLI Integration:

```bash
# Quick grade check
/sv g

# Grade with specific PRD
/sv grade --against-prd docs/features/auth-PRD.md

# Compare implementations
/sv grade --compare main
```

## Benefits:
- Objective quality metrics
- Clear completion criteria
- Identifies gaps early
- Tracks improvement
- Enables data-driven decisions
