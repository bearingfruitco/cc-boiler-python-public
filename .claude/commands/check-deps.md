---
name: check-deps
aliases: ["deps", "dependencies", "check-dependencies"]
description: Check and update project dependencies
category: maintenance
---

# Check Dependencies Command

Checks all project dependencies for updates and provides commands to update them.

## Usage

```bash
/check-deps              # Check all dependencies
/deps                    # Short alias
/dependencies update     # Check and show update commands
```

## What It Does

1. **Version Check**
   - Compares installed versions with latest
   - Shows which packages need updates
   - Identifies security vulnerabilities

2. **Update Commands**
   - Generates exact update commands
   - Groups by prod/dev dependencies
   - Respects version pinning strategy

3. **Report Generation**
   - Creates dependency report
   - Tracks update history
   - Shows package health

## Example Output

```
🔍 Checking dependency versions...

✅ next@15.3.5 - Up to date
✅ react@19.1.0 - Up to date
🔄 @biomejs/biome@2.0.0 → 2.1.1
🔄 vitest@3.0.0 → 3.2.4

📊 Summary:
✅ Up to date: 25
🔄 Updates available: 4

📦 Update Commands:

# Production dependencies:
pnpm add framer-motion@^12.23.3 lucide-react@^0.525.0

# Development dependencies:
pnpm add -D @biomejs/biome@2.1.1 vitest@^3.2.4
```

## Options

- `update` - Show update commands
- `security` - Check for vulnerabilities
- `major` - Include major version updates
- `interactive` - Interactive update mode

## Version Strategy

- **Exact versions**: Biome, Prettier (formatting tools)
- **Caret (^)**: Most dependencies (get patches)
- **Latest**: When explicitly requested

## Related Commands

- `/audit` - Security audit
- `/clean-install` - Fresh dependency install
- `/package-add` - Add new dependency
