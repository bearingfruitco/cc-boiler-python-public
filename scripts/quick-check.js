#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔍 Claude Code Boilerplate v2.3.6 - Quick Check\n');

// Get the absolute path to the project root
const scriptDir = __dirname;
const projectRoot = path.resolve(scriptDir, '..');

console.log(`Script directory: ${scriptDir}`);
console.log(`Project root: ${projectRoot}`);
console.log(`Current working directory: ${process.cwd()}\n`);

// Simple file existence checks
const files = [
  'tsconfig.json',
  'package.json',
  '.env.example',
  'lib/events/index.ts',
  'field-registry/core/index.ts',
  '.claude/hooks/pre-tool-use/02-design-check.py'
];

console.log('Checking files:\n');

files.forEach(file => {
  const fullPath = path.join(projectRoot, file);
  try {
    const stats = fs.statSync(fullPath);
    console.log(`✅ ${file} (${stats.size} bytes)`);
  } catch (err) {
    console.log(`❌ ${file}`);
    console.log(`   Path: ${fullPath}`);
    console.log(`   Error: ${err.code}`);
  }
});

console.log('\n✨ If you see all green checkmarks, the boilerplate is ready to use!');
