#!/usr/bin/env python3
"""
AppleScript integration for Git Worktrees
Opens worktrees in new Terminal windows/tabs and monitors progress
"""

import subprocess
import json
import sys
from pathlib import Path

class WorktreeAppleScript:
    def __init__(self):
        self.project_root = Path.cwd()
        self.worktree_base = self.project_root.parent / "worktrees"
        
    def open_worktree_terminal(self, worktree_name: str, new_window: bool = True) -> bool:
        """Open a worktree in a new Terminal window/tab"""
        worktree_path = self.worktree_base / worktree_name
        
        if not worktree_path.exists():
            print(f"Worktree path not found: {worktree_path}")
            return False
            
        # AppleScript to open Terminal and navigate to worktree
        if new_window:
            applescript = f'''
            tell application "Terminal"
                activate
                do script "cd {worktree_path} && echo '🌳 Worktree: {worktree_name}' && echo '📁 Path: {worktree_path}' && echo '' && git status"
                set custom title of front window to "WT: {worktree_name}"
            end tell
            '''
        else:
            applescript = f'''
            tell application "Terminal"
                activate
                tell application "System Events" to keystroke "t" using command down
                delay 0.5
                do script "cd {worktree_path} && echo '🌳 Worktree: {worktree_name}' && echo '📁 Path: {worktree_path}' && echo '' && git status" in front window
            end tell
            '''
            
        try:
            subprocess.run(['osascript', '-e', applescript], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to open terminal: {e}")
            return False
            
    def open_claude_in_worktree(self, worktree_name: str) -> bool:
        """Open Claude Code in a worktree"""
        worktree_path = self.worktree_base / worktree_name
        
        if not worktree_path.exists():
            print(f"Worktree path not found: {worktree_path}")
            return False
            
        # Read task from worktree config
        config_path = worktree_path / ".claude" / "worktree-config.json"
        task = ""
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                task = config.get('worktree', {}).get('task', '')
                
        # AppleScript to open Claude Code with task context
        applescript = f'''
        tell application "Terminal"
            activate
            do script "cd {worktree_path} && echo '🤖 Starting Claude Code in worktree: {worktree_name}' && echo '📋 Task: {task}' && echo '' && echo 'Starting Claude Code...' && claude"
            set custom title of front window to "Claude: {worktree_name}"
        end tell
        '''
        
        try:
            subprocess.run(['osascript', '-e', applescript], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to open Claude Code: {e}")
            return False
            
    def open_monitoring_dashboard(self, worktree_names: list) -> bool:
        """Open a monitoring dashboard for multiple worktrees"""
        
        # Create monitoring script
        monitor_script = '''
        tell application "Terminal"
            activate
            
            -- Create new window for monitoring
            do script "echo '📊 Worktree Monitoring Dashboard' && echo '================================'"
            set custom title of front window to "Worktree Monitor"
            
            -- Split into panes for each worktree (if supported)
        '''
        
        for i, name in enumerate(worktree_names):
            path = self.worktree_base / name
            if i > 0:
                monitor_script += '''
                tell application "System Events" to keystroke "d" using command down
                delay 0.5
                '''
                
            monitor_script += f'''
            do script "cd {path} && watch -n 5 'echo \\"🌳 {name}\\" && git status -s && echo \\"\\" && tail -n 20 .task-ledger.md 2>/dev/null || echo \\"No task ledger\\"'" in front window
            '''
            
        monitor_script += '''
        end tell
        '''
        
        try:
            subprocess.run(['osascript', '-e', monitor_script], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to open monitoring dashboard: {e}")
            return False
            
    def show_worktree_notification(self, title: str, message: str) -> bool:
        """Show a macOS notification"""
        applescript = f'''
        display notification "{message}" with title "{title}" sound name "Glass"
        '''
        
        try:
            subprocess.run(['osascript', '-e', applescript], check=True)
            return True
        except:
            return False
            
    def open_finder_in_worktree(self, worktree_name: str) -> bool:
        """Open Finder in worktree directory"""
        worktree_path = self.worktree_base / worktree_name
        
        if not worktree_path.exists():
            return False
            
        applescript = f'''
        tell application "Finder"
            activate
            open POSIX file "{worktree_path}"
            set current view of front window to column view
        end tell
        '''
        
        try:
            subprocess.run(['osascript', '-e', applescript], check=True)
            return True
        except:
            return False


def main():
    """CLI interface for AppleScript worktree integration"""
    if len(sys.argv) < 2:
        print("Usage: worktree_applescript.py <command> [args]")
        print("Commands:")
        print("  terminal <name>     - Open worktree in Terminal")
        print("  claude <name>       - Open Claude Code in worktree")
        print("  monitor <names...>  - Open monitoring dashboard")
        print("  finder <name>       - Open in Finder")
        return
        
    script = WorktreeAppleScript()
    command = sys.argv[1]
    
    if command == "terminal" and len(sys.argv) > 2:
        script.open_worktree_terminal(sys.argv[2])
        
    elif command == "claude" and len(sys.argv) > 2:
        script.open_claude_in_worktree(sys.argv[2])
        
    elif command == "monitor" and len(sys.argv) > 2:
        script.open_monitoring_dashboard(sys.argv[2:])
        
    elif command == "finder" and len(sys.argv) > 2:
        script.open_finder_in_worktree(sys.argv[2])
        
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
