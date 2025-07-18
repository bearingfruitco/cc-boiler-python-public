#!/bin/bash
# setup-all-dependencies.sh - Complete dependency setup for Claude Code Boilerplate

echo "🚀 Claude Code Boilerplate - Complete Setup"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is not installed"
        return 1
    fi
}

# Function to check version
check_version() {
    local cmd=$1
    local required=$2
    local version=$($cmd --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)
    
    if [ -n "$version" ]; then
        echo -e "${GREEN}✓${NC} $cmd version: $version (required: $required+)"
    else
        echo -e "${YELLOW}⚠${NC} Could not determine $cmd version"
    fi
}

echo -e "\n📋 Checking prerequisites..."
echo "----------------------------"

# Check required tools
MISSING_DEPS=false

# Claude Code
if check_command "claude-code"; then
    echo -e "${GREEN}✓${NC} Claude Code is installed"
else
    echo -e "${YELLOW}→ Claude Code not found. Installing...${NC}"
    echo -e "${YELLOW}→ This is included with Claude Pro/Max subscriptions${NC}"
    
    # Install Claude Code
    npm install -g @anthropic-ai/claude-code
    
    # Check if installation succeeded
    if command -v claude-code &> /dev/null; then
        echo -e "${GREEN}✓${NC} Claude Code installed successfully"
    else
        echo -e "${RED}✗${NC} Claude Code installation failed"
        echo -e "${YELLOW}→ Try manually: npm install -g @anthropic-ai/claude-code${NC}"
        echo -e "${YELLOW}→ Then restart your terminal${NC}"
        MISSING_DEPS=true
    fi
fi

# Git
if ! check_command "git"; then
    echo -e "${YELLOW}→ Run: brew install git${NC}"
    MISSING_DEPS=true
fi

# GitHub CLI
if ! check_command "gh"; then
    echo -e "${YELLOW}→ Run: brew install gh${NC}"
    MISSING_DEPS=true
fi

# Node.js
if check_command "node"; then
    check_version "node" "22.0"
else
    echo -e "${YELLOW}→ Run: brew install node@22${NC}"
    MISSING_DEPS=true
fi

# pnpm
if check_command "pnpm"; then
    check_version "pnpm" "9.0"
else
    echo -e "${YELLOW}→ Run: npm install -g pnpm@9${NC}"
    MISSING_DEPS=true
fi

# Python 3
if ! check_command "python3"; then
    echo -e "${YELLOW}→ Run: brew install python@3${NC}"
    MISSING_DEPS=true
fi

# Bun
if check_command "bun"; then
    check_version "bun" "1.0"
else
    echo -e "${YELLOW}→ Install Bun...${NC}"
    read -p "Install Bun now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -fsSL https://bun.sh/install | bash
        # Add to current session
        export BUN_INSTALL="$HOME/.bun"
        export PATH="$BUN_INSTALL/bin:$PATH"
    else
        MISSING_DEPS=true
    fi
fi

# Stop if missing critical dependencies
if [ "$MISSING_DEPS" = true ]; then
    echo -e "\n${RED}⚠️  Please install missing dependencies first${NC}"
    exit 1
fi

echo -e "\n📦 Installing project dependencies..."
echo "------------------------------------"

# Install Node dependencies
if [ -f "package.json" ]; then
    echo "Installing Node packages with pnpm..."
    pnpm install
    
    # Verify Biome installation
    if pnpm biome --version &> /dev/null; then
        echo -e "${GREEN}✓${NC} Biome is installed"
    else
        echo -e "${RED}✗${NC} Biome installation failed"
    fi
else
    echo -e "${RED}✗${NC} package.json not found"
    exit 1
fi

echo -e "\n🛠️  Installing global tools..."
echo "----------------------------"

# Install Playwright MCP
echo "Installing Playwright MCP..."
npm install -g @modelcontextprotocol/server-playwright

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install gitpython

echo -e "\n🔒 Setting up permissions..."
echo "--------------------------"

# Make all scripts executable
chmod +x setup-enhanced-boilerplate.sh 2>/dev/null
chmod +x setup-hooks.sh 2>/dev/null
chmod +x .claude/scripts/*.sh 2>/dev/null
chmod +x .claude/scripts/*.py 2>/dev/null
chmod +x .claude/hooks/pre-tool-use/*.py 2>/dev/null
chmod +x .claude/hooks/post-tool-use/*.py 2>/dev/null

echo -e "${GREEN}✓${NC} All scripts made executable"

echo -e "\n🎣 Setting up hooks..."
echo "--------------------"

if [ -f "./setup-hooks.sh" ]; then
    ./setup-hooks.sh
else
    echo -e "${YELLOW}⚠${NC} setup-hooks.sh not found, skipping..."
fi

echo -e "\n✅ Setup Complete!"
echo "================="
echo ""
echo "Next steps:"
echo "1. Run: claude-code ."
echo "2. In Claude Code, run: /init"
echo "3. Start with: /sr"
echo ""
echo "See DAY_1_COMPLETE_GUIDE.md for detailed instructions"
