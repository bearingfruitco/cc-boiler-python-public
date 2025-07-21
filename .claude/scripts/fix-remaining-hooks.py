#!/usr/bin/env python3
"""
Fix remaining hook issues after the initial automated fix.
Targets specific files that need manual intervention.
"""

import sys
from pathlib import Path

def fix_async_patterns_hook():
    """Fix the pre-tool-use/08-async-patterns.py hook."""
    hook_path = Path(".claude/hooks/pre-tool-use/08-async-patterns.py")
    
    with open(hook_path, 'r') as f:
        content = f.read()
    
    # Replace all the action field usages
    content = content.replace("print(json.dumps({'action': 'allow'}))", "sys.exit(0)")
    content = content.replace("print(json.dumps({'action': 'block',", "print(json.dumps({'decision': 'block',")
    content = content.replace("print(json.dumps({'action': 'warn',", "# Show warning in transcript\n            print(json.dumps({")
    
    # Add sys.exit(0) at the end of main if missing
    if "if __name__ == '__main__':" in content and not content.strip().endswith("sys.exit(0)"):
        content = content.rstrip() + "\n    sys.exit(0)\n"
    
    with open(hook_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {hook_path}")

def fix_pattern_learning_hook():
    """Fix the post-tool-use/06-pattern-learning.py hook."""
    hook_path = Path(".claude/hooks/post-tool-use/06-pattern-learning.py")
    
    with open(hook_path, 'r') as f:
        content = f.read()
    
    # Add sys.exit(0) at the end of main
    if "if __name__ == '__main__':" in content:
        # Find the main() call and add sys.exit after it
        lines = content.split('\n')
        for i in range(len(lines) - 1, -1, -1):
            if "main()" in lines[i] and not "sys.exit" in lines[i]:
                # Add proper indentation
                indent = len(lines[i]) - len(lines[i].lstrip())
                lines.insert(i + 1, " " * indent + "sys.exit(0)")
                break
        content = '\n'.join(lines)
    
    with open(hook_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {hook_path}")

def fix_research_capture_hook():
    """Fix the post-tool-use/08-research-capture.py hook."""
    hook_path = Path(".claude/hooks/post-tool-use/08-research-capture.py")
    
    with open(hook_path, 'r') as f:
        content = f.read()
    
    # This file doesn't have a main function, so we need to add proper structure
    # Add sys.exit(0) at the very end
    if not content.strip().endswith("sys.exit(0)"):
        content = content.rstrip() + "\n\n# Exit successfully\nsys.exit(0)\n"
    
    with open(hook_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {hook_path}")

def fix_dangerous_commands_hook():
    """Fix the pre-tool-use/01-dangerous-commands.py hook."""
    hook_path = Path(".claude/hooks/pre-tool-use/01-dangerous-commands.py")
    
    with open(hook_path, 'r') as f:
        content = f.read()
    
    # This hook has wrong JSON output format
    # Replace the success output with proper exit code
    content = content.replace(
        'print(json.dumps({"success": True}))',
        'sys.exit(0)  # Allow the command'
    )
    
    # Fix the error output to use exit code 2 for blocking
    content = content.replace(
        'print(json.dumps({\n            "error": reason,\n            "suggestion": "Please use a safer alternative or request permission"\n        }))\n        sys.exit(1)',
        'print(reason, file=sys.stderr)\n        print("Suggestion: Please use a safer alternative or request permission", file=sys.stderr)\n        sys.exit(2)  # Block the command'
    )
    
    with open(hook_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {hook_path}")

def main():
    print("🔧 Fixing remaining hook issues...\n")
    
    # Fix specific problematic hooks
    fix_async_patterns_hook()
    fix_pattern_learning_hook()
    fix_research_capture_hook()
    fix_dangerous_commands_hook()
    
    print("\n✅ All remaining hooks fixed!")
    print("\nNext steps:")
    print("1. Test Claude Code: claude")
    print("2. Check for any error messages")
    print("3. If issues persist, check .claude/hooks/fix-report.md")

if __name__ == "__main__":
    main()
