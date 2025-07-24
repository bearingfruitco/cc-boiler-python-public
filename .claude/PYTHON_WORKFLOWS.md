# Python Workflows Guide - v2.4.2

This guide covers all Python-specific workflows in the AI development system, from simple tasks to complex multi-agent orchestrations.

## 🚀 Quick Reference

### Essential Python Commands
```bash
/py-prd [name]        # Create Python PRD with orchestration analysis
/py-agent [name]      # Generate Pydantic AI agent
/py-api [path]        # Create FastAPI endpoint
/py-pipeline [name]   # Build Prefect data pipeline
/pyexists [name]      # Check before creating
/pydeps [command]     # Analyze dependencies
/cti [title]          # Capture AI response to issue
```

### Workflow Chains
```bash
/chain tdd            # Test-driven development
/chain pf             # Python feature workflow  
/chain pa             # Python API workflow
/chain pag            # Python agent workflow
/chain ppl            # Python pipeline workflow
/chain deps           # Dependency analysis
/chain pq             # Python quality checks
```

## 📋 Core Workflows

### 1. Standard Python Feature Development

**When to use**: Single-domain features with clear requirements

```bash
# Step 1: Start with context
/sr

# Step 2: Create Python PRD
/py-prd user-profile-management

# Step 3: Generate tasks from PRD
/gt

# Step 4: Capture to GitHub issue with tests
/cti "User Profile Management" --type=feature --tests

# Step 5: Start work (tests auto-generated!)
/fw start 125

# Step 6: Process tasks systematically
/pt user-profile

# Step 7: Run tests continuously
/test --watch    # In another terminal

# Step 8: Grade and complete
/grade
/fw complete
```

**Time**: 2-4 hours for typical feature

### 2. API Development Workflow

**When to use**: Building REST APIs with FastAPI

```bash
# Step 1: Design API specification
/py-prd user-api-v2

# Step 2: Generate API endpoint
/py-api /api/v2/users GET POST PUT DELETE --auth --pagination --cache

# Generated structure:
src/
├── api/
│   ├── routers/
│   │   └── v2/
│   │       └── users.py      # FastAPI router
│   ├── dependencies.py       # Auth, DB, etc.
│   └── middleware.py         # Custom middleware
├── models/
│   └── user.py              # Pydantic models
└── services/
    └── user_service.py      # Business logic

# Step 3: Customize the generated code
vim src/api/routers/v2/users.py

# Step 4: Test the API
/test api/

# Step 5: Run locally
uvicorn src.main:app --reload

# Step 6: Document
/generate-docs api
```

**Features included**:
- JWT authentication
- Request/response validation
- Pagination support
- Redis caching
- OpenAPI documentation
- Comprehensive tests

### 3. AI Agent Development Workflow

**When to use**: Building intelligent agents with Pydantic

```bash
# Step 1: Define agent purpose
/py-prd customer-support-agent

# Step 2: Create agent with tools
/py-agent CustomerSupport --role=support --tools=zendesk,slack,email

# Generated structure:
src/agents/
├── customer_support.py      # Agent implementation
├── models.py               # Request/response models
├── tools.py                # Tool integrations
└── prompts.py              # Prompt templates

# Step 3: Implement agent logic
vim src/agents/customer_support.py

# Example implementation:
class CustomerSupportAgent(BaseAgent):
    role: str = "customer_support_specialist"
    tools: List[str] = ["zendesk", "slack", "email"]
    
    async def process_request(self, request: SupportRequest) -> SupportResponse:
        # Analyze intent
        intent = await self.analyze_intent(request.message)
        
        # Route to appropriate handler
        if intent.type == "technical":
            return await self.handle_technical_issue(request)
        elif intent.type == "billing":
            return await self.handle_billing_inquiry(request)
        # ...

# Step 4: Test conversations
/test agents/customer_support --fixtures=conversations

# Step 5: Integration test with tools
/test agents/customer_support --integration
```

**Agent features**:
- Structured I/O with Pydantic
- Tool integration framework
- Memory persistence (Redis)
- Async operation support
- Conversation management
- Error handling

### 4. Data Pipeline Workflow

**When to use**: Building ETL pipelines with Prefect

