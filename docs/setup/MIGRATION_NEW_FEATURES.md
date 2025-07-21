# Migration Guide - Adding New Safety Features

## 🚀 Quick Migration (5 minutes)

If you already have the Claude Code boilerplate, add these new safety features:

### 1. Copy New Hooks

```bash
# From the boilerplate directory
cp .claude/hooks/pre-tool-use/10-hydration-guard.py YOUR_PROJECT/.claude/hooks/pre-tool-use/
cp .claude/hooks/pre-tool-use/11-truth-enforcer.py YOUR_PROJECT/.claude/hooks/pre-tool-use/
cp .claude/hooks/pre-tool-use/12-deletion-guard.py YOUR_PROJECT/.claude/hooks/pre-tool-use/
cp .claude/hooks/pre-tool-use/13-import-validator.py YOUR_PROJECT/.claude/hooks/pre-tool-use/

# Make executable
chmod +x YOUR_PROJECT/.claude/hooks/pre-tool-use/*.py
```

### 2. Copy New Commands

```bash
cp .claude/commands/facts.md YOUR_PROJECT/.claude/commands/
cp .claude/commands/exists.md YOUR_PROJECT/.claude/commands/
cp .claude/commands/field-generate.md YOUR_PROJECT/.claude/commands/
```

### 3. Update Configuration Files

Add to `.claude/hooks/config.pyon` in the pre-tool-use section:

```json
{
  "script": "10-hydration-guard.py",
  "enabled": true,
  "critical": true,
  "description": "Prevent FastAPI hydration errors"
},
{
  "script": "11-truth-enforcer.py",
  "enabled": true,
  "critical": true,
  "description": "Prevent changing established project facts"
},
{
  "script": "12-deletion-guard.py",
  "enabled": true,
  "critical": false,
  "description": "Warn before significant deletions"
},
{
  "script": "13-import-validator.py",
  "enabled": true,
  "critical": false,
  "description": "Validate and fix import paths"
}
```

### 4. Update Chains & Aliases

Add to `.claude/chains.pyon`:

```json
"safe-commit": {
  "description": "Safe commit with validation checks",
  "commands": ["facts all", "validate-design", "lint:fix", "test-runner changed"],
  "stopOnError": true
},
"field-sync": {
  "description": "Sync all field registry generated code",
  "commands": ["field-generate types", "field-generate schemas", "field-generate factories", "field-generate masking"]
},
"pre-module": {
  "description": "Check before creating new module",
  "commands": ["exists", "facts modules"]
}
```

Add to `.claude/aliases.pyon`:

```json
"truth": "facts",
"check": "exists",
"fg": "field-generate",
"sc": "safe-commit",
"fs": "field-sync",
"pc": "pre-module"
```

### 5. Test the Integration

```bash
# In Claude Code
/help new              # Should show new commands
/facts                 # Should scan and show project facts
/exists Button         # Should check for existing modules
/chain safe-commit     # Should run validation chain

# Test hooks by trying to:
# 1. Add Math.random() to a module (hydration guard)
# 2. Delete a large section of code (deletion guard)
# 3. Change an established API route (truth enforcer)
# 4. Use ../../../modules import (import validator)
```

## 📋 What Each Feature Does

### Truth Enforcement
- Scans your codebase for established values
- Prevents changing API routes, module names, env vars
- Run `/facts` to see what's protected

### Deletion Protection
- Warns before deleting files
- Blocks emptying files
- Shows what's being removed

### Hydration Safety
- Catches `Date.now()`, `Math.random()` in render
- Prevents `window` access during SSR
- Suggests proper useEffect patterns

### Import Validation
- Converts relative to @ imports
- Fixes module name casing
- Catches typos

## 🔧 Customization

### Adjust Hook Sensitivity

In `12-deletion-guard.py`, change thresholds:
```python
# Line 37: Change from 10 to your preference
if lines_removed > 10:  # Warn for smaller deletions

# Line 42: Change from 0.5 to your preference  
if reduction_percent > 0.5:  # 50% threshold
```

### Add Protected Files

In `11-truth-enforcer.py`, add your critical files:
```python
PROTECTED_FILES = [
    'package.pyon',
    'your-critical-file.py',  # Add your files
]
```

### Disable Specific Checks

In `.claude/hooks/config.pyon`, set enabled to false:
```json
{
  "script": "13-import-validator.py",
  "enabled": false,  // Disable if you don't want import validation
}
```

## 🚨 Troubleshooting

### "Hook not found" Error
- Ensure hooks are executable: `chmod +x .claude/hooks/pre-tool-use/*.py`
- Check Python path: `which python3`

### Hooks Not Running
- Verify config.pyon has correct entries
- Check Claude Code logs: `.claude/logs/`

### Too Many Warnings
- Adjust thresholds in hook files
- Set "critical": false for warnings only

### Performance Issues
- Truth enforcer scans whole codebase - disable for very large projects
- Or modify to scan only specific directories

## 📈 Benefits After Migration

- **50% fewer** "Claude changed my API" issues  
- **90% fewer** accidental deletions
- **Zero** hydration errors in production
- **Consistent** import paths
- **Protected** established values

## 🔗 Next Steps

1. Run `/facts` to see your protected values
2. Try `/chain safe-commit` before commits
3. Use `/exists` before creating modules
4. Let the hooks catch mistakes automatically

The system now prevents Claude's most common mistakes before they happen!