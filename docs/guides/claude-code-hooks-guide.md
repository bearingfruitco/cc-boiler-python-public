# Claude Code Hooks Configuration Guide

## Overview
Hooks allow you to intercept and enhance Claude Code's behavior at key points in its lifecycle. This guide explains how to set up and use hooks based on the advanced patterns from the video.

## Available Hooks

### 1. **pre-tool-use**
- **When**: Before any tool/command runs
- **Purpose**: Block dangerous operations, validate inputs
- **Example**: Prevent `rm -rf`, protect .env files

### 2. **post-tool-use**
- **When**: After a tool/command completes
- **Purpose**: Logging, metrics, observability
- **Example**: Track all file changes, command usage

### 3. **notification**
- **When**: Claude Code needs user input
- **Purpose**: Custom notifications, alerts
- **Example**: Voice notifications, Slack alerts

### 4. **stop**
- **When**: Claude Code finishes responding
- **Purpose**: Save state, create summaries
- **Example**: Save chat transcript, checkpoint creation

### 5. **sub-agent-stop**
- **When**: A parallel sub-agent completes
- **Purpose**: Track parallel task progress
- **Example**: Monitor multiple concurrent operations

## Setting Up Hooks

### 1. Update settings.json
Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "pre-tool-use": [
      {
        "match": {},
        "command": ["python3", ".claude/hooks/pre-tool-use/01-dangerous-commands.py"]
      }
    ],
    "post-tool-use": [
      {
        "match": {},
        "command": ["python3", ".claude/hooks/post-tool-use/01-action-logger.py"]
      }
    ],
    "stop": [
      {
        "match": {},
        "command": ["python3", ".claude/hooks/stop/01-save-transcript.py"]
      }
    ],
    "sub-agent-stop": [
      {
        "match": {},
        "command": ["python3", ".claude/hooks/sub-agent-stop/01-track-completion.py"]
      }
    ]
  }
}
```

### 2. Hook Script Structure
All hook scripts follow this pattern:

```python
#!/usr/bin/env python3
import json
import sys

def main():
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Process the data
    # ... your logic here ...
    
    # Return response
    print(json.dumps({"success": True}))

if __name__ == "__main__":
    main()
```

## Practical Use Cases

### 1. **Observability & Debugging**
```python
# Log every action for debugging
.claude/logs/
  ├── actions-2024-01-15.jsonl      # All commands run
  ├── blocked-commands.jsonl        # Dangerous attempts
  └── sub-agents-2024-01-15.jsonl  # Parallel task tracking
```

### 2. **Safety & Security**
- Block `rm -rf` commands
- Prevent access to `.env` files
- Stop production database modifications
- Log all security-related blocks

### 3. **Team Notifications**
- Voice alerts when long tasks complete
- Slack notifications for important events
- Email summaries of agent sessions

### 4. **Context Preservation**
```
.claude/transcripts/
  ├── chat_20240115_143022.json    # Full conversation
  └── summary_20240115_143022.md   # Human-readable summary
```

## Advanced Patterns

### 1. **Chain Multiple Hooks**
```json
"post-tool-use": [
  {
    "match": {"tool_name": "file_write"},
    "command": ["python3", ".claude/hooks/post-tool-use/01-action-logger.py"]
  },
  {
    "match": {"tool_name": "file_write"},
    "command": ["python3", ".claude/hooks/post-tool-use/02-git-commit.py"]
  }
]
```

### 2. **Conditional Matching**
```json
"pre-tool-use": [
  {
    "match": {"tool_name": "shell_command"},
    "command": ["python3", ".claude/hooks/pre-tool-use/01-shell-validator.py"]
  }
]
```

### 3. **Voice Notifications** (from video)
```python
# Add text-to-speech for completion
import subprocess

def announce_completion():
    message = "All set and ready for your next step"
    # Use say command on macOS
    subprocess.run(["say", message])
```

## Benefits

1. **Better Debugging**: See exactly what Claude Code did
2. **Improved Safety**: Prevent accidental damage
3. **Team Awareness**: Know when tasks complete
4. **Learning**: Analyze what worked and what didn't
5. **Compliance**: Audit trail of all actions

## Quick Start

1. Create hooks directory structure:
```bash
mkdir -p .claude/hooks/{pre-tool-use,post-tool-use,stop,sub-agent-stop,notification}
```

2. Copy the provided hook scripts

3. Update your settings.json

4. Test with a simple command:
```bash
/sr  # Should trigger logging hooks
```

5. Check logs:
```bash
ls -la .claude/logs/
ls -la .claude/transcripts/
```

## Troubleshooting

- **Hooks not running**: Check settings.json syntax
- **Permission errors**: Make scripts executable: `chmod +x .claude/hooks/**/*.py`
- **No logs appearing**: Ensure log directories exist
- **Python errors**: Check Python version (3.11+)

---

Hooks transform Claude Code from a tool into a controllable, observable system that integrates with your workflow!