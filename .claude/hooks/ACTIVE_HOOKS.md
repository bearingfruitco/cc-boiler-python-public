# Active Claude Code Hooks

This file lists all currently active hooks in your Claude Code configuration.

## PreToolUse (24 hooks) 

### Core Safety & Validation

- `00-auto-approve-safe-ops.py` **(ENHANCED)** - Now supports permission profiles
- `01-dangerous-commands.py`
- `02-collab-sync.py`
- `03-python-style-check.py`
- `04-conflict-check.py`
- `05-actually-works.py`
- `06-code-quality.py`
- `07-pii-protection.py`
- `08-async-patterns.py`
- `09-evidence-language.py`
- `10-auto-persona.py`
- `11-truth-enforcer.py`
- `12-deletion-guard.py`
- `13-import-validator.py`
- `14-prd-clarity.py`
- `15-implementation-guide.py`
- `16-python-creation-guard.py`
- `17-python-dependency-tracker.py`
- `18-cloud-config-validator.py`
- `19-test-generation-enforcer.py`
- `20-feature-state-guardian.py` **(NEW)** - Prevents recreation of completed features
- `21-branch-controller.py` **(NEW)** - Enforces branch management rules
- `22-thinking-level-integration.py` - Manages thinking depth for complex problems
- `23-existing-project-analyzer.py` - Analyzes existing projects for integration
- `24-worktree-integration.py` **(NEW)** - Git worktree context awareness

## PostToolUse (19 hooks)

- `01-action-logger.py`
- `02-state-save.py`
- `03-metrics.py`
- `04-auto-orchestrate.py`
- `05-command-logger.py`
- `06-pattern-learning.py`
- `07-python-response-capture.py`
- `08-research-capture.py`
- `09-python-import-updater.py`
- `10-prp-progress-tracker.py`
- `11-workflow-context-flow.py`
- `12-code-test-validator.py`
- `13-auto-test-generation.py`
- `14-branch-activity-tracker.py` - Tracks file modifications per branch
- `15-next-command-suggester.py` - Provides contextual next step suggestions
- `16-next-command-suggester.py` - Enhanced suggestion engine
- `17-task-ledger-updater.py` - Updates central task tracking
- `18-screenshot-capture.py` **(NEW)** - Captures browser screenshots on test failures
- `19-auto-stage-working.py` **(NEW)** - Auto-stages files after successful operations

## Stop (4 hooks)

- `01-save-transcript.py`
- `02-handoff-prep.py`
- `03-knowledge-share.py`
- `04-save-state.py`

## SubagentStop (2 hooks)

- `01-track-completion.py`
- `02-coordinate.py`

## Notification (4 hooks)

- `01-precompact-handler.py`
- `02-pr-feedback-monitor.py`
- `03-smart-suggest.py`
- `04-team-aware.py`

## Hook Status

All hooks have been updated to match the official Claude Code documentation:
- Using exit codes (0, 1, 2) for control flow
- Using 'decision' field instead of 'action' where applicable  
- Proper error handling with stderr output
- Python 3 compatible with json and sys imports

## New TDD Features

### Test-Driven Development Hooks
- **19-test-generation-enforcer.py**: Enforces test-first development by blocking code without tests
- **12-code-test-validator.py**: Automatically validates code against pre-written tests

### TDD Configuration
- Configurable enforcement levels
- Coverage thresholds
- Override options for emergencies
- Integration with existing workflows

## New Branch Management Features

### Branch Protection Hooks
- **20-feature-state-guardian.py**: Prevents modifying completed features from wrong branches
- **21-branch-controller.py**: Enforces branch limits and prevents conflicts
- **14-branch-activity-tracker.py**: Automatically tracks which files are modified on which branches

### Branch Management Configuration
- Maximum active branches enforcement
- Required main sync before new branches
- File locking to prevent conflicts
- Feature state protection
- Smart branch switching with context preservation

### New Commands
- `/branch-status` (`/bs`) - Comprehensive branch overview
- `/feature-status` (`/fs`) - Check feature completion state
- `/sync-main` - Safely update from main branch
- `/branch-switch` (`/bsw`) - Context-aware branch switching
- `/think-level` (`/tl-think`) - Set thinking depth for complex problems

## New Next Command Suggestions Feature

### Intelligent Workflow Guidance
- **15-next-command-suggester.py**: Provides contextual suggestions after every command
- Learns from your command patterns over time
- Adapts suggestions based on:
  - Current workflow stage
  - Time of day
  - Task complexity
  - Success patterns

### Configuration
- Managed via `.claude/suggestions-config.json`
- Can disable for specific commands
- Adjustable suggestion limit
- Learning system can be toggled

### Benefits
- Never get stuck wondering what to do next
- Discover optimal workflows
- Reduce cognitive load
- Personalized to your development style

## New Features from Claude Code Integration

### Permission Profiles (ENHANCED)
- **Dynamic permission management** based on context
- Profiles: exploration, development, testing, ci_pipeline, multi_agent
- Auto-switches based on commands (e.g., `/test` → testing profile)
- Configured in `.claude/permission-profiles.json`

### Screenshot Capture
- **Automatic browser screenshot on test failures**
- Integrates with playwright, puppeteer, or native tools
- Links screenshots to Task Ledger entries
- Stores in `.claude/screenshots/`

### Auto-staging
- **Git auto-staging after successful operations**
- Stages files after tests pass
- Excludes sensitive files (.env, secrets)
- Maintains staging log for tracking

### Thinking Levels
- **Graduated reasoning depth** for complex problems
- Levels: standard, deep, ultra
- Token usage tracking
- Auto-escalation for security/critical issues

### Enhanced Context Compression
- **Focus areas** to preserve critical information
- Exclude specific topics from compression
- Target compression percentages
- Integration with workflow triggers
