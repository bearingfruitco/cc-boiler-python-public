#!/usr/bin/env python3
"""
Fix all system synchronization issues and add Python-specific workflow chains.
"""

import json
from pathlib import Path

def fix_system_sync():
    """Fix all synchronization issues found in the audit."""
    claude_dir = Path(".claude")
    
    print("🔧 FIXING SYSTEM SYNCHRONIZATION ISSUES\n")
    
    # 1. Update chains.json with Python-specific workflows
    print("## 1. Adding Python Workflow Chains")
    
    chains_path = claude_dir / "chains.json"
    with open(chains_path, 'r') as f:
        chains = json.load(f)
    
    # Add Python-specific chains
    python_chains = {
        "python-feature": {
            "description": "Complete Python feature development",
            "commands": [
                "py-prd",
                "generate-tasks",
                "capture-to-issue",
                "python-dependencies check"
            ]
        },
        "python-refactor": {
            "description": "Safe Python refactoring workflow",
            "commands": [
                "python-dependencies check",
                "python-exists-check",
                "checkpoint create pre-refactor",
                "python-import-updater --check"
            ],
            "stopOnError": True
        },
        "python-api": {
            "description": "Create Python API endpoint",
            "commands": [
                "py-prd",
                "python-exists-check",
                "py-api",
                "test-runner"
            ]
        },
        "python-agent": {
            "description": "Create AI agent with Pydantic",
            "commands": [
                "py-prd",
                "python-exists-check",
                "py-agent",
                "test-runner"
            ]
        },
        "python-pipeline": {
            "description": "Create data pipeline with Prefect",
            "commands": [
                "py-prd",
                "python-exists-check",
                "py-pipeline",
                "test-runner"
            ]
        },
        "prp-workflow": {
            "description": "Complete PRP workflow",
            "commands": [
                "prp-create",
                "prp-execute",
                "prp-status",
                "prp-complete"
            ]
        },
        "dependency-check": {
            "description": "Comprehensive dependency analysis",
            "commands": [
                "python-dependencies check",
                "python-dependencies circular",
                "python-dependencies breaking"
            ]
        },
        "python-quality": {
            "description": "Python code quality checks",
            "commands": [
                "lint-check",
                "test-runner",
                "python-dependencies circular",
                "security-check"
            ],
            "stopOnError": True
        },
        "issue-workflow": {
            "description": "Capture and create GitHub issue",
            "commands": [
                "capture-to-issue",
                "generate-issues",
                "issue-kanban"
            ]
        },
        "multi-agent": {
            "description": "Multi-agent orchestration",
            "commands": [
                "orchestrate-agents",
                "spawn-agent",
                "assign-tasks",
                "sub-agent-status"
            ]
        }
    }
    
    # Merge with existing chains
    chains["chains"].update(python_chains)
    
    # Add Python shortcuts
    python_shortcuts = {
        "pf": "python-feature",
        "pr": "python-refactor",
        "pa": "python-api",
        "pag": "python-agent",
        "ppl": "python-pipeline",
        "prpw": "prp-workflow",
        "dc": "dependency-check",
        "pq": "python-quality",
        "iw": "issue-workflow",
        "ma": "multi-agent"
    }
    
    chains["shortcuts"].update(python_shortcuts)
    
    # Save updated chains
    with open(chains_path, 'w') as f:
        json.dump(chains, f, indent=2)
    
    print("✅ Added 10 Python-specific workflow chains")
    
    # 2. Fix hook configuration settings
    print("\n## 2. Synchronizing Hook Configurations")
    
    # Update hooks/config.json
    hooks_config_path = claude_dir / "hooks" / "config.json"
    hooks_config = {
        "team": {
            "members": ["shawn", "nikki"],
            "sync_interval": 300,
            "auto_pull": True,
            "conflict_strategy": "prompt"
        },
        "github": {
            "gist_visibility": "secret",
            "use_worktrees": True
        },
        "python_specific": {
            "enforce_type_hints": True,
            "check_docstrings": True,
            "validate_imports": True,
            "track_dependencies": True
        },
        "safety": {
            "block_dangerous_commands": True,
            "protect_production": True,
            "require_evidence": True
        },
        "persistence": {
            "auto_save_interval": 60,
            "save_to_gist": True,
            "capture_responses": True
        }
    }
    
    with open(hooks_config_path, 'w') as f:
        json.dump(hooks_config, f, indent=2)
    
    print("✅ Updated hooks configuration")
    
    # 3. Create workflow documentation
    print("\n## 3. Creating Workflow Documentation")
    
    workflow_doc_path = claude_dir / "PYTHON_WORKFLOWS.md"
    
    with open(workflow_doc_path, 'w') as f:
        f.write("# Python Development Workflows\n\n")
        f.write("This document describes the Python-specific workflows available in your boilerplate.\n\n")
        
        f.write("## Quick Reference\n\n")
        f.write("| Shortcut | Workflow | Description |\n")
        f.write("|----------|----------|-------------|\n")
        f.write("| `/pf` | python-feature | Complete feature development |\n")
        f.write("| `/pr` | python-refactor | Safe refactoring workflow |\n")
        f.write("| `/pa` | python-api | Create API endpoint |\n")
        f.write("| `/pag` | python-agent | Create AI agent |\n")
        f.write("| `/ppl` | python-pipeline | Create data pipeline |\n")
        f.write("| `/prpw` | prp-workflow | Complete PRP workflow |\n")
        f.write("| `/dc` | dependency-check | Dependency analysis |\n")
        f.write("| `/pq` | python-quality | Code quality checks |\n")
        f.write("| `/iw` | issue-workflow | GitHub issue creation |\n")
        f.write("| `/ma` | multi-agent | Multi-agent orchestration |\n\n")
        
        f.write("## Common Workflows\n\n")
        
        f.write("### 1. New Feature Development\n")
        f.write("```bash\n")
        f.write("# Start with PRD\n")
        f.write("/py-prd \"User Authentication System\"\n\n")
        f.write("# Or use the chain\n")
        f.write("/chain pf\n")
        f.write("```\n\n")
        
        f.write("### 2. Refactoring Safely\n")
        f.write("```bash\n")
        f.write("# Check dependencies before refactoring\n")
        f.write("/chain pr\n\n")
        f.write("# Then update imports\n")
        f.write("/python-import-updater old.module new.module\n")
        f.write("```\n\n")
        
        f.write("### 3. Creating APIs\n")
        f.write("```bash\n")
        f.write("# FastAPI endpoint creation\n")
        f.write("/chain pa\n\n")
        f.write("# Or directly\n")
        f.write("/py-api /users POST\n")
        f.write("```\n\n")
        
        f.write("### 4. AI Agent Development\n")
        f.write("```bash\n")
        f.write("# Create Pydantic AI agent\n")
        f.write("/chain pag\n\n")
        f.write("# Or directly\n")
        f.write("/py-agent DataAnalyst --role=analyst\n")
        f.write("```\n\n")
        
        f.write("### 5. Quality Assurance\n")
        f.write("```bash\n")
        f.write("# Run all quality checks\n")
        f.write("/chain pq\n")
        f.write("```\n\n")
        
        f.write("## Hook Integration\n\n")
        f.write("These workflows integrate with the following hooks:\n\n")
        f.write("- **Creation Guard**: Prevents duplicates before creating\n")
        f.write("- **Dependency Tracker**: Tracks module dependencies\n")
        f.write("- **Import Updater**: Updates imports after refactoring\n")
        f.write("- **Response Capture**: Saves AI implementation plans\n")
        f.write("- **PRP Progress**: Tracks PRP workflow progress\n\n")
        
        f.write("## Best Practices\n\n")
        f.write("1. Always start with a PRD: `/py-prd`\n")
        f.write("2. Check existence before creating: `/pyexists`\n")
        f.write("3. Track dependencies: `/pydeps`\n")
        f.write("4. Use chains for complex workflows: `/chain pf`\n")
        f.write("5. Capture AI responses: `/cti`\n")
    
    print("✅ Created workflow documentation")
    
    # 4. Update team config for Python focus
    print("\n## 4. Updating Team Configuration")
    
    team_config_path = claude_dir / "team" / "config.json"
    team_config = {
        "current_user": "shawn",
        "project_type": "python",
        "focus_areas": [
            "AI agents",
            "FastAPI",
            "Data pipelines",
            "Python best practices"
        ],
        "excluded_patterns": [
            "*.js",
            "*.jsx",
            "*.ts",
            "*.tsx",
            "*.css",
            "*.scss"
        ]
    }
    
    with open(team_config_path, 'w') as f:
        json.dump(team_config, f, indent=2)
    
    print("✅ Updated team configuration for Python")
    
    # 5. Create a quick reference card
    print("\n## 5. Creating Quick Reference Card")
    
    quick_ref_path = claude_dir / "PYTHON_QUICK_REFERENCE.md"
    
    with open(quick_ref_path, 'w') as f:
        f.write("# Python Boilerplate Quick Reference\n\n")
        
        f.write("## 🚀 Most Used Commands\n\n")
        f.write("```bash\n")
        f.write("/sr              # Smart resume (start here)\n")
        f.write("/py-prd          # Create Python PRD\n")
        f.write("/cti             # Capture to issue\n")
        f.write("/pyexists        # Check if exists\n")
        f.write("/pydeps          # Check dependencies\n")
        f.write("/py-agent        # Create AI agent\n")
        f.write("/py-api          # Create API endpoint\n")
        f.write("/test            # Run tests\n")
        f.write("```\n\n")
        
        f.write("## 🔗 Workflow Chains\n\n")
        f.write("```bash\n")
        f.write("/chain pf        # Python feature (PRD → Tasks → Implementation)\n")
        f.write("/chain pr        # Python refactor (Deps → Check → Backup)\n")
        f.write("/chain pq        # Python quality (Lint → Test → Security)\n")
        f.write("/chain ma        # Multi-agent (Orchestrate → Spawn → Assign)\n")
        f.write("```\n\n")
        
        f.write("## 🪝 Active Hooks (35)\n\n")
        f.write("**Safety**: Dangerous commands, PII, deletion guard\n")
        f.write("**Python**: Creation guard, dependency tracking, import validation\n")
        f.write("**Process**: PRD clarity, evidence language, implementation guide\n")
        f.write("**Intelligence**: Pattern learning, response capture, auto-orchestrate\n")
        f.write("**Persistence**: State save, transcript, knowledge share\n\n")
        
        f.write("## 📊 Key Workflows\n\n")
        f.write("1. **New Feature**: `/py-prd` → `/cti` → `/py-agent` or `/py-api`\n")
        f.write("2. **Refactoring**: `/pydeps check` → move files → `/python-import-updater`\n")
        f.write("3. **Testing**: `/test` → `/coverage` → `/pq`\n")
        f.write("4. **Issue Creation**: AI response → `/cti` → GitHub issue\n")
        f.write("5. **Multi-Agent**: `/orch` → `/spawn` → `/at` → `/sas`\n")
    
    print("✅ Created quick reference card")
    
    print("\n" + "="*60)
    print("✅ SYSTEM SYNCHRONIZATION COMPLETE")
    print("="*60)
    
    print("\nWhat was fixed:")
    print("- Added 10 Python-specific workflow chains")
    print("- Synchronized hook configurations")
    print("- Created workflow documentation")
    print("- Updated team configuration for Python")
    print("- Created quick reference card")
    
    print("\nNext steps:")
    print("1. Test a workflow: /chain pf")
    print("2. Check hooks are working: /pyexists TestClass")
    print("3. Review workflows: cat .claude/PYTHON_WORKFLOWS.md")
    print("4. Use quick reference: cat .claude/PYTHON_QUICK_REFERENCE.md")

if __name__ == "__main__":
    fix_system_sync()
