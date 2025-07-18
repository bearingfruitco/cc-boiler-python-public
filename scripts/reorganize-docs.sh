#!/bin/bash

echo "📁 Reorganizing documentation structure..."
echo "This will move files to a cleaner structure."
echo ""

# Create directories
echo "Creating directories..."
mkdir -p docs/setup
mkdir -p docs/workflow  
mkdir -p docs/technical
mkdir -p docs/claude
mkdir -p scripts
mkdir -p templates

# Move setup guides
echo -e "\n📚 Moving setup guides..."
for file in DAY_1_COMPLETE_GUIDE.md QUICK_SETUP.md NEW_PROJECT_SETUP_GUIDE.md; do
    if [ -f "$file" ]; then
        mv "$file" docs/setup/
        echo "  ✓ $file"
    fi
done

# Move workflow docs
echo -e "\n📅 Moving workflow docs..."
for file in DAILY_WORKFLOW.md; do
    if [ -f "$file" ]; then
        mv "$file" docs/workflow/
        echo "  ✓ $file"
    fi
done

# Move technical docs
echo -e "\n🔧 Moving technical docs..."
for file in SYSTEM_OVERVIEW.md DOCUMENTATION_STRATEGY.md HOOKS-SUMMARY.md INTEGRATION_SUMMARY.md; do
    if [ -f "$file" ]; then
        mv "$file" docs/technical/
        echo "  ✓ $file"
    fi
done

# Move Claude-specific docs
echo -e "\n🤖 Moving Claude-specific docs..."
for file in CLAUDE_CODE_GUIDE.md AI_AGENT_DOCUMENTATION.md NEW_CHAT_CONTEXT.md PROJECT_CONTEXT.md; do
    if [ -f "$file" ]; then
        mv "$file" docs/claude/
        echo "  ✓ $file"
    fi
done

# Move scripts
echo -e "\n📜 Moving scripts..."
for file in setup-all-dependencies.sh setup-enhanced-boilerplate.sh setup-hooks.sh setup-project-sh.sh setup-security-features.sh quick-setup.sh; do
    if [ -f "$file" ]; then
        mv "$file" scripts/
        echo "  ✓ $file"
    fi
done

# Move templates
echo -e "\n📄 Moving templates..."
for file in project-knowledge-template.md gitignore-sample.txt vscode-snippets.json; do
    if [ -f "$file" ]; then
        mv "$file" templates/
        echo "  ✓ $file"
    fi
done

# Create QUICK_REFERENCE.md if it doesn't exist
if [ ! -f "QUICK_REFERENCE.md" ]; then
    echo -e "\n📝 Creating QUICK_REFERENCE.md..."
    cat > QUICK_REFERENCE.md << 'EOF'
# 🎯 Claude Code Quick Reference Card

## 🚀 Daily Flow
```bash
# Start day
/sr                     # Resume context (ALWAYS FIRST!)

# Feature work
/fw start [#]           # Start issue
/prd [name]             # Create feature PRD
/gt [name]              # Generate tasks
/pt [name]              # Process tasks

# During work
/vd                     # Validate design
/todo add "note"        # Quick reminders
/checkpoint             # Manual save

# Complete
/fw complete [#]        # Create PR
```

## 📊 Command Categories

### Context & State
- `/sr` - Smart Resume
- `/checkpoint` - Save progress
- `/compress` - Compress context

### Development
- `/cc` - Create component
- `/vd` - Validate design
- `/fw` - Feature workflow

### Testing
- `/btf` - Browser test flow
- `/tr` - Test runner

### Multi-Agent
- `/orch` - Orchestrate agents
- `/persona` - Switch persona
- `/sas` - Agent status

## 🔑 Key Files
- `docs/project/PROJECT_PRD.md` - Vision
- `docs/project/features/*` - Feature PRDs
- `.claude/orchestration/*` - Agent plans

## 💡 Remember
- Context auto-saves every 60s
- Design violations blocked automatically
- Everything tracked in GitHub issues
EOF
fi

# Clean up old files
echo -e "\n🧹 Cleaning up old files..."
for file in claude-md.md initial-md.md design-rules-md.md project-knowledge-md.md clauderules.txt; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "  ✓ Removed $file"
    fi
done

# Create documentation index
echo -e "\n📚 Creating documentation index..."
cat > docs/README.md << 'EOF'
# Documentation Index

## 📚 Setup Guides
- [Day 1 Complete Guide](setup/DAY_1_COMPLETE_GUIDE.md) - Full setup walkthrough
- [Quick Setup](setup/QUICK_SETUP.md) - Fast track setup
- [New Project Setup](setup/NEW_PROJECT_SETUP_GUIDE.md) - Starting fresh

## 📅 Workflow Guides  
- [Daily Workflow](workflow/DAILY_WORKFLOW.md) - Day-to-day usage

## 🔧 Technical Documentation
- [System Overview](technical/SYSTEM_OVERVIEW.md) - Architecture and concepts
- [Documentation Strategy](technical/DOCUMENTATION_STRATEGY.md) - How docs work
- [Hooks Summary](technical/HOOKS-SUMMARY.md) - Automation details
- [Integration Summary](technical/INTEGRATION_SUMMARY.md) - How everything connects

## 🤖 Claude-Specific
- [Claude Code Guide](claude/CLAUDE_CODE_GUIDE.md) - Using Claude Code
- [AI Agent Documentation](claude/AI_AGENT_DOCUMENTATION.md) - AI instructions
- [New Chat Context](claude/NEW_CHAT_CONTEXT.md) - Session setup
- [Project Context](claude/PROJECT_CONTEXT.md) - Project state

## 🔗 Quick Links
- [Main README](../README.md)
- [Claude Instructions](../CLAUDE.md)
- [Quick Reference](../QUICK_REFERENCE.md)
EOF

echo -e "\n✅ Reorganization complete!"
echo ""
echo "📊 Summary:"
echo "  - Documentation moved to docs/"
echo "  - Scripts moved to scripts/"
echo "  - Templates moved to templates/"
echo "  - Created documentation index"
echo "  - Created QUICK_REFERENCE.md"
echo ""
echo "⚠️  Next steps:"
echo "1. Review the new structure"
echo "2. Run: git add -A"
echo "3. Commit the changes"
