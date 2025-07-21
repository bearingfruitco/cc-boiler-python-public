#!/bin/bash

# Test script to verify all systems are working after reorganization

echo "🔍 Claude Code Boilerplate System Check"
echo "======================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check function
check() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
        FAILURES=$((FAILURES+1))
    fi
}

FAILURES=0

echo "📁 Checking Directory Structure..."
echo "----------------------------------"

# Check critical directories
[ -d ".claude" ] && check 0 ".claude directory exists" || check 1 ".claude directory exists"
[ -d ".claude/commands" ] && check 0 "Commands directory exists" || check 1 "Commands directory exists"
[ -d ".claude/hooks" ] && check 0 "Hooks directory exists" || check 1 "Hooks directory exists"
[ -d ".claude/personas" ] && check 0 "Personas directory exists" || check 1 "Personas directory exists"
[ -d "docs/setup" ] && check 0 "Setup docs directory exists" || check 1 "Setup docs directory exists"
[ -d "docs/workflow" ] && check 0 "Workflow docs directory exists" || check 1 "Workflow docs directory exists"
[ -d "field-registry" ] && check 0 "Field registry exists" || check 1 "Field registry exists"

echo ""
echo "📄 Checking Critical Files..."
echo "-----------------------------"

# Check root files
[ -f "README.md" ] && check 0 "README.md exists" || check 1 "README.md exists"
[ -f "CLAUDE.md" ] && check 0 "CLAUDE.md exists" || check 1 "CLAUDE.md exists"
[ -f "QUICK_REFERENCE.md" ] && check 0 "QUICK_REFERENCE.md exists" || check 1 "QUICK_REFERENCE.md exists"

echo ""
echo "🔗 Checking PRD → Issues → Tasks Flow..."
echo "----------------------------------------"

# Check key commands for the flow
[ -f ".claude/commands/init-project.md" ] && check 0 "init-project command exists" || check 1 "init-project command exists"
[ -f ".claude/commands/generate-issues.md" ] && check 0 "generate-issues command exists" || check 1 "generate-issues command exists"
[ -f ".claude/commands/create-prd.md" ] && check 0 "create-prd command exists" || check 1 "create-prd command exists"
[ -f ".claude/commands/generate-tasks.md" ] && check 0 "generate-tasks command exists" || check 1 "generate-tasks command exists"
[ -f ".claude/commands/process-tasks.md" ] && check 0 "process-tasks command exists" || check 1 "process-tasks command exists"
[ -f ".claude/commands/feature-workflow.md" ] && check 0 "feature-workflow command exists" || check 1 "feature-workflow command exists"

echo ""
echo "🪝 Checking Hook System..."
echo "--------------------------"

# Check critical hooks
[ -f ".claude/hooks/pre-tool-use/02-design-check.py" ] && check 0 "Design validation hook exists" || check 1 "Design validation hook exists"
[ -f ".claude/hooks/post-tool-use/01-state-save.py" ] && check 0 "State save hook exists" || check 1 "State save hook exists"
[ -f ".claude/hooks/pre-tool-use/07-pii-protection.py" ] && check 0 "PII protection hook exists" || check 1 "PII protection hook exists"

# Check hook executability
if [ -f ".claude/hooks/pre-tool-use/02-design-check.py" ]; then
    [ -x ".claude/hooks/pre-tool-use/02-design-check.py" ] && check 0 "Design hook is executable" || check 1 "Design hook is executable"
fi

echo ""
echo "⚙️ Checking Configuration..."
echo "----------------------------"

# Check config files
[ -f ".claude/config.json" ] && check 0 "Main config exists" || check 1 "Main config exists"
[ -f ".claude/aliases.json" ] && check 0 "Aliases config exists" || check 1 "Aliases config exists"
[ -f ".claude/chains.json" ] && check 0 "Chains config exists" || check 1 "Chains config exists"
[ -f ".claude/hooks/config.json" ] && check 0 "Hooks config exists" || check 1 "Hooks config exists"

echo ""
echo "📊 Checking Command Count..."
echo "----------------------------"

# Count commands
if [ -d ".claude/commands" ]; then
    COMMAND_COUNT=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
    if [ $COMMAND_COUNT -gt 40 ]; then
        check 0 "Found $COMMAND_COUNT commands (expected 40+)"
    else
        check 1 "Found only $COMMAND_COUNT commands (expected 40+)"
    fi
fi

echo ""
echo "🔐 Checking Security Features..."
echo "--------------------------------"

# Check field registry
[ -f "field-registry/core/tracking.json" ] && check 0 "Core tracking fields exist" || check 1 "Core tracking fields exist"
[ -f "field-registry/compliance/pii-fields.json" ] && check 0 "PII compliance fields exist" || check 1 "PII compliance fields exist"
[ -d "lib/security" ] && check 0 "Security library exists" || check 1 "Security library exists"

echo ""
echo "🎯 Checking Documentation..."
echo "----------------------------"

# Check reorganized docs
[ -f "docs/README.md" ] && check 0 "Documentation index exists" || check 1 "Documentation index exists"
[ -f "docs/setup/DAY_1_COMPLETE_GUIDE.md" ] && check 0 "Day 1 guide exists" || check 1 "Day 1 guide exists"
[ -f "docs/setup/QUICK_START_NEW_PROJECT.md" ] && check 0 "Quick start guide exists" || check 1 "Quick start guide exists"
[ -f "docs/workflow/DAILY_WORKFLOW.md" ] && check 0 "Daily workflow guide exists" || check 1 "Daily workflow guide exists"

echo ""
echo "📋 Aliases Check..."
echo "-------------------"

# Check some key aliases
if [ -f ".claude/aliases.json" ]; then
    grep -q '"sr": "smart-resume"' .claude/aliases.json && check 0 "sr → smart-resume alias" || check 1 "sr → smart-resume alias"
    grep -q '"prd": "create-prd"' .claude/aliases.json && check 0 "prd → create-prd alias" || check 1 "prd → create-prd alias"
    grep -q '"gi": "generate-issues"' .claude/aliases.json && check 0 "gi → generate-issues alias" || check 1 "gi → generate-issues alias"
fi

echo ""
echo "======================================="
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}✅ All systems operational!${NC}"
    echo ""
    echo "The PRD → Issues → Tasks → Code flow is ready:"
    echo "1. /init-project    - Define your project"
    echo "2. /gi PROJECT      - Generate GitHub issues"
    echo "3. /fw start [#]    - Start working on issue"
    echo "4. /prd [feature]   - Create feature PRD"
    echo "5. /gt [feature]    - Generate tasks"
    echo "6. /pt [feature]    - Process tasks"
    echo "7. /fw complete [#] - Create PR"
else
    echo -e "${RED}❌ Found $FAILURES issues that need attention${NC}"
    echo ""
    echo "Run these commands to fix:"
    echo "1. Ensure you're in the project root"
    echo "2. Check file permissions: chmod +x .claude/hooks/**/*.py"
    echo "3. Verify git is initialized: git init"
fi
echo "======================================="