```bash
# Step 1: Design pipeline flow
/py-prd daily-analytics-etl

# Step 2: Generate pipeline
/py-pipeline AnalyticsETL --source=bigquery --dest=postgres --schedule="0 2 * * *"

# Generated structure:
src/pipelines/
├── analytics_etl.py         # Main flow
├── tasks/
│   ├── extract.py          # Source extraction
│   ├── transform.py        # Data transformation
│   └── load.py            # Destination loading
└── utils/
    └── monitoring.py       # Metrics & alerts

# Step 3: Implement transformations
vim src/pipelines/tasks/transform.py

# Example transformation:
@task(retries=3, retry_delay_seconds=60)
async def transform_sales_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Transform raw sales data with validation."""
    # Validate input
    assert not raw_data.empty, "Empty dataset"
    
    # Transform
    transformed = raw_data.copy()
    transformed['revenue'] = transformed['quantity'] * transformed['price']
    transformed['date'] = pd.to_datetime(transformed['date'])
    
    # Quality checks
    assert transformed['revenue'].min() >= 0, "Negative revenue detected"
    
    return transformed

# Step 4: Test pipeline
/test pipelines/analytics --sample-data

# Step 5: Deploy
/cloud-deploy pipeline analytics-etl
```

**Pipeline features**:
- Automatic retries
- Error handling
- Data validation
- Performance monitoring
- Scheduled execution
- Alerting integration

### 5. Test-Driven Development (TDD) Workflow

**When to use**: Always! Enforced by default

```bash
# Option 1: Automatic TDD (recommended)
/chain tdd

# This automatically:
# 1. Creates PRD
# 2. Generates all tests
# 3. Shows failing tests
# 4. Guides implementation
# 5. Validates coverage

# Option 2: Manual TDD
# Step 1: Write tests first
/generate-tests user-authentication

# Step 2: See them fail
/test --expect-fail

# Step 3: Implement until green
/pt user-authentication
/test

# Step 4: Refactor with confidence
/refactor --safe
/test
```

**TDD Benefits**:
- Tests exist before code
- Clear implementation target
- Refactoring confidence
- Better design emergence
- 80%+ coverage guaranteed

## 🔧 Advanced Workflows

### 6. Multi-Agent Orchestration Workflow

**When to use**: Complex features touching 3+ domains

```bash
# Step 1: Create comprehensive PRD
/py-prd social-media-dashboard

# Step 2: Analyze complexity
/orch social-media-dashboard --analyze

# Output:
Orchestration Analysis:
  Domains: [api, frontend, data, ml, testing]
  Complexity Score: 24 (very high)
  Recommended Agents: 5
  Estimated Time Savings: 70%
  
Suggested Distribution:
  Agent 1 (API): Authentication, endpoints
  Agent 2 (Frontend): React components, state
  Agent 3 (Data): Pipeline, transformations
  Agent 4 (ML): Sentiment analysis, trends
  Agent 5 (Testing): Integration, E2E

# Step 3: Launch orchestration
/orch social-media-dashboard --execute

# Step 4: Monitor progress
/sas                    # Sub-agent status
/orchestration-view     # Visual progress

# Step 5: Integrate results
/orch integrate

# Step 6: Validate complete system
/test --integration
/test --e2e
```

**Time savings**: 50-70% on complex features

### 7. Research-Driven Development (PRP Workflow)

**When to use**: External APIs, complex algorithms, unfamiliar domains

```bash
# Step 1: Create PRP (Product Requirement Prompt)
/prp-create payment-gateway-integration

# Step 2: Execute research phase
/prp-execute

# Research includes:
# - API documentation analysis
# - Best practices research
# - Security considerations
# - Error handling patterns
# - Performance optimization

# Step 3: Monitor research
/prp-status

# Step 4: Review findings
cat PRPs/payment-gateway-integration/research.md

# Step 5: Implement with confidence
/prp-complete

# Generates:
# - Complete implementation
# - Comprehensive tests
# - Security measures
# - Error handling
# - Documentation
```

**Success rate**: 78% one-pass implementation

### 8. Dependency Management Workflow

**When to use**: Before refactoring, during maintenance

```bash
# Step 1: Check what depends on your module
/pydeps check UserModel

# Output:
UserModel is used by:
├── api/auth.py (5 references)
├── api/users.py (12 references)
├── services/user_service.py (8 references)
├── services/notification.py (2 references)
└── tests/test_user.py (15 references)

# Step 2: Check for breaking changes
/pydeps breaking UserModel

# Output:
⚠️ Breaking Changes Analysis:
- Removing 'email' field breaks 12 usages
- Changing 'id' type breaks 8 usages
- Safe to rename: 'created_at' (unused)

# Step 3: Find circular dependencies
/pydeps circular

# Output:
🔄 Circular Dependencies Found:
- services.user → services.auth → services.user
  Suggestion: Extract shared interface

# Step 4: Safe refactoring
/chain python-refactor
```

### 9. Microservice Development Workflow

**When to use**: Building standalone services

