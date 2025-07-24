#!/usr/bin/env python3
"""
PreCompact Hook - Preserves context before conversation compaction
Ensures critical files are re-read after Claude compacts the conversation
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def main():
    """Handle pre-compaction events to preserve context"""
    try:
        # Get the input from Claude
        input_data = json.loads(sys.stdin.read())
        
        # Check if this is a pre-compact event
        notification = input_data.get("notification", {})
        if notification.get("type") == "conversation_compaction":
            # Define critical files to preserve
            critical_files = [
                "CLAUDE.md",
                "QUICK_REFERENCE.md",
                "SYSTEM_OVERVIEW.md",
                ".claude/state/current-session.json",
                ".claude/checkpoints/latest.json"
            ]
            
            # Find current PRD and feature files
            project_docs = Path("docs/project")
            if project_docs.exists():
                # Add PROJECT_PRD.md
                project_prd = project_docs / "PROJECT_PRD.md"
                if project_prd.exists():
                    critical_files.append(str(project_prd))
                
                # Find active feature PRD
                features_dir = project_docs / "features"
                if features_dir.exists():
                    # Get most recently modified feature PRD
                    feature_prds = sorted(
                        features_dir.glob("*-PRD.md"),
                        key=lambda p: p.stat().st_mtime,
                        reverse=True
                    )
                    if feature_prds:
                        critical_files.append(str(feature_prds[0]))
            
            # Check for active task files
            task_files = [
                ".claude/team/current-task.md",
                ".claude/bugs/active-bugs.json",
                ".claude/context/active-profile.json"
            ]
            
            for task_file in task_files:
                if Path(task_file).exists():
                    critical_files.append(task_file)
            
            # ADD RESEARCH DOCUMENTS
            # Check for relevant research based on current feature
            research_base = Path(".claude/research")
            if research_base.exists():
                # Get current feature from git branch
                try:
                    import subprocess
                    branch = subprocess.check_output(
                        ['git', 'branch', '--show-current'],
                        text=True
                    ).strip()
                    
                    # Extract feature name
                    if '/' in branch:
                        feature = branch.split('/')[-1]
                        feature = feature.split('-', 1)[-1] if '-' in feature else feature
                        
                        # Check for feature-specific research
                        feature_research = research_base / "active" / "features" / feature
                        if feature_research.exists():
                            # Add most recent research doc (max 2)
                            research_files = sorted(
                                feature_research.glob("*.md"),
                                key=lambda p: p.stat().st_mtime,
                                reverse=True
                            )[:2]
                            for rf in research_files:
                                critical_files.append(str(rf))
                                print(f"📚 Including research: {rf.name}")
                except:
                    pass
                
                # Also check for recent general research (last 7 days)
                from datetime import timedelta
                week_ago = datetime.now() - timedelta(days=7)
                
                for category in ['analysis', 'planning', 'decisions']:
                    cat_path = research_base / "active" / category
                    if cat_path.exists():
                        recent_research = [
                            f for f in cat_path.glob("*.md")
                            if f.stat().st_mtime > week_ago.timestamp()
                        ]
                        if recent_research:
                            # Add most recent from each category
                            most_recent = max(recent_research, key=lambda p: p.stat().st_mtime)
                            critical_files.append(str(most_recent))
                            print(f"📚 Including {category}: {most_recent.name}")
            
            # Create a context preservation file
            context_dir = Path(".claude/context")
            context_dir.mkdir(parents=True, exist_ok=True)
            context_file = context_dir / "pre-compact-context.json"
            
            context_data = {
                "timestamp": datetime.now().isoformat(),
                "critical_files": critical_files,
                "session_id": input_data.get("session_id", "unknown"),
                "conversation_id": input_data.get("conversation_id", "unknown"),
                "message": "Context preserved before compaction. Run /sr to restore.",
                "active_features": [],
                "current_task": None
            }
            
            # Try to capture current task context
            current_task_file = Path(".claude/team/current-task.md")
            if current_task_file.exists():
                try:
                    context_data["current_task"] = current_task_file.read_text().strip()
                except:
                    pass
            
            # Save context
            with open(context_file, 'w') as f:
                json.dump(context_data, f, indent=2)
            
            # Output message to Claude
            print("🔄 Context preservation triggered before compaction")
            print(f"📁 Preserving {len(critical_files)} critical files")
            print("💡 Run /sr after compaction to restore full context")
            
            # Log the event
            log_dir = Path(".claude/logs")
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / "precompact-events.jsonl"
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event": "precompact",
                "files_preserved": len(critical_files),
                "session_id": input_data.get("session_id", "unknown")
            }
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
    
    except Exception as e:
        # Don't fail the hook chain
        print(f"⚠️  PreCompact handler error: {str(e)}", file=sys.stderr)
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
