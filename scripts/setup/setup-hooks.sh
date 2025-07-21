#!/bin/bash
# setup-hooks.sh - Set up Claude Code hooks for observability and safety

echo "🪝 Setting up Claude Code Hooks..."

# Create hooks directory structure
echo "📁 Creating hooks directories..."
mkdir -p .claude/hooks/{pre-tool-use,post-tool-use,stop,sub-agent-stop,notification}
mkdir -p .claude/{logs,transcripts}

# Make Python scripts executable
echo "🔧 Making hook scripts executable..."
find .claude/hooks -name "*.py" -exec chmod +x {} \;

# Check if settings.json exists
if [ ! -f ".claude/settings.json" ]; then
    echo "⚠️  No settings.json found. Creating one..."
    cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "file_system": {
      "read": true,
      "write": true,
      "create_directories": true
    },
    "shell": {
      "execute": true
    }
  }
}
EOF
fi

# Add hooks configuration to settings.json
echo "📝 Updating settings.json with hooks configuration..."

# Use Python to update JSON safely
python3 << 'EOF'
import json
import os

settings_path = ".claude/settings.json"

# Read existing settings
with open(settings_path, 'r') as f:
    settings = json.load(f)

# Add hooks configuration
settings['hooks'] = {
    "pre-tool-use": [
        {
            "match": {},
            "command": ["python3", ".claude/hooks/pre-tool-use/01-dangerous-commands.py"]
        }
    ],
    "post-tool-use": [
        {
            "match": {},
            "command": ["python3", ".claude/hooks/post-tool-use/01-action-logger.py"]
        }
    ],
    "stop": [
        {
            "match": {},
            "command": ["python3", ".claude/hooks/stop/01-save-transcript.py"]
        }
    ],
    "sub-agent-stop": [
        {
            "match": {},
            "command": ["python3", ".claude/hooks/sub-agent-stop/01-track-completion.py"]
        }
    ]
}

# Write updated settings
with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=2)

print("✅ Hooks configuration added to settings.json")
EOF

# Create .gitignore entries for logs
echo "📄 Updating .gitignore..."
if ! grep -q ".claude/logs/" .gitignore 2>/dev/null; then
    echo -e "\n# Claude Code logs and transcripts\n.claude/logs/\n.claude/transcripts/" >> .gitignore
fi

# Summary
echo ""
echo "✅ Claude Code Hooks setup complete!"
echo ""
echo "🪝 Hooks installed:"
echo "  • Pre-tool-use: Blocks dangerous commands"
echo "  • Post-tool-use: Logs all actions"
echo "  • Stop: Saves chat transcripts"
echo "  • Sub-agent-stop: Tracks parallel tasks"
echo ""
echo "📊 Observability features:"
echo "  • Action logs: .claude/logs/"
echo "  • Chat transcripts: .claude/transcripts/"
echo "  • Blocked commands: .claude/logs/blocked-commands.jsonl"
echo ""
echo "🚀 Next steps:"
echo "1. Restart Claude Code for hooks to take effect"
echo "2. Run a command to test logging"
echo "3. Check .claude/logs/ for output"
echo ""
echo "📚 See docs/guides/claude-code-hooks-guide.md for details"