#!/bin/bash

echo "🚀 Setting up project with AI agent boilerplate..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p components/{ui,forms,layout,features}
mkdir -p lib/{api,db,utils,validation,query,forms,supabase}
mkdir -p hooks/queries
mkdir -p types
mkdir -p public
mkdir -p app/{api/lib,\(public\),\(protected\)}
mkdir -p .claude/commands
mkdir -p scripts
mkdir -p stores

# Copy .claude directory if it exists in boilerplate
if [ -d "../boilerplate/.claude" ]; then
  echo "🤖 Copying Claude Code configuration..."
  cp -r ../boilerplate/.claude/* .claude/
elif [ -d "./claude" ]; then
  # If old claude folder exists, rename it
  echo "🤖 Converting claude folder to .claude..."
  mv ./claude .claude
fi

# Install dependencies
echo "📦 Installing dependencies..."
if command -v pnpm &> /dev/null; then
  pnpm add @tanstack/react-query @tanstack/react-query-devtools swr react-hook-form @hookform/resolvers zod
elif command -v bun &> /dev/null; then
  bun add @tanstack/react-query @tanstack/react-query-devtools swr react-hook-form @hookform/resolvers zod
else
  npm install @tanstack/react-query @tanstack/react-query-devtools swr react-hook-form @hookform/resolvers zod
fi

# Create environment file
echo "🔐 Creating environment template..."
cat > .env.local << EOL
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

# Other Services (optional)
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=
EOL

# Create .env.example
cp .env.local .env.example

# Create gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << EOL
# Dependencies
node_modules/
.pnp/
.pnp.js

# Testing
coverage/
.nyc_output/

# Next.js
.next/
out/
build/
dist/

# Production
*.production

# Misc
.DS_Store
*.pem
.vscode/
.idea/

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Local env files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Supabase
**/supabase/.branches
**/supabase/.temp
EOL

# Create VS Code settings
echo "⚙️ Creating VS Code settings..."
mkdir -p .vscode
cat > .vscode/settings.json << EOL
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
  ]
}
EOL

echo "✅ Project setup complete with React Query and API boilerplate!"
echo ""
echo "📋 Next steps:"
echo "1. Update .env.local with your values"
echo "2. Review PROJECT_CONTEXT.md for project overview"
echo "3. Check docs/design/design-system.md for design rules"
echo "4. Use Claude Code commands in .claude/commands/:"
echo "   - /init - Initialize project context"
echo "   - /create-component - Create new component"
echo "   - /validate-design - Check design compliance"
echo "   - /analyze-project - Analyze structure"
echo ""
echo "🎯 Remember: Only 4 font sizes, 2 weights, 4px grid!"
echo ""
echo "📚 Boilerplate includes:"
echo "   - React Query setup (lib/query/)"
echo "   - API route handlers (app/api/lib/)"
echo "   - Auth hooks (hooks/use-auth.ts)"
echo "   - Form utilities (lib/forms/)"
echo "   - Example API routes (app/api/users/)"
