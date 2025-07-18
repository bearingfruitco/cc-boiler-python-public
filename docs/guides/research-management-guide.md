# Research Management System (RMS) Guide

## Overview

The Research Management System solves the problem of research and planning documents becoming orphaned clutter in your codebase. Instead of having multiple versions of the same analysis scattered around (auth-v1.md, auth-v2.md, auth-final.md), RMS organizes and updates documents intelligently.

## The Problem It Solves

**Before RMS:**
```
project/
├── user-auth-analysis.md         # What is this?
├── user-auth-analysis-v2.md     # Is this newer?
├── auth-analysis-updated.md      # Or is this?
├── payment-planning-v2.md        # Which version is current?
├── cache-decision-final.md       # Final... or is there final-final?
├── performance-findings.md       # Never referenced again
└── src/                          # Actual code mixed with docs
```

**After RMS:**
```
project/
├── .claude/research/
│   ├── active/
│   │   ├── features/
│   │   │   └── user-auth/
│   │   │       └── analysis.md   # Single, updated document (v3)
│   │   └── decisions/
│   │       └── cache-strategy.md # One source of truth
│   └── archive/
│       └── versions/             # Previous versions preserved
└── src/                          # Clean codebase
```

## How It Works

### 1. Automatic Detection & Updates

When Claude Code creates a markdown file, the post-tool-use hook:
- Analyzes content for research indicators
- **Checks for existing similar documents**
- Detects document type (analysis, planning, decision, etc.)
- Extracts feature context and keywords
- **Prompts to update or create new**

**Update Logic by Type:**
- **Analysis**: Appends new findings, updates recommendations
- **Planning**: Adds change log, updates phases
- **Decisions**: Preserves decision, adds implementation notes
- **Findings**: Appends with timestamps

### 2. Organization

Documents are organized by:
- **Type**: analysis, planning, decision, findings
- **Feature**: Linked to current git branch/feature
- **Status**: active or archived
- **Version**: Full history preserved

### 3. Context Management

RMS respects context limits:
- **Manual inclusion by default** (`auto_include: false`)
- **Max 2 docs** in context at once
- **Summaries only** (500 chars) unless full doc requested
- **Feature-specific** - only loads relevant research
- **Recent only** - last 7 days by default

## Commands

### Review Pending Documents
```bash
/research review
```
Shows documents detected by hooks and lets you organize them.

### Search Research
```bash
/research search "authentication"
/research search "JWT" --type analysis
/research search --feature user-auth
```

### Update Existing Research
```bash
/research update "auth analysis"
# Opens existing doc for intelligent merging

/research update --feature user-auth
# Updates all docs for a feature
```

### Add to Context
```bash
/research context                    # Show what's in context
/research context add "auth analysis" # Add specific doc
/research context add --summaries    # Add summaries only
/research context clear              # Remove from context
```

### View History
```bash
/research history "auth analysis"
# Shows all versions with changes

/research rollback "auth analysis" --version 2
# Restore previous version
```

### List Research
```bash
/research list                       # All active research
/research list --feature user-auth   # Feature-specific
/research list --type decision       # By document type
/research list --archived            # Include archived
```

## Workflow Examples

### Example 1: Feature Development with Updates

```bash
# Start new feature
/fw start 123

# Claude creates initial analysis
# Creates: ./authentication-analysis.md

# Hook detects it (NEW document)
> Research document detected: Authentication Analysis

# Review and organize
/research review
> Move to research/features/auth/analysis.md

# Week later, Claude updates the analysis
# Creates: ./auth-analysis-oauth.md

# Hook detects it (UPDATE to existing)
> 📝 Research Document Update Detected
> Existing: research/features/auth/analysis.md
> 1. Update existing (merge changes)
> 2. Create new version

# Choose 1 - Intelligently merges
# Original preserved, new findings added
# No duplicate files!

# When resuming
/sr
> Found 1 research document (v3, updated today)
> - auth/analysis.md - Now includes OAuth findings
```

### Example 2: Architecture Decision

```bash
# Create decision document
# Creates: ./cache-strategy-decision.md

# Hook detects
> Research document detected: Cache Strategy Decision

# Organize
/research review
> Move to research/decisions/cache-strategy.md

# Later, add implementation notes
# Creates: ./cache-implementation-notes.md

# Hook detects UPDATE
> This appears to update: decisions/cache-strategy.md
> 1. Add implementation notes (preserve decision)

# Original decision preserved, notes added
```

### Example 3: Sprint Planning

