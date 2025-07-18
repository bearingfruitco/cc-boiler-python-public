#!/bin/bash

# Quick Setup Script for Claude Code Boilerplate
# This ensures proper repository configuration

set -e

echo "🚀 Claude Code Boilerplate - Quick Setup"
echo "========================================"
echo "Version: 2.3.2 with GitHub Apps Integration"
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "⚠️  No git repository found. Initializing..."
    git init
    echo "✓ Initialized git repository"
fi

# Check if we have the boilerplate files
if [ ! -f "CLAUDE.md" ] || [ ! -d ".claude" ]; then
    echo "❌ ERROR: Claude Code boilerplate files not found!"
    echo "Please run this from the boilerplate directory."
    exit 1
fi

# Check current remote
CURRENT_REMOTE=$(git config --get remote.origin.url 2>/dev/null || echo "none")
echo "Current git remote: $CURRENT_REMOTE"

# Check if still pointing to boilerplate
if [[ $CURRENT_REMOTE == *"claude-code-boilerplate"* ]]; then
    echo ""
    echo "⚠️  WARNING: You're still pointing to the boilerplate repository!"
    echo "Let's fix this..."
    echo ""
    
    # Get user input
    read -p "What's your GitHub username? " GITHUB_USER
    read -p "What's your repository name? " REPO_NAME
    read -p "Does this repository exist on GitHub yet? (y/n) " REPO_EXISTS
    
    if [[ $REPO_EXISTS == "n" ]]; then
        echo ""
        echo "Creating repository on GitHub..."
        
        # Check if gh CLI is installed
        if command -v gh &> /dev/null; then
            gh repo create "$REPO_NAME" --private --source=. --remote=origin
            echo "✓ Repository created!"
        else
            echo "GitHub CLI not found. Please create the repository manually:"
            echo "1. Go to https://github.com/new"
            echo "2. Name: $REPO_NAME"
            echo "3. Set as private (recommended)"
            echo "4. DON'T initialize with README"
            echo ""
            read -p "Press Enter when done..."
            
            # Update remote
            git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
        fi
    else
        # Update remote
        git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    fi
    
    echo "✓ Updated git remote!"
    
    # Update project config
    if [ -f .claude/project-config.json ]; then
        # Backup original
        cp .claude/project-config.json .claude/project-config.json.backup
        
        # Update with new values using sed (works on both Mac and Linux)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/\"owner\": \".*\"/\"owner\": \"$GITHUB_USER\"/" .claude/project-config.json
            sed -i '' "s/\"name\": \".*\"/\"name\": \"$REPO_NAME\"/" .claude/project-config.json
        else
            # Linux
            sed -i "s/\"owner\": \".*\"/\"owner\": \"$GITHUB_USER\"/" .claude/project-config.json
            sed -i "s/\"name\": \".*\"/\"name\": \"$REPO_NAME\"/" .claude/project-config.json
        fi
        
        echo "✓ Updated .claude/project-config.json"
    else
        # Create new config
        cat > .claude/project-config.json << EOF
{
  "repository": {
    "owner": "$GITHUB_USER",
    "name": "$REPO_NAME",
    "branch": "main"
  },
  "project": {
    "name": "$REPO_NAME",
    "type": "Next.js Application",
    "initialized_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  },
  "github_apps": {
    "coderabbit": false,
    "claude_code": false,
    "checked_at": null
  }
}
EOF
        echo "✓ Created .claude/project-config.json"
    fi
    
    # Update package.json name
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/\"name\": \".*\"/\"name\": \"$REPO_NAME\"/" package.json
    else
        sed -i "s/\"name\": \".*\"/\"name\": \"$REPO_NAME\"/" package.json
    fi
    
    echo "✓ Updated package.json"
else
    echo "✓ Git remote is already configured correctly!"
    GITHUB_USER=$(echo $CURRENT_REMOTE | sed -n 's/.*github.com[:/]\([^/]*\)\/.*/\1/p')
    REPO_NAME=$(basename -s .git $CURRENT_REMOTE)
fi

echo ""
echo "📱 Checking GitHub App Installation..."
echo ""
echo "Please install these GitHub Apps on your repository:"
echo ""
echo "1. CodeRabbit (AI Code Reviews)"
echo "   👉 https://github.com/marketplace/coderabbit"
echo "   - Select 'Only select repositories'"
echo "   - Choose: $GITHUB_USER/$REPO_NAME"
echo ""
echo "2. Claude Code (AI Development Assistant)"
echo "   👉 https://github.com/apps/claude"
echo "   - Select 'Only select repositories'"
echo "   - Choose: $GITHUB_USER/$REPO_NAME"
echo ""
read -p "Press Enter when you've installed both apps..."

# Create .coderabbit.yaml
if [ ! -f .coderabbit.yaml ]; then
    cat > .coderabbit.yaml << 'EOF'
# CodeRabbit Configuration
reviews:
  auto_review:
    enabled: true
  
  # Respect our design system
  custom_patterns:
    - pattern: "text-sm|text-lg|text-xl|font-bold|font-medium"
      message: "Use design tokens: text-size-[1-4], font-regular/semibold"
      level: error
    
    - pattern: "p-5|m-7|gap-5|space-x-5|space-y-5"
      message: "Use 4px grid: p-4, p-6, p-8"
      level: error
    
    - pattern: "console\\.log.*email|console\\.log.*phone|console\\.log.*ssn"
      message: "Never log PII to console"
      level: error

  # Don't review generated files
  path_filters:
    - "!pnpm-lock.yaml"
    - "!*.generated.ts"
    - "!*.d.ts"
EOF
    echo "✓ Created .coderabbit.yaml"
fi

# Commit changes
echo ""
echo "💾 Saving configuration..."
git add .claude/project-config.json package.json .coderabbit.yaml
git commit -m "chore: configure repository settings" || echo "No changes to commit"

# Final instructions
echo ""
echo "✅ Setup Complete!"
echo "================="
echo ""
echo "Repository: $GITHUB_USER/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Open in Claude Code: claude ."
echo "2. Run: /init"
echo "3. Run: /init-project"
echo "4. Run: /gi PROJECT"
echo ""
echo "Your project is ready for PRD-driven development with AI-powered reviews!"
echo ""
echo "🎉 Happy coding!"
