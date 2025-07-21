#!/usr/bin/env python3
"""
Final comprehensive fix for all remaining hook issues.
This addresses all validation failures found.
"""

import re
import sys
import json
from pathlib import Path

class ComprehensiveHookFixer:
    def __init__(self):
        self.hooks_dir = Path(".claude/hooks")
        self.fixed_count = 0
        
    def fix_hook_content(self, content, hook_type, file_path):
        """Apply all necessary fixes to hook content."""
        original = content
        
        # Ensure proper imports
        if 'import json' not in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import') or line.startswith('from'):
                    lines.insert(i, 'import json')
                    break
            else:
                lines.insert(0, 'import json')
            content = '\n'.join(lines)
            
        if 'import sys' not in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'import json' in line:
                    lines.insert(i + 1, 'import sys')
                    break
            content = '\n'.join(lines)
        
        # Fix all "action" field occurrences
        if hook_type == "PreToolUse":
            # Replace action fields with proper format
            content = re.sub(
                r'["\']action["\']\s*:\s*["\']block["\']',
                '"decision": "block"',
                content
            )
            content = re.sub(
                r'["\']action["\']\s*:\s*["\']approve["\']',
                '"decision": "approve"',
                content
            )
            content = re.sub(
                r'["\']action["\']\s*:\s*["\']continue["\']',
                'sys.exit(0)  # Continue',
                content
            )
            content = re.sub(
                r'["\']action["\']\s*:\s*["\']allow["\']',
                'sys.exit(0)  # Allow',
                content
            )
            
        elif hook_type in ["PostToolUse", "Stop", "SubagentStop"]:
            # These can use decision field
            content = re.sub(
                r'["\']action["\']\s*:\s*["\']block["\']',
                '"decision": "block"',
                content
            )
            # Replace continue/allow with exit codes
            content = re.sub(
                r'print\s*\(\s*json\.dumps\s*\(\s*\{\s*["\']action["\']\s*:\s*["\']continue["\']\s*\}\s*\)\s*\)',
                'sys.exit(0)',
                content
            )
            
        elif hook_type == "Notification":
            # Notification hooks just use exit codes
            content = re.sub(
                r'["\']action["\']\s*:\s*["\']notify["\']',
                'sys.exit(0)  # Show notification',
                content
            )
            content = re.sub(
                r'print\s*\(\s*json\.dumps\s*\(\s*\{[^}]*["\']action["\']\s*:[^}]*\}\s*\)\s*\)',
                'sys.exit(0)',
                content
            )
        
        # Fix research-capture.py which has no main function
        if 'research-capture.py' in str(file_path) and 'def main' not in content:
            # Wrap the loose code in a main function
            lines = content.split('\n')
            import_end = 0
            for i, line in enumerate(lines):
                if not line.startswith('import') and not line.startswith('from') and line.strip() and not line.startswith('#'):
                    import_end = i
                    break
            
            # Insert main function
            main_code = ['', 'def main():', '    """Main hook logic."""', '    try:']
            rest_code = ['    ' + line if line.strip() else line for line in lines[import_end:]]
            rest_code.append('    except Exception as e:')
            rest_code.append('        print(f"Hook error: {e}", file=sys.stderr)')
            rest_code.append('        sys.exit(1)')
            rest_code.append('')
            rest_code.append('if __name__ == "__main__":')
            rest_code.append('    main()')
            rest_code.append('    sys.exit(0)')
            
            content = '\n'.join(lines[:import_end] + main_code + rest_code)
        
        # Ensure all files have proper exit
        if 'sys.exit' not in content:
            if 'if __name__' in content:
                # Add sys.exit(0) before if __name__
                lines = content.split('\n')
                for i in range(len(lines) - 1, -1, -1):
                    if 'if __name__' in lines[i]:
                        indent = len(lines[i-1]) - len(lines[i-1].lstrip()) if i > 0 else 0
                        lines.insert(i, ' ' * indent + 'sys.exit(0)')
                        break
                content = '\n'.join(lines)
            else:
                # Add at the end
                content = content.rstrip() + '\n\nsys.exit(0)\n'
        
        return content != original, content
    
    def fix_all_remaining_hooks(self):
        """Fix all hooks with remaining issues."""
        print("🔧 Applying comprehensive fixes to all hooks...\n")
        
        # Get all hook files
        hook_types = {
            'pre-tool-use': 'PreToolUse',
            'post-tool-use': 'PostToolUse',
            'notification': 'Notification',
            'stop': 'Stop',
            'sub-agent-stop': 'SubagentStop'
        }
        
        for dir_name, hook_type in hook_types.items():
            hook_dir = self.hooks_dir / dir_name
            if not hook_dir.exists():
                continue
                
            for hook_file in hook_dir.glob('*.py'):
                try:
                    with open(hook_file, 'r') as f:
                        content = f.read()
                    
                    changed, new_content = self.fix_hook_content(content, hook_type, hook_file)
                    
                    if changed:
                        with open(hook_file, 'w') as f:
                            f.write(new_content)
                        print(f"  ✅ Fixed: {hook_file.name}")
                        self.fixed_count += 1
                        
                except Exception as e:
                    print(f"  ❌ Error fixing {hook_file.name}: {e}")
        
        # Fix settings.json to remove duplicate entries
        self.fix_settings_duplicates()
    
    def fix_settings_duplicates(self):
        """Remove duplicate hook entries from settings.json."""
        settings_path = Path(".claude/settings.json")
        
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        # Remove duplicates while preserving order
        for event_type in settings.get("hooks", {}):
            seen = set()
            unique_hooks = []
            
            for hook in settings["hooks"][event_type]:
                hook_key = tuple(hook["command"])
                if hook_key not in seen:
                    seen.add(hook_key)
                    unique_hooks.append(hook)
            
            settings["hooks"][event_type] = unique_hooks
        
        # Save cleaned settings
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print("\n✅ Cleaned up duplicate entries in settings.json")

def main():
    fixer = ComprehensiveHookFixer()
    fixer.fix_all_remaining_hooks()
    
    print(f"\n✅ Fixed {fixer.fixed_count} hooks")
    print("\nAll hooks should now be compliant with official documentation.")
    print("\nNext steps:")
    print("1. Run validation: python3 .claude/scripts/validate-hooks.py")
    print("2. Test Claude Code: claude")

if __name__ == "__main__":
    main()
