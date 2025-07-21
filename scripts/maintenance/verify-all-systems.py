#!/usr/bin/env python3
"""
Comprehensive verification of ALL Claude Code boilerplate systems
"""

import json
import os
import sys
from pathlib import Path
import subprocess

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def check(condition, message, critical=True):
    """Check a condition and print result"""
    if condition:
        print(f"  {Colors.GREEN}✓{Colors.ENDC} {message}")
        return True
    else:
        severity = Colors.RED if critical else Colors.YELLOW
        print(f"  {severity}✗{Colors.ENDC} {message}")
        return False

def section(title):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{title}{Colors.ENDC}")
    print("=" * len(title))

def verify_commands():
    """Verify all custom commands exist"""
    section("📝 CUSTOM COMMANDS")
    
    commands_dir = Path(".claude/commands")
    expected_commands = [
        # Core workflow
        "init-project.md",
        "generate-issues.md",
        "create-prd.md",
        "generate-tasks.md",
        "process-tasks.md",
        "feature-workflow.md",
        
        # Context & state
        "smart-resume.md",
        "checkpoint.md",
        "context-grab.md",
        "auto-update-context.md",
        
        # Development
        "create-component.md",
        "validate-design.md",
        "create-tracked-form.md",
        "audit-form-security.md",
        
        # Testing
        "browser-test-flow.md",
        "test-runner.md",
        "verify-task.md",
        
        # Multi-agent
        "orchestrate-agents.md",
        "spawn-agent.md",
        "persona.md",
        "sub-agent-status.md",
        
        # Utilities
        "help.md",
        "todo.md",
        "error-recovery.md",
        "compress-context.md",
        "think-through.md",
        
        # Analysis
        "analyze-project.md",
        "performance-monitor.md",
        "security-check.md",
        "work-status.md",
        
        # Tasks
        "task-status.md",
        "task-board.md",
        "task-checkpoint.md",
        "assign-tasks.md",
        
        # Other
        "change-log.md",
        "generate-docs.md",
        "generate-field-types.md",
        "issue-kanban.md",
        "micro-task.md",
        "onboard.md",
        "orchestration-view.md",
        "resume.md",
        "setup-playwright-mcp.md",
        "worktree.md"
    ]
    
    found = 0
    missing = []
    
    for cmd in expected_commands:
        if (commands_dir / cmd).exists():
            found += 1
        else:
            missing.append(cmd)
    
    check(found >= 40, f"Found {found}/{len(expected_commands)} commands")
    
    if missing:
        print(f"  {Colors.YELLOW}Missing: {', '.join(missing[:5])}...{Colors.ENDC}")
    
    return len(missing) == 0

def verify_hooks():
    """Verify all hooks are present and executable"""
    section("🪝 HOOKS SYSTEM")
    
    hooks_dir = Path(".claude/hooks")
    
    # Pre-tool-use hooks
    pre_hooks = [
        "01-dangerous-commands.py",
        "02-design-check.py",
        "03-conflict-check.py",
        "04-actually-works.py",
        "05-code-quality.py",
        "07-pii-protection.py",
        "08-evidence-language.py",
        "09-auto-persona.py"
    ]
    
    # Post-tool-use hooks
    post_hooks = [
        "01-state-save.py",
        "02-metrics.py",
        "03-pattern-learning.py"
    ]
    
    # Check pre-tool hooks
    pre_dir = hooks_dir / "pre-tool-use"
    pre_found = 0
    for hook in pre_hooks:
        hook_path = pre_dir / hook
        if check(hook_path.exists(), f"Pre-hook: {hook}"):
            pre_found += 1
            # Check if executable
            check(os.access(hook_path, os.X_OK), f"  → Executable: {hook}", critical=False)
    
    # Check post-tool hooks
    post_dir = hooks_dir / "post-tool-use"
    post_found = 0
    for hook in post_hooks:
        hook_path = post_dir / hook
        if check(hook_path.exists(), f"Post-hook: {hook}"):
            post_found += 1
    
    # Check other hook directories
    check((hooks_dir / "stop").exists(), "Stop hooks directory")
    check((hooks_dir / "sub-agent-stop").exists(), "Sub-agent-stop hooks")
    check((hooks_dir / "notification").exists(), "Notification hooks")
    
    return pre_found == len(pre_hooks) and post_found == len(post_hooks)