```bash
# Create planning doc
# Creates: ./sprint-23-planning.md

# Review
/research review
> Move to research/planning/sprint-23.md

# Search later
/research search "API redesign"
> Found in: planning/sprint-23.md
> "...considering API redesign in phase 2..."
```

## Best Practices

### 1. Let Claude Create Research
Don't discourage Claude from creating analysis/planning docs - they're valuable! RMS will organize them.

### 2. Use Descriptive Titles
Helps the system detect updates:
- Good: "User Authentication Analysis"
- Bad: "Notes" or "Research"

### 3. Review Regularly
```bash
/research review  # Check weekly
```

### 4. Use Templates
```bash
/research new planning "Feature Name"
# Creates structured document with sections
```

### 5. Check History Before Major Changes
```bash
/research history "auth analysis"
# See how thinking evolved
```

### 6. Archive Completed Work
```bash
/fw complete 123
# Prompts: Archive related research? [Y/n]
```

## Configuration

The system uses conservative defaults to prevent context overload:

```json
{
  "research": {
    "auto_capture": true,        // Detect documents
    "auto_include": false,       // Manual context control
    "archive_after_days": 30,    // Auto-archive old docs
    "max_context_docs": 2,       // Very limited
    "max_doc_size_kb": 5,        // Small docs only
    "summary_only": true,        // Not full content
    "include_recent_only": 7,    // Days
    "search_preview_length": 200,
    "auto_link_features": true,
    "templates": [
      "analysis",
      "planning", 
      "decision",
      "findings"
    ]
  }
}
```

## Document Types

### Analysis Documents
- Technical investigations
- Performance analysis
- Security reviews
- Feature analysis

**Merge behavior**: Appends new findings, updates recommendations

### Planning Documents
- Sprint planning
- Feature planning
- Implementation plans
- Architecture proposals

**Merge behavior**: Adds change log, updates phases

### Decision Documents (ADRs)
- Architecture Decision Records
- Technology choices
- Design decisions

**Merge behavior**: Preserves original decision, adds implementation notes

### Findings Documents
- Bug investigations
- User research
- Performance findings

**Merge behavior**: Appends with timestamps

## Integration with Other Systems

### PRDs
Reference research in PRDs:
```markdown
## Technical Approach
Based on research in `.claude/research/features/auth/analysis.md`:
- JWT provides stateless auth
- Refresh token rotation recommended
```

### Context Profiles
Save research sets:
```bash
/cp save auth-work
# Includes current research docs
```

### Smart Resume
```bash
/sr
# Shows if relevant research exists
# Suggests: /research context
```

### Compaction Handling
Research is automatically preserved during Claude's context compaction:
- PreCompact hook includes relevant research (max 3-5 docs)
- Feature-specific research prioritized
- Recent docs (7 days) included
- After compaction: `/sr` restores everything

See [Compaction Handling Guide](compaction-handling-guide.md) for details.

## Benefits

1. **Clean Codebase**: No scattered .md files
2. **Single Source of Truth**: One doc per topic, continuously updated
3. **Version History**: See how thinking evolved
4. **Searchable Knowledge**: Find past decisions
5. **Context Aware**: Only loads what's relevant
6. **Team Knowledge**: Shared research base

## Troubleshooting

### Research Not Detected as Update
- Ensure similar title/topic
- Must be for same feature
- Check existing docs: `/research list --feature X`

### Merge Conflicts
```bash
/research conflicts "auth analysis"
# Shows sections that need manual review

/research merge --manual "auth analysis"
# Opens side-by-side merge tool
```

### Can't Find Old Research
```bash
/research list --all  # Including archived
/research search --archived "keyword"
```

### Context Overload
```bash
/research context clear
/research context add --summaries  # Summaries only
```

## Advanced Usage

### Bulk Operations
```bash
/research archive --older-than 30d
/research archive --feature old-feature
```

### Export Research
```bash
/research export --format markdown
/research export --feature auth --format pdf
```

### Research Metrics
```bash
/research stats
> Total documents: 42
> Active: 15
> Updates per doc: 3.2 avg
> Most updated: auth/analysis.md (8 versions)
```

## The Philosophy

Research documents are **living artifacts** in AI-assisted development. They should evolve with your understanding, not multiply into confusion. RMS ensures:

1. **Single Source of Truth** - One document per topic, continuously updated
2. **Historical Context** - See how decisions evolved over time
3. **Clean Workspace** - No more duplicate/versioned files
4. **Intelligent Merging** - Updates preserve important history

Remember: The goal isn't to prevent research creation, but to **organize and evolve it effectively**.
