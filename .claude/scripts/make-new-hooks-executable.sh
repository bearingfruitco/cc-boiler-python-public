#!/bin/bash
# Make new hooks executable

chmod +x .claude/hooks/post-tool-use/18-screenshot-capture.py
chmod +x .claude/hooks/post-tool-use/19-auto-stage-working.py
chmod +x .claude/hooks/pre-tool-use/22-thinking-level-integration.py

echo "✅ New hooks are now executable"

# Verify hooks are properly formatted
echo "🔍 Verifying hook formatting..."
python3 -m py_compile .claude/hooks/post-tool-use/18-screenshot-capture.py
python3 -m py_compile .claude/hooks/post-tool-use/19-auto-stage-working.py
python3 -m py_compile .claude/hooks/pre-tool-use/22-thinking-level-integration.py
echo "✅ All hooks are valid Python"
