#!/usr/bin/env python3
"""
Get accurate count of all hooks and their activation status.
"""

import json
from pathlib import Path

def analyze_all_hooks():
    """Count all hooks and check their status."""
    hooks_dir = Path(".claude/hooks")
    settings_path = Path(".claude/settings.json")
    
    # Load current settings
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Get all configured hooks
    configured_hooks = set()
    for event_type, hooks in settings.get("hooks", {}).items():
        for hook in hooks:
            command = hook.get("command", [])
            if len(command) >= 2:
                hook_path = command[1]
                configured_hooks.add(hook_path)
    
    # Count all hook files
    all_hooks = {}
    hook_dirs = {
        'pre-tool-use': 'PreToolUse',
        'post-tool-use': 'PostToolUse',
        'notification': 'Notification',
        'stop': 'Stop',
        'sub-agent-stop': 'SubagentStop'
    }
    
    total_hooks = 0
    active_hooks = 0
    
    print("## Hook Status Report\n")
    
    for dir_name, event_type in hook_dirs.items():
        hook_dir = hooks_dir / dir_name
        if not hook_dir.exists():
            continue
            
        hooks = sorted(list(hook_dir.glob('*.py')))
        all_hooks[event_type] = []
        
        print(f"### {event_type} ({len(hooks)} total)")
        
        for hook_file in hooks:
            total_hooks += 1
            hook_path = f".claude/hooks/{dir_name}/{hook_file.name}"
            is_active = hook_path in configured_hooks
            
            if is_active:
                active_hooks += 1
                status = "✅ ACTIVE"
            else:
                status = "❌ NOT CONFIGURED"
            
            all_hooks[event_type].append({
                'file': hook_file.name,
                'path': hook_path,
                'active': is_active
            })
            
            print(f"- {hook_file.name}: {status}")
        
        print()
    
    # Check for utils directory
    utils_dir = hooks_dir / 'utils'
    if utils_dir.exists():
        utils_files = list(utils_dir.glob('*.py'))
        print(f"### Utils ({len(utils_files)} files)")
        for util_file in utils_files:
            total_hooks += 1
            print(f"- {util_file.name}: 📁 UTILITY (not a hook)")
        print()
    
    print(f"\n## Summary")
    print(f"- Total Python files: {total_hooks}")
    print(f"- Active hooks: {active_hooks}")
    print(f"- Inactive hooks: {total_hooks - active_hooks - 2}")  # -2 for utils
    print(f"- Utility files: 2")
    
    # List inactive hooks
    print(f"\n## Inactive Hooks (not in settings.json)")
    for event_type, hooks in all_hooks.items():
        inactive = [h for h in hooks if not h['active']]
        if inactive:
            print(f"\n### {event_type}")
            for hook in inactive:
                print(f"- {hook['file']}")
    
    return all_hooks, active_hooks, total_hooks

if __name__ == "__main__":
    analyze_all_hooks()
