import { glob } from 'glob';
import { readFile, writeFile } from 'fs/promises';
import chalk from 'chalk';

interface Violation {
  file: string;
  line: number;
  column: number;
  issue: string;
  fix: string;
  autoFixable: boolean;
}

interface FixRule {
  pattern: RegExp;
  replacement: string;
  description: string;
}

const typographyFixes: FixRule[] = [
  { pattern: /\btext-xs\b/g, replacement: 'text-size-4', description: 'Extra small text' },
  { pattern: /\btext-sm\b/g, replacement: 'text-size-4', description: 'Small text' },
  { pattern: /\btext-base\b/g, replacement: 'text-size-3', description: 'Base text' },
  { pattern: /\btext-lg\b/g, replacement: 'text-size-2', description: 'Large text' },
  { pattern: /\btext-xl\b/g, replacement: 'text-size-2', description: 'Extra large text' },
  { pattern: /\btext-2xl\b/g, replacement: 'text-size-1', description: '2XL text' },
  { pattern: /\btext-3xl\b/g, replacement: 'text-size-1', description: '3XL text' },
  { pattern: /\bfont-thin\b/g, replacement: 'font-regular', description: 'Thin weight' },
  { pattern: /\bfont-light\b/g, replacement: 'font-regular', description: 'Light weight' },
  { pattern: /\bfont-normal\b/g, replacement: 'font-regular', description: 'Normal weight' },
  { pattern: /\bfont-medium\b/g, replacement: 'font-semibold', description: 'Medium weight' },
  { pattern: /\bfont-bold\b/g, replacement: 'font-semibold', description: 'Bold weight' },
  { pattern: /\bfont-extrabold\b/g, replacement: 'font-semibold', description: 'Extra bold weight' },
];

const spacingFixes: FixRule[] = [
  { pattern: /\b(p|m|gap|space-[xy]?)-5\b/g, replacement: '$1-4', description: '20px → 16px' },
  { pattern: /\b(p|m|gap|space-[xy]?)-7\b/g, replacement: '$1-6', description: '28px → 24px' },
  { pattern: /\b(p|m|gap|space-[xy]?)-9\b/g, replacement: '$1-8', description: '36px → 32px' },
  { pattern: /\b(p|m|gap|space-[xy]?)-10\b/g, replacement: '$1-8', description: '40px → 32px' },
  { pattern: /\b(p|m|gap|space-[xy]?)-11\b/g, replacement: '$1-12', description: '44px → 48px' },
];

async function validateFile(filePath: string): Promise<Violation[]> {
  const content = await readFile(filePath, 'utf-8');
  const lines = content.split('\n');
  const violations: Violation[] = [];

  lines.forEach((line, lineIndex) => {
    // Check typography
    typographyFixes.forEach(rule => {
      const matches = [...line.matchAll(rule.pattern)];
      matches.forEach(match => {
        if (match.index !== undefined) {
          violations.push({
            file: filePath,
            line: lineIndex + 1,
            column: match.index + 1,
            issue: `Invalid: ${match[0]} (${rule.description})`,
            fix: `Use: ${rule.replacement}`,
            autoFixable: true
          });
        }
      });
    });

    // Check spacing
    spacingFixes.forEach(rule => {
      const matches = [...line.matchAll(rule.pattern)];
      matches.forEach(match => {
        if (match.index !== undefined) {
          violations.push({
            file: filePath,
            line: lineIndex + 1,
            column: match.index + 1,
            issue: `Non-grid spacing: ${match[0]} (${rule.description})`,
            fix: `Use: ${match[0].replace(rule.pattern, rule.replacement)}`,
            autoFixable: true
          });
        }
      });
    });

    // Check touch targets
    const touchTargetMatch = line.match(/\bh-([0-9]+)\b/);
    if (touchTargetMatch && parseInt(touchTargetMatch[1]) < 11) {
      violations.push({
        file: filePath,
        line: lineIndex + 1,
        column: line.indexOf(touchTargetMatch[0]) + 1,
        issue: `Touch target too small: ${touchTargetMatch[0]} (${parseInt(touchTargetMatch[1]) * 4}px)`,
        fix: 'Use: h-11 (44px) or h-12 (48px) for interactive elements',
        autoFixable: false
      });
    }
  });

  return violations;
}

async function fixFile(filePath: string, violations: Violation[]): Promise<void> {
  let content = await readFile(filePath, 'utf-8');
  const autoFixable = violations.filter(v => v.autoFixable);

  // Apply all typography fixes
  typographyFixes.forEach(rule => {
    content = content.replace(rule.pattern, rule.replacement);
  });

  // Apply all spacing fixes
  spacingFixes.forEach(rule => {
    content = content.replace(rule.pattern, rule.replacement);
  });

  await writeFile(filePath, content);
  
  console.log(chalk.green(`✓ Fixed ${autoFixable.length} violations in ${filePath}`));
}

async function analyzeColorDistribution(files: string[]): Promise<void> {
  let neutralCount = 0;
  let textCount = 0;
  let accentCount = 0;

  for (const file of files) {
    const content = await readFile(file, 'utf-8');
    
    // Count neutral backgrounds
    neutralCount += (content.match(/bg-(white|gray-50)/g) || []).length;
    
    // Count text/borders
    textCount += (content.match(/(text|border)-(gray-[67]00|gray-200)/g) || []).length;
    
    // Count accents
    accentCount += (content.match(/(bg|text)-(blue|red|green)-[56]00/g) || []).length;
  }

  const total = neutralCount + textCount + accentCount;
  const neutralPercent = Math.round((neutralCount / total) * 100);
  const textPercent = Math.round((textCount / total) * 100);
  const accentPercent = Math.round((accentCount / total) * 100);

  console.log(chalk.blue('\n📊 Color Distribution Analysis:'));
  console.log(`   Neutral: ${neutralPercent}% (target: 60%)`);
  console.log(`   Text/UI: ${textPercent}% (target: 30%)`);
  console.log(`   Accent:  ${accentPercent}% (target: 10%)`);
  
  if (Math.abs(neutralPercent - 60) > 10 || 
      Math.abs(textPercent - 30) > 10 || 
      Math.abs(accentPercent - 10) > 5) {
    console.log(chalk.yellow('   ⚠️  Color distribution is off target'));
  } else {
    console.log(chalk.green('   ✓ Color distribution is balanced'));
  }
}

// Main execution
async function main() {
  const fix = process.argv.includes('--fix');
  const files = await glob('**/*.{tsx,jsx}', { 
    ignore: ['node_modules/**', '.next/**', 'dist/**'] 
  });

  console.log(chalk.blue(`🔍 Validating ${files.length} files...\n`));

  const allViolations: Violation[] = [];
  
  for (const file of files) {
    const violations = await validateFile(file);
    if (violations.length > 0) {
      allViolations.push(...violations);
      
      if (fix) {
        await fixFile(file, violations);
      } else {
        console.log(chalk.red(`\n❌ ${file}:`));
        violations.forEach(v => {
          console.log(`   Line ${v.line}:${v.column} - ${v.issue}`);
          console.log(chalk.gray(`   ${v.fix}`));
        });
      }
    }
  }

  await analyzeColorDistribution(files);

  if (allViolations.length === 0) {
    console.log(chalk.green('\n✅ All files pass design system validation!'));
  } else if (!fix) {
    console.log(chalk.yellow(`\n⚠️  Found ${allViolations.length} violations`));
    console.log(chalk.gray('Run with --fix to auto-fix violations'));
    process.exit(1);
  }
}

main().catch(console.error);