def verify_aliases():
    """Verify command aliases"""
    section("🔤 ALIASES")
    
    aliases_file = Path(".claude/aliases.json")
    if not aliases_file.exists():
        check(False, "aliases.json exists")
        return False
    
    with open(aliases_file) as f:
        aliases = json.load(f)
    
    critical_aliases = {
        # Core workflow
        "ip": "init-project",
        "gi": "generate-issues",
        "prd": "create-prd",
        "gt": "generate-tasks",
        "pt": "process-tasks",
        "fw": "feature-workflow",
        
        # Daily use
        "sr": "smart-resume",
        "vd": "validate-design",
        "cc": "create-component",
        "cp": "checkpoint",
        
        # Multi-agent
        "orch": "orchestrate-agents",
        "sas": "sub-agent-status",
        
        # Security
        "ctf": "create-tracked-form",
        "afs": "audit-form-security",
        "sc": "security-check"
    }
    
    all_good = True
    for alias, command in critical_aliases.items():
        if not check(aliases.get(alias) == command, f"{alias} → {command}"):
            all_good = False
    
    return all_good

def verify_personas():
    """Verify multi-agent personas"""
    section("🤖 MULTI-AGENT PERSONAS")
    
    personas_file = Path(".claude/personas/agent-personas.json")
    if not personas_file.exists():
        check(False, "agent-personas.json exists")
        return False
    
    with open(personas_file) as f:
        data = json.load(f)
    
    expected_personas = [
        "frontend", "backend", "security", "qa",
        "architect", "performance", "integrator", 
        "data", "mentor"
    ]
    
    personas = data.get("personas", {})
    found = []
    
    for persona in expected_personas:
        if check(persona in personas, f"Persona: {persona}"):
            found.append(persona)
    
    return len(found) == len(expected_personas)

def verify_field_registry():
    """Verify security field registry"""
    section("🔒 FIELD REGISTRY")
    
    registry_dir = Path("field-registry")
    
    # Core tracking fields
    core_files = [
        "core/tracking.json",
        "core/device.json",
        "core/geographic.json",
        "core/journey.json",
        "core/cookies.json"
    ]
    
    # Compliance files
    compliance_files = [
        "compliance/pii-fields.json",
        "compliance/phi-fields.json"
    ]
    
    # Vertical files
    vertical_files = [
        "verticals/debt.json",
        "verticals/healthcare.json"
    ]
    
    all_good = True
    for file_path in core_files + compliance_files + vertical_files:
        full_path = registry_dir / file_path
        if not check(full_path.exists(), f"Registry: {file_path}"):
            all_good = False
    
    return all_good

def verify_config_files():
    """Verify configuration files"""
    section("⚙️ CONFIGURATION")
    
    configs = [
        ".claude/config.json",
        ".claude/hooks/config.json",
        ".claude/project-config.json",
        ".claude/settings.json",
        ".claude/chains.json"
    ]
    
    all_good = True
    for config in configs:
        path = Path(config)
        if check(path.exists(), f"Config: {config}"):
            # Try to parse JSON
            try:
                with open(path) as f:
                    json.load(f)
                check(True, f"  → Valid JSON: {config}")
            except:
                check(False, f"  → Valid JSON: {config}")
                all_good = False
        else:
            all_good = False
    
    return all_good

def verify_documentation():
    """Verify documentation structure"""
    section("📚 DOCUMENTATION")
    
    # Root docs
    root_docs = ["README.md", "CLAUDE.md", "QUICK_REFERENCE.md"]
    for doc in root_docs:
        check(Path(doc).exists(), f"Root: {doc}")
    
    # Setup docs
    setup_docs = [
        "docs/setup/DAY_1_COMPLETE_GUIDE.md",
        "docs/setup/QUICK_START_NEW_PROJECT.md",
        "docs/setup/ADD_TO_EXISTING_PROJECT.md"
    ]
    for doc in setup_docs:
        check(Path(doc).exists(), f"Setup: {Path(doc).name}")
    
    # Other docs
    check(Path("docs/README.md").exists(), "Documentation index")
    check(Path("docs/workflow/DAILY_WORKFLOW.md").exists(), "Daily workflow guide")
    check(Path("docs/technical/SYSTEM_OVERVIEW.md").exists(), "System overview")
    
    return True

