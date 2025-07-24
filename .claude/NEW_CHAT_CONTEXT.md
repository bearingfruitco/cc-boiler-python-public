# New Chat Context - Python Boilerplate v2.4.2

## 🚀 Quick Start for New Chats

You're working with an **intelligent Python development system** that actively helps you code better and faster. Here's what you need to know:

### First Command Always:
```bash
/sr    # Smart Resume - restores everything you need
```

### What This System Does:
- **Prevents mistakes** before they happen (40+ safety hooks)
- **Tracks all work** centrally (Task Ledger system)
- **Generates tests** automatically (TDD enforced)
- **Never loses context** between sessions
- **Orchestrates AI agents** for complex features

## 🆕 What's New in v2.4.2

### Enhanced Intelligence Features
- **Permission Profiles**: Dynamic safety levels (exploration → ci_pipeline)
- **Screenshot Capture**: Automatic browser screenshots on test failures
- **Auto-staging**: Git stages files after successful tests/edits
- **Thinking Levels**: Control reasoning depth with `/think-level`
- **Enhanced Compression**: Focus-aware context compression

### New Commands
```bash
/think-level deep              # Enhanced reasoning for complex problems
/compress --focus="api design" # Targeted context compression
/chain drop-in                # Full system setup for existing projects
```

## 🎯 Core Concepts

### 1. Task Ledger (Your Central Hub)
The `.task-ledger.md` file tracks EVERYTHING:
- All features and their tasks
- Progress on each feature (X/Y complete)
- Links to GitHub issues
- Who's working on what
- What's blocked and why

Access with:
```bash
/tl              # View everything
/tl view auth    # Specific feature
/tl update       # Update progress
```

### 2. Automatic Safety System
**40+ hooks** run automatically to:
- Prevent duplicate code creation
- Block circular imports
- Protect sensitive data
- Enforce test coverage
- Manage git branches
- Update dependencies

You don't need to remember these - they just work!

### 3. Python-Specific Commands
```bash
# Create Components
/py-agent AIAssistant    # Pydantic AI agent
/py-api /users CRUD      # FastAPI endpoints  
/py-pipeline ETLFlow     # Prefect pipeline

# Check Before Creating
/pyexists UserModel      # Already exists?
/pydeps check auth       # What depends on this?
/pysimilar AuthService   # Find similar code
```

### 4. Workflow Automation (Chains)
Pre-configured workflows for common tasks:
```bash
/chain tdd          # Test-driven development
/chain pf           # Python feature
/chain ma           # Multi-agent orchestration
/chain deps         # Dependency analysis
```

## 📋 Essential Commands Reference

### Must-Know Commands
| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `/sr` | Restore context | ALWAYS start here |
| `/tl` | View all tasks | Check progress |
| `/help` | Get help | When stuck |
| `/py-prd` | Create feature spec | New features |
| `/pt` | Process tasks | Implementation |

### Development Flow
| Command | Purpose | Example |
|---------|---------|---------|
| `/cti` | Capture AI response to issue | `/cti "auth system" --tests` |
| `/fw start 123` | Start work on issue #123 | Tests auto-generate |
| `/test` | Run tests | After changes |
| `/grade` | Check quality | Before completing |

### Intelligence Features
| Command | Purpose | Power Feature |
|---------|---------|---------------|
| `/orch` | Multi-agent mode | 50-70% faster |
| `/prp-create` | Research mode | External APIs |
| `/think-through` | Deep analysis | Complex problems |

## 🛡️ How Safety Works

### Example: Creating a New Model
```python
# You type:
class UserModel(BaseModel):
    email: str
    
# System automatically:
1. Checks if UserModel exists ✓
2. Finds similar models ✓
3. Validates imports ✓
4. Generates tests ✓
5. Updates dependencies ✓
```

### Example: Preventing Breaks
```bash
# You want to refactor:
/pydeps breaking UserModel

# System shows:
⚠️ Breaking Changes Detected:
- api/endpoints/auth.py uses UserModel
- services/user_service.py imports UserModel
- tests/test_user.py depends on UserModel

Suggested approach:
1. Create new model alongside old
2. Migrate usage incrementally
3. Remove old when safe
```

