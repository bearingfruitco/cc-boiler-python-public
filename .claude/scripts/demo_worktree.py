#!/usr/bin/env python3
"""
Demo script to test worktree functionality
"""

import sys
from pathlib import Path

# Add worktree scripts to path
sys.path.insert(0, str(Path(__file__).parent / "worktree"))

from worktree_manager import WorktreeManager

def demo_worktree():
    """Demo worktree creation and listing"""
    print("🌳 Git Worktree Demo")
    print("=" * 40)
    
    manager = WorktreeManager()
    
    # List current worktrees
    print("\n📋 Current worktrees:")
    worktrees = manager.list_worktrees()
    if not worktrees:
        print("   No worktrees found (this is normal)")
    else:
        for wt in worktrees:
            print(f"   - {wt['name']} ({wt['branch']})")
    
    # Show how to create a worktree
    print("\n💡 To create a worktree in Claude Code:")
    print("   /wt auth-feature payment-feature")
    print("\n   Or with tasks:")
    print("   /wt auth payment --tasks \"Add authentication\" \"Add payment processing\"")
    
    print("\n🚀 Ready to use worktrees!")

if __name__ == "__main__":
    demo_worktree()
