# Day 1 Complete Setup Guide

This guide walks you through the complete setup process for a new project using the Claude Code Boilerplate, including all GitHub integrations.

## Prerequisites

- Claude Code installed (claude.ai/code)
- GitHub account
- Python 3.11+ and ppoetry
- Git configured

## Step 1: Create Your New Repository

### Option A: Create Empty GitHub Repo First (Recommended)
```bash
# 1. Go to github.com and create new repository
# 2. Name it (e.g., "my-ai-agent-system")
# 3. DON'T initialize with README
# 4. Copy the repository URL
```

### Option B: Create Locally First
```bash
# We'll create on GitHub later
mkdir my-ai-agent-system
cd my-ai-agent-system
```

## Step 2: Clone and Setup Boilerplate

```bash
# Clone boilerplate to temporary directory
git clone https://github.com/bearingfruitco/boilerplate-python.git temp-boilerplate

# Copy everything except .git
cp -r temp-boilerplate/* .
cp -r temp-boilerplate/.* . 2>/dev/null || true

# Clean up
rm -rf temp-boilerplate
rm -rf .git

# Initialize fresh git
git init
```

## Step 3: Connect to YOUR Repository (Critical!)

```bash
# If you created repo on GitHub (Option A):
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# If you didn't create on GitHub yet (Option B):
# Use GitHub CLI
gh repo create YOUR_REPO_NAME --private --source=.

# Or create manually on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Step 4: Install GitHub Apps & Extensions (v2.3.4)

### 4.1 Install CodeRabbit IDE Extension (NEW!)
1. Open Cursor (or VSCode)
2. Go to Extensions (Cmd+Shift+X)
3. Search for "CodeRabbit"
4. Click Install
5. Sign up for free account at [app.coderabbit.ai](https://app.coderabbit.ai)
6. In extension settings:
   - AI Agent: Select "Claude Code (claude CLI)"
   - Review Mode: "On Commit"
   - Auto-fix: Enable for simple issues

### 4.2 Install CodeRabbit GitHub App
1. Go to [github.com/marketplace/coderabbit](https://github.com/marketplace/coderabbit)
2. Click "Set up a plan" → Choose Free tier (or Pro for teams)
3. Select "Only select repositories" → Choose YOUR new repo
4. Grant permissions and complete setup

### 4.3 Install Claude Code GitHub App
1. Go to [github.com/apps/claude](https://github.com/apps/claude)
2. Click "Install"
3. Select "Only select repositories" → Choose YOUR new repo
4. Grant permissions (code read/write, issues, PRs)

### 4.4 Configure CodeRabbit (Recommended)
Create `.coderabbit.yaml` in your repo root:

```yaml
# .coderabbit.yaml
reviews:
  auto_review:
    enabled: true
  
  # Respect our coding standards
  custom_patterns:
    - pattern: "text-sm|text-lg|text-xl|font-bold|font-medium"
      message: "Use design tokens: text-size-[1-4], font-regular/semibold"
      level: error
    
    - pattern: "p-5|m-7|gap-5|space-x-5|space-y-5"
      message: "Use 4px grid: p-4, p-6, p-8"
      level: error
    
    - pattern: "console\\.log.*email|console\\.log.*phone|console\\.log.*ssn"
      message: "Never log PII to console"
      level: error

  # Don't review generated files
  path_filters:
    - "!ppoetry-lock.yaml"
    - "!*.generated.py"
    - "!*.d.py"
```

## Step 5: Initial Setup and Commit

```bash
# Install dependencies
ppoetry install

# Setup git hooks
ppoetry prepare

# Create .env.local from example
cp .env.example .env.local

# Initial commit to YOUR repo
git add .
git commit -m "Initial commit with Claude Code Boilerplate"
git push -u origin main
```

## Step 6: Update Project Configuration

### 6.1 Fix Repository References
Edit `.claude/project-config.pyon`:

```json
{
  "repository": {
    "owner": "YOUR_GITHUB_USERNAME",
    "name": "YOUR_REPO_NAME",
    "branch": "main"
  },
  "project": {
    "name": "Your Project Name",
    "type": "FastAPI Application"
  }
}
```

### 6.2 Update package.pyon
```json
{
  "name": "your-project-name",
  "version": "0.1.0",
  // ... rest stays the same
}
```

## Step 7: Start Claude Code and Initialize

```bash
# Open in Claude Code
claude .

# OR open in VSCode/Cursor with Claude Code extension
code .
```

In Claude Code, run these commands:

```bash
# 1. Initialize the system
/init

