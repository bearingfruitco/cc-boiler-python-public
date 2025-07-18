# Updated Claude Code Boilerplate System Prompt v2.3.0

Use the MCP filesystem and AppleScript to review our enhanced project boilerplate and setup for Claude Code.

**Project Location**: `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/`

## System Overview
This is our enhanced Claude Code boilerplate project that embodies Sean Grove's vision of "The New Code" - where specifications are the primary development artifact and clear communication drives everything.

### Core Features
- **SYSTEM_OVERVIEW.md** - Complete technical documentation
- **NEW_CHAT_CONTEXT.md** - Quick reference for new sessions
- **90+ custom commands** with aliases
- **Specification-driven development** with PRD clarity linting
- **Automated design system** (4 sizes, 2 weights, 4px grid)
- **Hooks for safety and observability**
- **Zero context loss between sessions**

### Grove-Inspired Enhancements (v2.3.0)
- **PRD Clarity Linter** - Catches ambiguous language in requirements
- **Specification Patterns** (`/specs`) - Extract and reuse successful implementations
- **Test Generation** (`/prd-tests`) - Acceptance criteria → executable tests
- **Implementation Grading** (`/grade`) - Score alignment with PRD (0-100%)

### Context Management (v2.2.0)
- **Bug Tracking** (`/bt`) - Persistent across sessions with GitHub sync
- **Context Profiles** (`/cp`) - Focused work modes (frontend, backend, debug)
- **Documentation Cache** (`/dc`) - Offline access to library docs
- **Stage Validation** (`/sv`) - Enforce phase completion gates

### Integrated Systems
1. **Specification System** - PRDs as primary artifacts with clarity enforcement
2. **Hooks System** - Automated enforcement and safety
3. **Custom Commands** - 90+ commands for every workflow
4. **Pattern Learning** - Extract and reuse successful specifications
5. **GitHub Integration** - Issues, PRs, and gists
6. **Multi-Agent Orchestration** - 9 specialized personas

### Key Directories
```
.claude/
  ├── commands/      # 90+ custom commands
  ├── hooks/         # Automation & safety
  ├── personas/      # Agent personalities
  ├── bugs/          # Bug tracking
  ├── profiles/      # Context profiles
  ├── doc-cache/     # Documentation cache
  └── specs/         # Specification patterns (NEW)
      ├── patterns/  # Extracted patterns
      └── templates/ # Reusable templates
```

## Philosophy
Following Sean Grove's insights:
- **80-90% of programmer value is communication, not code**
- **Specifications are the "source code"**
- **Code is a "lossy projection" of intent**
- **Clear communication = effective programming**

## Workflow
```
IDEA → CLEAR PRD → TESTS → IMPLEMENTATION → GRADING → PATTERN EXTRACTION
         ↓           ↓           ↓              ↓              ↓
    Lint for    Generate    Guided by      Scored vs     Learn for
    clarity     from specs   micro-tasks   original      future
```

## Your Task
Review the entire system to understand:
1. How specifications drive all development
2. The role of clarity in requirements
3. How patterns are extracted and reused
4. How implementation quality is measured
5. The complete workflow from idea to deployment

Focus areas:
- Specification-driven development
- Automated quality measurements
- Pattern extraction and reuse
- Objective alignment scoring
- Communication as primary skill

This system represents the future of AI-assisted development where the person who communicates most effectively is the most valuable programmer.