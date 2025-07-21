# System Overview - Python Boilerplate v2.4.1

## 🌟 What Makes This Special

This isn't just a boilerplate - it's an intelligent development system that:
- **Never loses context** between sessions
- **Tracks all tasks centrally** with Task Ledger (NEW!)
- **Enforces TDD automatically** (tests generate when you need them)
- **Prevents common mistakes** through 40+ hooks
- **Learns from your patterns** and improves
- **Orchestrates multi-agent work** for complex features

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                        Claude Code                          │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  Commands   │  │    Hooks     │  │  Context Store   │ │
│  │  (86+)      │  │  (40 active) │  │  (Persistent)    │ │
│  └─────────────┘  └──────────────┘  └──────────────────┘ │
│                   ┌──────────────┐                         │
│                   │ Task Ledger  │ (NEW!)                  │
│                   │  (.task-ledger.md)                     │
│                   └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Python Application                      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │   Agents    │  │   FastAPI    │  │    Pipelines     │ │
│  │ (Pydantic)  │  │  (Async)     │  │   (Prefect)      │ │
│  └─────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Hook System Flow

```
User Input → Pre-Tool Hooks → Tool Execution → Post-Tool Hooks → Response
     ↓              ↓                               ↓
  Validation   Safety Checks                 Learning & Capture
```

## 🚀 Key Features

### 1. Test-Driven Development (Automatic!)
- Tests generate automatically when starting work
- Can't write code without tests (configurable)
- Test status visible throughout workflow
- Coverage tracked and enforced

### 2. Context Preservation
- **Smart Resume**: Never lose work between sessions
- **State Tracking**: Every action logged and recoverable
- **Profile Management**: Switch contexts without losing work
- **Checkpoint System**: Save states at important moments

### 3. Intelligent Orchestration
- Analyzes task complexity
- Recommends multi-agent execution
- Distributes work optimally
- 50-70% time savings on complex features

### 4. Safety & Quality Hooks
- **Creation Guard**: Prevents duplicate code
- **Dependency Tracking**: Knows what uses what
- **Import Validation**: Catches broken imports
- **PII Protection**: No sensitive data in logs
- **Deletion Guard**: Warns before removing code

### 5. Learning System
- **Pattern Capture**: Learns from successful implementations
- **Response Storage**: Saves AI recommendations
- **Command Tracking**: Optimizes common workflows
- **Success Metrics**: Tracks what works

### 6. Task Ledger (NEW!)
- **Central Tracking**: All tasks in `.task-ledger.md`
- **Progress Visibility**: Real-time task completion
- **Issue Linking**: Connects tasks to GitHub issues
- **Automatic Updates**: Hook system maintains ledger
- **Team Coordination**: Everyone sees same status

## 📋 Command Categories

### Context & State (Never Lose Work)
```bash
/sr              # Smart Resume - start here ALWAYS
/tl              # Task Ledger - view all tasks (NEW!)
/checkpoint      # Save current state
/context-profile # Manage work contexts
/compress        # Optimize token usage
```

### Development (TDD Enforced)
```bash
/py-prd          # Python-specific PRD
/py-agent        # Create AI agent
/py-api          # Create API endpoint
/py-pipeline     # Create data pipeline
/generate-tests  # Manual test generation (usually automatic)
```

### Workflow (Automated Chains)
```bash
/chain tdd       # Complete TDD workflow
/chain pf        # Python feature workflow
/chain pq        # Python quality checks
/fw start        # Start issue (auto-tests!)
/pt              # Process tasks (TDD enforced)
```

### Intelligence (AI-Powered)
```bash
/cti             # Capture AI responses to issues
/orch            # Multi-agent orchestration
/prp-create      # Research-heavy features
/think-through   # Deep problem analysis
```

### Safety (Automatic Protection)
```bash
/pyexists        # Check before creating
/pydeps          # Track dependencies
/facts           # Show unchangeable truths
/truth-override  # Override protections (careful!)
```

## 🔄 Workflow Examples

### Standard Feature (2-3 hours)
```bash
/sr → /py-prd → /cti --tests → /fw start → /pt → /test → /fw complete
```

### Complex Feature with Research (1-2 days)
```bash
/sr → /prp-create → /prp-execute → /prp-status → /prp-complete
```

### Multi-Agent Feature (4+ hours → 2 hours)
```bash
/sr → /py-prd → /gt → /orch → monitor → /sas
```

### Quick Bug Fix (< 1 hour)
```bash
/sr → /bt add → /generate-tests → fix → /test → /bt resolve
```

## 🛡️ Automatic Protections

These run without any action from you:

1. **Before Writing Code**
   - Checks if component exists
   - Validates imports
   - Ensures tests exist
   - Checks for PII

2. **After Writing Code**
   - Updates dependencies
   - Runs tests
   - Captures patterns
   - Saves state

3. **Throughout Development**
   - Tracks context
   - Logs decisions
   - Learns patterns
   - Prevents mistakes

## 📊 Metrics & Tracking

The system tracks:
- Task completion rates
- Test coverage trends
- Command usage patterns
- Error frequencies
- Time savings from orchestration
- Success patterns

Access with:
```bash
/analytics report
/prp-metrics
/performance-monitor
```

## 🔧 Configuration

### Core Settings (.claude/settings.json)
```json
{
  "tdd": {
    "auto_generate_tests": true,
    "enforce_tests_first": true,
    "minimum_coverage": 80
  },
  "orchestration": {
    "auto_suggest": true,
    "complexity_threshold": 10
  },
  "context": {
    "auto_save": true,
    "compression": true
  }
}
```

### MCP Configuration (.mcp.json)
- GitHub integration
- Supabase (optional)
- Browserbase (optional)
- Custom tools

## 🚦 Getting Started Path

1. **Day 1**: [Day 1 Quick Start](DAY_1_QUICK_START.md)
2. **Daily**: [Daily Workflow Guide](DAILY_WORKFLOW_GUIDE.md)
3. **Features**: [Python Workflows](../PYTHON_WORKFLOWS.md)
4. **Advanced**: [PRP Guide](../../docs/guides/PRP_GUIDE.md)

## 💡 Philosophy

This system embodies:
- **Context is King**: Never lose work or thoughts
- **Quality by Default**: TDD isn't optional, it's automatic
- **Learn and Improve**: Every session makes the next better
- **Automate Toil**: Hooks handle the repetitive stuff
- **Fail Fast**: Catch problems before they compound

Ready to build with intelligence? Start with `/sr`! 🚀
