# Research Management Command

Organize, search, and manage internal research/planning documents created during development.

## Arguments:
- $ACTION: review|search|list|context|update|history|new|archive
- $ARGUMENTS: Varies by action

## Actions

### Review Pending Documents
```bash
/research review

# Shows documents detected by hooks
# Lets you categorize and organize them
# Detects if updating existing docs
```

### Update Existing Research
```bash
/research update "authentication analysis"
# Opens existing doc for editing

/research update --feature user-auth
# Updates all docs for a feature
```

### Search Research
```bash
/research search "authentication"
/research search "performance analysis"
/research search --type decision "cache"
```

### List Research
```bash
/research list
/research list --feature user-auth
/research list --type analysis
/research list --archived
```

### Add to Context
```bash
/research context                    # Show what's in context
/research context add "auth analysis" # Add specific doc
/research context clear              # Clear research from context
/research context --summaries        # Add summaries only
```

### View History
```bash
/research history "auth analysis"
# Shows all versions with diffs

/research rollback "auth analysis" --version 2
# Restore previous version
```

### Create New Research
```bash
/research new analysis "Feature Name"
/research new planning "Sprint Planning"
/research new decision "Cache Strategy"
```

### Archive Research
```bash
/research archive "old-feature"
/research archive --older-than 30d
```

## How It Works

### Detection
Post-tool-use hook detects when Claude creates:
- Analysis documents
- Planning documents
- Architecture decisions
- Research findings

### Organization
```
.claude/research/
├── active/
│   ├── features/
│   │   └── user-auth/
│   │       └── analysis.md      # Living document
│   ├── analysis/
│   ├── planning/
│   └── decisions/
├── archive/
│   └── versions/                # Previous versions
├── templates/
└── index.json                   # Searchable index
```

### Smart Updates
When new research is created:
1. Checks for existing similar documents
2. Prompts to update or create new
3. Merges intelligently by type
4. Preserves version history

## Examples

### Typical Workflow
```bash
# Claude creates research doc
# Hook detects and prompts

# Review pending
/research review
> 1. auth-analysis.md - Authentication Analysis
> Choose: [U]pdate existing, [N]ew document, [S]kip

# Search later
/research search "JWT"
> Found in: active/features/auth/analysis.md (v3)
> "JWT tokens provide stateless auth..."

# Add to context when needed
/research context add "auth analysis" --summary
> Added summary (500 chars) to context
```

### Feature Development
```bash
# Start feature
/fw start 123

# Research automatically available
/sr
> Including research: auth/analysis.md (summary)

# Update research
/research update "auth analysis"
> Opening for edit...
> Will merge changes intelligently
```

## Context Management

### Conservative Defaults
```json
{
  "research": {
    "auto_include": false,    // Manual control
    "max_context_docs": 2,    // Very limited
    "summary_only": true,     // Not full docs
    "include_recent_only": 7  // Days
  }
}
```

### Smart Loading
- Only loads research for current feature
- Summaries by default (500 chars)
- Full docs on explicit request
- Won't load if context > 50KB

## Document Types

### Analysis
- Research findings
- Technical investigations
- Performance analysis
- Security reviews

### Planning
- Feature planning
- Sprint planning
- Architecture proposals
- Implementation plans

### Decisions
- Architecture Decision Records (ADRs)
- Technology choices
- Design decisions
- Trade-off documentation

### Findings
- Bug investigations
- Performance findings
- User research
- Market analysis

## Automatic Features

### Smart Document Updates
When Claude creates a research document:
1. **Checks for existing docs** with similar title/feature
2. **Merges intelligently** based on document type:
   - **Analysis**: Appends new findings, updates recommendations
   - **Planning**: Tracks changes, updates phases with change log
   - **Decisions**: Preserves original decision, adds implementation notes
3. **Versions automatically** - Never loses previous work
4. **Prevents duplicates** - One source of truth per topic

### Version History
```bash
/research history "auth analysis"
# Shows all versions with diffs

/research rollback "auth analysis" --version 2
# Restore previous version
```

### Context Awareness
- Knows current feature context
- Suggests related research
- Auto-includes in `/sr`

### PRD Integration
```markdown
## Technical Approach
Based on research in `.claude/research/features/auth/analysis.md`:
- JWT provides stateless auth
- Refresh token rotation recommended
- See full analysis: `/research show "auth analysis"`
```

## Templates

### Analysis Template
```markdown
# [Feature] Analysis

## Summary
Brief overview of findings

## Key Findings
1. Finding one
2. Finding two

## Recommendations
- Recommendation one
- Recommendation two

## Next Steps
- [ ] Action item
```

### Decision Template
```markdown
# ADR-001: [Decision Title]

## Status
Accepted

## Context
Why this decision is needed

## Decision
What we decided

## Consequences
- Positive: 
- Negative:
- Neutral:
```

## Benefits

1. **No More Clutter**: Research organized automatically
2. **Always Available**: Retrieved when needed
3. **Context Aware**: Linked to features/PRDs
4. **Searchable**: Find past research easily
5. **Team Knowledge**: Shared research base
6. **Single Source of Truth**: Updates existing docs instead of creating duplicates
7. **Version Control**: Track how thinking evolved

## Configuration

In `.claude/config.json`:
```json
{
  "research": {
    "auto_capture": true,
    "archive_after_days": 30,
    "templates_enabled": true,
    "auto_include": false,
    "max_context_docs": 2
  }
}
```

## Workflow Example

```bash
# Claude creates initial research
# Creates: ./user-auth-analysis.md
# Hook detects it's NEW

# Later...
/research review
> 1. user-auth-analysis.md - Authentication Analysis
> Move to research/features/user-auth/

# Days later, Claude updates the analysis
# Creates: ./authentication-updated-analysis.md
# Hook detects it's an UPDATE

> 📝 Research Document Update Detected
> Existing: research/features/user-auth/analysis.md
> Would you like to:
> 1. Update existing (merge changes)
> 2. Create new version

# Choose 1 - Merges intelligently
# Original analysis preserved with new findings added

# When working on auth:
/fw start 124  # Auth feature
# Latest merged research automatically included!

# Check history:
/research history "auth analysis"
> v3 - 2025-01-17 (current) - Added OAuth findings
> v2 - 2025-01-15 - Updated recommendations
> v1 - 2025-01-14 - Initial analysis
```

This integrates seamlessly with your existing workflow while solving the orphaned document problem!
