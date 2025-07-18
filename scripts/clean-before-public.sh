#!/bin/bash

# Clean Before Public - Remove all sensitive data before making repository public
# This script helps ensure no sensitive data is accidentally exposed

set -e  # Exit on error

echo "🔒 Starting pre-public cleanup..."
echo "================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 1. Check for sensitive files
echo -e "\n📋 Checking for sensitive files..."

if [ -f ".env.local" ]; then
    print_warning "Found .env.local - Removing..."
    rm -f .env.local
    print_status $? "Removed .env.local"
else
    print_status 0 "No .env.local found"
fi

if [ -f ".mcp.json" ]; then
    print_warning "Found .mcp.json - Removing..."
    rm -f .mcp.json
    print_status $? "Removed .mcp.json"
else
    print_status 0 "No .mcp.json found"
fi

if [ -f ".mcp.json.local" ]; then
    print_warning "Found .mcp.json.local - Removing..."
    rm -f .mcp.json.local
    print_status $? "Removed .mcp.json.local"
else
    print_status 0 "No .mcp.json.local found"
fi

# 2. Clean sensitive Claude directories
echo -e "\n📁 Cleaning sensitive Claude directories..."

CLAUDE_DIRS=(
    ".claude/logs"
    ".claude/transcripts"
    ".claude/team"
    ".claude/checkpoints"
    ".claude/backups"
    ".claude/captures"
    ".claude/analytics"
    ".claude/bugs"
    ".claude/profiles"
    ".claude/python-deps"
    ".claude/research"
)

for dir in "${CLAUDE_DIRS[@]}"; do
    if [ -d "$dir" ] && [ "$(ls -A $dir 2>/dev/null)" ]; then
        print_warning "Cleaning $dir..."
        rm -rf "$dir"/*
        print_status $? "Cleaned $dir"
    else
        print_status 0 "$dir is clean"
    fi
done

# 3. Remove Python cache files
echo -e "\n🐍 Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
print_status 0 "Python cache cleaned"

# 4. Remove OS-specific files
echo -e "\n💻 Cleaning OS-specific files..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true
find . -name "desktop.ini" -delete 2>/dev/null || true
print_status 0 "OS files cleaned"

# 5. Remove backup and temporary files
echo -e "\n🗑️  Cleaning backup and temporary files..."
find . -name "*.bak" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.swp" -delete 2>/dev/null || true
find . -name "*.swo" -delete 2>/dev/null || true
print_status 0 "Backup files cleaned"

# 6. Check for large files
echo -e "\n📊 Checking for large files..."
LARGE_FILES=$(find . -type f -size +1M -not -path "./.git/*" -not -path "./poetry.lock" 2>/dev/null)
if [ -z "$LARGE_FILES" ]; then
    print_status 0 "No large files found"
else
    print_warning "Large files found:"
    echo "$LARGE_FILES"
    echo "Consider if these should be included"
fi

# 7. Run security verification
echo -e "\n🔍 Running security verification..."
if [ -f "./scripts/verify-security.sh" ]; then
    ./scripts/verify-security.sh
    print_status $? "Security verification passed"
else
    print_warning "Security verification script not found"
fi

# 8. Check git status
echo -e "\n📝 Git status check..."
git status --porcelain

# 9. Final checks
echo -e "\n✅ Final verification..."

# Check for any remaining env files
ENV_FILES=$(find . -name ".env*" -not -name ".env.example" -type f 2>/dev/null)
if [ -z "$ENV_FILES" ]; then
    print_status 0 "No .env files found"
else
    print_warning "Found .env files:"
    echo "$ENV_FILES"
    exit 1
fi

# Check for any remaining mcp files
MCP_FILES=$(find . -name "*mcp*.json" -not -name ".mcp-example.json" -not -name "*.md" -type f 2>/dev/null)
if [ -z "$MCP_FILES" ]; then
    print_status 0 "No MCP config files found"
else
    print_warning "Found MCP config files:"
    echo "$MCP_FILES"
    exit 1
fi

echo -e "\n================================"
echo -e "${GREEN}✅ Pre-public cleanup complete!${NC}"
echo -e "\nNext steps:"
echo "1. Review git status above"
echo "2. Commit any changes"
echo "3. Review PRE_PUBLIC_CHECKLIST.md"
echo "4. Run final manual review"
echo "5. Make repository public when ready"
echo -e "\n${YELLOW}Remember: Once public, all history is visible!${NC}"
