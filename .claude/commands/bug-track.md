# Bug Track Command

Track and manage bugs persistently across sessions with automatic GitHub sync.

## Arguments:
- $ACTION: add|resolve|list|update|search
- $ARGUMENTS: Additional arguments based on action

## Actions:

### ADD - Record a new bug
```bash
/bug-track add "Component render issue with props in AuthForm"
```

Creates entry:
```json
{
  "id": "bug_1234",
  "timestamp": "2024-01-15T10:30:00Z",
  "description": "Component render issue with props in AuthForm",
  "status": "open",
  "file": "components/auth/AuthForm.tsx",
  "line": null,
  "session": "sr_session_123",
  "user": "shawn",
  "tags": ["render", "props", "auth"]
}
```

### RESOLVE - Mark bug as fixed
```bash
/bug-track resolve bug_1234 "Fixed by updating prop types"
```

Updates entry with:
- resolution
- resolved_at timestamp
- resolved_by user
- fix_commit (if available)

### LIST - Show bugs
```bash
/bug-track list                    # All open bugs
/bug-track list --all             # All bugs
/bug-track list --resolved        # Resolved only
/bug-track list --tag auth        # By tag
/bug-track list --file AuthForm   # By file
```

### UPDATE - Add information
```bash
/bug-track update bug_1234 --file components/auth/AuthForm.tsx --line 45
/bug-track update bug_1234 --tag security
/bug-track update bug_1234 --note "Also affects RegisterForm"
```

### SEARCH - Find bugs
```bash
/bug-track search "render"        # Search descriptions
/bug-track search --similar       # Find similar to current error
```

## Implementation:

1. **Storage Location**
   ```
   .claude/bugs/
     ├── active.json      # Currently open bugs
     ├── resolved.json    # Fixed bugs  
     └── archive/         # Old bugs by month
   ```

2. **GitHub Sync**
   - Auto-syncs to secret gist every 10 bugs
   - Gist name: `claude-bugs-{project-name}.json`
   - Restored on `/sr` automatically

3. **Integration with Hooks**
   - Error hook auto-creates bug entries
   - Links bugs to checkpoints
   - Shows related bugs in context

4. **Bug Entry Format**
   ```typescript
   interface Bug {
     id: string;
     timestamp: string;
     description: string;
     status: 'open' | 'resolved' | 'wontfix';
     file?: string;
     line?: number;
     error_message?: string;
     stack_trace?: string;
     session: string;
     user: string;
     tags: string[];
     notes: string[];
     resolution?: string;
     resolved_at?: string;
     resolved_by?: string;
     fix_commit?: string;
     related_bugs?: string[];
   }
   ```

5. **Auto-Detection**
   When errors occur, prompt:
   ```
   🐛 Error detected! Track this bug? (y/n)
   > y
   Bug tracked: bug_1234
   ```

6. **Context Integration**
   Before working on a file, check:
   ```
   📋 3 open bugs in this file:
   - bug_1234: Render issue with props
   - bug_1235: Memory leak in useEffect
   - bug_1236: Type mismatch in API call
   ```

## Display Format:

```
=== BUG TRACKER ===
Open: 5 | Resolved: 23 | This Session: 2

🔴 OPEN BUGS:
[bug_1234] Component render issue with props in AuthForm
  📁 components/auth/AuthForm.tsx:45
  🏷️  render, props, auth
  👤 shawn | 2 hours ago

[bug_1235] Memory leak in dashboard useEffect  
  📁 components/dashboard/Dashboard.tsx
  🏷️  performance, memory
  👤 nikki | 1 day ago
  
💡 Run: /bug-track list --all for complete history
```

## Benefits:
- Never lose track of known issues
- Avoid fixing the same bug twice
- Build knowledge base over time
- Perfect handoffs with bug context
- Automatic pattern detection
