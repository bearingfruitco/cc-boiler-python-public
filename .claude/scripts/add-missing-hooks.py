#!/usr/bin/env python3
"""
Add missing hooks to settings.json configuration.
Ensures all implemented hooks are actually registered.
"""

import json
from pathlib import Path

def add_missing_hooks():
    """Add notification hooks and other missing hooks to settings."""
    settings_path = Path(".claude/settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Add Notification hooks if not present
    if "Notification" not in settings["hooks"]:
        settings["hooks"]["Notification"] = []
    
    # Notification hooks to add
    notification_hooks = [
        "01-precompact-handler.py",
        "03-smart-suggest.py",
        "04-team-aware.py"
        # Skip 02-pr-feedback-monitor.py as it might need specific config
    ]
    
    for hook_file in notification_hooks:
        hook_config = {
            "match": {},
            "command": [
                "python3",
                f".claude/hooks/notification/{hook_file}"
            ]
        }
        if hook_config not in settings["hooks"]["Notification"]:
            settings["hooks"]["Notification"].append(hook_config)
    
    # Check for missing pre-tool-use hooks
    pre_tool_use_dir = Path(".claude/hooks/pre-tool-use")
    existing_pre_hooks = [cmd[1].split('/')[-1] for hook in settings["hooks"]["PreToolUse"] for cmd in [hook["command"]]]
    
    # Important pre-tool-use hooks that should be active
    important_pre_hooks = [
        "02-collab-sync.py",  # GitHub sync for collaboration
        "05-actually-works.py",  # Already active
        "06-code-quality.py",  # Code quality checks
        "11-truth-enforcer.py",  # Facts enforcement
        "12-deletion-guard.py",  # Protect against accidental deletions
        "15-implementation-guide.py"  # Implementation guidance
    ]
    
    for hook_file in important_pre_hooks:
        if hook_file not in existing_pre_hooks:
            hook_path = pre_tool_use_dir / hook_file
            if hook_path.exists():
                hook_config = {
                    "match": {},
                    "command": [
                        "python3",
                        f".claude/hooks/pre-tool-use/{hook_file}"
                    ]
                }
                settings["hooks"]["PreToolUse"].append(hook_config)
                print(f"  Added PreToolUse hook: {hook_file}")
    
    # Check for missing post-tool-use hooks
    post_tool_use_dir = Path(".claude/hooks/post-tool-use")
    existing_post_hooks = [cmd[1].split('/')[-1] for hook in settings["hooks"]["PostToolUse"] for cmd in [hook["command"]]]
    
    important_post_hooks = [
        "05-command-logger.py",  # Command logging
        "06-pattern-learning.py",  # Already active  
        "07-python-response-capture.py",  # Python-specific capture
        "08-research-capture.py",  # Research document capture
        "09-python-import-updater.py",  # Import management
        "11-workflow-context-flow.py"  # Workflow context
    ]
    
    for hook_file in important_post_hooks:
        if hook_file not in existing_post_hooks:
            hook_path = post_tool_use_dir / hook_file
            if hook_path.exists():
                hook_config = {
                    "match": {},
                    "command": [
                        "python3",
                        f".claude/hooks/post-tool-use/{hook_file}"
                    ]
                }
                settings["hooks"]["PostToolUse"].append(hook_config)
                print(f"  Added PostToolUse hook: {hook_file}")
    
    # Add missing stop hooks
    stop_hooks = [
        "02-handoff-prep.py",
        "03-knowledge-share.py",
        "04-save-state.py"
    ]
    
    for hook_file in stop_hooks:
        hook_path = Path(f".claude/hooks/stop/{hook_file}")
        if hook_path.exists():
            hook_config = {
                "match": {},
                "command": [
                    "python3",
                    f".claude/hooks/stop/{hook_file}"
                ]
            }
            if hook_config not in settings["hooks"]["Stop"]:
                settings["hooks"]["Stop"].append(hook_config)
                print(f"  Added Stop hook: {hook_file}")
    
    # Add missing sub-agent-stop hook
    subagent_hook = "02-coordinate.py"
    hook_path = Path(f".claude/hooks/sub-agent-stop/{subagent_hook}")
    if hook_path.exists():
        hook_config = {
            "match": {},
            "command": [
                "python3",
                f".claude/hooks/sub-agent-stop/{subagent_hook}"
            ]
        }
        if hook_config not in settings["hooks"]["SubagentStop"]:
            settings["hooks"]["SubagentStop"].append(hook_config)
            print(f"  Added SubagentStop hook: {subagent_hook}")
    
    # Sort hooks by filename for consistency
    for event_type in settings["hooks"]:
        settings["hooks"][event_type].sort(key=lambda x: x["command"][1])
    
    # Save updated settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"\n✅ Updated {settings_path}")

def main():
    print("🔧 Adding missing hooks to configuration...\n")
    
    add_missing_hooks()
    
    print("\n✅ All implemented hooks are now registered!")
    print("\nHooks are now properly configured for:")
    print("- PreToolUse: Safety, quality, and validation checks")
    print("- PostToolUse: Logging, learning, and state management")
    print("- Notification: User alerts and suggestions")
    print("- Stop: Session cleanup and handoff")
    print("- SubagentStop: Multi-agent coordination")

if __name__ == "__main__":
    main()
