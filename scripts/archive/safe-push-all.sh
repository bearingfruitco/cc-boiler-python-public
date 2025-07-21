#!/bin/bash

echo "🔍 Checking for sensitive files before pushing..."
echo

# Check for any files that might contain secrets
echo "⚠️  Checking for potential sensitive files..."
find . -name "*.key" -o -name "*.pem" -o -name "*.env" -o -name "*secret*" -o -name "*token*" -o -name "*password*" | grep -v ".gitignore" | head -20

echo
echo "📋 Files that will be added:"
echo

# Add all Claude commands
echo "✅ Adding all Claude commands..."
git add .claude/commands/*.md

# Add all Claude hooks  
echo "✅ Adding all Claude hooks..."
git add .claude/hooks/**/*.py
git add .claude/hooks/**/*.md
git add .claude/hooks/**/*.json

# Add other Claude files (excluding sensitive ones)
echo "✅ Adding other Claude configuration..."
git add .claude/*.md
git add .claude/config*.json
git add .claude/scripts/*.py
git add .claude/scripts/*.sh

# Add documentation
echo "✅ Adding all documentation..."
git add docs/**/*.md

# Add templates
echo "✅ Adding templates..."
git add templates/**/*

# Add source files
echo "✅ Adding source files..."
git add src/**/*.py
git add src/**/*.ts
git add src/**/*.tsx

# Add configuration files
echo "✅ Adding config files..."
git add *.json
git add *.yaml
git add *.yml
git add *.toml
git add Makefile
git add .*.yaml
git add .*.yml

# Add other important files
git add *.md
git add scripts/*.sh
git add scripts/*.py
git add types/**/*
git add config/**/*
git add prisma/**/*
git add tests/**/*

echo
echo "📊 Git status:"
git status --short

echo
echo "🔍 Double-checking no secrets are staged..."
git diff --cached --name-only | grep -E "(\.env|secret|token|key|password)" || echo "✅ No obvious secret files found"

echo
read -p "Ready to commit and push? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git commit -m "feat: add complete Claude development system with all commands and hooks"
    git push origin main
    echo "✅ Successfully pushed to GitHub!"
else
    echo "❌ Cancelled. Run 'git reset' to unstage files."
fi
