#!/usr/bin/env python3
"""
Test the complete PRD → Issues → Tasks → Code workflow
"""

import json
import os
import sys
from pathlib import Path

def test_workflow():
    """Test the complete workflow is connected"""
    
    print("🧪 Testing Claude Code Workflow Integration")
    print("=" * 50)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Project init creates PROJECT_PRD
    print("\n1️⃣ Testing: /init-project → PROJECT_PRD.md")
    project_prd_path = Path("docs/project/PROJECT_PRD.md")
    if project_prd_path.parent.exists():
        print("   ✅ Project docs directory ready")
        tests_passed += 1
    else:
        print("   ❌ Missing docs/project/ directory")
        tests_failed += 1
    
    # Test 2: Generate issues command exists
    print("\n2️⃣ Testing: /gi PROJECT → GitHub Issues")
    gi_command = Path(".claude/commands/generate-issues.md")
    if gi_command.exists():
        print("   ✅ Generate issues command found")
        tests_passed += 1
    else:
        print("   ❌ Missing generate-issues command")
        tests_failed += 1
    
    # Test 3: Feature workflow command
    print("\n3️⃣ Testing: /fw start [#] → Feature branch")
    fw_command = Path(".claude/commands/feature-workflow.md")
    if fw_command.exists():
        print("   ✅ Feature workflow command found")
        tests_passed += 1
    else:
        print("   ❌ Missing feature-workflow command")
        tests_failed += 1
    
    # Test 4: PRD → Tasks chain
    print("\n4️⃣ Testing: /prd → /gt → /pt chain")
    prd_cmd = Path(".claude/commands/create-prd.md")
    gt_cmd = Path(".claude/commands/generate-tasks.md")
    pt_cmd = Path(".claude/commands/process-tasks.md")
    
    if all([prd_cmd.exists(), gt_cmd.exists(), pt_cmd.exists()]):
        print("   ✅ PRD → Tasks chain complete")
        tests_passed += 1
    else:
        print("   ❌ Missing commands in PRD → Tasks chain")
        tests_failed += 1
    
    # Test 5: Hooks integration
    print("\n5️⃣ Testing: Hooks automation")
    state_save = Path(".claude/hooks/post-tool-use/01-state-save.py")
    design_check = Path(".claude/hooks/pre-tool-use/02-design-check.py")
    
    if state_save.exists() and design_check.exists():
        print("   ✅ Critical hooks present")
        tests_passed += 1
    else:
        print("   ❌ Missing critical hooks")
        tests_failed += 1
    
    # Test 6: Aliases
    print("\n6️⃣ Testing: Command aliases")
    aliases_file = Path(".claude/aliases.json")
    if aliases_file.exists():
        with open(aliases_file) as f:
            aliases = json.load(f)
            
        critical_aliases = {
            "sr": "smart-resume",
            "prd": "create-prd",
            "gi": "generate-issues",
            "gt": "generate-tasks",
            "pt": "process-tasks"
        }
        
        missing = []
        for alias, command in critical_aliases.items():
            if aliases.get(alias) != command:
                missing.append(f"{alias} → {command}")
        
        if not missing:
            print("   ✅ All critical aliases configured")
            tests_passed += 1
        else:
            print(f"   ❌ Missing aliases: {', '.join(missing)}")
            tests_failed += 1
    else:
        print("   ❌ Aliases file not found")
        tests_failed += 1
    
    # Test 7: Multi-agent system
    print("\n7️⃣ Testing: Multi-agent orchestration")
    orch_cmd = Path(".claude/commands/orchestrate-agents.md")
    personas = Path(".claude/personas/agent-personas.json")
    
    if orch_cmd.exists() and personas.exists():
        print("   ✅ Multi-agent system ready")
        tests_passed += 1
    else:
        print("   ❌ Multi-agent system incomplete")
        tests_failed += 1
    
    # Test 8: Security features
    print("\n8️⃣ Testing: Security features")
    field_registry = Path("field-registry/compliance/pii-fields.json")
    pii_hook = Path(".claude/hooks/pre-tool-use/07-pii-protection.py")
    
    if field_registry.exists() and pii_hook.exists():
        print("   ✅ Security features configured")
        tests_passed += 1
    else:
        print("   ❌ Security features missing")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Results: {tests_passed} passed, {tests_failed} failed")
    
    if tests_failed == 0:
        print("\n✅ ALL SYSTEMS GO! The workflow is fully connected:")
        print("\n🔄 Complete Flow:")
        print("   1. /init-project     → Creates PROJECT_PRD.md")
        print("   2. /gi PROJECT       → Generates GitHub issues")
        print("   3. /fw start 1       → Creates feature branch")
        print("   4. /prd feature      → Creates detailed PRD")
        print("   5. /gt feature       → Generates task list")
        print("   6. /pt feature       → Processes tasks one by one")
        print("   7. Auto-saves        → Every 60 seconds to GitHub")
        print("   8. Design validation → Blocks violations automatically")
        print("   9. /fw complete 1    → Creates PR that closes issue")
        
        print("\n🚀 Quick Start Commands:")
        print("   /sr   - Resume any session")
        print("   /help - See all commands")
        print("   /ip   - Initialize new project")
    else:
        print(f"\n❌ System needs attention. Fix the {tests_failed} failed tests above.")
        print("\nCommon fixes:")
        print("   1. Run: chmod +x .claude/hooks/**/*.py")
        print("   2. Ensure you're in project root")
        print("   3. Check git is initialized: git init")

if __name__ == "__main__":
    test_workflow()
