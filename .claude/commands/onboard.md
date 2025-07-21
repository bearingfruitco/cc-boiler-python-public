# Onboard

Complete project setup and onboarding for new developers.

## Arguments:
- $TYPE: fresh|existing|check

## Why This Command:
- One-command complete setup
- Ensures all tools configured
- Creates initial context
- Shows available workflows

## Steps:

### Type: FRESH (New Project)
```bash
echo "## 🚀 Welcome to FreshSlate Project Setup"
echo ""

# 1. Project Structure
echo "### 📁 Creating project structure..."
mkdir -p components/{ui,forms,layout,features}
mkdir -p lib/{api,db,utils,validation,query,forms,supabase}
mkdir -p hooks/queries
mkdir -p app/{api/lib,\(public\),\(protected\)}
mkdir -p .claude/{commands,context,checkpoints}
echo "✅ Directories created"

# 2. Git Configuration
echo -e "\n### 🔧 Configuring Git..."
cat > .gitignore << 'EOL'
# Dependencies
node_modules/
.pnp.*

# Production
.next/
out/
build/
dist/

# Local env files
.env
.env.local
.env.*.local

# Debug
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*

# Misc
.DS_Store
*.pem
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json

# Testing
coverage/
.nyc_output/

# TypeScript
*.tsbuildinfo
next-env.d.ts
EOL

# Git hooks
mkdir -p .husky
cat > .husky/pre-commit << 'EOL'
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run validation
npm run validate:design --silent || {
  echo "❌ Design system violations found"
  exit 1
}

# Check for secrets
/claude-code /security-check secrets report || {
  echo "❌ Potential secrets detected"
  exit 1
}
EOL
chmod +x .husky/pre-commit

echo "✅ Git configured with hooks"

# 3. VS Code Setup
echo -e "\n### ⚙️ Configuring VS Code..."
mkdir -p .vscode
cat > .vscode/settings.json << 'EOL'
{
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'\`]([^\"'\`]*).*?[\"'\`]"],
    ["cx\\(([^)]*)\\)", "[\"'\`]([^\"'\`]*).*?[\"'\`]"]
  ],
  "files.exclude": {
    "**/.git": true,
    "**/.next": true,
    "**/node_modules": true,
    "**/coverage": true
  },
  "claude.commands": {
    "path": ".claude/commands",
    "aliases": ".claude/aliases.json"
  }
}
EOL

cat > .vscode/extensions.json << 'EOL'
{
  "recommendations": [
    "bradlc.vscode-tailwindcss",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "anthropic.claude-code"
  ]
}
EOL

echo "✅ VS Code configured"

# 4. Dependencies
echo -e "\n### 📦 Installing dependencies..."
if command -v pnpm &> /dev/null; then
  PKG_MANAGER="pnpm"
elif command -v bun &> /dev/null; then
  PKG_MANAGER="bun"
else
  PKG_MANAGER="npm"
fi

$PKG_MANAGER install

echo "✅ Dependencies installed with $PKG_MANAGER"

# 5. Environment Setup
echo -e "\n### 🔐 Setting up environment..."
if [ ! -f .env.local ]; then
  cat > .env.local << 'EOL'
# Database
DATABASE_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Analytics (optional)
NEXT_PUBLIC_RUDDERSTACK_KEY=
NEXT_PUBLIC_RUDDERSTACK_URL=

# Error Tracking (optional)
NEXT_PUBLIC_SENTRY_DSN=
EOL
  echo "✅ Created .env.local template"
  echo "⚠️  Please fill in your environment variables"
else
  echo "✅ .env.local already exists"
fi

# 6. Initial Context
echo -e "\n### 📝 Creating initial context..."
/context-grab capture
/checkpoint create initial-setup

echo "✅ Initial context saved"

# 7. Run Initial Checks
echo -e "\n### 🔍 Running initial checks..."
echo "Design System: "
/validate-design --quiet && echo "✅ Ready" || echo "⚠️  Check needed"

echo "Security: "
/security-check deps report --quiet && echo "✅ Clean" || echo "⚠️  Issues found"

echo "Project Structure: "
/analyze-project --summary

# 8. Show Next Steps
echo -e "\n## ✨ Setup Complete!"
echo ""
echo "### 🎯 Quick Start Commands:"
echo "- \`/help\` - See all available commands"
echo "- \`/cc ui Button\` - Create your first component"
echo "- \`/fw start <issue>\` - Start a feature"
echo "- \`/sr\` - Resume previous work"
echo ""
echo "### 📚 Documentation:"
echo "- Design System: docs/design/design-system.md"
echo "- API Guide: docs/technical/api-boilerplate.md"
echo "- Commands: .claude/commands/*.md"
echo ""
echo "### 🚦 Status:"
MODIFIED=$(git status --porcelain 2>/dev/null | wc -l)
if [ $MODIFIED -gt 0 ]; then
  echo "- Git: $MODIFIED uncommitted files"
else
  echo "- Git: ✅ Clean"
fi
echo "- Context: ✅ Initialized"
echo "- Commands: ✅ $(ls .claude/commands/*.md | wc -l) available"
```

