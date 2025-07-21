#!/usr/bin/env python3
"""
Validate all Claude Code hooks are properly formatted and functional.
Tests against official documentation requirements.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class HookValidator:
    def __init__(self):
        self.hooks_dir = Path(".claude/hooks")
        self.settings_path = Path(".claude/settings.json")
        self.issues = []
        self.valid_hooks = 0
        self.total_hooks = 0
        
    def load_settings(self):
        """Load hooks configuration from settings.json."""
        with open(self.settings_path, 'r') as f:
            return json.load(f)
    
    def validate_hook_file(self, hook_path):
        """Validate a single hook file."""
        self.total_hooks += 1
        issues = []
        
        try:
            with open(hook_path, 'r') as f:
                content = f.read()
            
            # Check for required imports
            if 'import json' not in content:
                issues.append("Missing 'import json'")
            if 'import sys' not in content:
                issues.append("Missing 'import sys'")
            
            # Check for forbidden patterns
            if '"action"' in content:
                issues.append("Still using outdated 'action' field")
            
            # Check for proper exit codes
            if 'sys.exit' not in content:
                issues.append("Missing sys.exit() calls")
            
            # Check for main function or proper structure
            if 'if __name__' not in content and 'def main' not in content:
                issues.append("No main function or proper entry point")
            
            # Test hook with sample input
            test_input = {
                "session_id": "test-session",
                "transcript_path": "/tmp/test.jsonl",
                "cwd": str(Path.cwd()),
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {"path": "test.py", "content": "print('test')"}
            }
            
            # Run the hook
            result = subprocess.run(
                ["python3", str(hook_path)],
                input=json.dumps(test_input),
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Check exit code
            if result.returncode not in [0, 1, 2]:
                issues.append(f"Invalid exit code: {result.returncode}")
            
            # Check for JSON parsing errors in output
            if result.stdout.strip():
                try:
                    output = json.loads(result.stdout.strip())
                    # Validate output fields based on official docs
                    if "action" in output:
                        issues.append("Output contains forbidden 'action' field")
                except json.JSONDecodeError:
                    # stdout might be plain text for some hooks, which is OK
                    pass
            
            if not issues:
                self.valid_hooks += 1
                return True, "Valid"
            else:
                self.issues.append({
                    "hook": str(hook_path.relative_to(self.hooks_dir)),
                    "issues": issues
                })
                return False, issues
                
        except subprocess.TimeoutExpired:
            issues.append("Hook timed out (>5 seconds)")
            self.issues.append({
                "hook": str(hook_path.relative_to(self.hooks_dir)),
                "issues": issues
            })
            return False, issues
        except Exception as e:
            issues.append(f"Error running hook: {str(e)}")
            self.issues.append({
                "hook": str(hook_path.relative_to(self.hooks_dir)),
                "issues": issues
            })
            return False, issues
    
    def validate_all_hooks(self):
        """Validate all configured hooks."""
        print("🔍 Validating Claude Code hooks...\n")
        
        settings = self.load_settings()
        
        # Check hook event names
        valid_events = ["PreToolUse", "PostToolUse", "Notification", "Stop", "SubagentStop"]
        for event in settings.get("hooks", {}).keys():
            if event not in valid_events:
                self.issues.append({
                    "hook": "settings.json",
                    "issues": [f"Invalid hook event name: {event}"]
                })
        
        # Validate each configured hook
        for event_type, hooks in settings.get("hooks", {}).items():
            print(f"\n📁 {event_type} hooks:")
            
            for hook_config in hooks:
                command = hook_config.get("command", [])
                if len(command) >= 2 and command[0] == "python3":
                    hook_path = Path(command[1])
                    
                    if not hook_path.exists():
                        print(f"  ❌ {hook_path.name} - File not found!")
                        self.issues.append({
                            "hook": str(hook_path),
                            "issues": ["File not found"]
                        })
                        continue
                    
                    valid, result = self.validate_hook_file(hook_path)
                    
                    if valid:
                        print(f"  ✅ {hook_path.name}")
                    else:
                        print(f"  ❌ {hook_path.name}")
                        for issue in result:
                            print(f"     - {issue}")
    
    def generate_report(self):
        """Generate validation report."""
        report_path = self.hooks_dir / "validation-report.md"
        
        with open(report_path, 'w') as f:
            f.write("# Claude Code Hooks Validation Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- Total hooks: {self.total_hooks}\n")
            f.write(f"- Valid hooks: {self.valid_hooks}\n")
            f.write(f"- Issues found: {len(self.issues)}\n\n")
            
            if self.issues:
                f.write("## Issues\n\n")
                for issue in self.issues:
                    f.write(f"### {issue['hook']}\n\n")
                    for problem in issue['issues']:
                        f.write(f"- {problem}\n")
                    f.write("\n")
            else:
                f.write("## ✅ All hooks are valid!\n\n")
            
            f.write("## Official Hook Format Reference\n\n")
            f.write("According to https://docs.anthropic.com/en/docs/claude-code/hooks:\n\n")
            f.write("- Exit code 0: Success\n")
            f.write("- Exit code 2: Blocking error (stderr to Claude)\n")
            f.write("- Other codes: Non-blocking error (stderr to user)\n\n")
            f.write("JSON output fields:\n")
            f.write("- `decision`: 'approve' | 'block' (PreToolUse, PostToolUse, Stop)\n")
            f.write("- `reason`: Explanation string\n")
            f.write("- `continue`: boolean (stop processing)\n")
            f.write("- `stopReason`: Message when continue=false\n")
            f.write("- `suppressOutput`: Hide stdout from transcript\n")
        
        print(f"\n📋 Validation report saved to: {report_path}")

def main():
    validator = HookValidator()
    
    validator.validate_all_hooks()
    validator.generate_report()
    
    print(f"\n{'='*50}")
    print(f"Validation complete: {validator.valid_hooks}/{validator.total_hooks} hooks are valid")
    
    if validator.issues:
        print(f"\n⚠️  {len(validator.issues)} hooks have issues that need attention")
        print("See .claude/hooks/validation-report.md for details")
    else:
        print("\n✅ All hooks are properly formatted!")

if __name__ == "__main__":
    main()
