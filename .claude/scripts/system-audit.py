#!/usr/bin/env python3
"""
Comprehensive system audit to ensure all automations, workflows, and commands are synced.
"""

import json
import os
from pathlib import Path
from collections import defaultdict

class SystemAuditor:
    def __init__(self):
        self.claude_dir = Path(".claude")
        self.issues = []
        self.warnings = []
        self.successes = []
        
    def audit_all(self):
        """Run comprehensive system audit."""
        print("🔍 COMPREHENSIVE SYSTEM AUDIT\n")
        print("=" * 60)
        
        # 1. Audit command definitions vs aliases
        self.audit_commands_and_aliases()
        
        # 2. Audit hook configurations
        self.audit_hook_configurations()
        
        # 3. Audit workflow integrations
        self.audit_workflow_integrations()
        
        # 4. Audit config synchronization
        self.audit_config_sync()
        
        # 5. Generate report
        self.generate_audit_report()
        
    def audit_commands_and_aliases(self):
        """Check that all aliases point to existing commands."""
        print("\n## 1. COMMAND & ALIAS AUDIT\n")
        
        # Load aliases
        aliases_path = self.claude_dir / "aliases.json"
        with open(aliases_path, 'r') as f:
            aliases = json.load(f)
        
        # Get all command files
        commands_dir = self.claude_dir / "commands"
        command_files = set()
        
        for cmd_file in commands_dir.rglob("*.md"):
            if not cmd_file.is_dir():
                command_name = cmd_file.stem
                command_files.add(command_name)
        
        # Check each alias
        missing_commands = []
        valid_aliases = []
        
        for alias, command in aliases.items():
            if command not in command_files:
                missing_commands.append((alias, command))
            else:
                valid_aliases.append((alias, command))
        
        if missing_commands:
            print("❌ Missing Command Definitions:")
            for alias, cmd in sorted(missing_commands):
                print(f"   {alias} -> {cmd} (NOT FOUND)")
                self.issues.append(f"Missing command: {cmd} (alias: {alias})")
        else:
            print("✅ All aliases point to existing commands")
            self.successes.append("All command aliases are valid")
        
        print(f"\n📊 Stats: {len(valid_aliases)} valid aliases, {len(missing_commands)} missing")
        
    def audit_hook_configurations(self):
        """Ensure hook configurations match actual hook implementations."""
        print("\n## 2. HOOK CONFIGURATION AUDIT\n")
        
        # Load settings
        settings_path = self.claude_dir / "settings.json"
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        # Load config.json for hook-specific settings
        config_path = self.claude_dir / "config.json"
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check hook-triggered features
        print("### Hook-Triggered Features:")
        
        # Python dependency tracking
        if config.get("dependencies", {}).get("auto_track"):
            print("✅ Python dependency tracking: ENABLED")
            # Check if dependency tracker hook is active
            dep_hook_active = any(
                "17-python-dependency-tracker.py" in hook["command"][1]
                for hooks in settings["hooks"].values()
                for hook in hooks
            )
            if dep_hook_active:
                print("   ✅ Dependency tracker hook: ACTIVE")
            else:
                print("   ❌ Dependency tracker hook: NOT ACTIVE")
                self.issues.append("Dependency tracking enabled but hook not active")
        
        # Creation guard
        if config.get("creation_guard", {}).get("enabled"):
            print("✅ Python creation guard: ENABLED")
            guard_hook_active = any(
                "16-python-creation-guard.py" in hook["command"][1]
                for hooks in settings["hooks"].values()
                for hook in hooks
            )
            if guard_hook_active:
                print("   ✅ Creation guard hook: ACTIVE")
            else:
                print("   ❌ Creation guard hook: NOT ACTIVE")
                self.issues.append("Creation guard enabled but hook not active")
        
        # Response capture
        if config.get("response_capture", {}).get("enabled"):
            print("✅ Response capture: ENABLED")
            capture_hook_active = any(
                "07-python-response-capture.py" in hook["command"][1]
                for hooks in settings["hooks"].values()
                for hook in hooks
            )
            if capture_hook_active:
                print("   ✅ Response capture hook: ACTIVE")
            else:
                print("   ❌ Response capture hook: NOT ACTIVE")
                self.issues.append("Response capture enabled but hook not active")
        
    def audit_workflow_integrations(self):
        """Check workflow command chains and integrations."""
        print("\n## 3. WORKFLOW INTEGRATION AUDIT\n")
        
        # Check key Python workflows
        workflows = {
            "PRD → Issue → Implementation": [
                ("py-prd", "Create Python PRD"),
                ("capture-to-issue", "Capture AI response to issue"),
                ("py-agent", "Create AI agent"),
                ("py-api", "Create API endpoint"),
                ("python-dependencies", "Check dependencies")
            ],
            "Dependency Management": [
                ("python-dependencies", "Check dependencies"),
                ("python-exists-check", "Check if exists"),
                ("python-import-updater", "Update imports")
            ],
            "PRP Workflow": [
                ("prp-create", "Create PRP"),
                ("prp-execute", "Execute PRP"),
                ("prp-status", "Check status"),
                ("prp-complete", "Complete PRP")
            ],
            "Multi-Agent Orchestration": [
                ("orchestrate-agents", "Orchestrate"),
                ("spawn-agent", "Spawn sub-agent"),
                ("assign-tasks", "Assign tasks"),
                ("sub-agent-status", "Check status")
            ]
        }
        
        # Load command files to check
        commands_dir = self.claude_dir / "commands"
        
        for workflow_name, commands in workflows.items():
            print(f"### {workflow_name}:")
            all_exist = True
            
            for cmd_name, description in commands:
                # Check if command exists
                cmd_path = None
                for cmd_file in commands_dir.rglob("*.md"):
                    if cmd_file.stem == cmd_name:
                        cmd_path = cmd_file
                        break
                
                if cmd_path:
                    print(f"   ✅ {cmd_name}: {description}")
                else:
                    print(f"   ❌ {cmd_name}: MISSING")
                    all_exist = False
                    self.issues.append(f"Missing workflow command: {cmd_name}")
            
            if all_exist:
                self.successes.append(f"Workflow '{workflow_name}' is complete")
            
    def audit_config_sync(self):
        """Ensure all config files are synchronized."""
        print("\n## 4. CONFIGURATION SYNC AUDIT\n")
        
        # Load all config files
        configs = {
            "config.json": self.claude_dir / "config.json",
            "settings.json": self.claude_dir / "settings.json",
            "hooks/config.json": self.claude_dir / "hooks" / "config.json",
            "team/config.json": self.claude_dir / "team" / "config.json",
        }
        
        config_data = {}
        for name, path in configs.items():
            if path.exists():
                with open(path, 'r') as f:
                    config_data[name] = json.load(f)
                print(f"✅ Found: {name}")
            else:
                print(f"❌ Missing: {name}")
                self.warnings.append(f"Config file missing: {name}")
        
        # Check version consistency
        main_version = config_data.get("config.json", {}).get("version")
        print(f"\n### Version Check:")
        print(f"Main version: {main_version}")
        
        # Check hook enablement consistency
        if "hooks/config.json" in config_data:
            hook_config = config_data["hooks/config.json"]
            print("\n### Hook Feature Flags:")
            
            for feature, settings in hook_config.items():
                if isinstance(settings, dict) and "enabled" in settings:
                    status = "✅" if settings["enabled"] else "❌"
                    print(f"   {status} {feature}: {settings.get('enabled')}")
        
        # Check Python-specific settings
        print("\n### Python Configuration:")
        main_config = config_data.get("config.json", {})
        
        python_settings = main_config.get("python", {})
        for key, value in python_settings.items():
            print(f"   {key}: {value}")
        
        # Verify Python tools are configured
        if python_settings.get("linter") == "ruff":
            print("   ✅ Ruff linter configured")
        else:
            self.warnings.append("Ruff linter not configured")
            
        if python_settings.get("formatter") == "black":
            print("   ✅ Black formatter configured")
        else:
            self.warnings.append("Black formatter not configured")
    
    def generate_audit_report(self):
        """Generate comprehensive audit report."""
        report_path = self.claude_dir / "SYSTEM_AUDIT_REPORT.md"
        
        with open(report_path, 'w') as f:
            f.write("# System Audit Report\n\n")
            f.write(f"Generated: {Path.cwd()}\n\n")
            
            # Summary
            f.write("## Summary\n\n")
            f.write(f"- 🟢 Successes: {len(self.successes)}\n")
            f.write(f"- 🟡 Warnings: {len(self.warnings)}\n")
            f.write(f"- 🔴 Issues: {len(self.issues)}\n\n")
            
            # Details
            if self.issues:
                f.write("## 🔴 Issues (Need Fixing)\n\n")
                for issue in self.issues:
                    f.write(f"- {issue}\n")
                f.write("\n")
            
            if self.warnings:
                f.write("## 🟡 Warnings (Should Review)\n\n")
                for warning in self.warnings:
                    f.write(f"- {warning}\n")
                f.write("\n")
            
            if self.successes:
                f.write("## 🟢 Successes\n\n")
                for success in self.successes:
                    f.write(f"- {success}\n")
                f.write("\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            
            if self.issues:
                f.write("### Fix Critical Issues:\n")
                f.write("1. Create missing command files for broken aliases\n")
                f.write("2. Ensure all workflow commands exist\n")
                f.write("3. Sync hook configurations with config settings\n\n")
            
            f.write("### Next Steps:\n")
            f.write("1. Run `/sr` to restore context\n")
            f.write("2. Test key workflows: `/py-prd`, `/cti`, `/pydeps`\n")
            f.write("3. Verify hooks trigger correctly\n")
            f.write("4. Check `.claude/logs/` for activity\n")
        
        print(f"\n📋 Full report saved to: {report_path}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("AUDIT SUMMARY")
        print("=" * 60)
        print(f"🟢 Successes: {len(self.successes)}")
        print(f"🟡 Warnings: {len(self.warnings)}")
        print(f"🔴 Issues: {len(self.issues)}")
        
        if self.issues:
            print("\n⚠️  Critical issues found! See report for details.")
        else:
            print("\n✅ No critical issues found!")

if __name__ == "__main__":
    auditor = SystemAuditor()
    auditor.audit_all()