```bash
# Step 1: Design service
/py-prd notification-microservice

# Step 2: Generate service structure
/py-api microservice --name=notifications --port=8001

# Creates:
notifications/
├── Dockerfile
├── docker-compose.yml
├── src/
│   ├── main.py
│   ├── api/
│   ├── models/
│   ├── services/
│   └── config.py
├── tests/
└── requirements.txt

# Step 3: Add message queue integration
/py-pipeline NotificationQueue --type=consumer --queue=rabbitmq

# Step 4: Add health checks
/py-api /health GET --monitoring

# Step 5: Test locally
docker-compose up

# Step 6: Deploy
/cloud-deploy microservice notifications
```

### 10. Performance Optimization Workflow

**When to use**: Optimizing existing code

```bash
# Step 1: Baseline performance
/performance-monitor baseline

# Step 2: Identify bottlenecks
/performance-monitor analyze

# Output:
Performance Bottlenecks:
1. Database queries: 67% time (N+1 problem)
2. JSON serialization: 18% time
3. External API calls: 12% time

# Step 3: Optimize with AI guidance
/think-level deep
/optimize database-queries

# Step 4: Implement async patterns
/chain async-conversion

# Step 5: Compare results
/performance-monitor compare

# Results:
- Response time: 450ms → 120ms (73% improvement)
- Throughput: 100 req/s → 380 req/s
- Memory usage: 512MB → 380MB
```

## 🛡️ Safety Workflows

### 11. Security Audit Workflow

```bash
# Step 1: Run security scan
/security-check all

# Step 2: Fix critical issues
/process-tasks security-critical

# Step 3: Add security tests
/generate-tests security

# Step 4: Verify fixes
/security-check verify
```

### 12. Production Debugging Workflow

```bash
# Step 1: Analyze logs
/check-logs --service=api --error

# Step 2: Reproduce locally
/debug reproduce-issue --id=12345

# Step 3: Fix with deep analysis
/think-level ultra
/debug fix-issue

# Step 4: Test fix
/test --regression

# Step 5: Deploy hotfix
/cloud-deploy hotfix --emergency
```

## 📊 Productivity Workflows

### 13. Daily Standup Workflow

```bash
# Morning routine
/chain daily-startup

# Generates:
Yesterday: Completed auth system (5/5 tasks)
Today: Starting notification system
Blockers: Waiting for SMS provider API key
```

### 14. Code Review Workflow

```bash
# Prepare for review
/chain pre-pr

# Runs:
- Design validation
- Test coverage check
- Security scan
- Performance analysis
- Documentation check
```

### 15. Knowledge Capture Workflow

```bash
# After solving complex problem
/capture-pattern "async-queue-optimization"

# After successful implementation
/log-decision "chose-redis-over-rabbitmq"

# After learning something new
/capture-learning "prefect-retry-patterns"
```

## 🎯 Workflow Selection Guide

### By Time Available
- **< 30 min**: `/mt` micro tasks
- **30 min - 2 hr**: Standard workflow
- **2-4 hr**: TDD workflow
- **4-8 hr**: Multi-agent workflow
- **1-2 days**: PRP workflow

### By Complexity
- **Simple CRUD**: `/py-api` workflow
- **Business Logic**: Standard workflow
- **External APIs**: PRP workflow
- **Multiple Domains**: Orchestration
- **Research Heavy**: PRP workflow

### By Quality Requirements
- **Prototype**: Fast workflow, skip some tests
- **Production**: Full TDD workflow
- **Mission Critical**: PRP + Security audit
- **High Performance**: Include optimization workflow

## 💡 Pro Tips

### Speed Optimization
1. Use chains instead of individual commands
2. Let orchestration handle complex features
3. Trust automatic test generation
4. Enable auto-staging for commits

### Quality Assurance
1. Never skip `/pyexists` check
2. Always run `/pydeps` before refactoring
3. Use `/grade` before completing features
4. Enable TDD enforcement in config

### Context Management
1. Checkpoint before major changes
2. Compress context every 2-3 hours
3. Use profiles for different features
4. Save successful patterns

## 🚀 Putting It All Together

### Example: Building a Complete Feature

```bash
# Monday: Research and Planning
/prp-create user-notification-system

# Tuesday: Implementation
/prp-execute
/orch user-notifications --execute

# Wednesday: Integration and Testing
/orch integrate
/test --integration
/test --e2e

# Thursday: Optimization and Security
/performance-monitor optimize
/security-check all

# Friday: Documentation and Deployment
/generate-docs all
/cloud-deploy production
```

Remember: **The system adapts to your patterns**. The more you use these workflows, the more efficient they become!

---

*Workflow tip: Start with standard workflows, then experiment with advanced ones as you gain confidence. The system will guide you!*
