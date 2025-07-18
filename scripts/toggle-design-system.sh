#!/bin/bash

# Toggle Design System Enforcement
# Quick way to switch between strict and flexible design modes

set -e

HOOKS_DIR=".claude/hooks/pre-tool-use"
DESIGN_HOOK="02-design-check.py"
CONFIG_FILE=".claude/hooks/config.json"

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🎨 Design System Toggle"
echo "====================="
echo ""

# Check current status
if [ -f "$HOOKS_DIR/$DESIGN_HOOK" ]; then
    CURRENT_STATUS="ENABLED"
    STATUS_COLOR=$GREEN
else
    CURRENT_STATUS="DISABLED"
    STATUS_COLOR=$RED
fi

echo -e "Current status: ${STATUS_COLOR}${CURRENT_STATUS}${NC}"
echo ""

# Show options
echo "Choose an option:"
echo "1) Disable design system (full flexibility)"
echo "2) Enable design system (strict mode)"
echo "3) Customize design rules"
echo "4) Use shadcn/ui mode"
echo "5) View current settings"
echo ""

read -p "Enter choice (1-5): " CHOICE

case $CHOICE in
    1)
        echo -e "${YELLOW}Disabling design system...${NC}"
        
        # Disable hook
        if [ -f "$HOOKS_DIR/$DESIGN_HOOK" ]; then
            mv "$HOOKS_DIR/$DESIGN_HOOK" "$HOOKS_DIR/$DESIGN_HOOK.disabled"
        fi
        
        # Update config
        if command -v jq &> /dev/null; then
            jq '.design_system.enforce = false' "$CONFIG_FILE" > temp.json && mv temp.json "$CONFIG_FILE"
        fi
        
        # Clear CodeRabbit rules
        cat > .coderabbit.yaml << 'EOF'
# Design system disabled - no restrictions
reviews:
  auto_review:
    enabled: true
EOF
        
        echo -e "${GREEN}✓ Design system disabled!${NC}"
        echo ""
        echo "You can now use:"
        echo "- Any Tailwind classes (text-sm, text-lg, etc.)"
        echo "- Any spacing values"
        echo "- Custom CSS"
        echo "- External component libraries"
        ;;
        
    2)
        echo -e "${YELLOW}Enabling design system...${NC}"
        
        # Enable hook
        if [ -f "$HOOKS_DIR/$DESIGN_HOOK.disabled" ]; then
            mv "$HOOKS_DIR/$DESIGN_HOOK.disabled" "$HOOKS_DIR/$DESIGN_HOOK"
        fi
        
        # Update config
        if command -v jq &> /dev/null; then
            jq '.design_system.enforce = true' "$CONFIG_FILE" > temp.json && mv temp.json "$CONFIG_FILE"
        fi
        
        # Restore CodeRabbit rules
        cat > .coderabbit.yaml << 'EOF'
reviews:
  auto_review:
    enabled: true
  
  custom_patterns:
    - pattern: "text-sm|text-lg|text-xl|font-bold|font-medium"
      message: "Use design tokens: text-size-[1-4], font-regular/semibold"
      level: error
    
    - pattern: "p-5|m-7|gap-5|space-x-5|space-y-5"
      message: "Use 4px grid: p-4, p-6, p-8"
      level: error
EOF
        
        echo -e "${GREEN}✓ Design system enabled!${NC}"
        echo ""
        echo "Enforcing:"
        echo "- 4 font sizes (text-size-[1-4])"
        echo "- 2 font weights (font-regular, font-semibold)"
        echo "- 4px spacing grid"
        ;;
        
    3)
        echo -e "${YELLOW}Opening design configuration...${NC}"
        
        # Open in default editor
        if [ -n "$EDITOR" ]; then
            $EDITOR "$CONFIG_FILE"
        else
            echo "Edit $CONFIG_FILE to customize:"
            echo ""
            cat << 'EOF'
{
  "design_system": {
    "enforce": true,
    "auto_fix": false,
    "allowed_font_sizes": ["your", "custom", "sizes"],
    "allowed_font_weights": ["your", "weights"],
    "spacing_grid": null,  // or 4, 8, etc.
    "min_touch_target": 44
  }
}
EOF
        fi
        ;;
        
    4)
        echo -e "${YELLOW}Setting up shadcn/ui mode...${NC}"
        
        # Disable strict enforcement
        if [ -f "$HOOKS_DIR/$DESIGN_HOOK" ]; then
            mv "$HOOKS_DIR/$DESIGN_HOOK" "$HOOKS_DIR/$DESIGN_HOOK.disabled"
        fi
        
        # Update CLAUDE.md
        cat >> CLAUDE.md << 'EOF'

## Design System - shadcn/ui

We use shadcn/ui components. Always:
- Import from @/components/ui/
- Use component variants (default, destructive, outline, etc.)
- Apply cn() for className merging
- Follow shadcn/ui patterns
EOF
        
        echo -e "${GREEN}✓ Switched to shadcn/ui mode!${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Run: npx shadcn-ui@latest init"
        echo "2. Add components: npx shadcn-ui@latest add button card"
        echo "3. Use: import { Button } from '@/components/ui/button'"
        ;;
        
    5)
        echo -e "${BLUE}Current Design System Settings:${NC}"
        echo ""
        
        if [ -f "$CONFIG_FILE" ]; then
            if command -v jq &> /dev/null; then
                jq '.design_system' "$CONFIG_FILE"
            else
                grep -A 10 '"design_system"' "$CONFIG_FILE"
            fi
        else
            echo "No configuration file found"
        fi
        ;;
        
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo "Run this script again to toggle or change settings."
