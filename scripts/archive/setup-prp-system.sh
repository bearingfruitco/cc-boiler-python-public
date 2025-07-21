#!/bin/bash
# Setup PRP System

echo "🚀 Setting up PRP (Product Requirement Prompt) System..."

# Check if we're in the project root
if [ ! -f ".claude/config.json" ]; then
    echo "❌ Error: Must run from project root"
    exit 1
fi

# Create directory structure
echo "📁 Creating PRP directories..."
mkdir -p PRPs/{templates,ai_docs,active,completed,execution_logs}
mkdir -p .claude/commands/PRPs
mkdir -p docs/templates/prp_examples

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/prp_runner.py
chmod +x scripts/prp_validator.py
chmod +x .claude/hooks/post-tool-use/10-prp-progress-tracker.py

# Check dependencies
echo "📦 Checking dependencies..."
if ! command -v claude &> /dev/null; then
    echo "⚠️  Warning: Claude Code CLI not found"
    echo "   PRPs can still be created manually and executed with prp_runner.py"
fi

if ! command -v poetry &> /dev/null; then
    echo "❌ Error: Poetry not found. Please install Poetry first."
    exit 1
fi

# Summary
echo ""
echo "✅ PRP System Setup Complete!"
echo ""
echo "📚 Quick Start:"
echo "  1. Create a PRP: /prp-create feature-name"
echo "  2. Review PRP: /prp-review feature-name"
echo "  3. Execute PRP: python scripts/prp_runner.py --prp feature-name --interactive"
echo "  4. Track progress: /prp-status feature-name"
echo ""
echo "📖 Documentation:"
echo "  - Full Guide: docs/guides/PRP_GUIDE.md"
echo "  - Example PRP: docs/templates/prp_examples/user_authentication_prp.md"
echo "  - Templates: PRPs/templates/"
echo ""
echo "🎯 Next Steps:"
echo "  - Try creating your first PRP with /prp-create"
echo "  - Or copy an example to PRPs/active/ and customize it"
echo ""
