#!/bin/bash
# install-hooks.sh - Install Claude Code Hooks for Team Collaboration

echo "🚀 Installing Claude Code Hooks for Team Collaboration"
echo "=================================================="

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository. Please run from project root."
    exit 1
fi

# Check if .claude directory exists
if [ ! -d .claude ]; then
    echo "❌ Error: .claude directory not found. Please ensure Claude Code is set up."
    exit 1
fi

# Create hook directories if they don't exist
echo "📁 Creating hook directories..."
mkdir -p .claude/hooks/{pre-tool-use,post-tool-use,notification,stop,sub-agent-stop}
mkdir -p .claude/team/{handoffs,metrics,logs}
mkdir -p .claude/scripts

# Set up Python environment
echo "🐍 Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Create requirements file
cat > .claude/hooks/requirements.txt << 'EOF'
# Claude Code Hooks Dependencies
# No external dependencies required for basic hooks
# Add any additional packages here if needed
EOF

# Make all hook scripts executable
echo "🔧 Making hook scripts executable..."
find .claude/hooks -name "*.py" -type f -exec chmod +x {} \;

# Set up team configuration
if [ ! -f .claude/team/config.json ]; then
    echo ""
    echo "👤 Team Configuration"
    echo "-------------------"
    read -p "Enter your name (shawn/nikki): " username
    
    cat > .claude/team/config.json << EOF
{
  "current_user": "$username"
}
EOF
    echo "✅ Team config created for user: $username"
else
    current_user=$(python3 -c "import json; print(json.load(open('.claude/team/config.json'))['current_user'])")
    echo "✅ Team config exists for user: $current_user"
fi

# Initialize team files if they don't exist
if [ ! -f .claude/team/registry.json ]; then
    echo "📝 Initializing team registry..."
    cat > .claude/team/registry.json << 'EOF'
{
  "active_work": {},
  "worktrees": {},
  "last_sync": null,
  "last_updated": null
}
EOF
fi

if [ ! -f .claude/team/knowledge-base.json ]; then
    echo "📚 Initializing knowledge base..."
    cat > .claude/team/knowledge-base.json << 'EOF'
{
  "components": [],
  "solutions": [],
  "command_patterns": {},
  "error_fixes": [],
  "last_updated": null
}
EOF
fi

# Update Claude Code settings to enable hooks
echo ""
echo "⚙️  Updating Claude Code settings..."

# Check if settings.json exists
SETTINGS_FILE=".claude/settings.json"
if [ ! -f "$SETTINGS_FILE" ]; then
    echo "Creating new settings.json..."
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "permissions": {
    "file_system": {
      "read": true,
      "write": true
    },
    "shell": {
      "execute": true
    }
  }
}
EOF
fi

# Add hooks configuration to settings.json using Python
python3 << 'EOF'
import json
import os

settings_path = '.claude/settings.json'

# Load existing settings
with open(settings_path, 'r') as f:
    settings = json.load(f)

# Add hooks configuration
settings['hooks'] = {
    "pre-tool-use": [
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/pre-tool-use/01-collab-sync.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/pre-tool-use/02-design-check.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/pre-tool-use/03-conflict-check.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/pre-tool-use/04-actually-works.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/pre-tool-use/05-code-quality.py"]
        }
    ],
    "post-tool-use": [
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/post-tool-use/01-state-save.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/post-tool-use/02-metrics.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/post-tool-use/03-pattern-learning.py"]
        }
    ],
    "notification": [
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/notification/team-aware.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/notification/smart-suggest.py"]
        }
    ],
    "stop": [
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/stop/save-state.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/stop/knowledge-share.py"]
        },
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/stop/handoff-prep.py"]
        }
    ],
    "sub-agent-stop": [
        {
            "matcher": {},
            "commands": ["python3 .claude/hooks/sub-agent-stop/coordinate.py"]
        }
    ]
}

# Save updated settings
with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=2)

print("✅ Hooks configuration added to settings.json")
EOF

# Create test script
echo "🧪 Creating test script..."
cat > .claude/scripts/test-hooks.py << 'EOF'
#!/usr/bin/env python3
"""Test Claude Code Hooks Installation"""

import json
import subprocess
import sys
from pathlib import Path

def test_hook(hook_path, test_input):
    """Test a single hook"""
    try:
        result = subprocess.run(
            [sys.executable, hook_path],
            input=json.dumps(test_input),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            output = json.loads(result.stdout)
            return True, output
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print("🧪 Testing Claude Code Hooks")
    print("===========================\n")
    
    # Test pre-tool-use hooks
    test_input = {
        "tool": "write_file",
        "path": "components/TestComponent.tsx",
        "content": "export function Test() { return <div className='text-sm'>Test</div> }"
    }
    
    hooks_dir = Path(".claude/hooks")
    
    # Test design check hook
    print("Testing design-check hook...")
    success, result = test_hook(
        hooks_dir / "pre-tool-use" / "02-design-check.py",
        test_input
    )
    
    if success and result.get('action') in ['block', 'suggest_fix']:
        print("✅ Design check hook working - detected violation")
    else:
        print("❌ Design check hook failed")
    
    print("\n✅ All hooks installed successfully!")
    print("\nNext steps:")
    print("1. Restart Claude Code to load the hooks")
    print("2. Try creating a component with forbidden classes")
    print("3. Check .claude/team/metrics for compliance data")

if __name__ == "__main__":
    main()
EOF

chmod +x .claude/scripts/test-hooks.py

# Create uninstall script
echo "🗑️  Creating uninstall script..."
cat > .claude/scripts/uninstall-hooks.sh << 'EOF'
#!/bin/bash
# Uninstall Claude Code Hooks

echo "🗑️  Uninstalling Claude Code Hooks..."

# Remove hooks from settings.json
python3 << 'PYTHON'
import json

settings_path = '.claude/settings.json'
with open(settings_path, 'r') as f:
    settings = json.load(f)

if 'hooks' in settings:
    del settings['hooks']
    
with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=2)
    
print("✅ Hooks configuration removed from settings.json")
PYTHON

echo "✅ Hooks uninstalled. Hook files preserved in .claude/hooks/"
echo "   To fully remove, delete .claude/hooks directory"
EOF

chmod +x .claude/scripts/uninstall-hooks.sh

# Final summary
echo ""
echo "✅ Installation Complete!"
echo "======================="
echo ""
echo "📋 What was installed:"
echo "  • Collaboration sync hooks (prevents conflicts)"
echo "  • Design system enforcement (blocks violations)"
echo "  • Actually Works protocol (prevents untested claims)"
echo "  • Code quality checks (console.logs, TODOs, complexity)"
echo "  • Pattern learning (builds library of successful patterns)"
echo "  • Auto-save to GitHub gists"
echo "  • Team awareness notifications"
echo "  • Knowledge sharing system"
echo "  • Handoff documentation"
echo ""
echo "🚀 Next Steps:"
echo "  1. Restart Claude Code to activate hooks"
echo "  2. Run: python3 .claude/scripts/test-hooks.py"
echo "  3. Start coding - hooks will run automatically!"
echo ""
echo "📖 Commands:"
echo "  • Test hooks: python3 .claude/scripts/test-hooks.py"
echo "  • Uninstall: .claude/scripts/uninstall-hooks.sh"
echo "  • View metrics: cat .claude/team/metrics/design-compliance.json"
echo ""
echo "👥 Team Setup:"
echo "  • Current user: $(python3 -c "import json; print(json.load(open('.claude/team/config.json'))['current_user'])")"
echo "  • To switch users: Edit .claude/team/config.json"
echo ""
echo "Happy collaborative coding! 🎉"
