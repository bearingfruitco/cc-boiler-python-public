# 🚀 Complete Python Boilerplate Workflow Guide

This guide covers ALL features of the system - not just TDD, but the complete automation and workflow ecosystem.

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     COMPLETE WORKFLOW SYSTEM                     │
├─────────────────────┬─────────────────────┬────────────────────┤
│     Planning        │   Development       │    Automation      │
├─────────────────────┼─────────────────────┼────────────────────┤
│ • PRD (Requirements)│ • TDD (Auto Tests)  │ • 35+ Hooks        │
│ • PRP (Research)    │ • Tasks (Tracking)  │ • Context Preserve │
│ • Issues (GitHub)   │ • Agents (AI)       │ • Pattern Learning │
│ • Gists (Snippets)  │ • APIs (FastAPI)    │ • Auto Orchestrate │
│ • Specs (Patterns)  │ • Pipelines (Data)  │ • Response Capture │
└─────────────────────┴─────────────────────┴────────────────────┘
```

## 📋 Complete Feature Development Workflow

### Phase 1: Planning & Research

#### PRD-Driven Development
```bash
# Create comprehensive PRD with domain analysis
/py-prd "E-commerce Platform"

# PRD includes:
# - Business requirements
# - Technical architecture
# - Domain analysis (backend, data, security, etc.)
# - Orchestration recommendations
# - Test specifications
```

#### PRP for Complex Features
```bash
# When you need deep research and validation
/prp-create "Payment Gateway Integration"

# PRP provides:
# - Sub-agent research
# - Documentation caching
# - 4-level validation gates
# - Success metrics
# - Automated execution option
```

#### Specification Patterns
```bash
# Capture successful patterns for reuse
/specs capture "Authentication Flow"
/specs list auth
/specs apply "Authentication Flow" --to="new-feature"
```

### Phase 2: Issue & Task Management

#### Smart Issue Creation
```bash
# Capture AI analysis to GitHub issue
/cti "Payment System" --tests --create-prp

# This creates:
# - GitHub issue with structured format
# - Auto-generated test suite
# - Linked PRP for complex features
# - Python component extraction
# - Dependency tracking
```

#### Task Generation & Tracking
```bash
# Generate tasks from PRD
/gt payment-system

# Analyze orchestration potential
# System: "15 tasks across 3 domains, recommend /orch"

# Track progress
/ts                    # Task status
/tb                    # Task board (visual)
/verify-task 1.2       # Verify specific task
```

#### GitHub Gist Integration
```bash
# Save code snippets as gists
/gist-save "auth_middleware.py" --desc="Reusable auth middleware"

# Retrieve and apply gists
/gist-list auth
/gist-apply auth_middleware --to=src/middleware/
```

### Phase 3: Development with Automation

#### TDD Automation (Enhanced)
```bash
# Start feature (tests auto-generate from issue)
/fw start 123

# Process tasks with TDD enforcement
/pt payment-system

# Hooks ensure:
# - Tests exist before code
# - Tests run after changes
# - Coverage requirements met
# - Type safety enforced
```

#### Multi-Agent Orchestration
```bash
# For complex features with parallel work
/orch payment-system --strategy=feature_development

# Orchestration includes:
# - Automatic task distribution
# - Parallel agent execution
# - Progress monitoring
# - Smart handoffs
# - 50-70% time savings
```

#### Component Creation with Guards
```bash
# Creation guard prevents duplicates
/pyexists PaymentService       # Check first
/pysimilar PaymentService      # Find similar

# Create with automatic validation
/py-agent PaymentProcessor --tools=stripe,square
/py-api /payments POST --auth=required
/py-pipeline payment-reconciliation --schedule=daily
```

### Phase 4: Context & State Management

#### Context Preservation
```bash
# Save work contexts
/checkpoint save "Payment feature v1 complete"
/context-profile save "payment-work"

# Switch contexts without losing work
/context-profile load "user-auth-work"

# Compress for optimization
/compress-context      # Reduce token usage
```

#### Knowledge Management
```bash
# Document caching for offline access
/doc-cache cache "Stripe API Reference"
/doc-cache search "webhook"

# Research capture
/research "Payment providers comparison"
# Auto-saved for future reference
```

### Phase 5: Quality & Validation

#### Automated Quality Gates
```bash
# Stage validation
/stage-validate check 1    # Check foundation stage
/stage-validate require 2  # Enforce stage completion

