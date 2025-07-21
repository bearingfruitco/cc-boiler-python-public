# AI Assistant MCP Instructions for FreshSlate

## IMPORTANT: Use MCP Tools When Available

When working on this project, **always check if MCP tools are available** and use them for:

### 1. **Supabase MCP** - For Database Operations
```
Instead of writing SQL for me to run, use Supabase MCP to:
- Query database tables
- Check schema structure
- Create/modify tables
- Insert/update data
- Test queries directly
- Verify data relationships
```

### 2. **GitHub MCP** - For Version Control
```
When you need to:
- Check git status
- Create branches
- Commit changes
- Push to remote
- Create pull requests
- Check commit history
```

**Note**: Claude Code already has direct file system access, so you can read/write files directly without needing MCP for that.

## Example MCP Usage

### ❌ DON'T DO THIS:
```
"Here's the code for your new component. Please create a file at components/NewComponent.tsx and paste this code..."
```

### ✅ DO THIS:
```
"I'll create the component directly using GitHub MCP..."
[Actually creates the file using MCP]
"Done! I've created components/NewComponent.tsx with the design system compliant code."
```

### ❌ DON'T DO THIS:
```
"To check your database schema, run this SQL query:
SELECT * FROM information_schema.tables..."
```

### ✅ DO THIS:
```
"Let me check your database schema using Supabase MCP..."
[Executes query directly]
"I can see you have the following tables: leads, partners, users..."
```

## Quick Start Message for AI Assistants

When starting work on FreshSlate, include this in your first message:

```
I'm working on FreshSlate with Claude Code. Please note:

1. I have direct file system access - I'll read/write files directly
2. Use Supabase MCP to query the database instead of giving me SQL to run
3. Use GitHub MCP for version control operations
4. Follow the design system strictly (4 sizes, 2 weights, 4px grid)

Can you confirm you have access to Supabase MCP?
```

## MCP Tool Benefits

Using MCP tools means:
- **Faster Development**: Direct file creation/modification
- **Fewer Errors**: No copy/paste mistakes
- **Real-time Verification**: Can check database state immediately
- **Better Context**: Can read actual project structure
- **Immediate Testing**: Can verify changes work correctly

## If MCP Tools Aren't Available

Only if MCP tools are not available:
1. For database operations: Provide SQL queries for manual execution
2. For git operations: Provide git commands to run in terminal

But always **check for MCP availability first**!

## Remember

- Claude Code = Direct file system access (no MCP needed)
- Supabase MCP = Direct database access (use this!)
- GitHub MCP = Git operations (if available)
- The goal is direct manipulation, not instruction giving