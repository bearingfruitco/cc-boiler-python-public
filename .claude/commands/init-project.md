# Initialize Project

Initializes a new project with Claude Code, creating the foundational PRD and project context.

## Usage

```bash
/init-project
/ip  # alias
```

## What It Does

1. **Interviews you about the project**:
   - What problem are you solving?
   - Who is your target user?
   - What's your MVP scope?
   - What's your tech stack preference?

2. **Creates Project-Level Documentation**:
   - `docs/project/PROJECT_PRD.md` - Overall project vision
   - `docs/project/BUSINESS_RULES.md` - Core business logic
   - `docs/project/TECH_DECISIONS.md` - Architecture choices
   - Updates `CLAUDE.md` with project-specific context

3. **Sets up project structure**:
   - Creates necessary directories
   - Configures for your tech choices
   - Sets up field registry for your domain

4. **Generates initial feature list**:
   - Breaks down MVP into features
   - Prioritizes features
   - Creates roadmap

## Interview Flow

```
Claude: Let's set up your project! First, what are you building?
You: A quiz app for learning about tofu

Claude: Great! Who will use this quiz app?
You: People interested in plant-based cooking

Claude: What problem does it solve for them?
You: Helps them learn about tofu varieties and cooking methods

Claude: What's your MVP - the minimum to test this idea?
You: 10 quizzes about tofu, score tracking, basic progress

Claude: Technical preferences? (Next.js, database, etc.)
You: Next.js, Supabase, Tailwind

[Claude generates PROJECT_PRD.md with all this context]
```

## After Project Init

Once the project PRD exists, THEN you can:
- `/prd user-authentication` - Feature-level PRDs
- `/gt user-authentication` - Generate tasks
- `/pt user-authentication` - Process tasks

## Implementation

The command should:
1. Check if `PROJECT_PRD.md` exists
2. If not, start the interview
3. Generate comprehensive project documentation
4. Update CLAUDE.md with project context
5. Create initial feature list
6. Set up project-specific configurations

This gives Claude the full context about what you're building before diving into features!
