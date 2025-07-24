#!/usr/bin/env python3
"""
Comprehensive test suite for worktree and multi-perspective review integration
"""

import json
import subprocess
import sys
from pathlib import Path
import os

class IntegrationTester:
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.claude_dir = Path('.claude')
        
    def run_tests(self):
        """Run all integration tests"""
        print("🧪 Running Comprehensive Integration Tests")
        print("=" * 60)
        
        # Test categories
        self.test_file_structure()
        self.test_command_registration()
        self.test_hook_integration()
        self.test_chain_configuration()
        self.test_alias_configuration()
        self.test_git_worktree_support()
        self.test_applescript_integration()
        self.test_next_command_suggestions()
        
        # Print results
        self.print_results()
        
    def test_file_structure(self):
        """Test that all required files exist"""
        print("\n📁 Testing File Structure...")
        
        required_files = [
            # Commands
            "commands/worktree-parallel.md",
            "commands/worktree-status.md",
            "commands/worktree-list.md",
            "commands/review-perspectives.md",
            
            # Scripts
            "scripts/worktree/worktree_manager.py",
            "scripts/worktree/worktree_applescript.py",
            
            # Hooks
            "hooks/pre-tool-use/24-worktree-integration.py",
            
            # Documentation
            "docs/WORKTREE_AND_REVIEW_GUIDE.md"
        ]
        
        for file in required_files:
            path = self.claude_dir / file
            if path.exists():
                self.results['passed'].append(f"✅ File exists: {file}")
            else:
                self.results['failed'].append(f"❌ Missing file: {file}")
                
    def test_command_registration(self):
        """Test that commands are properly registered"""
        print("\n📝 Testing Command Registration...")
        
        commands = [
            "worktree-parallel",
            "worktree-status",
            "worktree-list",
            "review-perspectives"
        ]
        
        for cmd in commands:
            cmd_file = self.claude_dir / f"commands/{cmd}.md"
            if cmd_file.exists():
                content = cmd_file.read_text()
                if f"name: {cmd}" in content:
                    self.results['passed'].append(f"✅ Command registered: {cmd}")
                else:
                    self.results['failed'].append(f"❌ Command misconfigured: {cmd}")
                    
    def test_hook_integration(self):
        """Test hook configuration"""
        print("\n🪝 Testing Hook Integration...")
        
        # Check if hook is executable
        hook_path = self.claude_dir / "hooks/pre-tool-use/24-worktree-integration.py"
        if hook_path.exists():
            # Check shebang
            with open(hook_path) as f:
                first_line = f.readline().strip()
                if first_line == "#!/usr/bin/env python3":
                    self.results['passed'].append("✅ Hook has correct shebang")
                else:
                    self.results['failed'].append("❌ Hook missing proper shebang")
                    
            # Check if it's in ACTIVE_HOOKS.md
            active_hooks = self.claude_dir / "hooks/ACTIVE_HOOKS.md"
            if active_hooks.exists():
                content = active_hooks.read_text()
                if "24-worktree-integration.py" in content:
                    self.results['passed'].append("✅ Hook listed in ACTIVE_HOOKS.md")
                else:
                    self.results['warnings'].append("⚠️  Hook not listed in ACTIVE_HOOKS.md")
                    
    def test_chain_configuration(self):
        """Test chains.json configuration"""
        print("\n⛓️  Testing Chain Configuration...")
        
        chains_file = self.claude_dir / "chains.json"
        if chains_file.exists():
            with open(chains_file) as f:
                chains = json.load(f)
                
            required_chains = [
                "worktree-setup",
                "worktree-execute",
                "worktree-merge",
                "worktree-feature",
                "multi-perspective-review",
                "pr-multi-review"
            ]
            
            for chain in required_chains:
                if chain in chains.get("chains", {}):
                    self.results['passed'].append(f"✅ Chain configured: {chain}")
                else:
                    self.results['failed'].append(f"❌ Chain missing: {chain}")
                    
            # Check shortcuts
            shortcuts = chains.get("shortcuts", {})
            expected_shortcuts = {
                "wts": "worktree-setup",
                "wte": "worktree-execute",
                "wtm": "worktree-merge",
                "mpr": "multi-perspective-review",
                "pmr": "pr-multi-review"
            }
            
            for short, full in expected_shortcuts.items():
                if shortcuts.get(short) == full:
                    self.results['passed'].append(f"✅ Shortcut configured: {short} → {full}")
                else:
                    self.results['failed'].append(f"❌ Shortcut missing: {short}")
                    
    def test_alias_configuration(self):
        """Test aliases.json configuration"""
        print("\n🔤 Testing Alias Configuration...")
        
        aliases_file = self.claude_dir / "aliases.json"
        if aliases_file.exists():
            with open(aliases_file) as f:
                aliases = json.load(f)
                
            expected_aliases = {
                "wt": "worktree-parallel",
                "wts": "worktree-status",
                "wtl": "worktree-list",
                "rp": "review-perspectives",
                "multi-review": "review-perspectives"
            }
            
            for alias, cmd in expected_aliases.items():
                if aliases.get(alias) == cmd:
                    self.results['passed'].append(f"✅ Alias configured: {alias} → {cmd}")
                else:
                    self.results['failed'].append(f"❌ Alias missing: {alias}")
                    
    def test_git_worktree_support(self):
        """Test git worktree functionality"""
        print("\n🌳 Testing Git Worktree Support...")
        
        # Check git version
        try:
            result = subprocess.run(["git", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.results['passed'].append(f"✅ Git available: {version}")
                
                # Check worktree support
                help_result = subprocess.run(["git", "worktree", "--help"],
                                           capture_output=True, text=True)
                if help_result.returncode == 0:
                    self.results['passed'].append("✅ Git worktree command available")
                else:
                    self.results['failed'].append("❌ Git worktree not supported")
            else:
                self.results['failed'].append("❌ Git not available")
        except Exception as e:
            self.results['failed'].append(f"❌ Git test failed: {e}")
            
    def test_applescript_integration(self):
        """Test AppleScript integration (macOS only)"""
        print("\n🍎 Testing AppleScript Integration...")
        
        # Check if we're on macOS
        import platform
        if platform.system() != "Darwin":
            self.results['warnings'].append("⚠️  AppleScript only available on macOS")
            return
            
        # Test osascript availability
        try:
            result = subprocess.run(["osascript", "-e", "return \"test\""],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.results['passed'].append("✅ AppleScript (osascript) available")
            else:
                self.results['failed'].append("❌ AppleScript not working")
        except:
            self.results['failed'].append("❌ osascript command not found")
            
    def test_next_command_suggestions(self):
        """Test next command suggester integration"""
        print("\n💡 Testing Next Command Suggestions...")
        
        suggester_path = self.claude_dir / "hooks/post-tool-use/16-next-command-suggester.py"
        if suggester_path.exists():
            content = suggester_path.read_text()
            
            # Check for worktree commands
            worktree_commands = [
                "worktree-parallel",
                "worktree-status",
                "worktree-list",
                "worktree-review",
                "worktree-merge"
            ]
            
            for cmd in worktree_commands:
                if f"'{cmd}':" in content:
                    self.results['passed'].append(f"✅ Suggestion configured: {cmd}")
                else:
                    self.results['warnings'].append(f"⚠️  No suggestions for: {cmd}")
                    
            # Check for multi-perspective review
            if "'multi-perspective-review':" in content:
                self.results['passed'].append("✅ Multi-perspective review suggestions configured")
            else:
                self.results['warnings'].append("⚠️  No multi-perspective review suggestions")
                
    def print_results(self):
        """Print test results"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        
        # Passed tests
        if self.results['passed']:
            print(f"\n✅ Passed: {len(self.results['passed'])}")
            for test in self.results['passed']:
                print(f"   {test}")
                
        # Warnings
        if self.results['warnings']:
            print(f"\n⚠️  Warnings: {len(self.results['warnings'])}")
            for warning in self.results['warnings']:
                print(f"   {warning}")
                
        # Failed tests
        if self.results['failed']:
            print(f"\n❌ Failed: {len(self.results['failed'])}")
            for test in self.results['failed']:
                print(f"   {test}")
                
        # Summary
        total = len(self.results['passed']) + len(self.results['failed'])
        pass_rate = (len(self.results['passed']) / total * 100) if total > 0 else 0
        
        print(f"\n📈 Pass Rate: {pass_rate:.1f}% ({len(self.results['passed'])}/{total})")
        
        if not self.results['failed']:
            print("\n🎉 All tests passed! Worktree and Multi-Perspective Review integration is ready!")
        else:
            print("\n⚠️  Some tests failed. Please review and fix the issues above.")
            
        # Next steps
        print("\n🚀 Next Steps:")
        print("1. Try: /wt feature-1 feature-2")
        print("2. Monitor: /wt-status --monitor")
        print("3. Review: /chain mpr")
        print("4. Merge: /wt-merge feature-1")
        
        print("\n📚 Full guide: .claude/docs/WORKTREE_AND_REVIEW_GUIDE.md")

if __name__ == "__main__":
    tester = IntegrationTester()
    tester.run_tests()
