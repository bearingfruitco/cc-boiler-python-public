#!/bin/bash
# Make all Python hooks executable

find ./.claude/hooks -name "*.py" -type f -exec chmod +x {} \;
echo "✅ All Python hooks are now executable"