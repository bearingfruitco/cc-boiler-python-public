# Hook System Enhancements Documentation

## Overview

Version 2.3.3 introduces three major enhancements to the Claude Code Boilerplate hook system:

1. **PreCompact Hook Support** - Context preservation during conversation compaction
2. **Command Suggestion Engine** - Educational design violation feedback
3. **Structured Command Logging** - Analytics and performance insights

## PreCompact Hook Support

### Problem Solved
During long Claude sessions (4+ hours), conversations get compacted to save memory. This often results in Claude "forgetting" the current context, requiring developers to re-explain what they were working on.

### How It Works

1. **Detection**: The notification hook monitors for `conversation_compaction` events
2. **Preservation**: Critical files and context are saved to `.claude/context/pre-compact-context.json`
3. **Restoration**: The `/sr` (smart resume) command detects and restores the saved context

### Critical Files Preserved
- `CLAUDE.md` - AI instructions
- `QUICK_REFERENCE.md` - Command reference
- Current session state
- Latest checkpoint
- Active project PRD
- Current feature PRD
- Active task files

### Usage
```bash
# Automatic - no action needed!
# When compaction occurs:
🔄 Context preservation triggered before compaction
📁 Preserving 7 critical files
💡 Run /sr after compaction to restore full context

# After compaction:
/sr
## 🔄 PreCompact Context Detected!
📅 Saved at: 2024-01-15T14:30:00
📋 Active task: Adding error handling to LoginForm
## 📚 Re-reading Critical Files...
✓ Re-reading: CLAUDE.md
✓ Re-reading: docs/project/features/auth-PRD.md
✅ Context restoration complete!
```

## Command Suggestion Engine

### Features
- **Pattern Matching**: Detects common design violations
- **Helpful Suggestions**: Provides specific corrections
- **Learning System**: Tracks patterns over time
- **Educational Focus**: Explains why rules exist

### Violation Categories

#### Typography
- `text-sm` → `text-size-3` (16px)
- `text-lg` → `text-size-2` (24px)
- `font-bold` → `font-semibold` (600)

#### Spacing
- `p-5` → `p-4` or `p-6` (4px grid)
- `gap-5` → `gap-4` or `gap-6`

#### Accessibility
- Missing touch targets on buttons
- Text too small for mobile

### Example Output
```
❌ Design System Violation: Typography
📍 Line 23: Found 'text-sm'
✅ Use instead: text-size-3
💡 Why: Use text-size-3 (16px) for small text. Our design system uses only 4 font sizes.
📄 Context: ...<p className="text-sm text-gray-600">Description</p>...

📊 Your Most Common Violations:
  • 'text-sm' (12 times) → Use: text-size-3
  • 'p-5' (8 times) → Use: p-4 (16px) or p-6 (24px)

📈 Violation Categories:
  • typography: 15 total violations
  • spacing: 8 total violations
```

### Analytics Tracking
Violations are tracked in `.claude/analytics/design-violations.json`:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "matched_text": "text-sm",
  "category": "typography",
  "file": "components/ui/Card.tsx",
  "suggestion": "text-size-3",
  "session_id": "session-123"
}
```

## Structured Command Logging

### Features
- **Comprehensive Logging**: All commands with timing
- **JSON Lines Format**: Easy streaming and parsing
- **Daily Log Files**: Organized by date
- **Statistics Tracking**: Aggregate metrics
- **Query Interface**: Powerful analytics tool

### Log Structure
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "session_id": "session-123",
  "command_type": "claude_command",
  "command": "/cc",
  "args": ["Button", "--animate"],
  "full_command": "/cc Button --animate",
  "status": "success",
  "duration": 2340,
  "files_changed": ["components/ui/Button.tsx"],
  "error": null,
  "user": "shawnsmith"
}
```

### Query Examples

#### Basic Queries
```bash
# View recent commands
/query-logs

# Filter by command
/query-logs --command /cc

# Show only errors
/query-logs --errors-only

# Last 7 days
/query-logs --days 7
```

#### Analytics
```bash
# Show statistics
/query-logs --stats

📊 Command Usage Statistics
==================================================
📈 Overall:
  Total Commands: 247
  Total Time: 3.2m
  Success Rate: 94.3%

🔥 Most Used Commands:
  /cc             -   42 uses, 100.0% success,    2.3s avg
  /vd             -   38 uses,  92.1% success,    0.8s avg
```

#### Session Analysis
```bash
/query-logs --sessions

📋 Recent Sessions
==================================================
🔹 Session: abc123...
   Duration: 45.2 minutes
   Commands: 23 (2 errors)
   Total Processing: 52.3s
   Top Commands: /cc (8), /vd (5), /pt (3)
```

### Performance Queries
```bash
# Find slow operations
/query-logs --min-duration 5000

# Sort by duration
/query-logs --sort duration --limit 10
```

## Configuration

### Enabling/Disabling Features
In `.claude/config.json`:
```json
{
  "features": {
    "precompact_support": true,
    "suggestion_engine": true,
    "command_logging": true
  },
  "logging": {
    "retention_days": 30,
    "max_log_size_mb": 100
  }
}
```

### Design System Auto-Fix
```json
{
  "design_system": {
    "enforce": true,
    "auto_fix": false  // Set to true for automatic corrections
  }
}
```

## Implementation Details

### Hook Execution Order
1. **Pre-Tool-Use**: Design check with suggestions
2. **Tool Execution**: Command runs
3. **Post-Tool-Use**: Command logging
4. **Notification**: PreCompact handler

### Performance Considerations
- Suggestion engine adds ~50ms to file writes
- Command logging adds ~10ms overhead
- PreCompact check is near-instant
- All hooks fail gracefully

## Troubleshooting

### PreCompact Not Working
- Requires Claude Code v1.0.48+
- Check `.claude/context/` permissions
- Verify notification hooks are enabled

### Missing Suggestions
- Ensure `.claude/utils/` is in Python path
- Check `suggestion_engine.py` exists
- Verify design check hook uses enhanced version

### No Command Logs
- Check `.claude/logs/commands/` exists
- Verify post-tool-use hooks are enabled
- Ensure write permissions

## Best Practices

### For PreCompact
- Always run `/sr` after long breaks
- Keep critical docs in standard locations
- Don't rename core files during sessions

### For Suggestions
- Read the explanations to learn
- Review common mistakes weekly
- Share patterns with team

### For Logging
- Query stats weekly
- Identify slow commands
- Track error patterns
- Clean old logs monthly

## Future Enhancements

### Planned Features
- Multi-project suggestion sharing
- Command performance alerts
- PreCompact for team handoffs
- Export analytics to CSV
- Visual dashboards

### Integration Opportunities
- GitHub Actions for stats
- Slack notifications for errors
- Team violation leaderboards
- Performance benchmarks

## Contributing

To add new violation patterns:
1. Edit `suggestion_engine.py`
2. Add pattern to `self.suggestions`
3. Include category and explanation
4. Test with sample content

To enhance logging:
1. Modify `03-command-logger.py`
2. Add new fields to log entry
3. Update stats calculation
4. Extend query options

---

These enhancements make Claude Code Boilerplate more intelligent, educational, and resilient to long coding sessions.
