#!/bin/bash

echo "🔍 Fixing Claude Code configuration issues..."
echo ""

# Check if .claude directory exists
if [ ! -d ".claude" ]; then
    echo "❌ No .claude directory found in current directory"
    exit 1
fi

echo "📁 Found .claude directory"
echo ""

# Fix duplicate hook numbers in pre-tool-use
echo "🔧 Fixing duplicate hook numbers in pre-tool-use..."
cd .claude/hooks/pre-tool-use

# Rename duplicates
if [ -f "01-dangerous-commands.py" ] && [ -f "01-collab-sync.py" ]; then
    mv "01-dangerous-commands.py" "00-dangerous-commands.py"
    echo "   Renamed 01-dangerous-commands.py to 00-dangerous-commands.py"
fi

if [ -f "08-evidence-language.py" ] && [ -f "08-async-patterns.py" ]; then
    mv "08-evidence-language.py" "09-evidence-language.py"
    mv "09-auto-persona.py" "10-auto-persona.py"
    mv "10-hydration-guard.py" "11-hydration-guard.py"
    mv "11-truth-enforcer.py" "12-truth-enforcer.py"
    mv "12-deletion-guard.py" "13-deletion-guard.py"
    mv "13-import-validator.py" "14-import-validator.py"
    mv "14-prd-clarity.py" "15-prd-clarity.py"
    mv "15-implementation-guide.py" "16-implementation-guide.py"
    mv "16-python-creation-guard.py" "17-python-creation-guard.py"
    mv "16-tcpa-compliance.py" "18-tcpa-compliance.py"
    mv "17-python-dependency-tracker.py" "19-python-dependency-tracker.py"
    echo "   Fixed evidence-language and subsequent hooks"
fi

cd ../../..

# Fix duplicate hook numbers in post-tool-use
echo "🔧 Fixing duplicate hook numbers in post-tool-use..."
cd .claude/hooks/post-tool-use

if [ -f "01-action-logger.py" ] && [ -f "01-state-save.py" ]; then
    mv "01-action-logger.py" "00-action-logger.py"
    echo "   Renamed 01-action-logger.py to 00-action-logger.py"
fi

if [ -f "03-auto-orchestrate.py" ] && [ -f "03-command-logger.py" ] && [ -f "03-pattern-learning.py" ]; then
    mv "03-command-logger.py" "04-command-logger.py"
    mv "03-pattern-learning.py" "05-pattern-learning.py"
    mv "04-python-response-capture.py" "06-python-response-capture.py"
    mv "04-research-capture.py" "07-research-capture.py"
    mv "05-python-import-updater.py" "08-python-import-updater.py"
    echo "   Fixed command-logger and subsequent hooks"
fi

cd ../../..

# Backup existing settings
echo "📦 Backing up existing settings..."
mkdir -p .claude/backups
timestamp=$(date +%Y%m%d_%H%M%S)

# Move all settings files to backup
for file in .claude/settings*.json; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        mv "$file" ".claude/backups/${filename}.${timestamp}"
        echo "   Backed up: $filename"
    fi
done
echo ""

# Create new settings.json with correct format
echo "📝 Creating new settings.json with correct format..."
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
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": {},
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/00-dangerous-commands.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/01-collab-sync.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/02-design-check.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/03-conflict-check.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/04-actually-works.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/05-code-quality.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/06-biome-lint.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/07-pii-protection.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/08-async-patterns.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/09-evidence-language.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/10-auto-persona.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/11-hydration-guard.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/12-truth-enforcer.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/13-deletion-guard.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/14-import-validator.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/15-prd-clarity.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/16-implementation-guide.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/17-python-creation-guard.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/18-tcpa-compliance.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/19-python-dependency-tracker.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": {},
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/00-action-logger.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/01-state-save.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/02-metrics.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/03-auto-orchestrate.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/04-command-logger.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/05-pattern-learning.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/06-python-response-capture.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/07-research-capture.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/post-tool-use/08-python-import-updater.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": {},
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/stop/01-save-transcript.py"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": {},
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/sub-agent-stop/01-track-completion.py"
          }
        ]
      }
    ]
  }
}
EOF

echo "✅ Created new settings.json with correct format"
echo ""

echo "🎉 Configuration fixes complete!"
echo ""
echo "Summary of changes:"
echo "1. Fixed duplicate hook numbers by renaming files"
echo "2. Backed up old settings files to .claude/backups/"
echo "3. Created new settings.json with PascalCase format and proper structure"
echo ""
echo "Next steps:"
echo "1. Start Claude Code: claude"
echo "2. Test with: /help and /doctor"
echo "3. If you encounter issues, check .claude/backups/ for your original files"
