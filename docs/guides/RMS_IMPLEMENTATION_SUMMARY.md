# Research Management System (RMS) - Implementation Summary

## Problem Solved
Claude Code creates valuable research/planning documents that become orphaned clutter in the codebase. RMS organizes, updates, and integrates these documents into your workflow.

## Key Features

### 1. **Smart Document Updates** (Not Just Organization)
- Detects when Claude is updating existing research
- Intelligently merges based on document type:
  - **Analysis**: Appends findings, updates recommendations
  - **Planning**: Adds change logs, tracks evolution
  - **Decisions**: Preserves original, adds implementation notes
- Prevents duplicate documents (auth-analysis-v1, v2, v3, final, final-final...)
- Maintains version history

### 2. **Context-Aware Loading**
To prevent overload:
- **Manual inclusion by default**: `auto_include: false`
- **Strict limits**: Max 2 docs, 10KB total
- **Summaries only**: Full docs on demand
- **Feature-specific**: Only loads relevant research
- **Recency filter**: Last 7 days only

### 3. **Integration Points**
- `/sr` - Includes relevant research summaries
- `/fw` - Loads feature-specific docs
- PRDs - Can reference research
- Context profiles - Can include research sets

## Implementation Details

### Hook Configuration
```python
# .claude/hooks/post-tool-use/04-research-capture.py
- Detects new .md files
- Checks for existing similar docs
- Prompts for update vs create
- Merges intelligently
- Updates index
```

### Commands
```bash
/research review      # Organize pending docs
/research update      # Update existing research  
/research search      # Find past research
/research context     # Add to current session
/research history     # See version history
```

### Directory Structure
```
.claude/research/
├── active/          # Current research
│   └── features/    # One doc per topic (updated)
├── archive/         # Old versions preserved
├── templates/       # Consistent formats
└── index.json      # Searchable, versioned
```

## Context Management Safeguards

### Configuration (Conservative)
```json
{
  "research": {
    "auto_capture": true,       // Detect docs
    "auto_include": false,      // Manual context inclusion
    "max_context_docs": 2,      // Reduced from 3
    "max_doc_size_kb": 5,       // Small docs only
    "summary_only": true,       // Not full content
    "include_recent_only": 7    // Days
  }
}
```

### Smart Loading
```python
def should_include_research(context_size):
    if context_size > 50000:  # 50KB limit
        return []
    
    # Only current feature, last 7 days, summaries only
    return get_relevant_summaries(max=2)
```

## Benefits

1. **Clean Codebase**: No more scattered .md files
2. **Single Source of Truth**: Updates existing docs vs creating new
3. **Version History**: See how thinking evolved
4. **Searchable Knowledge**: Find past decisions
5. **Context Preservation**: Without overload

## Workflow Example

```bash
# Day 1: Initial research
Claude creates: ./auth-analysis.md
Hook prompts → Move to research/features/auth/

# Day 5: Updated research  
Claude creates: ./auth-oauth-analysis.md
Hook detects UPDATE → Merges into existing
No duplicates!

# Day 10: Working on feature
/sr
> Including research summary (500 chars)
> Full doc: /research show "auth analysis"
```

## Key Principle

Research documents are **living artifacts** that evolve with understanding. RMS ensures one source of truth per topic while preserving history - solving both the clutter problem and the conflicting documents problem.