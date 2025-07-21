#!/bin/bash

# Check for deprecated packages and other dependency issues
echo "🔍 Checking for dependency issues..."

# Check for deprecated packages
echo ""
echo "📦 Checking for deprecated packages..."
pnpm list --depth=0 | grep deprecated || echo "✅ No deprecated packages at top level"

# Check for outdated packages
echo ""
echo "📊 Checking for outdated packages..."
pnpm outdated

# Check for security vulnerabilities
echo ""
echo "🔒 Checking for security vulnerabilities..."
pnpm audit || true

# Check for duplicate packages
echo ""
echo "🔄 Checking for duplicate packages..."
pnpm dedupe --check

echo ""
echo "📝 Summary:"
echo "- Run './fix-dependencies.sh' to fix deprecated packages"
echo "- Run 'pnpm update' to update outdated packages"
echo "- Run 'pnpm audit --fix' to fix security vulnerabilities"
echo "- Run 'pnpm dedupe' to remove duplicate packages"
