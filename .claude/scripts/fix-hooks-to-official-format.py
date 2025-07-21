#!/usr/bin/env python3
"""
Fix Claude Code hooks to match official documentation format.
This script updates all hooks to use exit codes and proper JSON output
as specified in https://docs.anthropic.com/en/docs/claude-code/hooks
"""

import re
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class HookFixer:
    def __init__(self):
        self.hooks_dir = Path(".claude/hooks")
        self.backup_dir = Path(".claude/hooks-backup-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.fixes_applied = []
        
    def backup_hooks(self):
        """Create a backup of all hooks before making changes."""
        if self.hooks_dir.exists():
            shutil.copytree(self.hooks_dir, self.backup_dir)
            print(f"✅ Created backup at: {self.backup_dir}")
    
    def analyze_hook(self, file_path):
        """Analyze a hook file to determine what fixes are needed."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            issues = []
            
            # Check for outdated "action" field usage
            if '"action"' in content:
                issues.append("uses_action_field")
            
            # Check if it's using proper exit codes
            if 'sys.exit' not in content:
                issues.append("missing_exit_codes")
            
            # Check if it imports sys
            if 'import sys' not in content:
                issues.append("missing_sys_import")
            
            # Check for specific patterns
            if 'print(json.dumps({"action": "continue"' in content:
                issues.append("action_continue_pattern")
            
            if 'print(json.dumps({"action": "block"' in content:
                issues.append("action_block_pattern")
            
            if 'print(json.dumps({"action": "warn"' in content:
                issues.append("action_warn_pattern")
            
            if 'print(json.dumps({"action": "approve"' in content:
                issues.append("action_approve_pattern")
                
            # Determine hook type from path
            hook_type = None
            if 'pre-tool-use' in str(file_path):
                hook_type = 'pre-tool-use'
            elif 'post-tool-use' in str(file_path):
                hook_type = 'post-tool-use'
            elif 'stop' in str(file_path):
                hook_type = 'stop'
            elif 'sub-agent-stop' in str(file_path):
                hook_type = 'sub-agent-stop'
            elif 'notification' in str(file_path):
                hook_type = 'notification'
            
            return {
                'path': file_path,
                'hook_type': hook_type,
                'issues': issues,
                'content': content
            }
        except Exception as e:
            return {
                'path': file_path,
                'error': str(e)
            }
    
    def fix_hook(self, analysis):
        """Fix a hook file based on the analysis."""
        if 'error' in analysis:
            return False, f"Error reading file: {analysis['error']}"
        
        file_path = analysis['path']
        content = analysis['content']
        hook_type = analysis['hook_type']
        issues = analysis['issues']
        
        if not issues:
            return False, "No issues found"
        
        original_content = content
        
        # Add sys import if missing
        if 'missing_sys_import' in issues:
            if 'import json' in content:
                content = content.replace('import json', 'import json\nimport sys')
            else:
                # Add after shebang and docstring
                lines = content.split('\n')
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.startswith('#') and not line.startswith('"""'):
                        insert_pos = i
                        break
                lines.insert(insert_pos, 'import sys')
                content = '\n'.join(lines)
        
        # Fix action: continue patterns
        if 'action_continue_pattern' in issues:
            content = re.sub(
                r'print\(json\.dumps\(\s*\{\s*"action"\s*:\s*"continue"\s*\}\s*\)\)',
                'sys.exit(0)',
                content
            )
        
        # Fix action: block patterns based on hook type
        if 'action_block_pattern' in issues:
            if hook_type == 'pre-tool-use':
                # For PreToolUse, blocking should use exit code 2
                content = re.sub(
                    r'print\(json\.dumps\(\s*\{\s*"action"\s*:\s*"block"\s*,\s*"message"\s*:\s*([^}]+)\s*\}\s*\)\)',
                    r'print(\1, file=sys.stderr)\n        sys.exit(2)',
                    content
                )
            elif hook_type in ['post-tool-use', 'stop']:
                # For PostToolUse and Stop, use decision field
                content = re.sub(
                    r'"action"\s*:\s*"block"',
                    '"decision": "block"',
                    content
                )
        
        # Fix action: warn patterns (convert to non-blocking with exit 0)
        if 'action_warn_pattern' in issues:
            # Extract the message and print to stdout, then exit 0
            content = re.sub(
                r'print\(json\.dumps\(\s*\{\s*"action"\s*:\s*"warn"\s*,\s*"message"\s*:\s*([^,}]+).*?\}\s*\)\)',
                r'print(\1)  # Warning shown in transcript\n        sys.exit(0)',
                content
            )
        
        # Fix action: approve patterns (PreToolUse only)
        if 'action_approve_pattern' in issues and hook_type == 'pre-tool-use':
            content = re.sub(
                r'"action"\s*:\s*"approve"',
                '"decision": "approve"',
                content
            )
        
        # Fix generic action field usage
        content = re.sub(
            r'response\s*=\s*\{\s*"action"\s*:\s*"warn"[^}]*\}',
            'sys.exit(0)  # Continue normally',
            content
        )
        
        # Ensure all paths have proper exit codes at the end of main()
        if 'main()' in content and 'missing_exit_codes' in issues:
            # Add sys.exit(0) at the end of main if not present
            main_match = re.search(r'def main\(\)[^:]*:.*?(?=\ndef|\nif __name__|$)', content, re.DOTALL)
            if main_match:
                main_content = main_match.group(0)
                if not re.search(r'sys\.exit\s*\(\s*\d+\s*\)', main_content):
                    # Add sys.exit(0) before the last line of main
                    content = content.replace(
                        'if __name__ == "__main__":\n    main()',
                        '    sys.exit(0)\n\nif __name__ == "__main__":\n    main()'
                    )
        
        # Save the fixed content
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            return True, "Fixed"
        
        return False, "No changes needed"
    
    def fix_all_hooks(self):
        """Fix all hooks in the hooks directory."""
        print("🔍 Analyzing hooks...")
        
        # Find all Python hook files
        hook_files = list(self.hooks_dir.rglob('*.py'))
        
        for hook_file in hook_files:
            if '.backup' in str(hook_file):
                continue
                
            print(f"\n📄 {hook_file.relative_to(self.hooks_dir)}")
            
            # Analyze the hook
            analysis = self.analyze_hook(hook_file)
            
            if 'error' in analysis:
                print(f"  ❌ Error: {analysis['error']}")
                continue
            
            if not analysis['issues']:
                print("  ✅ Already compliant")
                continue
            
            print(f"  🔧 Issues found: {', '.join(analysis['issues'])}")
            
            # Fix the hook
            success, message = self.fix_hook(analysis)
            
            if success:
                print(f"  ✅ {message}")
                self.fixes_applied.append(str(hook_file))
            else:
                print(f"  ℹ️  {message}")
        
        return len(self.fixes_applied)
    
    def generate_report(self):
        """Generate a report of all fixes applied."""
        report_path = self.hooks_dir / "fix-report.md"
        
        with open(report_path, 'w') as f:
            f.write("# Claude Code Hooks Fix Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Backup location: `{self.backup_dir}`\n\n")
            
            if self.fixes_applied:
                f.write(f"## Fixed {len(self.fixes_applied)} hooks:\n\n")
                for hook in self.fixes_applied:
                    f.write(f"- {hook}\n")
            else:
                f.write("## No fixes were needed\n")
            
            f.write("\n## Next Steps\n\n")
            f.write("1. Test Claude Code: `claude`\n")
            f.write("2. Verify hooks are working\n")
            f.write("3. If issues occur, restore from backup\n")
        
        print(f"\n📋 Report saved to: {report_path}")

def main():
    print("🚀 Claude Code Hooks Fixer")
    print("This will update hooks to match the official documentation format\n")
    
    fixer = HookFixer()
    
    # Create backup
    fixer.backup_hooks()
    
    # Fix all hooks
    fixes_count = fixer.fix_all_hooks()
    
    # Generate report
    fixer.generate_report()
    
    print(f"\n✅ Complete! Fixed {fixes_count} hooks")
    print(f"Backup saved to: {fixer.backup_dir}")
    
    if fixes_count > 0:
        print("\n⚠️  Please test Claude Code to ensure hooks are working correctly")

if __name__ == "__main__":
    main()
