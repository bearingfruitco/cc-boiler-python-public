# Adding Claude Code Boilerplate v2.3.5 to Existing Projects

## 🎯 Overview

With v2.3.5's Research Management System (RMS), there are two recommended approaches for adding the boilerplate to existing projects. Choose based on your project's maturity and needs.

## 🚀 Approach 1: Fresh Start with Migration (Recommended for Most)

**Best for**: Projects that want the full benefit of the system, including RMS organization.

### Step 1: Clone Fresh Boilerplate
```bash
# Create a new directory for your migrated project
mkdir my-project-v2
cd my-project-v2

# Clone the latest boilerplate
git clone https://github.com/bearingfruitco/boilerplate-python.git .
rm -rf .git

# Initialize YOUR repository
git init
git remote add origin YOUR_REPO_URL
```

### Step 2: Migrate Your Code
```bash
# Copy your source code
cp -r ../old-project/app ./
cp -r ../old-project/modules ./
cp -r ../old-project/lib ./
cp -r ../old-project/public ./

# Copy your specific configurations
cp ../old-project/.env.local ./
cp ../old-project/package.pyon ./package-old.pyon

# Merge dependencies (manual review needed)
# Keep boilerplate's versions but add your unique packages
```

### Step 3: Organize Existing Documentation
```bash
# Move any existing research/planning docs
mkdir -p .claude/research/archive
mv ../old-project/*.md .claude/research/archive/

# These will be organized by RMS when you run:
# /research review
```

### Step 4: Configure and Push
```bash
# Run the setup script
./scripts/quick-setup.sh

# This will:
# - Configure YOUR repository (not boilerplate)
# - Set up GitHub Apps
# - Create proper project config

# Commit and push
git add .
git commit -m "chore: migrate to Claude Code Boilerplate v2.3.5"
git push -u origin main
```

## 🔧 Approach 2: Selective Integration (For Mature Projects)

**Best for**: Established projects that just want specific features.

### Option A: Just RMS (Research Management)
```bash
# From your existing project root
mkdir -p .claude/research
mkdir -p .claude/hooks/post-tool-use
mkdir -p .claude/commands

# Download RMS modules
curl -o .claude/hooks/post-tool-use/04-research-capture.py \
  https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/.claude/hooks/post-tool-use/04-research-capture.py

curl -o .claude/commands/research.md \
  https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/.claude/commands/research.md

# Add to your .claude/config.pyon
{
  "research": {
    "auto_capture": true,
    "auto_include": false,
    "archive_after_days": 30,
    "max_context_docs": 2,
    "max_doc_size_kb": 5,
    "summary_only": true,
    "include_recent_only": 7
  }
}
```

### Option B: Core System Only
```bash
# Download the add-to-existing script
curl -O https://raw.githubusercontent.com/bearingfruitco/boilerplate-python/main/scripts/add-to-existing.sh
chmod +x add-to-existing.sh

# Run with options
./add-to-existing.sh --core  # Just commands and hooks
./add-to-existing.sh --full  # Everything including RMS
```

## 📋 Migration Decision Matrix

| Your Situation | Recommended Approach | Why |
|---------------|---------------------|-----|
| New project (< 1 month old) | Fresh Start | Clean organization from day 1 |
| Small project (< 50 files) | Fresh Start | Easy to migrate, worth the benefits |
| Large project with messy docs | Fresh Start | RMS will organize everything |
| Established project, clean structure | Selective Integration | Minimal disruption |
| Just want bug tracking | Selective (Option B) | Add only what you need |
| Want full PRD workflow | Fresh Start | Best experience with all features |

## 🗂️ What Happens to Your Existing Docs?

### With Fresh Start Approach:
1. All existing markdown docs go to `.claude/research/archive/`
2. Run `/research review` to organize them
3. RMS detects relationships and merges duplicates
4. Clean project root, organized research

### With Selective Integration:
1. Existing docs stay where they are
2. NEW research gets organized automatically
3. Gradually migrate old docs as needed
4. Use `/research review` periodically

## ⚠️ Important Considerations

### Repository Configuration
**CRITICAL**: Whether you choose Fresh Start or Selective, you MUST update the repository configuration:

```bash
# Check .claude/project-config.pyon
{
  "repository": {
    "owner": "YOUR_GITHUB_USERNAME",  # NOT bearingfruitco
    "name": "YOUR_REPO_NAME",         # NOT boilerplate-python
    "branch": "main"
  }
}
```

### GitHub Apps Installation
1. Install on YOUR repository, not the boilerplate
2. CodeRabbit: https://github.com/marketplace/coderabbit
3. Claude Code: https://github.com/apps/claude
4. Select "Only select repositories" → YOUR repo

### Coding Standards Compatibility
If your project uses different CSS conventions:
1. Edit `.claude/hooks/pre-tool-use/02-design-check.py`
2. Update patterns in `.coderabbit.yaml`
3. Or disable design checks temporarily

## 🎯 Quick Start Commands

After migration, in Claude Code:
```bash
# Initialize the system
/init

# If Fresh Start: organize migrated docs
/research review

# Set up your project
/init-project

# Resume any existing work
/sr

# See what's new
/help new
```

## 📊 Expected Outcomes

### Fresh Start Migration
- ✅ All features working immediately
- ✅ Clean, organized structure
- ✅ Research docs managed by RMS
- ✅ Full PRD-driven workflow
- ⚠️ 1-2 hours migration time

### Selective Integration
- ✅ Minimal disruption
- ✅ Add features gradually
- ✅ Keep existing structure
- ⚠️ May miss some integrations
- ⚠️ Manual configuration needed

## 🆘 Troubleshooting

### "Can't push to boilerplate repository"
You're still pointing to the wrong repo. Run:
```bash
git remote set-url origin YOUR_REPO_URL
./scripts/quick-setup.sh
```

### "Commands not working"
Ensure you copied the entire `.claude/` directory:
```bash
ls -la .claude/
# Should show: commands/, hooks/, config.pyon, etc.
```

### "RMS not organizing my docs"
1. Check hook is installed: `.claude/hooks/post-tool-use/04-research-capture.py`
2. Verify config has research section
3. Run `/research review` manually

## 📚 Additional Resources

- [Research Management Guide](../guides/research-management-guide.md)
- [RMS Implementation Details](../guides/RMS_IMPLEMENTATION_SUMMARY.md)
- [Full v2.3.5 Release Notes](../releases/v2.3.5.md)

---

**Pro Tip**: The Fresh Start approach takes more initial effort but provides a much cleaner, more maintainable codebase. The RMS alone is worth the migration for most projects drowning in documentation versions!
