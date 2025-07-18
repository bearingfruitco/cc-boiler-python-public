#!/usr/bin/env bun
/**
 * Dependency version checker and updater
 * Checks current versions against latest and provides update commands
 */

import { readFile, writeFile } from 'fs/promises';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

// Dependencies to check
const dependenciesToCheck = [
  // Core
  { name: 'next', type: 'prod' },
  { name: 'react', type: 'prod' },
  { name: 'react-dom', type: 'prod' },
  { name: 'typescript', type: 'dev' },
  
  // Database
  { name: '@supabase/supabase-js', type: 'prod' },
  { name: 'drizzle-orm', type: 'prod' },
  { name: 'drizzle-kit', type: 'dev' },
  { name: 'prisma', type: 'dev' },
  { name: '@prisma/client', type: 'dev' },
  { name: 'postgres', type: 'prod' },
  { name: '@upstash/redis', type: 'prod' },
  
  // State & Data
  { name: '@tanstack/react-query', type: 'prod' },
  { name: 'swr', type: 'prod' },
  { name: 'zustand', type: 'prod' },
  { name: 'immer', type: 'prod' },
  
  // UI
  { name: 'tailwindcss', type: 'dev' },
  { name: 'framer-motion', type: 'prod' },
  { name: 'lucide-react', type: 'prod' },
  { name: 'clsx', type: 'prod' },
  { name: 'tailwind-merge', type: 'prod' },
  
  // Forms
  { name: 'react-hook-form', type: 'prod' },
  { name: '@hookform/resolvers', type: 'prod' },
  { name: 'zod', type: 'prod' },
  
  // Analytics
  { name: '@sentry/nextjs', type: 'prod' },
  { name: '@rudderstack/analytics-js', type: 'prod' },
  { name: '@vercel/analytics', type: 'prod' },
  { name: 'pino', type: 'prod' },
  { name: 'pino-pretty', type: 'prod' },
  
  // Dev Tools
  { name: '@biomejs/biome', type: 'dev', exact: true },
  { name: 'vitest', type: 'dev' },
  { name: '@playwright/test', type: 'dev' },
  { name: 'husky', type: 'dev' },
  { name: 'prettier', type: 'dev', exact: true },
  { name: 'webpack-bundle-analyzer', type: 'dev' },
];

async function getLatestVersion(packageName: string): Promise<string | null> {
  try {
    const { stdout } = await execAsync(`npm view ${packageName} version`);
    return stdout.trim();
  } catch (error) {
    console.error(`${colors.red}Error fetching version for ${packageName}${colors.reset}`);
    return null;
  }
}

async function getCurrentVersion(packageName: string, packageJson: any): Promise<string | null> {
  const version = packageJson.dependencies?.[packageName] || packageJson.devDependencies?.[packageName];
  return version ? version.replace(/^[\^~]/, '') : null;
}

async function checkDependencies() {
  console.log(`${colors.cyan}🔍 Checking dependency versions...${colors.reset}\n`);

  // Read package.json
  const packageJsonContent = await readFile('./package.json', 'utf-8');
  const packageJson = JSON.parse(packageJsonContent);

  const updates: any[] = [];
  const upToDate: any[] = [];

  for (const dep of dependenciesToCheck) {
    const currentVersion = await getCurrentVersion(dep.name, packageJson);
    const latestVersion = await getLatestVersion(dep.name);

    if (!currentVersion) {
      console.log(`${colors.yellow}⚠️  ${dep.name} - Not installed${colors.reset}`);
      continue;
    }

    if (!latestVersion) {
      console.log(`${colors.red}❌ ${dep.name} - Could not fetch latest version${colors.reset}`);
      continue;
    }

    if (currentVersion === latestVersion) {
      upToDate.push({ ...dep, version: currentVersion });
      console.log(`${colors.green}✅ ${dep.name}@${currentVersion} - Up to date${colors.reset}`);
    } else {
      updates.push({ ...dep, current: currentVersion, latest: latestVersion });
      console.log(
        `${colors.yellow}🔄 ${dep.name}@${currentVersion} → ${latestVersion}${colors.reset}`
      );
    }
  }

  console.log(`\n${colors.cyan}📊 Summary:${colors.reset}`);
  console.log(`${colors.green}✅ Up to date: ${upToDate.length}${colors.reset}`);
  console.log(`${colors.yellow}🔄 Updates available: ${updates.length}${colors.reset}`);

  if (updates.length > 0) {
    console.log(`\n${colors.cyan}📦 Update Commands:${colors.reset}\n`);

    // Group by type
    const prodUpdates = updates.filter(u => u.type === 'prod');
    const devUpdates = updates.filter(u => u.type === 'dev');

    if (prodUpdates.length > 0) {
      console.log(`${colors.magenta}# Production dependencies:${colors.reset}`);
      const prodCmd = prodUpdates
        .map(u => `${u.name}@${u.exact ? '' : '^'}${u.latest}`)
        .join(' ');
      console.log(`pnpm add ${prodCmd}\n`);
    }

    if (devUpdates.length > 0) {
      console.log(`${colors.magenta}# Development dependencies:${colors.reset}`);
      const devCmd = devUpdates
        .map(u => `${u.name}@${u.exact ? '' : '^'}${u.latest}`)
        .join(' ');
      console.log(`pnpm add -D ${devCmd}\n`);
    }

    console.log(`${colors.yellow}# Or update all at once:${colors.reset}`);
    console.log(`pnpm update --latest\n`);
  }

  // Write update report
  const report = {
    timestamp: new Date().toISOString(),
    upToDate: upToDate.length,
    needsUpdate: updates.length,
    updates,
    packageManager: packageJson.packageManager || 'pnpm@10.0.0',
  };

  await writeFile(
    './.claude/dependency-report.json',
    JSON.stringify(report, null, 2)
  );

  console.log(`${colors.blue}📄 Full report saved to .claude/dependency-report.json${colors.reset}`);
}

// Run the checker
checkDependencies().catch(console.error);
