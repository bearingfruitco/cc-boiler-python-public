#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log(`
╔═══════════════════════════════════════════════════════════╗
║       Claude Code Boilerplate v2.3.6 - Setup Helper       ║
╚═══════════════════════════════════════════════════════════╝
`);

const projectRoot = path.resolve(__dirname, '..');
process.chdir(projectRoot);

// Check Node version
const nodeVersion = process.version;
console.log(`📌 Node.js version: ${nodeVersion}`);
const majorVersion = parseInt(nodeVersion.split('.')[0].substring(1));
if (majorVersion < 22) {
  console.log('⚠️  Warning: Node.js 22+ recommended for best compatibility\n');
}

// Check if pnpm is installed
try {
  execSync('pnpm --version', { stdio: 'ignore' });
  console.log('✅ pnpm is installed\n');
} catch {
  console.log('❌ pnpm is not installed. Install it with: npm install -g pnpm\n');
  process.exit(1);
}

// Check critical files
console.log('📁 Checking project structure...\n');
const criticalFiles = {
  'Configuration': ['tsconfig.json', 'package.json', '.env.example'],
  'Event System': ['lib/events/index.ts', 'lib/events/event-queue.ts'],
  'Hooks System': ['.claude/hooks/pre-tool-use/02-design-check.py'],
  'Field Registry': ['field-registry/core/index.ts']
};

let allGood = true;
Object.entries(criticalFiles).forEach(([category, files]) => {
  console.log(`${category}:`);
  files.forEach(file => {
    if (fs.existsSync(path.join(projectRoot, file))) {
      console.log(`  ✅ ${file}`);
    } else {
      console.log(`  ❌ ${file} - MISSING`);
      allGood = false;
    }
  });
  console.log('');
});

if (!allGood) {
  console.log('⚠️  Some files are missing. The project structure may be incomplete.\n');
}

// Check if .env.local exists
if (!fs.existsSync(path.join(projectRoot, '.env.local'))) {
  console.log('📝 Setting up environment...\n');
  console.log('Creating .env.local from .env.example...');
  try {
    fs.copyFileSync(
      path.join(projectRoot, '.env.example'),
      path.join(projectRoot, '.env.local')
    );
    console.log('✅ Created .env.local - Please edit it with your credentials\n');
  } catch (err) {
    console.log('❌ Failed to create .env.local\n');
  }
} else {
  console.log('✅ .env.local exists\n');
}

// Setup instructions
console.log(`
╔═══════════════════════════════════════════════════════════╗
║                    🚀 Quick Start Guide                    ║
╚═══════════════════════════════════════════════════════════╝

1️⃣  Install dependencies:
    ${'\x1b[36m'}pnpm install${'\x1b[0m'}

2️⃣  Configure environment:
    ${'\x1b[36m'}nano .env.local${'\x1b[0m'}
    
    Required values:
    • NEXT_PUBLIC_SUPABASE_URL
    • NEXT_PUBLIC_SUPABASE_ANON_KEY
    • DATABASE_URL

3️⃣  Start development:
    ${'\x1b[36m'}pnpm run dev${'\x1b[0m'}

4️⃣  Use Claude Code commands:
    • ${'\x1b[33m'}/init-project${'\x1b[0m'} - Start new project
    • ${'\x1b[33m'}/sr${'\x1b[0m'} - Smart resume existing work
    • ${'\x1b[33m'}/help${'\x1b[0m'} - See all commands
    • ${'\x1b[33m'}/help new${'\x1b[0m'} - See latest v2.3.6 features

╔═══════════════════════════════════════════════════════════╗
║                  ✨ Key Features v2.3.6                    ║
╚═══════════════════════════════════════════════════════════╝

${'\x1b[32m'}Event-Driven Architecture:${'\x1b[0m'}
• Fire-and-forget async operations
• Non-blocking analytics & tracking
• Automatic retry with backoff

${'\x1b[32m'}Design System Enforcement:${'\x1b[0m'}
• 4 font sizes (text-size-[1-4])
• 2 weights (font-regular, font-semibold)
• 4px spacing grid
• Toggle with /dmoff and /dmon

${'\x1b[32m'}PRD-Driven Development:${'\x1b[0m'}
• Clarity linting for specifications
• Test generation from PRDs
• Implementation grading (0-100%)

${'\x1b[32m'}Zero Context Loss:${'\x1b[0m'}
• Auto-saves to GitHub gists
• Perfect session resumption
• Team collaboration support

📚 Full documentation: docs/
🐛 Report issues: GitHub Issues
💬 Get help: /help in Claude Code
`);
