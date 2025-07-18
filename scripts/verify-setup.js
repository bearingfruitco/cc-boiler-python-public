#!/usr/bin/env node

/**
 * Quick setup verification script
 * Checks that the boilerplate is properly configured
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 Claude Code Boilerplate v2.3.6 Setup Verification\n');
console.log(`Running from: ${__dirname}`);
console.log(`Project root: ${path.join(__dirname, '..')}\n`);

const checks = [
  {
    name: 'TypeScript Configuration',
    file: 'tsconfig.json',
    check: (content) => {
      const config = JSON.parse(content);
      return config.compilerOptions.strict === true &&
             config.compilerOptions.moduleResolution === 'bundler';
    }
  },
  {
    name: 'Event System',
    file: 'lib/events/index.ts',
    check: (content) => content.includes('eventQueue') && content.includes('LEAD_EVENTS')
  },
  {
    name: 'Field Registry',
    file: 'field-registry/core/index.ts',
    check: (content) => content.includes('FieldRegistry') && content.includes('getPIIFields')
  },
  {
    name: 'Design System Hooks',
    file: '.claude/hooks/pre-tool-use/02-design-check.py',
    check: (content) => content.includes('text-size-') && content.includes('font-regular')
  },
  {
    name: 'Async Patterns Hook',
    file: '.claude/hooks/pre-tool-use/08-async-patterns.py',
    check: (content) => content.includes('Promise.all') && content.includes('eventQueue')
  },
  {
    name: 'Environment Example',
    file: '.env.example',
    check: (content) => content.includes('NEXT_PUBLIC_SUPABASE_URL')
  }
];

// First, let's check if we can find any key files
console.log('🔎 Looking for key files...\n');
const testFiles = ['package.json', 'tsconfig.json', '.env.example'];
testFiles.forEach(file => {
  const fullPath = path.join(__dirname, '..', file);
  if (fs.existsSync(fullPath)) {
    console.log(`✓ Found: ${file}`);
  } else {
    console.log(`✗ Missing: ${file} (looked in ${fullPath})`);
  }
});

console.log('\n📋 Running checks...\n');

let passed = 0;
let failed = 0;

checks.forEach(({ name, file, check }) => {
  // Use parent directory since script is in scripts/ folder
  const filePath = path.join(__dirname, '..', file);
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    if (check(content)) {
      console.log(`✅ ${name}`);
      passed++;
    } else {
      console.log(`❌ ${name} - Check failed`);
      failed++;
    }
  } catch (error) {
    console.log(`❌ ${name} - File not found: ${file}`);
    console.log(`   Looked in: ${filePath}`);
    console.log(`   Error: ${error.message}`);
    failed++;
  }
});

console.log(`\n📊 Results: ${passed} passed, ${failed} failed\n`);

if (failed === 0) {
  console.log('🎉 All checks passed! The boilerplate is properly configured.');
  console.log('\n📚 Next steps:');
  console.log('1. Copy .env.example to .env.local and fill in your values');
  console.log('2. Run: pnpm install');
  console.log('3. Run: pnpm run dev');
  console.log('4. Start with: /sr or /init-project');
} else {
  console.log('⚠️  Some checks failed. Please review the setup.');
  
  // List actual directory structure
  console.log('\n📁 Current directory structure:');
  const rootDir = path.join(__dirname, '..');
  const dirs = ['lib', 'field-registry', '.claude', 'scripts'];
  dirs.forEach(dir => {
    const dirPath = path.join(rootDir, dir);
    if (fs.existsSync(dirPath)) {
      console.log(`\n${dir}/`);
      try {
        const files = fs.readdirSync(dirPath).slice(0, 5);
        files.forEach(file => console.log(`  - ${file}`));
        if (fs.readdirSync(dirPath).length > 5) {
          console.log(`  ... and ${fs.readdirSync(dirPath).length - 5} more`);
        }
      } catch (e) {
        console.log(`  (unable to read directory)`);
      }
    } else {
      console.log(`\n${dir}/ - NOT FOUND`);
    }
  });
  
  process.exit(1);
}