## 🚀 Workflow Examples

### Standard Feature Development
```bash
# 1. Start fresh
/sr

# 2. Define feature  
/py-prd user-authentication

# 3. Capture to issue (tests auto-generate!)
/cti "User Auth System" --type=api --tests

# 4. Start work (tests already exist!)
/fw start 123

# 5. Work through tasks
/pt user-auth

# 6. Verify and complete
/test && /grade && /fw complete
```

### Quick Bug Fix
```bash
/sr                          # Resume context
/mt "fix login timeout"      # Micro task
# Fix the bug
/test                        # Verify fix
/sc                          # Safe commit
```

### Complex Feature with Research
```bash
/sr                          # Resume
/prp-create payment-system   # Research-heavy
/prp-execute                 # Run research
/orch payment-system         # Multi-agent build
/sas                         # Monitor agents
```

## 🏗️ System Architecture

### Hook System Flow
```
Your Input → Pre-Hooks (Safety) → Action → Post-Hooks (Learning) → Response
             ↓                              ↓
             Validation                     State Updates
             Checks                         Pattern Capture
             Protection                     Task Updates
```

### File Organization
```
.claude/
├── commands/      # 70+ command definitions
├── hooks/         # 40+ safety & intelligence hooks
├── context/       # Persistent state
├── personas/      # AI agent configurations
└── research/      # Captured patterns

src/
├── agents/        # Pydantic AI agents
├── api/           # FastAPI endpoints
├── models/        # Data models
├── pipelines/     # Prefect workflows
└── services/      # Business logic
```

## 🔧 Configuration & Settings

### Key Config Files
1. **`.claude/settings.json`** - Hook configuration
2. **`.claude/config.json`** - System settings
3. **`.claude/aliases.json`** - Command shortcuts
4. **`.claude/chains.json`** - Workflow definitions

### Important Settings
```json
{
  "tdd": {
    "enforce": true,          // Can't code without tests
    "auto_generate": true,    // Tests appear automatically
    "coverage_threshold": 80  // Minimum coverage
  },
  "branch_management": {
    "max_active_branches": 1, // Focus on one feature
    "strict_mode": true       // Enforce rules
  }
}
```

## 📊 Performance Tips

### Token Optimization
```bash
/compress               # Standard compression
/compress --target=50   # Aggressive (50% reduction)
/compress --focus="api" # Keep API details, compress rest
```

### Speed Improvements
- Use `/orch` for features touching 3+ files
- Enable auto-staging for faster commits
- Use chains instead of individual commands
- Let hooks handle repetitive tasks

## 🐛 Troubleshooting

### Common Issues & Solutions

**"Can't find context"**
```bash
/sr              # Rebuilds everything
/cp load last    # Load last profile
```

**"Tests failing"**
```bash
/test --verbose  # See details
/think-level deep && /debug  # AI debugging
```

**"Too many tokens"**
```bash
/compress --aggressive  # Reduce context
/cp save minimal       # Save lightweight profile
```

## 💡 Pro Tips

1. **Always start with `/sr`** - It's fast and prevents confusion
2. **Use chains** - `/chain tdd` is faster than manual steps
3. **Trust the hooks** - They prevent 90% of common mistakes
4. **Check dependencies** - `/pydeps check` before big changes
5. **Let AI orchestrate** - `/orch` for complex features
6. **Review Task Ledger** - `/tl` shows the big picture

## 🎓 Learning Path

### Day 1: Basics
```bash
/sr → /help new → /py-prd → /cti → /fw start
```

### Week 1: Productivity
```bash
Learn chains → Use /orch → Master /prp workflows
```

### Month 1: Mastery
```bash
Custom personas → Multi-agent → Advanced patterns
```

## 🚦 Ready to Start?

1. Run `/sr` to load context
2. Check `/tl` for active work
3. Use `/help` if stuck
4. Trust the system - it's protecting you!

Remember: **This system learns from you**. Every successful pattern is captured and reused. The more you use it, the smarter it gets!

---

*Note: This system uses Python-based hooks that integrate with Claude Code through the settings.json configuration. All hooks are active and working - you don't need to configure anything!*