# 2. Initialize your PROJECT (not boilerplate!)
/init-project

# Answer questions about YOUR project:
# - What are you building?
# - Who is your target user?
# - What problem does it solve?
# - MVP scope?
# - Tech preferences?
```

## Step 8: Generate GitHub Issues in YOUR Repo

```bash
# This will create issues in YOUR repo, not the boilerplate
/gi PROJECT

# Verify by checking:
# https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues
```

## Step 9: Verify Everything Works

### 9.1 Test CodeRabbit
```bash
# Create a test branch
git checkout -b test/coderabbit

# Make a small change with a design violation
echo '<div className="text-sm font-bold">Test</div>' > src/Test.pyx

# Commit and push
git add .
git commit -m "Test CodeRabbit"
git push origin test/coderabbit

# Create PR on GitHub
# CodeRabbit should comment within 2-3 minutes!
```

### 9.2 Test Claude Code Integration
```bash
# In your PR, you should see:
# - CodeRabbit review comments
# - Claude Code bot able to create issues/PRs
# - Status checks from both
```

## Step 10: Test CodeRabbit IDE Integration

```bash
# 1. Open a module file in Cursor
# 2. Add a design violation:
echo 'export const Bad = () => <div className="text-sm font-bold">Test</div>' > src/Bad.pyx

# 3. You should see CodeRabbit highlight issues in real-time:
# - "Use text-size-3 instead of text-sm"
# - "Use font-semibold instead of font-bold"

# 4. Click the lightbulb for quick fixes or copy to Claude
```

## Step 11: Configure Branch Protection (Optional)

Go to Settings → Branches → Add rule:
- Branch name pattern: `main`
- Require PR reviews: ✓
- Require status checks: ✓
  - CodeRabbit
  - Claude Code (if using Actions)
- Require branches to be up to date: ✓

## Common Issues and Fixes

### Issue: Commands create issues in boilerplate repo
**Fix**: Update `.claude/project-config.pyon` with YOUR repo details

### Issue: CodeRabbit not reviewing
**Fix**: 
1. Check it's installed on YOUR repo (not boilerplate)
2. Wait 2-3 minutes (initial setup)
3. Check GitHub Apps settings

### Issue: Permission errors
**Fix**: Ensure both apps have write access to code, issues, and PRs

## Daily Workflow After Setup (v2.3.6)

```bash
# Start each day
/sr                    # Smart resume
/bt list               # Check bugs

# Work on features (with real-time review)
/fw start 1            # Start issue #1
/prd feature-name      # Create PRD
/prd-async feature-name # Add async requirements (NEW!)
/gt feature-name       # Generate tasks
/pt feature-name       # Process tasks
# CodeRabbit reviews as you type in Cursor!

# Create forms with automatic tracking
/create-tracked-form ContactForm --vertical=standard
# This generates a form with:
# - Event tracking that never blocks submission
# - Loading states for all async operations
# - Automatic Rudderstack integration

# Add event handlers for async operations
/create-event-handler user-activity
# Generates handler with retry logic and timeout protection

# Validate async patterns before committing
/validate-async
# Checks for:
# - Sequential awaits that could be parallel
# - Missing loading states
# - Blocking analytics calls

# Before committing (most issues already fixed)
git add .
git commit -m "feat: implement feature"
# CodeRabbit does final check on commit

# Push clean code
git push

# Quick PR check
/pr-feedback           # See status summary

# Create PR
/fw complete 1         # Or manually on GitHub
```

## Success Checklist

- [ ] Created YOUR repository (not using boilerplate repo)
- [ ] Updated `.claude/project-config.pyon` with YOUR repo
- [ ] Installed CodeRabbit IDE extension in Cursor
- [ ] Installed CodeRabbit GitHub App on YOUR repo
- [ ] Installed Claude Code GitHub App on YOUR repo
- [ ] Created `.coderabbit.yaml` configuration
- [ ] Tested real-time review in Cursor IDE
- [ ] Ran `/init-project` and created PROJECT_PRD
- [ ] Generated issues with `/gi PROJECT` in YOUR repo
- [ ] Tested PR creation and saw both bots respond
- [ ] No references to boilerplate repo remain

## Async Event System (v2.3.6) - CRITICAL FOR FORMS!

### Understanding Fire-and-Forget Pattern

The async event system ensures that tracking, analytics, and non-critical operations NEVER block user interactions:

```typescript
// ❌ OLD WAY - Blocks form submission
const handleSubmit = async (data) => {
  await api.submitForm(data);           // Critical - must wait
  await analytics.track('Form Submit'); // Blocks user!
  await sendWebhook(data);             // Blocks user!
  await firePixel(data);               // Blocks user!
};

