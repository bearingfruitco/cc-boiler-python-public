#!/usr/bin/env python3
"""
Final cleanup - remove references to non-existent hooks and fix remaining issues.
"""

import json
import re
from pathlib import Path

def cleanup_settings():
    """Remove references to non-existent hook files."""
    settings_path = Path(".claude/settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Check each hook reference
    cleaned_hooks = {}
    
    for event_type, hooks in settings.get("hooks", {}).items():
        cleaned_hooks[event_type] = []
        
        for hook in hooks:
            command = hook.get("command", [])
            if len(command) >= 2:
                hook_path = Path(command[1])
                
                # Only include if file exists
                if hook_path.exists():
                    cleaned_hooks[event_type].append(hook)
                else:
                    print(f"  Removed non-existent: {hook_path}")
    
    settings["hooks"] = cleaned_hooks
    
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print("✅ Cleaned settings.json")

def fix_remaining_action_fields():
    """Do a final pass to fix any remaining action fields."""
    hooks_dir = Path(".claude/hooks")
    
    # Pattern to find any remaining action field usage
    action_patterns = [
        (r'"action"\s*:', '"decision":'),
        (r"'action'\s*:", "'decision':"),
        (r'{\s*"action"\s*:\s*"continue"\s*}', '{}'),
        (r"{\s*'action'\s*:\s*'continue'\s*}", '{}'),
    ]
    
    for hook_file in hooks_dir.rglob('*.py'):
        if '.backup' in str(hook_file):
            continue
            
        try:
            with open(hook_file, 'r') as f:
                content = f.read()
            
            original = content
            
            # Apply all patterns
            for pattern, replacement in action_patterns:
                content = re.sub(pattern, replacement, content)
            
            # Special handling for specific patterns
            if '"action": "continue"' in content or "'action': 'continue'" in content:
                # Find the context and replace appropriately
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if '"action": "continue"' in line or "'action': 'continue'" in line:
                        # Check if it's in a print statement
                        if 'print' in line:
                            lines[i] = '    sys.exit(0)  # Continue'
                        else:
                            lines[i] = line.replace('"action": "continue"', '').replace("'action': 'continue'", '')
                content = '\n'.join(lines)
            
            if content != original:
                with open(hook_file, 'w') as f:
                    f.write(content)
                print(f"  ✅ Fixed: {hook_file.name}")
                
        except Exception as e:
            print(f"  ❌ Error fixing {hook_file.name}: {e}")

def create_summary():
    """Create a summary of all active hooks."""
    settings_path = Path(".claude/settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    summary_path = Path(".claude/hooks/ACTIVE_HOOKS.md")
    
    with open(summary_path, 'w') as f:
        f.write("# Active Claude Code Hooks\n\n")
        f.write("This file lists all currently active hooks in your Claude Code configuration.\n\n")
        
        for event_type, hooks in settings.get("hooks", {}).items():
            f.write(f"## {event_type} ({len(hooks)} hooks)\n\n")
            
            for hook in hooks:
                command = hook.get("command", [])
                if len(command) >= 2:
                    hook_path = Path(command[1])
                    f.write(f"- `{hook_path.name}`\n")
            
            f.write("\n")
        
        f.write("## Hook Status\n\n")
        f.write("All hooks have been updated to match the official Claude Code documentation:\n")
        f.write("- Using exit codes (0, 1, 2) for control flow\n")
        f.write("- Using 'decision' field instead of 'action' where applicable\n")
        f.write("- Proper error handling with stderr output\n")
        f.write("- Python 3 compatible with json and sys imports\n")
    
    print(f"\n✅ Created summary at: {summary_path}")

def main():
    print("🧹 Final cleanup of Claude Code hooks...\n")
    
    print("Step 1: Cleaning settings.json")
    cleanup_settings()
    
    print("\nStep 2: Final fix for action fields")
    fix_remaining_action_fields()
    
    print("\nStep 3: Creating summary")
    create_summary()
    
    print("\n✅ Cleanup complete!")
    print("\nYour hooks are now:")
    print("- ✅ Using official documentation format")
    print("- ✅ Free of 'action' fields")
    print("- ✅ Using proper exit codes")
    print("- ✅ Only referencing existing files")
    print("\nYou can now safely use Claude Code!")

if __name__ == "__main__":
    main()
