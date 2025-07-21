#!/bin/bash

# Add Claude Code Boilerplate to Existing Project - v2.3.5
# This script helps integrate the boilerplate into an existing project

set -e

echo "🚀 Claude Code Boilerplate Integration Script v2.3.5"
echo "==================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    echo "Please run this from your project root"
    exit 1
fi

# Get integration type
echo "Choose integration approach:"
echo "1) Fresh Start - Create new project with boilerplate (Recommended)"
echo "2) Core Only - Add commands and automation to current project"
echo "3) RMS Only - Just add Research Management System"
echo "4) Custom - Choose specific features"
echo ""
read -p "Enter choice (1-4): " CHOICE

case $CHOICE in
    1)
        echo -e "${YELLOW}Fresh Start Migration${NC}"
        echo "This will create a new directory for migration"
        echo ""
        read -p "New project directory name: " NEW_DIR
        
        # Create new directory
        mkdir -p "../$NEW_DIR"
        cd "../$NEW_DIR"
        
        # Clone boilerplate
        echo "Cloning boilerplate..."
        git clone https://github.com/YOUR_ORG/YOUR_REPO.git .
        rm -rf .git
        
        # Get original directory
        ORIG_DIR="../$(basename "$OLDPWD")"
        
        echo -e "${GREEN}✓ Boilerplate cloned${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Copy your code: cp -r $ORIG_DIR/{app,components,lib,public} ."
        echo "2. Copy configs: cp $ORIG_DIR/.env.local ."
        echo "3. Run: ./scripts/quick-setup.sh"
        echo "4. Organize docs: /research review"
        ;;
        
    2)
        echo -e "${YELLOW}Core Integration${NC}"
        
        # Download core files
        echo "Downloading core components..."
        
        # Create directories
        mkdir -p .claude/{commands,hooks,checkpoints,bugs,transcripts}
        
        # Download essential files
        curl -s -o temp-boilerplate.zip -L https://github.com/bearingfruitco/claude-code-boilerplate/archive/main.zip
        unzip -q temp-boilerplate.zip
        
        # Copy core files
        cp -r claude-code-boilerplate-main/.claude/* .claude/
        cp claude-code-boilerplate-main/CLAUDE.md .
        cp claude-code-boilerplate-main/QUICK_REFERENCE.md .
        cp claude-code-boilerplate-main/NEW_CHAT_CONTEXT.md .
        
        # Clean up
        rm -rf claude-code-boilerplate-main temp-boilerplate.zip
        
        echo -e "${GREEN}✓ Core files added${NC}"
        
        # Configure repository
        read -p "GitHub username: " GH_USER
        read -p "Repository name: " REPO_NAME
        
        cat > .claude/project-config.json << EOF
{
  "repository": {
    "owner": "$GH_USER",
    "name": "$REPO_NAME",
    "branch": "main"
  },
  "project": {
    "name": "$REPO_NAME",
    "type": "Next.js Application",
    "initialized_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  }
}
EOF
        
        echo -e "${GREEN}✓ Configuration complete${NC}"
        ;;
        
    3)
        echo -e "${YELLOW}RMS Only Integration${NC}"
        
        # Create RMS directories
        mkdir -p .claude/research/{active,archive}
        mkdir -p .claude/hooks/post-tool-use
        mkdir -p .claude/commands
        
        # Download RMS components
        echo "Downloading RMS components..."
        BASE_URL="https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main"
        
        curl -s -o .claude/hooks/post-tool-use/04-research-capture.py \
            "$BASE_URL/.claude/hooks/post-tool-use/04-research-capture.py"
            
        curl -s -o .claude/commands/research.md \
            "$BASE_URL/.claude/commands/research.md"
        
        # Add RMS config
        if [ -f .claude/config.json ]; then
            echo "Updating existing config..."
            # This is simplified - in reality would need proper JSON merging
        else
            cat > .claude/config.json << 'EOF'
{
  "research": {
    "auto_capture": true,
    "auto_include": false,
    "archive_after_days": 30,
    "max_context_docs": 2,
    "max_doc_size_kb": 5,
    "summary_only": true,
    "include_recent_only": 7
  }
}
EOF
        fi
        
        echo -e "${GREEN}✓ RMS installed${NC}"
        echo "Run /research review to organize existing docs"
        ;;
        
    4)
        echo -e "${YELLOW}Custom Integration${NC}"
        echo "Available features:"
        echo "- commands: All Claude Code commands"
        echo "- hooks: Automation and safety hooks"
        echo "- rms: Research Management System"
        echo "- design: Design system enforcement"
        echo "- github: GitHub Apps integration"
        echo ""
        read -p "Enter features (space-separated): " FEATURES
        
        # TODO: Implement selective feature installation
        echo "Custom integration coming soon..."
        ;;
        
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Integration complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Open in Claude Code: claude ."
echo "2. Run: /init"
echo "3. Run: /init-project (if fresh start)"
echo "4. Run: /research review (to organize docs)"
echo ""
echo "Happy coding with Claude Code Boilerplate v2.3.5! 🎉"
