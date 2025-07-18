# Handling Claude Compaction with Research Management

## Overview

Claude Code has context limits and will periodically need to compact conversations. This guide explains how the Research Management System (RMS) integrates with compaction handling to ensure you never lose important research context.

## How Compaction Works

### 1. Pre-Compaction Detection
The system detects when Claude is about to compact and automatically:
- Saves critical files list
- Includes relevant research documents
- Creates restoration instructions
- Preserves current task state

### 2. What Gets Saved

**Always Included:**
- CLAUDE.md (instructions)
- QUICK_REFERENCE.md (commands)
- SYSTEM_OVERVIEW.md
- Current PRD files
- Active task/bug files

**Research Documents (NEW):**
- Feature-specific research (max 2 docs)
- Recent general research (last 7 days)
- One doc per category (analysis, planning, decisions)

### 3. Post-Compaction Recovery
Run `/sr` (smart resume) after compaction to:
- Re-read all critical files
- Restore research context
- Resume exactly where you left off

## Best Practices

### Option 1: Continue in Same Session (Recommended)

```bash
# When you see compaction happening:
# 1. Let it complete
# 2. Run smart resume
/sr

# System will:
# - Detect pre-compact context
# - Re-read all critical files including research
# - Restore your working state
```

### Option 2: Start New Session

```bash
# In new Claude Code session:
/sr

# Then check research:
/research list --feature [current-feature]
/research context add --summaries
```

### Option 3: Proactive Management

```bash
# Before hitting limits:
/checkpoint              # Manual save
/compress               # Reduce context
/research context clear # Remove research temporarily
```

## Research-Specific Compaction Features

### Automatic Selection
The precompact handler now:
1. Detects current feature from git branch
2. Includes feature-specific research
3. Adds recent general research (7 days)
4. Limits to prevent overload (max 5 docs)

### Manual Override
Before compaction, you can:
```bash
# Mark specific research as critical
/research context add "auth analysis" --critical
/research context add "cache decision" --critical
```

### Post-Compaction Research
After compaction:
```bash
# Check what research was preserved
/research context

# Add more if needed
/research context add "planning doc" --summary
```

## Configuration

In `.claude/config.json`:
```json
{
  "research": {
    "precompact": {
      "auto_include": true,
      "max_docs": 3,
      "recency_days": 7,
      "prefer_feature_specific": true
    }
  }
}
```

## Common Scenarios

### Scenario 1: Mid-Feature Development
```
Working on auth feature → Compaction warning
↓
System saves:
- auth/analysis.md (feature-specific)
- auth/planning.md (feature-specific)
- decisions/cache-strategy.md (recent)
↓
After compaction → /sr
↓
All research restored automatically
```

### Scenario 2: Multiple Features
```
Switching between features → Context grows
↓
/research context clear
/research context add "current-feature" --summary
↓
Manually control what's loaded
```

### Scenario 3: Long Research Documents
```
Large analysis docs → Quick context fill
↓
Use summaries by default:
/research context add --summaries
↓
Full doc on demand:
/research show "analysis" --full
```

## Troubleshooting

### "Research not included after compaction"
```bash
# Check what was saved
cat .claude/context/pre-compact-context.json

# Manually add
/research context add "important-doc"
```

### "Too much context after resume"
```bash
# Clear and selective add
/research context clear
/research list --feature current
/research context add "specific-doc" --summary
```

### "Can't find research after compaction"
```bash
# Research persists in filesystem
/research list --all
/research search "topic"
```

## Tips for Long Sessions

1. **Monitor Context Usage**
   ```bash
   # Add to your workflow
   /context-size    # Check periodically
   ```

2. **Rotate Research**
   ```bash
   # Morning: Load planning
   /research context add "planning" --summary
   
   # Afternoon: Switch to analysis
   /research context clear
   /research context add "analysis" --summary
   ```

3. **Use Profiles**
   ```bash
   # Save research sets
   /cp save auth-research
   /cp load auth-research  # After compaction
   ```

## The Key Principle

**Research documents persist on disk** - they're never lost during compaction. The system just manages what's actively loaded in context. You can always:

1. Find past research: `/research search`
2. Load when needed: `/research context add`
3. Continue seamlessly: `/sr` after compaction

This ensures you maintain productivity even with Claude's context limits while building a searchable knowledge base over time.