# Grade implementation
/grade payment-system      # 0-100% PRD alignment score
```

#### Dependency Management
```bash
# Track all dependencies
/pydeps scan               # Full dependency graph
/pydeps check PaymentModule # What depends on this?
/pydeps circular           # Find circular imports
/pydeps breaking           # Detect breaking changes
```

#### Security & Performance
```bash
# Security scanning
/security-check all
/audit-form-security

# Performance monitoring
/performance-monitor start
/performance-monitor report
```

## 🔄 Advanced Workflows

### Bug Investigation with Root Cause
```bash
# Comprehensive bug tracking
/bt add "Payment fails for amounts > 1000" --severity=high

# Create failing test
/generate-tests payment-bug --regression

# Investigate with orchestration
/orch investigate-bug --bug=payment_1234

# Track fix
/bt resolve payment_1234 "Fixed decimal precision issue"
```

### Feature Migration
```bash
# Migrate existing code with improvements
/analyze-project old-payment-system

# Generate migration plan
/migration-plan old-payment-system --to=new-architecture

# Execute with validation
/migrate --source=old-payment-system --validate-each-step
```

### Documentation Generation
```bash
# Auto-generate comprehensive docs
/generate-docs --format=markdown
/generate-docs api --openapi
/generate-docs architecture --diagrams
```

## 🤖 Hook System Powers

The 35+ hooks provide automatic:

### Pre-Tool Hooks
- **Creation Guard** - Prevents duplicates
- **Import Validation** - Catches broken imports
- **PII Protection** - No sensitive data in logs
- **Style Enforcement** - Python PEP 8
- **Truth Enforcement** - Protects established facts
- **PRD Clarity** - Ensures clear requirements

### Post-Tool Hooks
- **Action Logging** - Complete audit trail
- **State Saving** - Never lose work
- **Pattern Learning** - Improves over time
- **Response Capture** - Saves AI insights
- **Import Updates** - Auto-fixes after moves
- **Progress Tracking** - Real-time status

### Notification Hooks
- **Smart Suggestions** - Context-aware help
- **Team Awareness** - Multi-dev coordination
- **PR Feedback** - CodeRabbit integration

## 📊 Metrics & Analytics

```bash
# Track everything
/analytics report          # Overall metrics
/prp-metrics              # PRP success rates
/performance-monitor      # Speed improvements
/orchestration-stats      # Time saved

# Team insights
/team-performance         # Who's doing what
/knowledge-gaps          # What to document
```

## 🔗 Complete Workflow Examples

### Standard Feature with All Features
```bash
# 1. Research and plan
/research "Payment processing options"
/py-prd "Payment System"

# 2. Deep dive if complex
/prp-create payment-system

# 3. Generate work items
/gt payment-system
/cti "Payment System" --tests --create-prp

# 4. Start with orchestration
/orch payment-system --analyze
/fw start 123

# 5. Development with all guards
/pt payment-system        # TDD enforced
/checkpoint regularly     # State saved
/pydeps check often      # Dependencies tracked

# 6. Validate and grade
/stage-validate all
/grade payment-system
/security-check
/performance-monitor report
```

### Research-Heavy External Integration
```bash
# 1. PRP with documentation caching
/prp-create stripe-integration
/doc-cache cache "https://stripe.com/docs"

# 2. Research with sub-agents
/prp-execute stripe-integration

# 3. Capture patterns
/specs capture "Stripe Webhook Handler"

# 4. Build with validation
/prp-status               # Check gates
/prp-complete            # Generate report
```

## 🎯 Key Principles

1. **Everything is Tracked** - Context, dependencies, patterns
2. **Automation First** - Hooks handle repetitive work
3. **Research Before Build** - PRD/PRP drive development
4. **Parallel When Possible** - Orchestration saves time
5. **Quality Gates** - Can't proceed without passing
6. **Learn and Improve** - System gets smarter with use

## 💡 Remember

This system is FAR more than TDD. It's a complete:
- Requirements management system (PRD)
- Research platform (PRP)
- Task orchestrator
- Quality enforcer
- Knowledge manager
- Team coordinator
- Learning system

Use ALL the features to maximize productivity!
