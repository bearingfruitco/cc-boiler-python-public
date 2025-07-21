# Initialize Project (Enhanced)

Initializes a new project with Claude Code, ensuring correct repository setup and creating foundational PRD.

## Usage

```bash
/init-project
/ip  # alias
```

## What It Does

1. **Verifies Repository Setup**:
   - Checks current git remote configuration
   - Confirms this is YOUR project repo (not boilerplate)
   - Offers to create GitHub repo if needed
   - Updates `.claude/project-config.json`

2. **Checks GitHub App Installation**:
   - Verifies CodeRabbit is installed
   - Verifies Claude Code App is installed
   - Provides installation links if missing

3. **Interviews you about the project**:
   - What problem are you solving?
   - Who is your target user?
   - What's your MVP scope?
   - What's your tech stack preference?

4. **Creates Project Documentation**:
   - `docs/project/PROJECT_PRD.md` - Overall vision
   - `docs/project/BUSINESS_RULES.md` - Core logic
   - `docs/project/TECH_DECISIONS.md` - Architecture
   - Updates `CLAUDE.md` with project context

5. **Sets up project structure**:
   - Creates necessary directories
   - Configures for your tech choices
   - Sets up field registry for your domain

## New Repository Check Flow

```
Claude: Let me check your repository setup...

Current git remote: https://github.com/bearingfruitco/claude-code-boilerplate.git
⚠️  WARNING: You're still pointing to the boilerplate repo!

Let's fix this:
1. What's your GitHub username? 
2. What's your repository name?
3. Does this repo exist on GitHub yet? (y/n)

[If no, offers to create it]
[If yes, updates git remote]

✓ Updated git remote to: https://github.com/YOUR_USERNAME/YOUR_REPO.git
✓ Updated .claude/project-config.json
```

## GitHub Apps Check

```
Claude: Checking GitHub App installations...

❌ CodeRabbit: Not found
   Install at: https://github.com/marketplace/coderabbit
   
❌ Claude Code: Not found  
   Install at: https://github.com/apps/claude

Please install both apps on your repository, then continue.
Continue anyway? (y/n)
```

## Updated Interview Flow

```
Claude: Great! Your repository is properly configured. 
        Now let's set up your project! 
        
        First, what are you building?
You: A quiz app for learning about tofu

Claude: Excellent! Who will use this quiz app?
You: People interested in plant-based cooking

[... rest of interview continues ...]

Claude: Creating project documentation in YOUR repo...
✓ Created docs/project/PROJECT_PRD.md
✓ Created docs/project/BUSINESS_RULES.md
✓ Created docs/project/TECH_DECISIONS.md
✓ Updated .claude/project-config.json
✓ Ready to generate GitHub issues!

Next step: Run `/gi PROJECT` to create issues in YOUR repo
```

## Project Config Format

```json
{
  "repository": {
    "owner": "YOUR_USERNAME",
    "name": "YOUR_REPO_NAME", 
    "branch": "main",
    "original_boilerplate": "bearingfruitco/claude-code-boilerplate"
  },
  "project": {
    "name": "Tofu Learning Quiz",
    "type": "Next.js Application",
    "initialized_at": "2024-12-30T10:00:00Z"
  },
  "github_apps": {
    "coderabbit": true,
    "claude_code": true,
    "checked_at": "2024-12-30T10:00:00Z"
  }
}
```

## Safety Checks

The command now:
1. NEVER creates issues in the boilerplate repo
2. ALWAYS verifies correct repository before proceeding
3. Warns if GitHub Apps aren't installed
4. Updates all configuration to point to YOUR repo
5. Creates a clear audit trail

## After Project Init

Once properly initialized:
- `/gi PROJECT` - Creates issues in YOUR repo
- `/fw start 1` - Works with YOUR repo's issues  
- All PRs go to YOUR repo
- Both AI tools review YOUR code

## Error Prevention

If someone tries to run commands before proper init:
```
❌ ERROR: Repository not properly configured!
   You're still using the boilerplate repository.
   Run /init-project to set up YOUR repository.
```

This ensures no one accidentally pollutes the boilerplate repo with their project-specific issues!
