#!/usr/bin/env python3
"""
Test script for worktree integration
"""

import sys
import json
from pathlib import Path

# Add the worktree scripts to path
sys.path.insert(0, str(Path(__file__).parent / "worktree"))

from worktree_manager import WorktreeManager

def test_worktree_integration():
    """Test basic worktree functionality"""
    
    print("🧪 Testing Worktree Integration")
    print("=" * 40)
    
    manager = WorktreeManager()
    
    # Test 1: List existing worktrees
    print("\n1️⃣ Listing existing worktrees:")
    worktrees = manager.list_worktrees()
    print(f"   Found {len(worktrees)} worktrees")
    for wt in worktrees:
        print(f"   - {wt.get('name', 'main')} ({wt.get('branch', 'N/A')})")
    
    # Test 2: Check if we can read git status
    print("\n2️⃣ Checking git integration:")
    try:
        import subprocess
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Git commands work")
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            print(f"   📝 Current directory has {changes} uncommitted changes")
        else:
            print("   ❌ Git command failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check Claude configuration
    print("\n3️⃣ Checking Claude configuration:")
    claude_dir = Path(".claude")
    if claude_dir.exists():
        print("   ✅ .claude directory exists")
        
        # Check for key files
        key_files = [
            "commands/worktree-parallel.md",
            "commands/worktree-status.md", 
            "commands/worktree-list.md",
            "commands/review-perspectives.md",
            "scripts/worktree/worktree_manager.py",
            "scripts/worktree/worktree_applescript.py",
            "hooks/pre-tool-use/24-worktree-integration.py"
        ]
        
        for file in key_files:
            if (claude_dir / file).exists():
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ Missing: {file}")
    else:
        print("   ❌ .claude directory not found")
    
    # Test 4: Check chains.json for worktree chains
    print("\n4️⃣ Checking chains.json integration:")
    chains_file = claude_dir / "chains.json"
    if chains_file.exists():
        with open(chains_file) as f:
            chains = json.load(f)
        
        worktree_chains = [
            "worktree-setup",
            "worktree-execute", 
            "worktree-merge",
            "multi-perspective-review"
        ]
        
        for chain in worktree_chains:
            if chain in chains.get("chains", {}):
                print(f"   ✅ Chain '{chain}' configured")
            else:
                print(f"   ❌ Chain '{chain}' missing")
    
    print("\n✨ Integration test complete!")
    print("\nNext steps:")
    print("1. Try: /worktree-parallel test-feature")
    print("2. Monitor with: /wt-status")
    print("3. Review with: /chain multi-perspective-review")

if __name__ == "__main__":
    test_worktree_integration()