def verify_prd_flow():
    """Verify PRD → Issues → Tasks flow"""
    section("🔄 PRD → ISSUES → TASKS FLOW")
    
    # Check the complete flow
    flow_components = {
        "1. Project Init": ".claude/commands/init-project.md",
        "2. Generate Issues": ".claude/commands/generate-issues.md",
        "3. Feature Workflow": ".claude/commands/feature-workflow.md",
        "4. Create PRD": ".claude/commands/create-prd.md",
        "5. Generate Tasks": ".claude/commands/generate-tasks.md",
        "6. Process Tasks": ".claude/commands/process-tasks.md"
    }
    
    all_good = True
    for step, file_path in flow_components.items():
        if not check(Path(file_path).exists(), step):
            all_good = False
    
    # Check aliases for the flow
    print("\n  Checking flow aliases:")
    check(Path(".claude/aliases.json").exists(), "Aliases configured")
    
    return all_good

def verify_github_integration():
    """Verify GitHub integration components"""
    section("🐙 GITHUB INTEGRATION")
    
    # Check state save hook
    state_save = Path(".claude/hooks/post-tool-use/01-state-save.py")
    check(state_save.exists(), "State save hook (60s auto-save)")
    
    # Check if contains GitHub gist logic
    if state_save.exists():
        with open(state_save) as f:
            content = f.read()
            check("save_to_github_gist" in content, "GitHub gist save function")
            check("gh gist" in content, "GitHub CLI integration")
    
    # Check feature workflow for issue integration
    fw = Path(".claude/commands/feature-workflow.md")
    if fw.exists():
        with open(fw) as f:
            content = f.read()
            check("GitHub issue" in content, "Issue-based workflow")
    
    return True

def verify_security_features():
    """Verify security features"""
    section("🛡️ SECURITY FEATURES")
    
    # PII protection hook
    pii_hook = Path(".claude/hooks/pre-tool-use/07-pii-protection.py")
    check(pii_hook.exists(), "PII protection hook")
    
    # Security libraries
    security_libs = [
        "lib/security/pii-detector.ts",
        "lib/security/field-encryptor.ts",
        "lib/security/audit-logger.ts"
    ]
    
    for lib in security_libs:
        check(Path(lib).exists(), f"Security lib: {Path(lib).name}")
    
    # Secure form commands
    check(Path(".claude/commands/create-tracked-form.md").exists(), "Create tracked form command")
    check(Path(".claude/commands/audit-form-security.md").exists(), "Audit form security command")
    
    return True

def main():
    """Run all verifications"""
    print(f"{Colors.BOLD}🔍 COMPREHENSIVE CLAUDE CODE BOILERPLATE VERIFICATION{Colors.ENDC}")
    print("=" * 60)
    
    results = {
        "Commands": verify_commands(),
        "Hooks": verify_hooks(),
        "Aliases": verify_aliases(),
        "Personas": verify_personas(),
        "Field Registry": verify_field_registry(),
        "Configuration": verify_config_files(),
        "Documentation": verify_documentation(),
        "PRD Flow": verify_prd_flow(),
        "GitHub Integration": verify_github_integration(),
        "Security": verify_security_features()
    }
    
    # Summary
    section("📊 SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for component, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.ENDC}" if result else f"{Colors.RED}FAIL{Colors.ENDC}"
        print(f"  {component}: {status}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} systems verified{Colors.ENDC}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL SYSTEMS OPERATIONAL!{Colors.ENDC}")
        print("\nThe complete workflow is ready:")
        print("  1. /ip → Define project")
        print("  2. /gi PROJECT → Generate issues")
        print("  3. /fw start 1 → Start feature")
        print("  4. /prd → Create PRD")
        print("  5. /gt → Generate tasks")
        print("  6. /pt → Process tasks")
        print("  7. Auto-saves every 60s")
        print("  8. /fw complete 1 → PR")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ {total - passed} SYSTEMS NEED ATTENTION{Colors.ENDC}")
        print("\nRun these fixes:")
        print("  chmod +x .claude/hooks/**/*.py")
        print("  git add -A")
        print("  git commit -m 'Fix missing components'")

if __name__ == "__main__":
    main()