### Type: EXISTING
For existing projects:
```bash
echo "## 🔄 Setting up Claude Code for existing project"

# Detect project type
if [ -f "package.json" ]; then
  PROJECT_TYPE="Next.js"
  FRAMEWORK=$(cat package.json | jq -r '.dependencies.next // "unknown"')
fi

echo "Detected: $PROJECT_TYPE project"

# Create Claude directories
mkdir -p .claude/{commands,context,checkpoints}

# Copy commands
cp -r /path/to/boilerplate/.claude/commands/* .claude/commands/

# Analyze existing structure
/analyze-project

# Create initial context from existing code
echo -e "\n### 📸 Capturing existing context..."
/context-grab capture full

# Show summary
echo -e "\n## ✅ Claude Code Ready!"
echo "- Commands: $(ls .claude/commands/*.md | wc -l) available"
echo "- Use \`/help\` to see all commands"
echo "- Use \`/sr\` to see current state"
```

### Type: CHECK
Verify setup:
```bash
echo "## 🏥 Setup Health Check"
echo ""

# Check directories
echo "### 📁 Directory Structure"
DIRS=(.claude .vscode components lib hooks app)
for dir in "${DIRS[@]}"; do
  if [ -d "$dir" ]; then
    echo "✅ $dir"
  else
    echo "❌ $dir missing"
  fi
done

# Check files
echo -e "\n### 📄 Configuration Files"
FILES=(.gitignore tsconfig.json tailwind.config.js .env.local)
for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file"
  else
    echo "❌ $file missing"
  fi
done

# Check Claude setup
echo -e "\n### 🤖 Claude Code Setup"
if [ -d ".claude/commands" ]; then
  CMD_COUNT=$(ls .claude/commands/*.md 2>/dev/null | wc -l)
  echo "✅ Commands: $CMD_COUNT available"
else
  echo "❌ Commands directory missing"
fi

if [ -f ".claude/context/current.md" ]; then
  CONTEXT_AGE=$(find .claude/context/current.md -mmin +1440 | wc -l)
  if [ $CONTEXT_AGE -eq 0 ]; then
    echo "✅ Context: Recent (< 24h)"
  else
    echo "⚠️  Context: Stale (> 24h)"
  fi
else
  echo "❌ Context not initialized"
fi

# Check dependencies
echo -e "\n### 📦 Dependencies"
REQUIRED_DEPS=("next" "react" "typescript" "@tanstack/react-query")
for dep in "${REQUIRED_DEPS[@]}"; do
  if grep -q "\"$dep\"" package.json; then
    echo "✅ $dep"
  else
    echo "❌ $dep missing"
  fi
done

# Check git hooks
echo -e "\n### 🪝 Git Hooks"
if [ -f ".husky/pre-commit" ]; then
  echo "✅ Pre-commit hook"
else
  echo "⚠️  No pre-commit hook"
fi

# Summary
echo -e "\n### 📊 Summary"
echo "Run \`/onboard fresh\` to fix any issues"
```

## Welcome Message
Show on first run:
```markdown
# 👋 Welcome to Claude Code!

You're using the FreshSlate boilerplate system with:
- **Smart Commands**: Type `/` to see available commands
- **Design System**: Strict rules enforced automatically
- **Context Aware**: Remembers your work across sessions
- **GitHub Integrated**: Never lose progress

## 🚀 Get Started:
1. Run `/onboard fresh` for new projects
2. Run `/onboard existing` for existing projects
3. Run `/help` to see all commands

## 💡 Pro Tips:
- Use aliases: `/sr` instead of `/smart-resume`
- Chain commands: `/vd && /tr` for validate + test
- Check status: `/ws` to see all active work

Happy coding! 🎉
```
