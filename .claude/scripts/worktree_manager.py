#!/usr/bin/env python3
"""
Git Worktree Manager for Claude Code
Provides filesystem isolation for parallel agent execution
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import shutil
import argparse

class WorktreeManager:
    def __init__(self):
        self.project_root = Path.cwd()
        self.worktree_base = self.project_root.parent / "worktrees"
        self.claude_dir = self.project_root / ".claude"
        self.config_file = self.claude_dir / "worktree-config.json"
        
    def create_worktree(self, name: str, task: str = "", base_branch: str = "main") -> dict:
        """Create a new worktree with Claude configuration"""
        
        # Validate name
        if not name or "/" in name:
            return {"error": "Invalid worktree name"}
            
        # Create branch name
        branch = f"feature/{name}"
        worktree_path = self.worktree_base / name
        
        # Check if worktree already exists
        existing = self._list_worktrees()
        if any(wt['branch'] == branch for wt in existing):
            return {"error": f"Worktree with branch {branch} already exists"}
            
        # Create worktree directory
        self.worktree_base.mkdir(parents=True, exist_ok=True)
        
        # Create git worktree
        try:
            cmd = ["git", "worktree", "add", "-b", branch, str(worktree_path), base_branch]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"error": f"Failed to create worktree: {result.stderr}"}
                
        except Exception as e:
            return {"error": f"Git command failed: {str(e)}"}
            
        # Copy Claude configuration
        if self.claude_dir.exists():
            dest_claude = worktree_path / ".claude"
            shutil.copytree(self.claude_dir, dest_claude, dirs_exist_ok=True)
            
            # Create worktree-specific config
            worktree_config = {
                "worktree": {
                    "name": name,
                    "branch": branch,
                    "task": task,
                    "base_branch": base_branch,
                    "created": datetime.now().isoformat(),
                    "path": str(worktree_path)
                }
            }
            
            config_path = dest_claude / "worktree-config.json"
            with open(config_path, 'w') as f:
                json.dump(worktree_config, f, indent=2)
                
            # Create task file if task provided
            if task:
                task_file = dest_claude / "context" / "current-task.md"
                task_file.parent.mkdir(parents=True, exist_ok=True)
                task_file.write_text(f"# Current Task\n\n{task}\n")
                
        return {
            "success": True,
            "worktree": {
                "name": name,
                "path": str(worktree_path),
                "branch": branch,
                "task": task
            }
        }
        
    def list_worktrees(self, detailed: bool = False) -> list:
        """List all active worktrees"""
        worktrees = self._list_worktrees()
        
        if detailed:
            for wt in worktrees:
                # Add Claude config info if available
                config_path = Path(wt['path']) / ".claude" / "worktree-config.json"
                if config_path.exists():
                    with open(config_path) as f:
                        config = json.load(f)
                        wt['task'] = config.get('worktree', {}).get('task', '')
                        wt['created'] = config.get('worktree', {}).get('created', '')
                        
                # Add git status
                wt['status'] = self._get_worktree_status(wt['path'])
                
        return worktrees
        
    def get_status(self, name: str = None) -> dict:
        """Get status of worktree(s)"""
        if name:
            worktrees = [wt for wt in self._list_worktrees() if wt['name'] == name]
        else:
            worktrees = self._list_worktrees()
            
        status_data = []
        
        for wt in worktrees:
            path = Path(wt['path'])
            
            # Get task info
            config_path = path / ".claude" / "worktree-config.json"
            task_info = {}
            if config_path.exists():
                with open(config_path) as f:
                    config = json.load(f)
                    task_info = config.get('worktree', {})
                    
            # Get task ledger progress
            ledger_path = path / ".task-ledger.md"
            progress = self._parse_task_ledger(ledger_path) if ledger_path.exists() else {}
            
            # Get git status
            git_status = self._get_worktree_status(str(path))
            
            status_data.append({
                "name": wt['name'],
                "branch": wt['branch'],
                "path": wt['path'],
                "task": task_info.get('task', ''),
                "created": task_info.get('created', ''),
                "progress": progress,
                "git": git_status
            })
            
        return {"worktrees": status_data}
        
    def remove_worktree(self, name: str, force: bool = False) -> dict:
        """Remove a worktree"""
        worktrees = self._list_worktrees()
        worktree = next((wt for wt in worktrees if wt['name'] == name), None)
        
        if not worktree:
            return {"error": f"Worktree '{name}' not found"}
            
        # Check for uncommitted changes
        if not force:
            status = self._get_worktree_status(worktree['path'])
            if status.get('has_changes'):
                return {"error": "Worktree has uncommitted changes. Use --force to remove anyway"}
                
        # Remove worktree
        try:
            cmd = ["git", "worktree", "remove", worktree['path']]
            if force:
                cmd.append("--force")
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"error": f"Failed to remove worktree: {result.stderr}"}
                
            # Prune worktree refs
            subprocess.run(["git", "worktree", "prune"], capture_output=True)
            
            return {"success": True, "removed": name}
            
        except Exception as e:
            return {"error": f"Failed to remove worktree: {str(e)}"}
            
    def _list_worktrees(self) -> list:
        """Get list of git worktrees"""
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            
            worktrees = []
            current_wt = {}
            
            for line in result.stdout.strip().split('\n'):
                if line.startswith('worktree '):
                    if current_wt:
                        worktrees.append(current_wt)
                    current_wt = {'path': line[9:]}
                elif line.startswith('branch '):
                    current_wt['branch'] = line[7:]
                    # Extract name from branch
                    if current_wt['branch'].startswith('refs/heads/feature/'):
                        current_wt['name'] = current_wt['branch'][19:]
                    else:
                        current_wt['name'] = Path(current_wt['path']).name
                elif line == '':
                    if current_wt:
                        worktrees.append(current_wt)
                        current_wt = {}
                        
            if current_wt:
                worktrees.append(current_wt)
                
            return worktrees
            
        except subprocess.CalledProcessError:
            return []
            
    def _get_worktree_status(self, path: str) -> dict:
        """Get git status for a worktree"""
        try:
            # Change to worktree directory
            original_dir = os.getcwd()
            os.chdir(path)
            
            # Get status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
            )
            
            changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            # Get branch info
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True
            )
            
            current_branch = branch_result.stdout.strip()
            
            # Get commits ahead/behind
            ahead_behind = subprocess.run(
                ["git", "rev-list", "--left-right", "--count", f"origin/main...{current_branch}"],
                capture_output=True,
                text=True
            )
            
            ahead = behind = 0
            if ahead_behind.returncode == 0 and ahead_behind.stdout.strip():
                parts = ahead_behind.stdout.strip().split()
                if len(parts) == 2:
                    behind, ahead = int(parts[0]), int(parts[1])
                    
            os.chdir(original_dir)
            
            return {
                "has_changes": len(changes) > 0,
                "changes_count": len(changes),
                "branch": current_branch,
                "ahead": ahead,
                "behind": behind
            }
            
        except Exception as e:
            os.chdir(original_dir)
            return {"error": str(e)}
            
    def _parse_task_ledger(self, ledger_path: Path) -> dict:
        """Parse task ledger for progress info"""
        try:
            content = ledger_path.read_text()
            
            # Simple parsing - look for X/Y pattern
            import re
            matches = re.findall(r'(\d+)/(\d+)\s+tasks?', content)
            
            if matches:
                completed = sum(int(m[0]) for m in matches)
                total = sum(int(m[1]) for m in matches)
                return {
                    "completed": completed,
                    "total": total,
                    "percentage": int((completed / total) * 100) if total > 0 else 0
                }
                
            return {"completed": 0, "total": 0, "percentage": 0}
            
        except Exception:
            return {"completed": 0, "total": 0, "percentage": 0}


def main():
    parser = argparse.ArgumentParser(description='Git Worktree Manager')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new worktree')
    create_parser.add_argument('name', help='Worktree name')
    create_parser.add_argument('--task', default='', help='Task description')
    create_parser.add_argument('--base', default='main', help='Base branch')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List worktrees')
    list_parser.add_argument('--detailed', action='store_true', help='Show details')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show worktree status')
    status_parser.add_argument('name', nargs='?', help='Worktree name')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a worktree')
    remove_parser.add_argument('name', help='Worktree name')
    remove_parser.add_argument('--force', action='store_true', help='Force removal')
    
    args = parser.parse_args()
    
    manager = WorktreeManager()
    
    if args.command == 'create':
        result = manager.create_worktree(args.name, args.task, args.base)
        print(json.dumps(result, indent=2))
        
    elif args.command == 'list':
        worktrees = manager.list_worktrees(args.detailed)
        print(json.dumps(worktrees, indent=2))
        
    elif args.command == 'status':
        status = manager.get_status(args.name)
        print(json.dumps(status, indent=2))
        
    elif args.command == 'remove':
        result = manager.remove_worktree(args.name, args.force)
        print(json.dumps(result, indent=2))
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
