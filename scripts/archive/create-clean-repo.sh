#!/bin/bash
# Create a clean version of the repository

echo "🧹 Creating clean repository without secrets..."

# Create a temporary directory
TEMP_DIR="/tmp/boilerplate-python-clean-$(date +%s)"
CURRENT_DIR=$(pwd)

# Clone the repository
echo "📦 Cloning repository..."
git clone /Users/shawnsmith/dev/bfc/boilerplate-python "$TEMP_DIR"
cd "$TEMP_DIR"

# Remove the problematic file from all history
echo "🔍 Removing .mcp.json from history..."
git filter-repo --path .mcp.json --invert-paths --force

# Also remove any other potentially sensitive files
echo "🔍 Removing other sensitive files..."
git filter-repo --path .env --invert-paths --force
git filter-repo --path .env.local --invert-paths --force

# Add remote back
git remote add origin git@github.com:bearingfruitco/boilerplate-python.git

echo "✅ Clean repository created at: $TEMP_DIR"
echo ""
echo "Next steps:"
echo "1. cd $TEMP_DIR"
echo "2. Review the changes with: git log --oneline"
echo "3. Force push with: git push --force origin main"
echo ""
echo "⚠️  WARNING: This will rewrite history on the remote repository!"
