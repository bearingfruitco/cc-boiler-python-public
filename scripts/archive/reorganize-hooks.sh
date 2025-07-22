#!/bin/bash

echo "🔍 Analyzing hook conflicts and duplicates..."
echo

# Function to find duplicates
find_duplicates() {
    local dir=$1
    echo "📂 Checking $dir:"
    
    # Find duplicate numbers
    for num in $(ls "$dir" | grep -E '^[0-9]{2}-' | cut -d'-' -f1 | sort | uniq -d); do
        echo "  ⚠️  Duplicate number $num:"
        ls "$dir" | grep "^$num-" | while read file; do
            echo "     - $file"
        done
    done
    echo
}

# Check each hook directory
for hookdir in .claude/hooks/*/; do
    if [ -d "$hookdir" ] && [ "$(ls -A $hookdir 2>/dev/null | grep -E '^[0-9]{2}-.*\.py$')" ]; then
        find_duplicates "$hookdir"
    fi
done

echo "📋 Hook inventory by directory:"
echo
for hookdir in .claude/hooks/*/; do
    if [ -d "$hookdir" ]; then
        count=$(ls "$hookdir" 2>/dev/null | grep -E '\.py$' | wc -l)
        echo "$hookdir: $count hooks"
    fi
done

echo
echo "🔧 Proposed reorganization:"
echo
echo "PRE-TOOL-USE hooks (in order):"
echo "00-auto-approve-safe-ops.py         - Keep as is"
echo "01-dangerous-commands.py             - Primary safety check"
echo "02-collab-sync.py                    - Rename from 01-collab-sync.py"
echo "03-design-check.py                   - Rename from 02-design-check.py"
echo "04-conflict-check.py                 - Rename from 03-conflict-check.py"
echo "05-actually-works.py                 - Rename from 04-actually-works.py"
echo "06-code-quality.py                   - Rename from 05-code-quality.py"
echo "07-biome-lint.py                     - Rename from 06-biome-lint.py"
echo "08-pii-protection.py                 - Rename from 07-pii-protection.py"
echo "09-async-patterns.py                 - Rename from 08-async-patterns.py"
echo "10-evidence-language.py              - Rename from 08-evidence-language.py"
echo "11-auto-persona.py                   - Rename from 09-auto-persona.py"
echo "12-hydration-guard.py                - Rename from 10-hydration-guard.py"
echo "13-truth-enforcer.py                 - Rename from 11-truth-enforcer.py"
echo "14-deletion-guard.py                 - Rename from 12-deletion-guard.py"
echo "15-import-validator.py               - Rename from 13-import-validator.py"
echo "16-prd-clarity.py                    - Rename from 14-prd-clarity.py"
echo "17-implementation-guide.py           - Rename from 15-implementation-guide.py"
echo "18-python-creation-guard.py          - Rename from 16-python-creation-guard.py"
echo "19-tcpa-compliance.py                - Rename from 16-tcpa-compliance.py"
echo "20-python-dependency-tracker.py      - Rename from 17-python-dependency-tracker.py"
echo
echo "POST-TOOL-USE hooks (in order):"
echo "01-action-logger.py                  - Keep primary logger"
echo "02-state-save.py                     - Rename from 01-state-save.py"
echo "03-metrics.py                        - Rename from 02-metrics.py"
echo "04-command-logger.py                 - Rename from 03-command-logger.py"
echo "05-pattern-learning.py               - Rename from 03-pattern-learning.py"
echo "06-auto-orchestrate.py               - Rename from 03-auto-orchestrate.py"
echo "07-python-response-capture.py        - Rename from 04-python-response-capture.py"
echo "08-research-capture.py               - Rename from 04-research-capture.py"
echo "09-python-import-updater.py          - Rename from 05-python-import-updater.py"

echo
read -p "Apply this reorganization? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Reorganizing hooks..."
    
    # Pre-tool-use reorganization
    cd .claude/hooks/pre-tool-use/
    
    # Fix duplicates and reorder
    mv 01-collab-sync.py 02-collab-sync.py 2>/dev/null
    mv 02-design-check.py 03-design-check.py 2>/dev/null
    mv 03-conflict-check.py 04-conflict-check.py 2>/dev/null
    mv 04-actually-works.py 05-actually-works.py 2>/dev/null
    mv 05-code-quality.py 06-code-quality.py 2>/dev/null
    mv 06-biome-lint.py 07-biome-lint.py 2>/dev/null
    mv 07-pii-protection.py 08-pii-protection.py 2>/dev/null
    mv 08-async-patterns.py 09-async-patterns.py 2>/dev/null
    mv 08-evidence-language.py 10-evidence-language.py 2>/dev/null
    mv 09-auto-persona.py 11-auto-persona.py 2>/dev/null
    mv 10-hydration-guard.py 12-hydration-guard.py 2>/dev/null
    mv 11-truth-enforcer.py 13-truth-enforcer.py 2>/dev/null
    mv 12-deletion-guard.py 14-deletion-guard.py 2>/dev/null
    mv 13-import-validator.py 15-import-validator.py 2>/dev/null
    mv 14-prd-clarity.py 16-prd-clarity.py 2>/dev/null
    mv 15-implementation-guide.py 17-implementation-guide.py 2>/dev/null
    mv 16-python-creation-guard.py 18-python-creation-guard.py 2>/dev/null
    mv 16-tcpa-compliance.py 19-tcpa-compliance.py 2>/dev/null
    mv 17-python-dependency-tracker.py 20-python-dependency-tracker.py 2>/dev/null
    
    cd ../post-tool-use/
    
    # Keep 01-action-logger.py as primary
    mv 01-state-save.py 02-state-save.py 2>/dev/null
    mv 02-metrics.py 03-metrics.py 2>/dev/null
    mv 03-command-logger.py 04-command-logger.py 2>/dev/null
    mv 03-pattern-learning.py 05-pattern-learning.py 2>/dev/null
    mv 03-auto-orchestrate.py 06-auto-orchestrate.py 2>/dev/null
    mv 04-python-response-capture.py 07-python-response-capture.py 2>/dev/null
    mv 04-research-capture.py 08-research-capture.py 2>/dev/null
    mv 05-python-import-updater.py 09-python-import-updater.py 2>/dev/null
    
    cd ../../..
    
    echo "✅ Hooks reorganized!"
    echo
    echo "📋 New structure:"
    echo "PRE-TOOL-USE:"
    ls .claude/hooks/pre-tool-use/ | grep -E '^[0-9]{2}-.*\.py$' | sort
    echo
    echo "POST-TOOL-USE:"
    ls .claude/hooks/post-tool-use/ | grep -E '^[0-9]{2}-.*\.py$' | sort
else
    echo "❌ Reorganization cancelled"
fi
