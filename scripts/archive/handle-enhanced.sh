#!/bin/bash

echo "🔍 Handling enhanced versions of commands..."
echo

# Compare enhanced vs regular versions
echo "📊 Comparing file sizes (enhanced versions should be larger/newer):"
echo

echo "generate-issues:"
ls -la .claude/commands/generate-issues*.md
echo

echo "init-project:"
ls -la .claude/commands/init-project*.md
echo

# Check for other potential duplicates
echo "🔍 Checking for other enhanced patterns:"
find .claude -name "*enhanced*" -o -name "*-v2*" -o -name "*_new*" | grep -v ".git"
echo

echo "📋 Also checking in config files:"
ls -la .claude/config*.json
echo

read -p "Replace regular versions with enhanced versions? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Replacing with enhanced versions..."
    
    # Backup originals first
    cp .claude/commands/generate-issues.md .claude/commands/generate-issues.md.backup 2>/dev/null
    cp .claude/commands/init-project.md .claude/commands/init-project.md.backup 2>/dev/null
    
    # Replace with enhanced versions
    mv .claude/commands/generate-issues-enhanced.md .claude/commands/generate-issues.md
    mv .claude/commands/init-project-enhanced.md .claude/commands/init-project.md
    
    # Handle config file if needed
    if [ -f ".claude/config-enhanced.json" ] && [ -f ".claude/config.json" ]; then
        echo "Found config-enhanced.json. Comparing..."
        echo "Regular config size: $(wc -c < .claude/config.json)"
        echo "Enhanced config size: $(wc -c < .claude/config-enhanced.json)"
        read -p "Replace config.json with config-enhanced.json? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cp .claude/config.json .claude/config.json.backup
            mv .claude/config-enhanced.json .claude/config.json
        fi
    fi
    
    # Clean up backups
    read -p "Delete backup files? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f .claude/commands/*.backup
        rm -f .claude/*.backup
    fi
    
    echo "✅ Enhanced versions are now the primary versions!"
else
    echo "❌ Keeping both versions"
fi

echo
echo "📋 Final command list:"
ls .claude/commands/*.md | grep -E "(generate-issues|init-project)" | sort
