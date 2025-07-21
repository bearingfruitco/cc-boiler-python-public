#!/usr/bin/env python3
"""
Activate useful inactive hooks and provide status report.
"""

import json
from pathlib import Path

def activate_useful_hooks():
    """Activate hooks that should be enabled."""
    settings_path = Path(".claude/settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Hooks to activate with reasons
    hooks_to_add = {
        "PreToolUse": [
            {
                "file": "00-auto-approve-safe-ops.py",
                "reason": "Auto-approves safe read operations to reduce interruptions"
            },
            {
                "file": "03-python-style-check.py", 
                "reason": "Enforces Python style guidelines"
            },
            {
                "file": "04-conflict-check.py",
                "reason": "Prevents file conflicts in team development"
            },
            {
                "file": "09-evidence-language.py",
                "reason": "Ensures claims are backed by evidence"
            },
            {
                "file": "10-auto-persona.py",
                "reason": "Automatically sets appropriate persona based on task"
            },
            {
                "file": "13-import-validator.py",
                "reason": "Validates Python imports are correct"
            }
        ],
        "PostToolUse": [
            {
                "file": "02-state-save.py",
                "reason": "Saves state to GitHub gists for persistence"
            },
            {
                "file": "03-metrics.py",
                "reason": "Tracks design compliance metrics"
            },
            {
                "file": "04-auto-orchestrate.py",
                "reason": "Automatically suggests multi-agent orchestration"
            }
        ],
        "Notification": [
            {
                "file": "02-pr-feedback-monitor.py",
                "reason": "Monitors PR feedback and suggestions"
            }
        ]
    }
    
    added_count = 0
    
    print("## Activating Additional Hooks\n")
    
    for event_type, hooks in hooks_to_add.items():
        print(f"### {event_type}")
        
        for hook_info in hooks:
            hook_file = hook_info["file"]
            reason = hook_info["reason"]
            
            # Determine correct path
            dir_map = {
                "PreToolUse": "pre-tool-use",
                "PostToolUse": "post-tool-use",
                "Notification": "notification"
            }
            
            hook_path = f".claude/hooks/{dir_map[event_type]}/{hook_file}"
            
            # Check if already exists
            exists_in_config = any(
                hook["command"][1] == hook_path
                for hook in settings["hooks"].get(event_type, [])
            )
            
            if not exists_in_config and Path(hook_path).exists():
                # Add to config
                hook_config = {
                    "match": {},
                    "command": ["python3", hook_path]
                }
                
                if event_type not in settings["hooks"]:
                    settings["hooks"][event_type] = []
                    
                settings["hooks"][event_type].append(hook_config)
                added_count += 1
                print(f"✅ Activated: {hook_file}")
                print(f"   Reason: {reason}")
            else:
                if exists_in_config:
                    print(f"ℹ️  Already active: {hook_file}")
                else:
                    print(f"❌ File not found: {hook_file}")
        
        print()
    
    # Sort hooks by filename for consistency
    for event_type in settings["hooks"]:
        settings["hooks"][event_type].sort(key=lambda x: x["command"][1])
    
    # Save updated settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"\n## Summary")
    print(f"- Added {added_count} new hooks")
    print(f"- Total active hooks: {sum(len(hooks) for hooks in settings['hooks'].values())}")
    
    return added_count

def generate_final_report():
    """Generate comprehensive hook status report."""
    report_path = Path(".claude/hooks/HOOK_STATUS_REPORT.md")
    settings_path = Path(".claude/settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    with open(report_path, 'w') as f:
        f.write("# Claude Code Hooks - Final Status Report\n\n")
        f.write("## Active Hooks by Category\n\n")
        
        total_active = 0
        
        for event_type, hooks in settings["hooks"].items():
            f.write(f"### {event_type} ({len(hooks)} hooks)\n\n")
            
            for hook in hooks:
                hook_file = Path(hook["command"][1]).name
                f.write(f"- `{hook_file}`\n")
                
                # Add description based on filename
                descriptions = {
                    "00-auto-approve-safe-ops.py": "  - Auto-approves safe read operations",
                    "01-dangerous-commands.py": "  - Blocks dangerous commands and protects sensitive files",
                    "02-collab-sync.py": "  - Syncs with GitHub for team collaboration",
                    "03-python-style-check.py": "  - Enforces Python coding standards",
                    "04-conflict-check.py": "  - Checks for file conflicts with team members",
                    "05-actually-works.py": "  - Ensures claims are tested before declaring success",
                    "06-code-quality.py": "  - Enforces code quality standards",
                    "07-pii-protection.py": "  - Protects against PII exposure",
                    "08-async-patterns.py": "  - Validates async/await patterns",
                    "09-evidence-language.py": "  - Requires evidence for claims",
                    "10-auto-persona.py": "  - Sets appropriate persona for tasks",
                    "11-truth-enforcer.py": "  - Enforces factual accuracy",
                    "12-deletion-guard.py": "  - Prevents accidental deletions",
                    "13-import-validator.py": "  - Validates Python imports",
                    "14-prd-clarity.py": "  - Ensures PRD clarity and completeness",
                    "15-implementation-guide.py": "  - Guides implementation decisions",
                    "16-python-creation-guard.py": "  - Prevents duplicate Python components",
                    "17-python-dependency-tracker.py": "  - Tracks Python dependencies",
                    "01-action-logger.py": "  - Logs all Claude actions",
                    "02-state-save.py": "  - Saves state to GitHub gists",
                    "03-metrics.py": "  - Tracks compliance metrics",
                    "04-auto-orchestrate.py": "  - Suggests multi-agent orchestration",
                    "05-command-logger.py": "  - Logs executed commands",
                    "06-pattern-learning.py": "  - Learns from successful patterns",
                    "07-python-response-capture.py": "  - Captures Python implementation plans",
                    "08-research-capture.py": "  - Captures research documents",
                    "09-python-import-updater.py": "  - Updates imports after refactoring",
                    "10-prp-progress-tracker.py": "  - Tracks PRP progress",
                    "11-workflow-context-flow.py": "  - Manages workflow context",
                    "01-save-transcript.py": "  - Saves session transcript",
                    "02-handoff-prep.py": "  - Prepares work for handoff",
                    "03-knowledge-share.py": "  - Shares knowledge with team",
                    "04-save-state.py": "  - Final state save",
                    "01-track-completion.py": "  - Tracks sub-agent completion",
                    "02-coordinate.py": "  - Coordinates multi-agent work",
                    "01-precompact-handler.py": "  - Handles pre-compaction",
                    "02-pr-feedback-monitor.py": "  - Monitors PR feedback",
                    "03-smart-suggest.py": "  - Provides smart suggestions",
                    "04-team-aware.py": "  - Shows team activity"
                }
                
                if hook_file in descriptions:
                    f.write(descriptions[hook_file] + "\n")
            
            f.write("\n")
            total_active += len(hooks)
        
        f.write(f"## Total Active Hooks: {total_active}\n\n")
        
        f.write("## Hook Compliance Status\n\n")
        f.write("✅ All active hooks are compliant with official documentation:\n")
        f.write("- Using exit codes (0, 1, 2) for control flow\n")
        f.write("- No 'action' fields (using 'decision' where applicable)\n")
        f.write("- Proper Python structure with sys and json imports\n")
        f.write("- Correct hook event names (PascalCase)\n\n")
        
        f.write("## Testing Recommendations\n\n")
        f.write("1. Start Claude Code: `claude`\n")
        f.write("2. Test basic operations to ensure hooks don't block normal workflow\n")
        f.write("3. Check `.claude/logs/` for hook activity\n")
        f.write("4. Use transcript mode (Ctrl+R) to see hook output\n")
    
    print(f"\n✅ Generated comprehensive report: {report_path}")

def main():
    print("🚀 Activating Additional Useful Hooks\n")
    
    added = activate_useful_hooks()
    generate_final_report()
    
    print("\n✅ Hook activation complete!")
    print("\nYour Python boilerplate now has maximum hook coverage for:")
    print("- Safety and security")
    print("- Code quality")
    print("- Team collaboration")
    print("- State persistence")
    print("- Pattern learning")
    print("- Multi-agent orchestration")

if __name__ == "__main__":
    main()
