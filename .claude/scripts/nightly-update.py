#!/usr/bin/env python3
"""
Nightly script to update CLAUDE.md and context files
"""

import os
import git
import datetime
import json
from pathlib import Path

class ContextUpdater:
    def __init__(self):
        self.repo = git.Repo('.')
        self.changes = []
        
    def analyze_recent_changes(self, days=1):
        """Analyze commits from the last N days"""
        since = datetime.datetime.now() - datetime.timedelta(days=days)
        commits = list(self.repo.iter_commits(since=since))
        
        for commit in commits:
            # Analyze changed files
            for item in commit.stats.files:
                self.analyze_file_change(item)
                
    def analyze_file_change(self, filepath):
        """Extract patterns from file changes"""
        if filepath.endswith('.tsx') or filepath.endswith('.ts'):
            # Check for new components
            if 'components/' in filepath:
                self.changes.append({
                    'type': 'component',
                    'path': filepath,
                    'action': 'analyze_component'
                })
            # Check for new API routes
            elif 'app/api/' in filepath:
                self.changes.append({
                    'type': 'api',
                    'path': filepath,
                    'action': 'analyze_api'
                })
            # Check for database changes
            elif 'lib/db/' in filepath or 'schema' in filepath:
                self.changes.append({
                    'type': 'database',
                    'path': filepath,
                    'action': 'analyze_schema'
                })
                
    def apply_change(self, content, change):
        """Apply a specific change to the content"""
        # This is a simplified version - you'd implement actual parsing here
        if change['type'] == 'component':
            # Add component to documentation
            component_name = Path(change['path']).stem
            if f'- {component_name}' not in content:
                # Find components section and add
                content = content.replace(
                    '## Components',
                    f'## Components\n- {component_name}: New component added'
                )
        return content
                
    def update_claude_md(self):
        """Update CLAUDE.md with discovered changes"""
        # Read current CLAUDE.md
        with open('CLAUDE.md', 'r') as f:
            content = f.read()
            
        # Apply updates based on changes
        for change in self.changes:
            content = self.apply_change(content, change)
            
        # Create backup
        backup_path = f'CLAUDE.md.backup.{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'
        with open(backup_path, 'w') as f:
            f.write(content)
            
        # Write updated content
        with open('CLAUDE.md', 'w') as f:
            f.write(content)
            
        return len(self.changes)
        
    def generate_summary(self):
        """Generate summary of updates"""
        summary = f"Context Update Summary - {datetime.datetime.now()}\n"
        summary += f"Total changes: {len(self.changes)}\n\n"
        
        for change in self.changes:
            summary += f"- {change['type']}: {change['path']}\n"
            
        return summary

if __name__ == "__main__":
    updater = ContextUpdater()
    updater.analyze_recent_changes()
    updates = updater.update_claude_md()
    
    if updates > 0:
        print(updater.generate_summary())
        print(f"\nBackup created: CLAUDE.md.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
    else:
        print("No changes detected - CLAUDE.md is up to date")