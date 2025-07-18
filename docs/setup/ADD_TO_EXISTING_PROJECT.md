# Add Claude Code Boilerplate to Existing Project

> **📚 For v2.3.5 with Research Management System**: See [EXISTING_PROJECT_V2.3.5_GUIDE.md](./EXISTING_PROJECT_V2.3.5_GUIDE.md) for updated migration strategies including RMS.

This guide helps you add the Claude Code automation system to an existing project.

## Prerequisites

- Existing FastAPI project (or similar)
- Git repository already set up
- GitHub account
- Claude Code installed

## Quick Add Options

### Option 1: Minimal (Just Commands & Automation)

```bash
# From your project root
curl -sSL https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/scripts/add-to-existing.sh | bash -s minimal

# This adds:
# - .claude/ directory with all commands
# - CLAUDE.md and QUICK_REFERENCE.md
# - Basic hooks configuration
```

### Option 2: Full Integration (Recommended)

```bash
# Clone boilerplate to temp directory
git clone https://github.com/bearingfruitco/boilerplate-python.git temp-boilerplate

# Copy core files (adjust based on your needs)
cp -r temp-boilerplate/.claude .
cp temp-boilerplate/CLAUDE.md .
cp temp-boilerplate/QUICK_REFERENCE.md .
cp temp-boilerplate/.coderabbit.yaml .
cp -r temp-boilerplate/scripts/quick-setup.sh scripts/

# Clean up
rm -rf temp-boilerplate

# Run setup to configure YOUR repository
chmod +x scripts/quick-setup.sh
./scripts/quick-setup.sh
```

## Manual Integration Steps

### 1. Copy Core Files

Essential files to copy:
```
.claude/                    # All commands and automation
CLAUDE.md                   # AI instructions
QUICK_REFERENCE.md          # Command reference
.coderabbit.yaml           # AI review configuration
scripts/quick-setup.sh      # Repository setup
```

Optional (if you want full boilerplate features):
```
field-registry/            # Form field security
docs/                      # Documentation templates
```

### 2. Configure Your Repository

Run the setup script or manually update:

```bash
# Create/update .claude/project-config.pyon
{
  "repository": {
    "owner": "YOUR_GITHUB_USERNAME",
    "name": "YOUR_REPO_NAME",
    "branch": "main"
  },
  "project": {
    "name": "Your Project Name",
    "type": "Your Framework"
  }
}
```

### 3. Install GitHub Apps

**CRITICAL**: Install these on YOUR repository, not the boilerplate!

1. **CodeRabbit** - https://github.com/marketplace/coderabbit
   - Select YOUR repository
   - Choose Pro plan

2. **Claude Code** - https://github.com/apps/claude
   - Select YOUR repository
   - Grant permissions

### 4. Update Your package.pyon

Add helpful scripts if they don't exist:
```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "lint:fix": "next lint --fix",
    "test": "vitest"
  }
}
```

### 5. Configure Coding Standards Rules

Edit `.coderabbit.yaml` to match YOUR coding standards:
```yaml
reviews:
  auto_review:
    enabled: true
  custom_patterns:
    # Add your own patterns
    - pattern: "YOUR_FORBIDDEN_PATTERN"
      message: "Use YOUR_PREFERRED_PATTERN instead"
      level: error
```

### 6. Initialize in Claude Code

```bash
# Open your project
claude .

# Initialize
/init

# Set up project context
/init-project

# Start using commands!
/sr              # Smart resume
/help            # See all commands
```

## Selective Integration

### Just Want PRD-Driven Development?
Copy only:
- `.claude/commands/create-prd.md`
- `.claude/commands/generate-tasks.md`
- `.claude/commands/process-tasks.md`

### Just Want Bug Tracking?
Copy only:
- `.claude/commands/bug-track.md`
- `.claude/bugs/` directory

### Just Want AI Reviews?
- Install GitHub Apps only
- Add `.coderabbit.yaml`

## Compatibility Notes

The boilerplate works best with:
- FastAPI 13+ (App Router)
- Python projects
- Type hints CSS
- Git-based version control

For other frameworks:
- Commands still work
- Adjust coding standards rules
- Modify module creation templates

## Migration Checklist

- [ ] Copied .claude/ directory
- [ ] Added CLAUDE.md and QUICK_REFERENCE.md
- [ ] Configured .claude/project-config.pyon with YOUR repo
- [ ] Installed CodeRabbit on YOUR repo
- [ ] Installed Claude Code GitHub App on YOUR repo
- [ ] Created .coderabbit.yaml with your rules
- [ ] Ran /init in Claude Code
- [ ] Tested with /sr command

## Common Issues

### "Cannot create issues in boilerplate repository!"
Your project-config.pyon still points to boilerplate. Run:
```bash
./scripts/quick-setup.sh
```

### AI reviews not working
- Verify apps are installed on YOUR repo
- Check Settings → Integrations on GitHub
- Wait 2-3 minutes after installation

### Commands not found
Make sure you copied the entire `.claude/` directory, not just parts.

## Next Steps

1. Run `/init-project` to set up your project PRD
2. Use `/gi PROJECT` to create GitHub issues
3. Start with `/fw start 1` for your first feature
4. Enjoy AI-powered development!

---

**Tip**: The beauty of this system is it's additive - it won't break your existing code, just enhance your workflow!
