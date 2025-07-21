# Next Command Suggestion System

## 🎯 Overview

Every command now provides intelligent suggestions for what to do next, creating a guided workflow that reduces cognitive load and helps you discover the optimal path through your development process.

## 🌟 Features

### 1. Complete Workflow Coverage
Every command from the decision guide has smart suggestions:
- **Project initialization** → PRD → Issues → Development
- **Bug workflows** → Track → Test → Fix → Resolve
- **Research flows** → PRP create → Execute → Complete → Implement
- **Feature development** → CTI/PRD → Tasks → Process → Test → Complete
- **Quick fixes** → Micro-task → Test → Commit

### 2. Decision Context Detection
The system recognizes when you might be unsure:
- **Starting something new?** Shows init/PRD/PRP options
- **Got AI suggestion?** Shows CTI/think-through/PRP options  
- **Found a bug?** Shows BT/MT/test generation options
- **Complex problem?** Shows research and analysis options

### 3. Contextual Command Suggestions
After every command, you'll see relevant next steps:

```bash
/cti "Fix import script"
✅ Created issue #17

💡 Next steps:
  1. `/gt import-script-fix` - Generate detailed task breakdown
  2. `/fw start 17` - Start working immediately
  3. `/prp import-optimization` - If research needed

🤔 Need help?
  • `/help` - See all commands
  • `/ws` - Check work status
  • `/think-through` - Get AI guidance
```

### 2. Smart Flow Detection
The system understands your workflow state:
- **Complex features** → Suggests research (`/prp`)
- **Simple fixes** → Suggests immediate start (`/fw start`)
- **Orchestratable tasks** → Suggests multi-agent (`/orch`)
- **Test failures** → Suggests debugging (`/bt add`)

### 3. Time-Based Awareness
Suggestions adapt to your work patterns:
- **Morning** → Resume yesterday's work (`/sr`)
- **Evening** → Save progress (`/checkpoint`)
- **Long sessions** → Remind to save/test

### 4. Learning System
The more you use it, the smarter it gets:
- Tracks your command sequences
- Learns your preferences
- Identifies successful patterns
- Personalizes suggestions

## 🔧 Configuration

### Enable/Disable Suggestions
Edit `.claude/suggestions-config.json`:

```json
{
  "enabled": true,
  "suggestion_limit": 3,
  "show_help_section": true,
  "time_based_suggestions": true,
  "learning_enabled": true
}
```

### Skip Specific Commands
Some commands don't need suggestions:
```json
{
  "skip_commands": [
    "help",
    "work-status",
    "task-status",
    "branch-status"
  ]
}
```

## 📋 Command Flows

### Feature Development Flow
```
/py-prd → /gi → /fw start → /gt → /pt → /test → /fw complete
```

Each step suggests the logical next action!

### Research Flow
```
/prp → /prp-execute → /prp-status → /prp-complete → /cti
```

### Quick Fix Flow
```
/mt → /test → /commit-review
```

## 💡 Examples

### Starting New Feature
```bash
/py-prd "User Dashboard"
✅ PRD created

💡 Next steps:
  1. `/gi user-dashboard` - Create GitHub issues
  2. `/think-through architecture` - Design system architecture
  3. `/cti "Dashboard API" --prd=user-dashboard` - Capture implementation
```

### After Task Generation
```bash
/gt user-auth
📊 Generated 15 tasks across 3 domains

💡 Next steps:
  1. `/orch user-auth --agents=3` - Save 1.5h with parallel execution
  2. `/fw start 23` - Process tasks sequentially
  3. `/think-through "implementation approach"` - Get AI guidance
```

### Test Failures
```bash
/test
❌ 3 tests failed

💡 Next steps:
  1. `/bt add "Test failures in auth module"` - Track the issue
  2. `/debug "test_user_login"` - Debug specific test
  3. `/generate-tests --fix` - Update test expectations
```

### Decision Context: Starting New
```bash
# When output mentions "new project" or "starting"

🎯 Decision Guide:
Starting something new? Choose based on:
  1. `/init-project` - Brand new project/repository
  2. `/py-prd user-dashboard` - New feature with requirements
  3. `/prp ml-scoring` - Complex problem needing research
```

### Decision Context: AI Gave Solution
```bash
# When Claude provides implementation plan

🎯 Decision Guide:
AI gave you a solution? Choose based on:
  1. `/cti "Caching strategy"` - Capture AI solution to issue
  2. `/think-through` - Need more analysis
  3. `/prp caching-options` - Requires research
```

## 🎓 Learning from Your Patterns

The system tracks successful workflows:

### Pattern Recognition
- Which commands you use together
- What leads to successful completions
- Your preferred workflows

### Personalization
Over time, suggestions become more relevant:
- If you always run tests after tasks → Suggests `/test`
- If you prefer orchestration → Prioritizes `/orch`
- If you checkpoint frequently → Reminds you to save

## 🚀 Getting Started

1. **Just use commands normally** - Suggestions appear automatically
2. **Follow suggestions** - They guide you to success
3. **Provide feedback** - The system learns from your choices

## 🔍 How It Works

### Post-Command Hook
The `15-next-command-suggester.py` hook:
1. Analyzes command output
2. Checks current context
3. Generates relevant suggestions
4. Displays them after command completion

### Integration Points
- Works with all existing commands
- Reads workflow state
- Checks branch status
- Considers time factors
- Learns from usage

## 📊 Analytics

Track suggestion effectiveness:
```bash
/analytics suggestions
```

Shows:
- Most followed suggestions
- Success rates
- Common patterns
- Time saved

## 🆘 Troubleshooting

### Not Seeing Suggestions?
1. Check if enabled: `.claude/suggestions-config.json`
2. Verify hook is active: `/help hooks`
3. Command might be in skip list

### Too Many/Few Suggestions?
Adjust limit in config:
```json
{
  "suggestion_limit": 5  // Change from default 3
}
```

### Reset Learning Data
```bash
rm .claude/analytics/command-sequences.json
rm .claude/analytics/learned-patterns.json
```

## 🎯 Benefits

1. **Never Get Stuck** - Always know what to do next
2. **Discover Features** - Learn commands in context
3. **Optimal Workflows** - Follow proven patterns
4. **Reduced Cognitive Load** - Focus on coding, not process
5. **Personalized Experience** - Adapts to your style

The Next Command Suggestion System transforms your development experience from a collection of commands into an intelligent, guided workflow!
