---
name: suggestions-config
aliases: [suggest-config, next-config]
description: Configure the Next Command Suggestion system
category: configuration
---

Configure how command suggestions work, view patterns, and manage learning.

## Usage
```bash
/suggestions-config [action] [options]
```

## Actions

### `status` - View Current Configuration
```bash
/suggestions-config status
```
Shows:
- Enabled/disabled state
- Suggestion limit
- Skip list
- Learning status

### `enable/disable` - Toggle Suggestions
```bash
/suggestions-config enable
/suggestions-config disable
```

### `limit` - Set Suggestion Count
```bash
/suggestions-config limit 5  # Show up to 5 suggestions
```

### `skip` - Manage Skip List
```bash
/suggestions-config skip add checkpoint  # Don't show after checkpoint
/suggestions-config skip remove help     # Start showing after help
/suggestions-config skip list           # View skip list
```

### `patterns` - View Learned Patterns
```bash
/suggestions-config patterns
```
Shows:
- Most common command sequences
- Success patterns
- User preferences

### `reset` - Clear Learning Data
```bash
/suggestions-config reset           # Reset all learning
/suggestions-config reset patterns  # Reset patterns only
```

## Examples

### Quick Config Check
```bash
/suggestions-config
# Shows current status and settings
```

### Adjust for Minimal Suggestions
```bash
/suggestions-config limit 1
/suggestions-config disable time-based
```

### Debug Why No Suggestions
```bash
/suggestions-config debug capture-to-issue
# Shows why suggestions might not appear for a command
```

## Configuration File

Located at `.claude/suggestions-config.json`:
```json
{
  "enabled": true,
  "suggestion_limit": 3,
  "show_help_section": true,
  "time_based_suggestions": true,
  "learning_enabled": true,
  "skip_commands": ["help", "work-status"]
}
```

## Learning System

### How It Learns
1. Tracks command sequences
2. Identifies success patterns
3. Weights suggestions by frequency
4. Personalizes over time

### Privacy
- All data stays local
- No external sharing
- Can be disabled/reset anytime

## Integration

Suggestions appear automatically after commands:
```
/cti "New Feature"
✅ Created issue #25

💡 Next steps:
  1. `/gt new-feature` - Generate tasks
  2. `/fw start 25` - Start immediately
  3. `/prp new-feature` - Research first
```

## Troubleshooting

### Not Seeing Suggestions?
1. Check if enabled: `/suggestions-config status`
2. Verify command not in skip list
3. Check if hook is active: `ls .claude/hooks/post-tool-use/`

### Too Many Suggestions?
```bash
/suggestions-config limit 2
```

### Wrong Suggestions?
The system learns over time. You can:
1. Reset learning: `/suggestions-config reset`
2. Or just keep using - it will adapt

## Related Commands
- `/help` - General help
- `/analytics suggestions` - View suggestion metrics
- `/workflow-guide` - See full workflows
