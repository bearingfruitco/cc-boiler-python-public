#!/usr/bin/env python3
"""
Optimize hooks for Python-only development by disabling frontend-specific hooks.
"""

import json
from pathlib import Path

def analyze_and_optimize_hooks():
    """Identify and disable frontend/JS-specific hooks."""
    settings_path = Path(".claude/settings.json")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Hooks that are frontend/JS specific and should be disabled for Python projects
    frontend_hooks_to_remove = [
        # PreToolUse hooks
        "02-collab-sync.py",  # This might reference design system checks
        "08-async-patterns.py",  # This checks JS/TS async patterns, not Python
        
        # PostToolUse hooks
        "03-metrics.py",  # If it tracks design compliance metrics
    ]
    
    # Let me check what these hooks actually do
    hooks_to_analyze = {
        "02-collab-sync.py": ".claude/hooks/pre-tool-use/02-collab-sync.py",
        "08-async-patterns.py": ".claude/hooks/pre-tool-use/08-async-patterns.py",
        "03-metrics.py": ".claude/hooks/post-tool-use/03-metrics.py",
        "06-code-quality.py": ".claude/hooks/pre-tool-use/06-code-quality.py",
    }
    
    print("## Analyzing Hooks for Python-Only Development\n")
    
    frontend_specific_hooks = []
    
    for hook_name, hook_path in hooks_to_analyze.items():
        if Path(hook_path).exists():
            with open(hook_path, 'r') as f:
                content = f.read()
            
            # Check for frontend-specific patterns
            is_frontend = False
            reasons = []
            
            if any(x in content for x in ['.tsx', '.jsx', '.ts', '.js', 'tailwind', 'design system', 'font-size', 'text-size']):
                is_frontend = True
                reasons.append("Checks TypeScript/JavaScript files")
                
            if 'biome' in content.lower() or 'prettier' in content.lower():
                is_frontend = True
                reasons.append("Uses JS/TS formatters")
                
            if any(x in content for x in ['css', 'style', 'className', 'design token']):
                is_frontend = True
                reasons.append("Enforces CSS/design patterns")
                
            if 'async/await' in content and ('.ts' in content or '.js' in content):
                is_frontend = True
                reasons.append("Checks JS/TS async patterns")
            
            print(f"### {hook_name}")
            if is_frontend:
                print(f"❌ Frontend-specific: {', '.join(reasons)}")
                frontend_specific_hooks.append(hook_path)
            else:
                print(f"✅ Python-compatible")
            print()
    
    # Now remove frontend-specific hooks from settings
    removed_count = 0
    
    for event_type, hooks in settings["hooks"].items():
        original_count = len(hooks)
        settings["hooks"][event_type] = [
            hook for hook in hooks
            if not any(fe_hook in hook["command"][1] for fe_hook in frontend_specific_hooks)
        ]
        removed_count += original_count - len(settings["hooks"][event_type])
    
    # Save updated settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"\n## Summary")
    print(f"- Removed {removed_count} frontend-specific hooks")
    print(f"- Remaining active hooks: {sum(len(hooks) for hooks in settings['hooks'].values())}")
    
    # List remaining Python-focused hooks
    print("\n## Python-Focused Hooks Remaining:\n")
    
    python_hook_categories = {
        "PreToolUse": [
            "00-auto-approve-safe-ops.py - Auto-approves safe operations",
            "01-dangerous-commands.py - Security and safety",
            "03-python-style-check.py - Python code style",
            "04-conflict-check.py - Git conflict prevention", 
            "05-actually-works.py - Test verification",
            "07-pii-protection.py - Data protection",
            "09-evidence-language.py - Evidence-based claims",
            "10-auto-persona.py - Task-based personas",
            "11-truth-enforcer.py - Factual accuracy",
            "12-deletion-guard.py - Deletion protection",
            "13-import-validator.py - Python import validation",
            "14-prd-clarity.py - PRD quality",
            "15-implementation-guide.py - Implementation patterns",
            "16-python-creation-guard.py - Prevent duplicates",
            "17-python-dependency-tracker.py - Track dependencies"
        ],
        "PostToolUse": [
            "01-action-logger.py - Action logging",
            "02-state-save.py - State persistence",
            "04-auto-orchestrate.py - Multi-agent suggestions",
            "05-command-logger.py - Command logging",
            "06-pattern-learning.py - Pattern extraction",
            "07-python-response-capture.py - Capture Python plans",
            "08-research-capture.py - Research documents",
            "09-python-import-updater.py - Import updates",
            "10-prp-progress-tracker.py - PRP tracking",
            "11-workflow-context-flow.py - Workflow context"
        ]
    }
    
    for category, descriptions in python_hook_categories.items():
        print(f"### {category}")
        for desc in descriptions:
            print(f"- {desc}")
        print()

if __name__ == "__main__":
    analyze_and_optimize_hooks()
