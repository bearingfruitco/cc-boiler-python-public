#!/usr/bin/env python3
"""
Documentation Generator - Auto-generate documentation for your Claude Code setup
"""

import json
import os
from pathlib import Path
from datetime import datetime

class DocGenerator:
    def __init__(self):
        self.claude_dir = Path('.claude')
        self.output_dir = Path('docs/claude-code')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_docs(self):
        """Generate all documentation"""
        print("📚 Generating Claude Code Documentation")
        print("=====================================\n")
        
        # Generate command reference
        self.generate_command_reference()
        
        # Generate hook documentation
        self.generate_hook_documentation()
        
        # Generate configuration guide
        self.generate_config_guide()
        
        # Generate team setup guide
        self.generate_team_guide()
        
        print("\n✅ Documentation generated in docs/claude-code/")
    
    def generate_command_reference(self):
        """Generate command reference from .claude/commands"""
        print("Generating command reference...")
        
        commands_dir = self.claude_dir / 'commands'
        if not commands_dir.exists():
            return
        
        # Load aliases
        aliases = {}
        aliases_file = self.claude_dir / 'aliases.json'
        if aliases_file.exists():
            with open(aliases_file) as f:
                aliases = json.load(f)
        
        # Build command docs
        doc_content = "# Claude Code Command Reference\n\n"
        doc_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        doc_content += "## Available Commands\n\n"
        
        # Group commands by category
        categories = {
            'component': [],
            'validation': [],
            'workflow': [],
            'utility': [],
            'team': []
        }
        
        for cmd_file in sorted(commands_dir.glob('*.md')):
            cmd_name = cmd_file.stem
            
            # Determine category
            if 'component' in cmd_name:
                category = 'component'
            elif 'validate' in cmd_name or 'check' in cmd_name:
                category = 'validation'
            elif 'workflow' in cmd_name or 'feature' in cmd_name:
                category = 'workflow'
            elif 'team' in cmd_name or 'collab' in cmd_name:
                category = 'team'
            else:
                category = 'utility'
            
            categories[category].append((cmd_name, cmd_file))
        
        # Write categories
        for category, commands in categories.items():
            if commands:
                doc_content += f"### {category.title()} Commands\n\n"
                
                for cmd_name, cmd_file in commands:
                    # Find aliases
                    cmd_aliases = [f"/{alias}" for alias, target in aliases.items() if target == cmd_name]
                    
                    # Read first line of description
                    with open(cmd_file) as f:
                        first_line = f.readline().strip('# \n')
                    
                    doc_content += f"#### /{cmd_name}"
                    if cmd_aliases:
                        doc_content += f" (aliases: {', '.join(cmd_aliases)})"
                    doc_content += f"\n{first_line}\n\n"
        
        # Write chains
        chains_file = self.claude_dir / 'chains.json'
        if chains_file.exists():
            with open(chains_file) as f:
                chains_data = json.load(f)
            
            doc_content += "## Command Chains\n\n"
            for chain_name, chain_info in chains_data.get('chains', {}).items():
                doc_content += f"### {chain_name}\n"
                doc_content += f"{chain_info['description']}\n\n"
                doc_content += "Commands:\n"
                for cmd in chain_info['commands']:
                    doc_content += f"1. `{cmd}`\n"
                doc_content += "\n"
        
        # Save
        with open(self.output_dir / 'command-reference.md', 'w') as f:
            f.write(doc_content)
    
    def generate_hook_documentation(self):
        """Generate hook documentation"""
        print("Generating hook documentation...")
        
        hooks_dir = self.claude_dir / 'hooks'
        if not hooks_dir.exists():
            return
        
        doc_content = "# Claude Code Hooks Documentation\n\n"
        doc_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        hook_types = ['pre-tool-use', 'post-tool-use', 'notification', 'stop', 'sub-agent-stop']
        
        for hook_type in hook_types:
            hook_dir = hooks_dir / hook_type
            if hook_dir.exists():
                doc_content += f"## {hook_type.title()} Hooks\n\n"
                
                for hook_file in sorted(hook_dir.glob('*.py')):
                    # Extract docstring
                    with open(hook_file) as f:
                        content = f.read()
                        
                    # Find docstring
                    import ast
                    try:
                        tree = ast.parse(content)
                        docstring = ast.get_docstring(tree)
                        
                        if docstring:
                            doc_content += f"### {hook_file.stem}\n"
                            doc_content += f"{docstring.split('\\n')[0]}\n\n"
                    except:
                        pass
        
        # Add configuration example
        doc_content += "## Configuration\n\n"
        doc_content += "Add hooks to `.claude/settings.json`:\n\n"
        doc_content += "```json\n"
        doc_content += json.dumps({
            "hooks": {
                "pre-tool-use": [
                    {
                        "matcher": {},
                        "commands": ["python3 .claude/hooks/pre-tool-use/01-collab-sync.py"]
                    }
                ]
            }
        }, indent=2)
        doc_content += "\n```\n"
        
        # Save
        with open(self.output_dir / 'hooks-documentation.md', 'w') as f:
            f.write(doc_content)
    
    def generate_config_guide(self):
        """Generate configuration guide"""
        print("Generating configuration guide...")
        
        doc_content = "# Claude Code Configuration Guide\n\n"
        doc_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Document all config files
        config_files = {
            'settings.json': 'Main Claude Code settings',
            'aliases.json': 'Command aliases',
            'chains.json': 'Command chains',
            'hooks/config.json': 'Hook configuration',
            'team/config.json': 'Team settings'
        }
        
        for config_file, description in config_files.items():
            file_path = self.claude_dir / config_file
            if file_path.exists():
                doc_content += f"## {config_file}\n"
                doc_content += f"{description}\n\n"
                
                with open(file_path) as f:
                    content = json.load(f)
                
                doc_content += "```json\n"
                doc_content += json.dumps(content, indent=2)
                doc_content += "\n```\n\n"
        
        # Save
        with open(self.output_dir / 'configuration-guide.md', 'w') as f:
            f.write(doc_content)
    
    def generate_team_guide(self):
        """Generate team collaboration guide"""
        print("Generating team guide...")
        
        doc_content = "# Team Collaboration Guide\n\n"
        doc_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        doc_content += """## Setup for Team Members

### For Primary Developer (Shawn)
1. Run the standard setup
2. Your username is set by default

### For Team Member (Nikki)
1. Clone the repository
2. Update team config:
   ```bash
   echo '{"current_user": "nikki"}' > .claude/team/config.json
   ```
3. Start Claude Code

## How It Works

### Automatic Sync
- Before editing any file, latest changes are pulled from GitHub
- Conflicts are detected and warned about
- Work state saved every 60 seconds

### Handoffs
When finishing work:
- State automatically saved to GitHub gist
- Handoff document created in `.claude/team/handoffs/`
- Next person can resume exactly where you left off

### Shared Knowledge
- Successful patterns extracted and shared
- Common solutions documented
- Team metrics tracked

## Best Practices

1. **Start each session with**: `/sr` (smart resume)
2. **Before major changes**: `/checkpoint create`
3. **When switching tasks**: Let auto-save complete
4. **For questions**: Check `/help` first

## Troubleshooting

### Sync Conflicts
```bash
# Manual sync
git pull --rebase origin main

# Reset team state
echo '{}' > .claude/team/registry.json
```

### Missing Team Member
Ensure both team members are in:
```json
{
  "team": {
    "members": ["shawn", "nikki"]
  }
}
```
"""
        
        # Save
        with open(self.output_dir / 'team-collaboration-guide.md', 'w') as f:
            f.write(doc_content)

if __name__ == "__main__":
    generator = DocGenerator()
    generator.generate_all_docs()
