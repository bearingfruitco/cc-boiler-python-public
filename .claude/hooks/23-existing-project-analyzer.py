#!/usr/bin/env python3
"""
Existing Project Integration Hook
Handles special logic when dropping into an existing codebase
"""

import json
import sys
import os
from pathlib import Path
import subprocess

def detect_project_type():
    """Detect the type of Python project"""
    project_type = "generic"
    frameworks = []
    
    # Check for various Python frameworks
    if Path("manage.py").exists():
        project_type = "django"
        frameworks.append("Django")
    
    # Check imports in Python files
    py_files = list(Path(".").glob("**/*.py"))[:20]  # Sample first 20 files
    
    for py_file in py_files:
        try:
            content = py_file.read_text()
            if "from fastapi import" in content or "FastAPI()" in content:
                project_type = "fastapi"
                frameworks.append("FastAPI")
            if "from flask import" in content or "Flask(__name__)" in content:
                project_type = "flask" 
                frameworks.append("Flask")
            if "@flow" in content and "from prefect import" in content:
                frameworks.append("Prefect")
            if "import pandas" in content:
                frameworks.append("Pandas")
        except:
            continue
    
    return project_type, frameworks

def check_existing_setup():
    """Check if project already has some Claude setup"""
    existing = {
        "has_claude_dir": Path(".claude").exists(),
        "has_task_ledger": Path(".task-ledger.md").exists(),
        "has_claude_md": Path("CLAUDE.md").exists() or Path(".claude/CLAUDE.md").exists(),
        "has_hooks": Path(".claude/hooks").exists(),
        "has_commands": Path(".claude/commands").exists()
    }
    
    existing["partial_setup"] = any(existing.values())
    existing["full_setup"] = all(existing.values())
    
    return existing

def suggest_integration_approach(project_type, frameworks, existing_setup):
    """Suggest best integration approach"""
    suggestions = []
    
    if existing_setup["full_setup"]:
        suggestions.append("Project already fully integrated. Run /sr to resume.")
        return suggestions
    
    if existing_setup["partial_setup"]:
        suggestions.append("⚠️ Partial Claude setup detected. Recommending careful merge.")
        if not existing_setup["has_hooks"]:
            suggestions.append("- Missing hooks: Will install all 35 Python hooks")
        if not existing_setup["has_task_ledger"]:
            suggestions.append("- Missing task ledger: Will extract from TODOs and issues")
    
    # Framework-specific suggestions
    if project_type == "fastapi":
        suggestions.append("🚀 FastAPI project detected:")
        suggestions.append("- Will set up API endpoint tracking")
        suggestions.append("- Configure py-api command for FastAPI patterns")
        suggestions.append("- Enable async pattern validation")
    
    elif project_type == "django":
        suggestions.append("🎯 Django project detected:")
        suggestions.append("- Will adapt commands for Django structure")
        suggestions.append("- Set up model and view tracking")
        suggestions.append("- Configure for Django test runner")
    
    if "Prefect" in frameworks:
        suggestions.append("📊 Prefect flows detected:")
        suggestions.append("- Will enable py-pipeline command")
        suggestions.append("- Set up flow tracking in task ledger")
    
    if "Pandas" in frameworks:
        suggestions.append("📈 Data analysis code detected:")
        suggestions.append("- Will configure for Jupyter notebook support")
        suggestions.append("- Enable data pipeline patterns")
    
    return suggestions

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only activate on analyze-existing command
    if input_data.get('name') != 'run_command':
        json.dump({"action": "allow"}, sys.stdout)
        sys.exit(0)
        return
    
    command = input_data.get('parameters', {}).get('command', '')
    if 'analyze-existing' not in command:
        json.dump({"action": "allow"}, sys.stdout)
        sys.exit(0)
        return
    
    # Detect project characteristics
    project_type, frameworks = detect_project_type()
    existing_setup = check_existing_setup()
    
    # Generate suggestions
    suggestions = suggest_integration_approach(project_type, frameworks, existing_setup)
    
    # Create pre-tool-use hook response
    message = f"🔍 Project Analysis: {project_type} project with {', '.join(frameworks) if frameworks else 'standard Python'}"
    
    suggestions_text = "\n".join(suggestions)
    if len(frameworks) > 2:
        suggestions_text += "\n\nRecommended chains:\n"
        suggestions_text += "- /chain eps - Complete setup for existing project\n"
        suggestions_text += "- /chain epe - Enhance with AI capabilities"
    
    response = {
        "action": "allow",
        "message": message,
        "details": suggestions_text
    }
    
    json.dump(response, sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()