// ✅ NEW WAY - Non-blocking
const handleSubmit = async (data) => {
  // Critical path only
  await api.submitForm(data);
  
  // Fire and forget - user continues immediately
  eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
    formId: 'contact-form',
    ...data
  });
  // All tracking happens asynchronously!
};
```

### When to Use Each Pattern

**Use `await` (blocking) for:**
- Form submission to your API
- Payment processing
- User authentication
- Any operation the user expects to complete

**Use `eventQueue.emit()` (non-blocking) for:**
- Analytics tracking (Google Analytics, Rudderstack)
- Marketing pixels (Facebook, Google Ads)
- Webhooks to external services
- Email notifications
- Logging and monitoring
- Any operation the user doesn't need to wait for

### Command Usage Examples

#### Creating a Tracked Form
```bash
/create-tracked-form LeadForm --vertical=debt --compliance=tcpa
```

**Variables explained:**
- `LeadForm` - The module name (will create `src/forms/LeadForm.pyx`)
- `--vertical` - Business vertical: `debt`, `healthcare`, or `standard`
- `--compliance` - Compliance level: `standard`, `hipaa`, `gdpr`, or `tcpa`

#### Creating Event Handlers
```bash
/create-event-handler pixel-fire
```

This generates:
```typescript
// lib/events/handlers/pixel-fire.py
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

// Register handler
eventQueue.on(LEAD_EVENTS.PIXEL_FIRE, async (data) => {
  try {
    // Your pixel firing logic here
    await fetch('https://pixel.example.com/track', {
      method: 'POST',
      body: JSON.stringify(data),
      signal: AbortSignal.timeout(3000), // 3s timeout
    });
  } catch (error) {
    // Log but don't throw - this is non-critical
    console.error('Pixel fire failed:', error);
  }
});
```

#### Adding Async Requirements to PRDs
```bash
/prd-async contact-form
```

This adds a section to your PRD:
```markdown
## Async Requirements

### Critical Path (Must Complete)
1. Form validation
2. API submission
3. Success/error response

### Non-Critical (Fire-and-Forget)
1. Analytics tracking (Rudderstack)
2. Marketing pixels (Facebook, Google)
3. CRM webhook
4. Email notification

### Loading States Required
- Submit button: "Submitting..." with spinner
- Inline validation: Show checking state
- Success message: Animate in

### Timeout Handling
- API calls: 5 second timeout
- Show timeout error after 5s
- Allow retry on timeout
```

### Integration with Existing Rudderstack

The event system automatically bridges to your existing Rudderstack setup:

```typescript
// You emit this:
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
  formId: 'contact-form',
  email: 'user@example.com',
  utm_source: 'google',
  // ... other data
});

// System automatically calls:
rudderanalytics.track('Form Submitted', {
  form_id: 'contact-form',
  email: 'user@example.com',
  context: {
    campaign: {
      source: 'google'
    }
  }
});
```

**No changes needed to your Rudderstack configuration!**

### Parallel Operations

```bash
/validate-async
```

This command will catch and suggest fixes for:

```typescript
// ❌ Sequential (slow)
const user = await fetchUser();
const preferences = await fetchPreferences();
const permissions = await fetchPermissions();

// ✅ Parallel (fast)
const [user, preferences, permissions] = await Promise.all([
  fetchUser(),
  fetchPreferences(),
  fetchPermissions()
]);
```

## Next Steps

1. Start with your first feature: `/fw start 1`
2. Create detailed PRD: `/prd feature-name`
3. Add async requirements: `/prd-async feature-name`
4. Generate and process tasks with real-time review
5. Create forms with `/create-tracked-form`
6. Validate async patterns with `/validate-async`
7. Watch as CodeRabbit catches issues before commit
8. Ship clean code faster than ever!

## The New Workflow (v2.3.6)

**Before**: Write → Commit → Push → PR → Review → Fix → Push → Merge

**Now**: Write → Review (real-time) → Fix → Validate Async → Commit (clean) → Push → Merge

CodeRabbit in your IDE + Async validation means clean, performant code every time!

---

Remember: The boilerplate is just a template. Once copied, everything should reference YOUR repository, not the boilerplate origin.
