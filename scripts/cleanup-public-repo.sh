#!/bin/bash

echo "🧹 Cleaning up public repository..."
echo "================================"

# Files to delete from root
ROOT_FILES=(
    "COMMIT_MESSAGE.md"
    "DOCUMENTATION_UPDATE_COMPLETE.md"
    "GIT_COMMIT_GUIDE.md"
    "GO_PUBLIC_TODO.md"
    "INITIAL.md"
    "PYTHON_DEVELOPMENT_PLAN.md"
    "SECURITY_SWEEP_RESULTS.md"
    "SHARING_CHECKLIST.md"
    "UPDATE_SUMMARY.md"
    "biome.json"
    "bunfig.toml"
    "check-dependencies.sh"
    "components.json"
    ".npmrc"
    ".coderabbit.yaml"
)

# JavaScript/Next.js directories to remove
JS_DIRS=(
    "prisma"
    "types"
    "tests"  # These appear to be JS tests, not Python
)

echo "📝 Files to remove:"
for file in "${ROOT_FILES[@]}"; do
    echo "  - $file"
done

echo ""
echo "📁 Directories to remove:"
for dir in "${JS_DIRS[@]}"; do
    echo "  - $dir/"
done

echo ""
echo "This will clean up internal documentation and JavaScript-related files."
echo "The Python boilerplate structure will remain intact."
