#!/usr/bin/env python3
"""
Fix hook event names to match official documentation format.
Changes kebab-case to PascalCase as per https://docs.anthropic.com/en/docs/claude-code/hooks
"""

import json
from pathlib import Path

def fix_hook_event_names():
    """Fix the hook event names in settings.json."""
    settings_path = Path(".claude/settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Map old names to new names according to official docs
    name_mapping = {
        "pre-tool-use": "PreToolUse",
        "post-tool-use": "PostToolUse",
        "stop": "Stop",
        "sub-agent-stop": "SubagentStop",  # Not in docs but following pattern
        "notification": "Notification"
    }
    
    # Create new hooks section with corrected names
    new_hooks = {}
    
    for old_name, hooks_list in settings.get("hooks", {}).items():
        new_name = name_mapping.get(old_name, old_name)
        new_hooks[new_name] = hooks_list
    
    # Update settings
    settings["hooks"] = new_hooks
    
    # Save with proper formatting
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"✅ Fixed hook event names in {settings_path}")
    
    # Show what was changed
    print("\nChanges made:")
    for old, new in name_mapping.items():
        if old in settings.get("hooks", {}):
            print(f"  {old} → {new}")

def main():
    print("🔧 Fixing hook event names to match official documentation...\n")
    
    fix_hook_event_names()
    
    print("\n✅ Hook event names fixed!")
    print("\nThe hooks now use the official PascalCase naming:")
    print("- PreToolUse")
    print("- PostToolUse")
    print("- Stop")
    print("- SubagentStop")
    print("- Notification")

if __name__ == "__main__":
    main()
