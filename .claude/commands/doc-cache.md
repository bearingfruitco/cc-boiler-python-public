# Documentation Cache Command

Cache and index external documentation locally for instant access without repeated API calls.

## Arguments:
- $ACTION: cache|list|search|clear|update|show
- $ARGUMENTS: Documentation to cache or search

## Actions:

### CACHE - Save documentation locally
```bash
/doc-cache cache "React 19 hooks"
/doc-cache cache "Next.js 15 App Router" --sections "routing,layouts"
/doc-cache cache https://react.dev/reference/react/hooks --depth 2
```

Process:
1. Searches via MCP (context7, web_search)
2. Fetches relevant documentation
3. Parses and indexes content
4. Stores locally with metadata
5. Creates searchable index

### LIST - Show cached documentation
```bash
/doc-cache list
```

Output:
```
=== CACHED DOCUMENTATION ===

📚 React 19 Hooks (245KB)
   Source: react.dev
   Cached: 2 hours ago
   Sections: 15
   Usage: 12 times

📚 Next.js 15 App Router (189KB)
   Source: nextjs.org  
   Cached: Yesterday
   Sections: 8
   Usage: 5 times

📚 Supabase Auth Guide (67KB)
   Source: supabase.com
   Cached: 3 days ago
   Sections: 4
   Usage: 2 times

Total: 501KB cached | 3 sources | 27 sections
💡 Search with: /doc-cache search "query"
```

### SEARCH - Find in cached docs
```bash
/doc-cache search "useEffect cleanup"
/doc-cache search "parallel routes" --source nextjs
```

Returns relevant snippets with context

### SHOW - Display cached content
```bash
/doc-cache show "React 19 hooks" --section "useEffect"
```

### UPDATE - Refresh cached docs
```bash
/doc-cache update "React 19 hooks"
/doc-cache update --all  # Update all cached docs
```

### CLEAR - Remove cached docs
```bash
/doc-cache clear "old-library"
/doc-cache clear --older-than 30d
/doc-cache clear --all
```

## Smart Features:

### 1. Auto-Cache from PRD
When PRD includes documentation requirements:
```markdown
## 8. Documentation Requirements
- React 19 concurrent features
- Next.js 15 server components
- Supabase real-time subscriptions
```

Automatically prompts:
```
📚 Found 3 documentation requirements in PRD
   Cache them now? (y/n)
> y
Caching documentation...
✅ Cached 3 sources (412KB)
```

### 2. Context-Aware Suggestions
Based on current file:
```
💡 Working with authentication?
   Suggested docs to cache:
   - Next-Auth v5 configuration
   - Supabase Auth helpers
   Cache suggested? (y/n)
```

### 3. Offline Access
All cached docs work offline:
```
🔌 No internet connection
✅ Using cached documentation (3 days old)
```

### 4. Version Tracking
```bash
/doc-cache list --versions
```

Shows:
```
React Hooks:
  - v19.0.0 (current)
  - v18.2.0 (archived)
```

## Storage Structure:
```
.claude/doc-cache/
  ├── index.json           # Searchable index
  ├── metadata.json        # Cache metadata
  ├── sources/
  │   ├── react-dev/
  │   │   ├── hooks.md
  │   │   └── meta.json
  │   ├── nextjs-org/
  │   └── supabase-com/
  └── archives/           # Old versions
```

## Integration with Research Docs:

Enhanced `/research-docs` command:
```bash
/research-docs "React, Next.js" --cache
```

This now:
1. Searches documentation
2. Automatically caches results
3. Creates PRD section with links
4. Indexes for future use

## Cache Entry Format:
```typescript
interface CachedDoc {
  id: string;
  source: string;
  url: string;
  title: string;
  sections: {
    name: string;
    content: string;
    examples: string[];
  }[];
  metadata: {
    cachedAt: string;
    version: string;
    size: number;
    usage: number;
    lastAccessed: string;
  };
  index: {
    keywords: string[];
    snippets: Map<string, string>;
  };
}
```

## Automatic Cleanup:
- Removes docs unused for 30+ days
- Alerts before clearing large caches
- Maintains version history
- Compresses old documentation

## Quick Access:
During development, inline search:
```
Working on useEffect...
💡 Found in cache: "useEffect cleanup patterns"
View? (y/n)
```

## Benefits:
- No repeated API calls
- Instant documentation access  
- Works offline
- Version-specific docs
- Searchable snippets
- Reduced context pollution
