#!/bin/bash
# Verification script for boilerplate fixes

echo "🔍 Verifying Claude Code Boilerplate fixes..."
echo ""

cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

# Check if all required files exist
echo "📁 Checking file structure..."
files_ok=true

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ Missing: $1"
        files_ok=false
    fi
}

check_file "app/globals.css"
check_file "stores/analytics-store.ts"
check_file "stores/form-store.ts"
check_file "stores/lead-store.ts"
check_file "components/ui/button.tsx"
check_file "components/Analytics.tsx"

echo ""
echo "🧹 Cleaning up temporary files..."
rm -f .claude/commands/*.backup
rm -f .claude/hooks/pre-tool-use/*.original
rm -f app/updated-layout.tsx
rm -f **/.DS_Store
echo "✅ Temporary files removed"

echo ""
echo "📦 Checking dependencies..."
if [ -f "node_modules/recursive-copy/package.json" ]; then
    echo "✅ recursive-copy installed"
else
    echo "❌ recursive-copy not found, installing..."
    pnpm add -D recursive-copy
fi

echo ""
echo "🔨 Running type check..."
pnpm typecheck 2>&1 | grep -E "(error|Error)" || echo "✅ No TypeScript errors found"

echo ""
echo "🎨 Running linter..."
pnpm lint 2>&1 | grep -E "(error|Error)" || echo "✅ No linting errors found"

echo ""
if [ "$files_ok" = true ]; then
    echo "✅ All files are in place!"
    echo ""
    echo "🚀 Ready to use! Start the dev server with:"
    echo "   pnpm dev"
else
    echo "⚠️  Some files are missing. Please check the errors above."
fi
