# Stage Validate Command

Validate completion of PRD phases with automated gates before proceeding to next stage.

## Arguments:
- $ACTION: check|require|override|status
- $STAGE: 1|2|3|current|all

## Purpose:
Ensures each development phase meets exit criteria before moving forward, preventing incomplete implementations and technical debt.

## Actions:

### CHECK - Validate current stage
```bash
/stage-validate check 1
/stage-validate check current
```

Runs automated checks:
```
=== VALIDATING STAGE 1: Foundation ===

✅ Database Schema
   - All models defined
   - Migrations created
   - Test data seeded

✅ API Structure  
   - Routes configured
   - Middleware setup
   - Error handling

⚠️ Authentication
   - Basic auth working
   - [ ] Session management incomplete
   - [ ] Password reset missing

❌ Testing Setup
   - [ ] Unit test framework missing
   - [ ] E2E not configured

STAGE 1 STATUS: 75% Complete
❌ Cannot proceed to Stage 2

Missing items:
1. Complete session management
2. Add password reset flow
3. Setup testing framework

Run: /stage-validate require 1
```

### REQUIRE - Enforce validation
```bash
/stage-validate require 2
```

This:
1. Blocks proceeding until criteria met
2. Updates task list with missing items
3. Sets focused context profile
4. Shows exact commands to run

### STATUS - Overview of all stages
```bash
/stage-validate status
```

Output:
```
=== PROJECT STAGE STATUS ===

Stage 1: Foundation ✅ COMPLETE
  Duration: 2 days
  Commits: 23
  Tests: 45 passing

Stage 2: Core Features ⚠️ IN PROGRESS (82%)
  Started: Today 9:00 AM
  Remaining: 3 tasks
  Estimate: 2 hours

Stage 3: Polish 🔒 LOCKED
  Unlocks: After Stage 2
  Estimated: 1 day

📊 Overall Progress: 54% Complete
```

### OVERRIDE - Skip validation (with reason)
```bash
/stage-validate override 1 --reason "Client demo, auth incomplete"
```

Records override in project log

## Exit Criteria Configuration:

Each PRD automatically generates stage validations:

```typescript
interface StageValidation {
  stage: number;
  name: string;
  criteria: {
    category: string;
    items: ValidationItem[];
  }[];
  automated: AutomatedCheck[];
  manual: ManualCheck[];
}

interface ValidationItem {
  description: string;
  validator: () => boolean;
  errorMessage: string;
  fixCommand?: string;
}
```

## Stage 1: Foundation Criteria
```yaml
Database:
  - Schema fully defined
  - Migrations run successfully
  - Indexes created
  - Test data available

API:
  - All routes return 200/404
  - Error handling middleware
  - Request validation
  - CORS configured

Auth:
  - User registration works
  - Login returns token
  - Protected routes secured
  - Session management

Environment:
  - All env vars documented
  - Dev/prod configs separate
  - Secrets not in code
```

## Stage 2: Core Features Criteria  
```yaml
Features:
  - All PRD features implemented
  - Happy path tested
  - Error states handled
  - Loading states added

UI:
  - All components render
  - Forms validate properly  
  - Responsive on mobile
  - Accessibility basics

Integration:
  - Frontend connects to API
  - Real data displayed
  - CRUD operations work
  - File uploads functional
```

## Stage 3: Polish Criteria
```yaml
Performance:
  - Lighthouse score > 90
  - Bundle size optimized
  - Images optimized
  - API responses < 200ms

Security:
  - Auth fully tested
  - OWASP checklist passed
  - Rate limiting active
  - Input sanitization

Production:
  - Error tracking setup
  - Analytics configured
  - Monitoring active
  - Deployment automated
```

## Automated Validators:

### Code Validators
```bash
# Run automatically during validation
npm run typecheck      # No TypeScript errors
npm run lint          # No linting errors  
npm run test          # All tests pass
npm run build         # Build succeeds
```

### Design System Validators
```bash
/vd --strict          # Full design validation
```

### Security Validators
```bash
/security-check --stage 1
```

### Custom Validators
Each stage can have custom validation scripts:
```
.claude/validators/
  ├── stage-1-foundation.js
  ├── stage-2-features.js
  └── stage-3-polish.js
```

## Integration with Workflow:

### 1. PRD Auto-generates Validators
When creating PRD, validators are created:
```markdown
## Stage 1 Exit Criteria
- [ ] All database models defined
- [ ] API endpoints return correct status
- [ ] Authentication flow complete
- [ ] Automated tests: /stage-validate check 1
```

### 2. Task Integration
Tasks automatically tagged with stage:
```
[Stage 1] Create user model
[Stage 1] Setup auth routes
[Stage 2] Build dashboard component
```

### 3. Git Branch Protection
```bash
# Attempts to merge stage-2 work before stage-1 complete
❌ Stage validation failed
   Stage 1 incomplete (85%)
   Run: /stage-validate status
```

### 4. Checkpoint Integration
Checkpoints include stage status:
```json
{
  "checkpoint": "auth-work-tuesday",
  "stage": {
    "current": 1,
    "progress": 85,
    "blockers": ["session-management", "test-setup"]
  }
}
```

## Smart Features:

### Auto-Fix Suggestions
```
❌ Validation Failed: No test framework

Suggested fix:
/test-runner init --framework vitest
```

### Rollback Protection
```
⚠️ Detected work from Stage 2
   But Stage 1 only 85% complete
   
Options:
1. Complete Stage 1 first
2. Move Stage 2 work to branch
3. Override (not recommended)
```

### Time Tracking
```
📊 Stage Metrics:
   Stage 1: 2.5 days (est: 2 days)
   Stage 2: In progress
   
   Velocity: 92% of estimate
```

## Benefits:
- Prevents incomplete features
- Enforces quality gates
- Clear progress visibility
- Reduces technical debt
- Improves handoffs
- Client-ready milestones
