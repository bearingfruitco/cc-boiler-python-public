#!/bin/bash

# Clean Git History - Remove sensitive files from git history

echo "🔐 Cleaning Git History - Removing Sensitive Files"
echo "=================================================="
echo ""
echo "⚠️  WARNING: This will rewrite git history!"
echo "Make sure you have a backup of your repository."
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Install git-filter-repo if not already installed
if ! command -v git-filter-repo &> /dev/null; then
    echo "📦 Installing git-filter-repo..."
    pip3 install git-filter-repo
fi

# Create a backup branch
echo "🔄 Creating backup branch..."
git branch backup-before-cleanup-$(date +%Y%m%d-%H%M%S)

# Remove sensitive files from history
echo "🧹 Removing sensitive files from history..."

# Remove .mcp.json files
git filter-repo --path .mcp.json --invert-paths --force

# Remove any other potential sensitive files
git filter-repo --path .env --invert-paths --force
git filter-repo --path .env.local --invert-paths --force
git filter-repo --path .env.production --invert-paths --force
git filter-repo --path .mcp.json.local --invert-paths --force

echo ""
echo "✅ Git history cleaned!"
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo "1. Force push to remote: git push --force origin main"
echo "2. All collaborators must re-clone the repository"
echo "3. Delete any old clones/forks that contain sensitive data"
echo ""
echo "🔒 Security reminder: If any exposed keys were real, rotate them immediately!"
