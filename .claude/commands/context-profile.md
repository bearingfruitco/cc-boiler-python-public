# Context Profile Command

Manage context profiles for different work modes to optimize context window usage.

## Arguments:
- $ACTION: create|load|save|list|delete|show
- $PROFILE_NAME: Name of the profile

## Why Context Profiles?

Different tasks need different context. Loading everything wastes context window space and increases hallucination risk. Profiles let you instantly switch between focused contexts.

## Actions:

### CREATE - New profile from current context
```bash
/context-profile create "auth-work"
```

Saves current state:
- Open files
- Active documentation
- Loaded commands
- Current checkpoint
- Active persona

### SAVE - Update existing profile
```bash
/context-profile save "auth-work"
```

### LOAD - Switch to profile
```bash
/context-profile load "frontend-ui"
```

This will:
1. Save current context as "last-context"
2. Clear non-essential files
3. Load profile's files and docs
4. Set appropriate persona
5. Show profile summary

### LIST - Show available profiles
```bash
/context-profile list
```

Output:
```
=== CONTEXT PROFILES ===

📦 auth-work (324KB)
   Files: 12 | Docs: 3 | Commands: 8
   Last used: 2 hours ago
   Focus: Authentication implementation

📦 frontend-ui (256KB)  
   Files: 8 | Docs: 2 | Commands: 6
   Last used: Yesterday
   Focus: Component development

📦 bug-fixing (412KB)
   Files: 15 | Docs: 4 | Commands: 10
   Last used: 3 days ago
   Focus: Debugging and fixes

💡 Load with: /context-profile load [name]
```

### SHOW - Display profile contents
```bash
/context-profile show "auth-work"
```

### DELETE - Remove profile
```bash
/context-profile delete "old-profile"
```

## Profile Structure:

```typescript
interface ContextProfile {
  name: string;
  created: string;
  lastUsed: string;
  description: string;
  context: {
    files: string[];           // Open files
    documentation: string[];   // Active docs
    commands: string[];        // Frequently used commands
    checkpoint: string;        // Associated checkpoint
    persona: string;          // Active persona
    bugFilters: string[];     // Bug tracking filters
    workingDirectory: string;
  };
  stats: {
    totalSize: number;        // Context size in tokens
    fileCount: number;
    docCount: number;
  };
}
```

## Pre-built Profiles:

### 1. Frontend UI Work
```bash
/context-profile load "preset:frontend"
```
- Loads: Component library, design system, UI commands
- Persona: frontend
- Excludes: Backend, database docs

### 2. Backend API Work  
```bash
/context-profile load "preset:backend"
```
- Loads: API routes, database schemas, auth logic
- Persona: backend
- Excludes: UI components, styles

### 3. Bug Fixing Mode
```bash
/context-profile load "preset:debug"
```
- Loads: Bug tracker, error logs, test files
- Persona: qa
- Includes: All recent error locations

### 4. Documentation Mode
```bash
/context-profile load "preset:docs"
```
- Loads: All documentation, README files
- Persona: mentor
- Excludes: Implementation files

### 5. Security Audit
```bash
/context-profile load "preset:security"
```
- Loads: Security configs, auth files, field registry
- Persona: security
- Includes: Compliance docs

## Smart Features:

### Auto-Switch Suggestions
```
🔄 Switching from backend to UI work?
   Suggested profile: "frontend-ui"
   Load now? (y/n)
```

### Context Size Warning
```
⚠️ Current context: 82% full
   Recommend switching to focused profile
   Suggested: "backend-api" (45% size)
```

### Profile Inheritance
```bash
/context-profile create "auth-ui" --extends "frontend-ui"
```
Inherits base profile plus additions

## Storage:
```
.claude/profiles/
  ├── active.json         # Current profile
  ├── profiles.json       # All profiles
  └── presets/           # Built-in profiles
```

## Integration:

- **With Checkpoints**: Each checkpoint can reference a profile
- **With Bug Tracker**: Profiles can include bug filters  
- **With Orchestration**: Agents load appropriate profiles
- **With Smart Resume**: Restores last profile automatically

## Context Window Optimization:

Shows real-time context usage:
```
📊 Context Window Status:
   Used: 45,231 / 100,000 tokens (45%)
   Files: 12 (5.2K tokens)
   Docs: 3 (8.1K tokens)  
   System: 2.1K tokens
   Available: 54,769 tokens
```

## Quick Switch:
```bash
/cp frontend    # Shorthand for context-profile load
```
