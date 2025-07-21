#!/bin/bash

# Add Claude Code Boilerplate to Existing Project
# Usage: curl -sSL [url] | bash -s [minimal|full]

set -e

MODE=${1:-full}
BOILERPLATE_REPO="https://github.com/YOUR_ORG/YOUR_REPO.git"

echo "🚀 Adding Claude Code Boilerplate to Existing Project"
echo "===================================================="
echo "Mode: $MODE"
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Clone boilerplate
echo "📥 Downloading boilerplate..."
git clone --quiet $BOILERPLATE_REPO $TEMP_DIR

# Function to copy with backup
copy_with_backup() {
    local src=$1
    local dst=$2
    
    if [ -e "$dst" ]; then
        echo "⚠️  Backing up existing $dst to $dst.backup"
        cp -r "$dst" "$dst.backup"
    fi
    
    cp -r "$src" "$dst"
    echo "✓ Copied $dst"
}

# Minimal mode - just commands and docs
if [ "$MODE" = "minimal" ]; then
    echo ""
    echo "📦 Installing minimal Claude Code system..."
    
    # Copy essential files
    copy_with_backup "$TEMP_DIR/.claude" ".claude"
    copy_with_backup "$TEMP_DIR/CLAUDE.md" "CLAUDE.md"
    copy_with_backup "$TEMP_DIR/QUICK_REFERENCE.md" "QUICK_REFERENCE.md"
    
    # Create project config if doesn't exist
    if [ ! -f ".claude/project-config.json" ]; then
        cp "$TEMP_DIR/.claude/project-config.json" ".claude/project-config.json"
        echo "✓ Created project-config.json template"
    fi
    
    echo ""
    echo "✅ Minimal installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Update .claude/project-config.json with your repo details"
    echo "2. Open in Claude Code: claude ."
    echo "3. Run: /init"
    
else
    # Full mode - everything useful
    echo ""
    echo "📦 Installing full Claude Code system..."
    
    # Copy all essential directories and files
    copy_with_backup "$TEMP_DIR/.claude" ".claude"
    copy_with_backup "$TEMP_DIR/CLAUDE.md" "CLAUDE.md"
    copy_with_backup "$TEMP_DIR/QUICK_REFERENCE.md" "QUICK_REFERENCE.md"
    copy_with_backup "$TEMP_DIR/.coderabbit.yaml" ".coderabbit.yaml"
    
    # Copy scripts directory if it doesn't exist
    if [ ! -d "scripts" ]; then
        mkdir -p scripts
    fi
    cp "$TEMP_DIR/scripts/quick-setup.sh" "scripts/quick-setup.sh"
    chmod +x scripts/quick-setup.sh
    echo "✓ Copied setup script"
    
    # Optional: Copy field registry for form security
    if [ ! -d "field-registry" ]; then
        copy_with_backup "$TEMP_DIR/field-registry" "field-registry"
    fi
    
    # Optional: Copy docs structure
    if [ ! -d "docs/project" ]; then
        mkdir -p docs/project/features
        echo "✓ Created docs structure"
    fi
    
    echo ""
    echo "✅ Full installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./scripts/quick-setup.sh"
    echo "2. Install GitHub Apps when prompted"
    echo "3. Open in Claude Code and run: /init"
fi

echo ""
echo "📚 Documentation:"
echo "- Commands: QUICK_REFERENCE.md"
echo "- Full guide: .claude/commands/*.md"
echo "- AI instructions: CLAUDE.md"
echo ""
echo "🎉 Ready to enhance your development workflow!"
