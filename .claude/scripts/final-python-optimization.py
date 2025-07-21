#!/usr/bin/env python3
"""
Final optimization for Python development - ensure all Python-specific hooks are active.
"""

import json
from pathlib import Path

def final_python_optimization():
    """Ensure we have all the right hooks for Python development."""
    settings_path = Path(".claude/settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    print("## Python Boilerplate Hook Configuration\n")
    
    # Count current hooks
    current_total = sum(len(hooks) for hooks in settings["hooks"].values())
    print(f"Current active hooks: {current_total}\n")
    
    # Essential Python development hooks
    essential_categories = {
        "PreToolUse": {
            "Safety & Security": [
                "01-dangerous-commands.py",
                "07-pii-protection.py",
                "12-deletion-guard.py"
            ],
            "Python Quality": [
                "03-python-style-check.py",
                "13-import-validator.py",
                "16-python-creation-guard.py",
                "17-python-dependency-tracker.py"
            ],
            "Development Process": [
                "00-auto-approve-safe-ops.py",
                "04-conflict-check.py",
                "05-actually-works.py",
                "09-evidence-language.py",
                "14-prd-clarity.py",
                "15-implementation-guide.py"
            ],
            "Context & Behavior": [
                "10-auto-persona.py",
                "11-truth-enforcer.py"
            ]
        },
        "PostToolUse": {
            "Logging & Tracking": [
                "01-action-logger.py",
                "05-command-logger.py"
            ],
            "State & Context": [
                "02-state-save.py",
                "11-workflow-context-flow.py"
            ],
            "Python Intelligence": [
                "06-pattern-learning.py",
                "07-python-response-capture.py",
                "08-research-capture.py",
                "09-python-import-updater.py"
            ],
            "PRD & Orchestration": [
                "04-auto-orchestrate.py",
                "10-prp-progress-tracker.py"
            ]
        },
        "Stop": {
            "Session Management": [
                "01-save-transcript.py",
                "02-handoff-prep.py",
                "03-knowledge-share.py",
                "04-save-state.py"
            ]
        },
        "SubagentStop": {
            "Multi-Agent": [
                "01-track-completion.py",
                "02-coordinate.py"
            ]
        },
        "Notification": {
            "User Experience": [
                "01-precompact-handler.py",
                "02-pr-feedback-monitor.py",
                "03-smart-suggest.py",
                "04-team-aware.py"
            ]
        }
    }
    
    # Display organized hook structure
    for event_type, categories in essential_categories.items():
        active_count = len(settings["hooks"].get(event_type, []))
        print(f"### {event_type} ({active_count} active)\n")
        
        for category, hook_files in categories.items():
            print(f"**{category}:**")
            for hook_file in hook_files:
                # Check if hook is active
                hook_path = None
                if event_type == "PreToolUse":
                    hook_path = f".claude/hooks/pre-tool-use/{hook_file}"
                elif event_type == "PostToolUse":
                    hook_path = f".claude/hooks/post-tool-use/{hook_file}"
                elif event_type == "Stop":
                    hook_path = f".claude/hooks/stop/{hook_file}"
                elif event_type == "SubagentStop":
                    hook_path = f".claude/hooks/sub-agent-stop/{hook_file}"
                elif event_type == "Notification":
                    hook_path = f".claude/hooks/notification/{hook_file}"
                
                is_active = any(
                    hook["command"][1] == hook_path
                    for hook in settings["hooks"].get(event_type, [])
                )
                
                status = "✅" if is_active else "❌"
                print(f"  {status} {hook_file}")
            print()
    
    print("\n## Summary for Python Development\n")
    print(f"Total active hooks: {current_total}")
    print("\nThis configuration provides:")
    print("- 🛡️ Security: Dangerous command blocking, PII protection")
    print("- 🐍 Python Quality: Style checking, import validation, duplicate prevention")
    print("- 📋 PRD/PRP: Clear requirements, progress tracking")
    print("- 🤖 Intelligence: Pattern learning, response capture, dependency tracking")
    print("- 💾 Persistence: State saving, transcript logging")
    print("- 👥 Collaboration: Conflict detection, team awareness")
    print("- 🔄 Multi-Agent: Orchestration suggestions, sub-agent coordination")
    
    # Generate Python-specific documentation
    generate_python_docs()

def generate_python_docs():
    """Generate Python-specific hook documentation."""
    doc_path = Path(".claude/hooks/PYTHON_HOOKS_GUIDE.md")
    
    with open(doc_path, 'w') as f:
        f.write("# Python Development Hooks Guide\n\n")
        f.write("This guide explains how the hooks work specifically for Python development.\n\n")
        
        f.write("## Key Python-Specific Hooks\n\n")
        
        f.write("### 1. Python Creation Guard (`16-python-creation-guard.py`)\n")
        f.write("- Prevents creating duplicate classes, functions, or Pydantic models\n")
        f.write("- Checks all Python files before allowing new components\n")
        f.write("- Suggests imports instead of recreating existing code\n\n")
        
        f.write("### 2. Python Dependency Tracker (`17-python-dependency-tracker.py`)\n")
        f.write("- Tracks module dependencies using `@imports-from` annotations\n")
        f.write("- Alerts about breaking changes\n")
        f.write("- Updates import statements after refactoring\n\n")
        
        f.write("### 3. Python Response Capture (`07-python-response-capture.py`)\n")
        f.write("- Captures AI implementation plans\n")
        f.write("- Extracts Python components from responses\n")
        f.write("- Enables `/cti` (capture-to-issue) workflow\n\n")
        
        f.write("### 4. Import Validator (`13-import-validator.py`)\n")
        f.write("- Validates Python import statements\n")
        f.write("- Checks for circular imports\n")
        f.write("- Ensures imports follow project structure\n\n")
        
        f.write("### 5. Python Style Check (`03-python-style-check.py`)\n")
        f.write("- Enforces PEP 8 compliance\n")
        f.write("- Checks type hints usage\n")
        f.write("- Validates docstring format\n\n")
        
        f.write("## Workflow Integration\n\n")
        f.write("1. **PRD Creation**: Use `/py-prd` to create Python-specific PRDs\n")
        f.write("2. **Issue Creation**: Use `/cti` to capture implementation plans\n")
        f.write("3. **Dependency Check**: Use `/pydeps` before refactoring\n")
        f.write("4. **Pattern Learning**: Successful implementations are captured\n")
        f.write("5. **Multi-Agent**: Use `/orch` for complex Python projects\n\n")
        
        f.write("## Disabled Frontend Hooks\n\n")
        f.write("The following hooks were disabled as they're specific to frontend development:\n")
        f.write("- `02-collab-sync.py` (checks for JS/TS files)\n")
        f.write("- `08-async-patterns.py` (validates JS async/await)\n")
        f.write("- `03-metrics.py` (tracks design system compliance)\n")
        f.write("- `06-code-quality.py` (checks for console.log, etc.)\n")
    
    print(f"\n✅ Generated Python hooks guide: {doc_path}")

if __name__ == "__main__":
    final_python_optimization()
