# Claude Code AI Agent Documentation & Implementation Guide

## 🚀 Executive Summary

This documentation enables AI agents (Claude Code, Cursor, etc.) to implement a revolutionary development system that achieves:
- **70% faster development** through PRD-driven task decomposition
- **Zero design violations** via automated enforcement
- **Perfect team coordination** with multi-agent hooks
- **100% context preservation** between sessions
- **Verified working code** through "Actually Works" protocol
- **Direct service integration** via MCP (Model Context Protocol)

## 📚 Documentation Structure

### Part 1: System Architecture & Philosophy
### Part 2: Mandatory Design System Rules
### Part 3: Command System & Workflows
### Part 4: Hook System for Safety & Observability
### Part 5: Component Boilerplate Library
### Part 6: Setup Scripts & Configuration
### Part 7: PRD-Driven Development Workflow
### Part 8: AI Agent Behavioral Rules
### Part 9: MCP Integration & Service Access

---

## Part 1: System Architecture & Philosophy

### Core Innovation: "Vibe Coding"
You define WHAT to build (strategy), the system handles HOW (implementation).

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLAUDE CODE BOILERPLATE                      │
├─────────────────────────┬───────────────────────────────────────┤
│  COMMAND SYSTEM (70+)   │        HOOK SYSTEM                    │
│  ├── PRD Generation     │  ├── Pre-Tool-Use (Safety)          │
│  ├── Task Management    │  ├── Post-Tool-Use (Logging)        │
│  ├── Smart Resume       │  ├── Stop (Session Save)            │
│  └── Feature Workflow   │  └── Notification (Alerts)          │
├─────────────────────────┼───────────────────────────────────────┤
│  DESIGN ENFORCEMENT     │     CONTEXT PERSISTENCE             │
│  ├── 4 Font Sizes       │  ├── GitHub Gist Backups           │
│  ├── 2 Font Weights     │  ├── Checkpoint System             │
│  ├── 4px Grid System    │  ├── Team Handoffs                 │
│  └── Auto-Validation    │  └── Smart Resume                  │
├─────────────────────────┼───────────────────────────────────────┤
│    MCP INTEGRATIONS     │      SERVICE ACCESS                 │
│  ├── Supabase MCP       │  ├── Direct DB queries             │
│  ├── GitHub MCP         │  ├── No CLI needed                 │
│  ├── Upstash Redis      │  ├── Real-time operations         │
│  └── 10+ More MCPs      │  └── Fallback to CLI when needed   │
└─────────────────────────┴───────────────────────────────────────┘
```

### File Organization (MANDATORY)

```
project/
├── .claude/                    # Claude Code configuration
│   ├── commands/              # Custom command definitions
│   ├── hooks/                 # Automation hooks
│   ├── checkpoints/           # State snapshots
│   ├── team/                  # Multi-agent coordination
│   └── transcripts/           # Session history
├── app/                       # Next.js app directory
├── components/
│   ├── ui/                    # Base components (Button, Card)
│   ├── forms/                 # Form components
│   ├── layout/                # Layout components
│   └── features/              # Feature-specific
├── lib/
│   ├── api/                   # API utilities
│   ├── db/                    # Database queries
│   └── utils/                 # Helper functions
├── hooks/                     # React hooks
├── stores/                    # Zustand stores
├── docs/
│   ├── project/              # PRDs and business logic
│   ├── design/               # Design system docs
│   └── technical/            # Architecture docs
└── tests/                    # Test files
```

---

## Part 2: Mandatory Design System Rules

### 🚨 THESE RULES ARE NON-NEGOTIABLE

```markdown
# DESIGN SYSTEM ENFORCEMENT FOR AI AGENTS

## Typography: ONLY 4 Sizes, ONLY 2 Weights

### Font Sizes (NO EXCEPTIONS)
text-size-1: 32px (mobile: 28px)  # Major headings only
text-size-2: 24px (mobile: 20px)  # Section headers
text-size-3: 16px                 # ALL body text, buttons, inputs
text-size-4: 12px                 # Small labels, captions

### Font Weights (NO EXCEPTIONS)
font-regular: 400                 # ALL body text
font-semibold: 600                # ALL headings and buttons

### BANNED CSS CLASSES
❌ NEVER USE: text-sm, text-lg, text-xl, text-2xl, font-bold, font-medium
✅ ALWAYS USE: text-size-[1-4], font-regular, font-semibold

## Spacing: 4px Grid System ONLY

### Valid Spacing Values
✅ ALLOWED: 4, 8, 12, 16, 20, 24, 32, 48, 64
❌ FORBIDDEN: 5, 10, 15, 18, 25, 30, 36, 40

### Tailwind Mapping
p-1 = 4px    gap-1 = 4px    m-1 = 4px
p-2 = 8px    gap-2 = 8px    m-2 = 8px
p-3 = 12px   gap-3 = 12px   m-3 = 12px
p-4 = 16px   gap-4 = 16px   m-4 = 16px
p-6 = 24px   gap-6 = 24px   m-6 = 24px
p-8 = 32px   gap-8 = 32px   m-8 = 32px

## Color Distribution: 60/30/10 Rule

Every screen MUST follow:
- 60%: Neutral backgrounds (white, gray-50)
- 30%: Text and borders (gray-700, gray-200)
- 10%: Primary actions (blue-600, red-600 for errors)

## Mobile-First Requirements
- Minimum touch targets: 44px (h-11)
- Preferred touch targets: 48px (h-12)
- Minimum text size: 16px (text-size-3)
- Maximum content width: max-w-md
```

### Component Patterns (COPY EXACTLY)

```typescript
// STANDARD CONTAINER - Use for all pages
export function PageContainer({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-md mx-auto p-4">
        {children}
      </div>
    </div>
  );
}

// STANDARD CARD - Use for all content blocks
export function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`bg-white border border-gray-200 rounded-xl p-4 space-y-3 ${className}`}>
      {children}
    </div>
  );
}

// STANDARD BUTTON - Primary CTA
export function Button({ children, onClick, disabled, variant = 'primary' }: ButtonProps) {
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-800 text-white hover:bg-gray-900'
  };
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`w-full h-12 px-4 rounded-xl font-semibold text-size-3 
        transition-all disabled:bg-gray-200 disabled:text-gray-400 
        ${variants[variant]}`}
    >
      {children}
    </button>
  );
}

// STANDARD INPUT - Form fields
export function Input({ label, error, ...props }: InputProps) {
  return (
    <div className="space-y-2">
      <label className="text-size-3 font-semibold text-gray-700">
        {label}
      </label>
      <input
        className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl 
          focus:border-blue-500 focus:outline-none transition-colors"
        {...props}
      />
      {error && <p className="text-size-4 text-red-600">{error}</p>}
    </div>
  );
}
```

---

## Part 3: Command System & Workflows

### Essential Commands Reference

```bash
# ALWAYS START WITH THESE
/sr                    # Smart Resume - restores all context
/init                  # One-time project setup
/help                  # Contextual help system

# PRD & TASK WORKFLOW
/prd [feature]         # Generate Product Requirements Document
/gt [feature]          # Generate tasks from PRD
/pt [feature]          # Process tasks one by one
/ts                    # Task status overview
/tb                    # Visual task board
/vt                    # Verify current task

# DEVELOPMENT COMMANDS
/cc ui Button          # Create component (auto-validated)
/vd                    # Validate design compliance
/fw start [issue#]     # Start feature workflow
/fw complete [issue#]  # Complete feature with PR

# TESTING & QUALITY
/btf [feature]         # Browser test flow
/tr                    # Run tests
/pp                    # Pre-PR validation suite

# CONTEXT & STATE
/checkpoint create     # Save current state
/cg                    # Context grab
/auc                   # Auto-update context

# TEAM COLLABORATION
/team-status          # See all team activity
/collab-sync [user]   # Sync with team member
/handoff prepare      # Prepare work for handoff
```

### Command Chains (Workflows)

```json
{
  "morning-setup": ["smart-resume", "security-check deps", "test-runner changed"],
  "feature-planning": ["create-prd", "generate-tasks", "task-status"],
  "task-sprint": ["task-status", "process-tasks", "verify-task", "task-checkpoint"],
  "pre-pr": ["validate-design", "test-runner all", "security-check all"]
}
```

---

## Part 4: Hook System for Safety & Observability

### Hook Implementation

```python
# Pre-Tool-Use Hook: Design Enforcement
#!/usr/bin/env python3
"""Blocks design system violations before they're written"""

FORBIDDEN_PATTERNS = [
    # Font sizes
    r'text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl)',
    # Font weights  
    r'font-(thin|light|medium|bold|extrabold|black)',
    # Non-4px spacing
    r'(p|m|gap|space)-(5|7|10|11|13|14|15)'
]

def check_design_compliance(content):
    violations = []
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, content):
            violations.append(f"Forbidden pattern: {pattern}")
    return violations

# Pre-Tool-Use Hook: Actually Works Protocol
def enforce_actually_works(content):
    untested_claims = [
        "should work", "might work", "probably works",
        "fixed", "done", "complete"
    ]
    
    for claim in untested_claims:
        if claim in content.lower():
            return {
                "error": "Actually Works Protocol Violation",
                "message": "Test your code before claiming it works!",
                "checklist": [
                    "1. Run the actual code",
                    "2. Check browser console",
                    "3. Verify expected output",
                    "4. Test edge cases"
                ]
            }
    return None
```

### Hook Categories

1. **Pre-Tool-Use** (Before file edits)
   - Design system validation
   - GitHub synchronization
   - Conflict detection
   - Dangerous command blocking

2. **Post-Tool-Use** (After file edits)
   - State persistence to GitHub
   - Metrics collection
   - Pattern extraction

3. **Stop Hooks** (Session end)
   - Transcript saving
   - Knowledge extraction
   - Handoff preparation

---

## Part 5: Component Boilerplate Library

### UI Component Templates

```typescript
// components/ui/Button.tsx
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'default' | 'small';
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

export function Button({ 
  children, 
  variant = 'primary',
  size = 'default',
  onClick,
  disabled,
  loading,
  type = 'button',
  className = ''
}: ButtonProps) {
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-800 text-white hover:bg-gray-900',
    danger: 'bg-red-600 text-white hover:bg-red-700'
  };
  
  const sizes = {
    default: 'h-12 px-4 text-size-3',
    small: 'h-10 px-3 text-size-4'
  };
  
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`rounded-xl font-semibold transition-all 
        disabled:bg-gray-200 disabled:text-gray-400 disabled:cursor-not-allowed
        ${variants[variant]} ${sizes[size]} ${className}`}
    >
      {loading ? (
        <span className="flex items-center justify-center gap-2">
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" 
              stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" 
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Loading...
        </span>
      ) : children}
    </button>
  );
}

// components/ui/Card.tsx
interface CardProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
  footer?: React.ReactNode;
  className?: string;
}

export function Card({ 
  children, 
  title, 
  description, 
  footer,
  className = '' 
}: CardProps) {
  return (
    <div className={`bg-white border border-gray-200 rounded-xl ${className}`}>
      {(title || description) && (
        <div className="p-4 border-b border-gray-200">
          {title && (
            <h3 className="text-size-2 font-semibold text-gray-900">{title}</h3>
          )}
          {description && (
            <p className="text-size-3 text-gray-600 mt-1">{description}</p>
          )}
        </div>
      )}
      <div className="p-4">
        {children}
      </div>
      {footer && (
        <div className="p-4 border-t border-gray-200 bg-gray-50 rounded-b-xl">
          {footer}
        </div>
      )}
    </div>
  );
}

// components/forms/FormField.tsx
interface FormFieldProps {
  label: string;
  error?: string;
  required?: boolean;
  children: React.ReactNode;
}

export function FormField({ 
  label, 
  error, 
  required,
  children 
}: FormFieldProps) {
  return (
    <div className="space-y-2">
      <label className="text-size-3 font-semibold text-gray-700 flex items-center gap-1">
        {label}
        {required && <span className="text-red-600">*</span>}
      </label>
      {children}
      {error && (
        <p className="text-size-4 text-red-600 flex items-center gap-1">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}
    </div>
  );
}
```

### Form Pattern with Validation

```typescript
// components/forms/ContactForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters')
});

type ContactFormData = z.infer<typeof contactSchema>;

export function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema)
  });

  const onSubmit = async (data: ContactFormData) => {
    try {
      await apiClient('/api/contact', {
        method: 'POST',
        body: JSON.stringify(data)
      });
      reset();
      // Show success message
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <FormField label="Name" error={errors.name?.message} required>
        <input
          {...register('name')}
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl 
            focus:border-blue-500 focus:outline-none transition-colors"
        />
      </FormField>

      <FormField label="Email" error={errors.email?.message} required>
        <input
          {...register('email')}
          type="email"
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl 
            focus:border-blue-500 focus:outline-none transition-colors"
        />
      </FormField>

      <FormField label="Message" error={errors.message?.message} required>
        <textarea
          {...register('message')}
          rows={4}
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl 
            focus:border-blue-500 focus:outline-none transition-colors resize-none"
        />
      </FormField>

      <Button type="submit" loading={isSubmitting} className="w-full">
        Send Message
      </Button>
    </form>
  );
}
```

---

## Part 6: Setup Scripts & Configuration

### Master Setup Script

```bash
#!/bin/bash
# setup-enhanced-boilerplate.sh

echo "🚀 Setting up Claude Code Boilerplate..."

# Create directory structure
mkdir -p {components/{ui,forms,layout,features},lib/{api,db,utils},hooks,stores,tests/browser}
mkdir -p {app/{api,\(public\),\(protected\)},docs/{project/features,design,technical,guides}}
mkdir -p .claude/{commands,hooks/{pre-tool-use,post-tool-use,stop,notification},checkpoints,team,transcripts}

# Create essential config files
cat > package.json << 'EOF'
{
  "name": "claude-code-project",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "test": "jest",
    "test:e2e": "playwright test",
    "validate:design": "node scripts/validate-design.js"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@supabase/supabase-js": "^2.39.0",
    "@supabase/ssr": "^0.0.10",
    "zustand": "^4.4.7",
    "react-hook-form": "^7.48.0",
    "@hookform/resolvers": "^3.3.2",
    "zod": "^3.22.4",
    "lucide-react": "^0.300.0",
    "framer-motion": "^10.16.0",
    "@tanstack/react-query": "^5.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.3.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "@playwright/test": "^1.40.0",
    "jest": "^29.7.0",
    "@testing-library/react": "^14.1.0",
    "prettier": "^3.1.0"
  }
}
EOF

# Create Tailwind config with design tokens
cat > tailwind.config.js << 'EOF'
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontSize: {
        'size-1': ['32px', { lineHeight: '1.25' }],
        'size-2': ['24px', { lineHeight: '1.375' }],
        'size-3': ['16px', { lineHeight: '1.5' }],
        'size-4': ['12px', { lineHeight: '1.5' }],
      },
      fontWeight: {
        regular: '400',
        semibold: '600',
      },
      height: {
        '11': '44px',
        '12': '48px',
      },
      screens: {
        'mobile': { 'raw': '(max-width: 639px)' },
      },
    },
  },
  plugins: [],
}
EOF

# Create TypeScript config
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
EOF

# Create .env.example
cat > .env.example << 'EOF'
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Optional: Analytics
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
EOF

# Create Claude settings
cat > .claude/settings.json << 'EOF'
{
  "version": "1.0.0",
  "hooks": {
    "pre-tool-use": {
      "enabled": true,
      "commands": [
        {"script": "01-collab-sync.py"},
        {"script": "02-design-check.py"},
        {"script": "03-conflict-check.py"},
        {"script": "04-actually-works.py"}
      ]
    },
    "post-tool-use": {
      "enabled": true,
      "commands": [
        {"script": "01-state-save.py"},
        {"script": "02-metrics.py"}
      ]
    }
  }
}
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
.nyc_output

# Next.js
.next/
out/
build/

# Production
dist/

# Misc
.DS_Store
*.pem
.vscode/

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env
.env.local
.env.production.local

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Claude Code
.claude/checkpoints/*
.claude/transcripts/*
.claude/team/registry.json
!.claude/checkpoints/.gitkeep
!.claude/transcripts/.gitkeep
EOF

# Create keep files
touch .claude/checkpoints/.gitkeep
touch .claude/transcripts/.gitkeep

echo "✅ Setup complete! Next steps:"
echo "1. Run: npm install"
echo "2. Copy .env.example to .env.local and fill in values"
echo "3. Start Claude Code and run: /init"
echo "4. Begin with: /prd [your-first-feature]"
```

---

## Part 7: PRD-Driven Development Workflow

### PRD Template

```markdown
# Product Requirements Document: [FEATURE NAME]

## 1. Feature Overview

### What is this feature?
[Clear description of the feature]

### Why are we building it?
[Business value and user benefits]

### Who will use it?
[Target users and use cases]

## 2. User Stories

1. As a [user type], I want to [action] so that [benefit]
2. As a [user type], I want to [action] so that [benefit]
3. As a [user type], I want to [action] so that [benefit]

## 3. Functional Requirements

### Must Have (MVP)
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Nice to Have
- [ ] Enhancement 1
- [ ] Enhancement 2

### Out of Scope (v1)
- Feature X (planned for v2)
- Feature Y (needs more research)

## 4. UI/UX Requirements

### Key Screens
1. **Screen Name**
   - Purpose: 
   - Key elements:
   - User actions:

### User Flow
1. User arrives at...
2. User clicks...
3. System shows...
4. User completes...

### Mobile Considerations
- Touch targets minimum 44px
- Responsive layout breakpoints
- Gesture support needed

## 5. Technical Requirements

### API Endpoints
```
POST /api/[feature]
GET /api/[feature]/:id
PUT /api/[feature]/:id
DELETE /api/[feature]/:id
```

### Database Schema
```sql
CREATE TABLE feature_name (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Performance Requirements
- Page load < 3 seconds
- API response < 500ms
- Support 100 concurrent users

### Security Considerations
- Authentication required
- Authorization rules
- Data validation
- Rate limiting

## 6. Success Metrics

### Primary KPIs
- Metric 1: Target value
- Metric 2: Target value

### Secondary Metrics
- User engagement
- Error rates
- Performance metrics

## 7. Edge Cases & Error Handling

### Edge Cases
1. What if user has no data?
2. What if network fails?
3. What if user lacks permissions?

### Error States
- Network errors → Show retry button
- Validation errors → Inline field errors
- Server errors → Friendly error message

## 8. Testing Requirements

### Unit Tests
- Business logic functions
- Validation rules
- API endpoints

### Integration Tests
- Full user flows
- API integration
- Database operations

### E2E Tests
- Critical user paths
- Cross-browser testing
- Mobile testing
```

### Task Generation Template

```markdown
# Task List: [FEATURE NAME]

## Phase 1: Foundation (Backend/Data)
- [ ] 1.1 Create database migrations
  - Add tables: [list tables]
  - Add indexes for performance
  - Verify: migration runs successfully
  
- [ ] 1.2 Set up API route structure
  - Create /api/[feature] directory
  - Add route handlers
  - Verify: routes respond with 200 OK

- [ ] 1.3 Implement data models
  - Create TypeScript interfaces
  - Add Zod validation schemas
  - Verify: types compile without errors

## Phase 2: Core Business Logic
- [ ] 2.1 Implement service layer
  - Create [feature]Service class
  - Add CRUD operations
  - Verify: unit tests pass

- [ ] 2.2 Add validation logic
  - Input validation
  - Business rule validation
  - Verify: invalid inputs rejected

- [ ] 2.3 Implement error handling
  - Try-catch blocks
  - Error logging
  - User-friendly messages
  - Verify: errors handled gracefully

## Phase 3: User Interface
- [ ] 3.1 Create base components
  - [Component1] with design system
  - [Component2] with design system
  - Verify: /vd shows no violations

- [ ] 3.2 Implement forms
  - Add form fields
  - Connect validation
  - Add loading states
  - Verify: form submits successfully

- [ ] 3.3 Add feedback states
  - Loading indicators
  - Success messages
  - Error displays
  - Verify: all states visible

## Phase 4: Integration
- [ ] 4.1 Connect UI to API
  - Add API calls
  - Handle responses
  - Update UI state
  - Verify: data flows correctly

- [ ] 4.2 Add real-time features
  - WebSocket connection
  - Live updates
  - Optimistic updates
  - Verify: changes appear instantly

## Phase 5: Polish & Testing
- [ ] 5.1 Add animations
  - Micro-interactions
  - Page transitions
  - Loading animations
  - Verify: smooth 60fps

- [ ] 5.2 Write comprehensive tests
  - Unit tests: 80% coverage
  - Integration tests
  - E2E happy path
  - Verify: all tests green

- [ ] 5.3 Performance optimization
  - Bundle size check
  - Lighthouse audit
  - API response times
  - Verify: meets targets

## Verification Checklist
Each task must be verifiable:
✓ Can be completed in 5-15 minutes
✓ Has clear success criteria
✓ Produces visible output
✓ Can be tested immediately
```

---

## Part 8: AI Agent Behavioral Rules

### MANDATORY BEHAVIORS FOR AI AGENTS

```markdown
# AI AGENT BEHAVIORAL CONTRACT

## 1. Context Awareness

ALWAYS start each session with:
```bash
/sr  # Smart Resume to restore context
```

NEVER claim to remember previous sessions. Instead:
❌ "As we discussed earlier..."
✅ "According to the context restored by /sr..."

## 2. File Organization Rules

ALWAYS create files in correct directories:
- UI components → components/ui/
- Form components → components/forms/
- Page layouts → components/layout/
- Feature-specific → components/features/[feature]/
- API routes → app/api/[feature]/
- Utilities → lib/utils/
- Database → lib/db/
- React hooks → hooks/

NEVER place files in root directory.

## 3. Import Order

ALWAYS organize imports in this EXACT order:
```typescript
// 1. React/Next imports
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

// 2. Third-party libraries
import { z } from 'zod';
import { useForm } from 'react-hook-form';

// 3. Internal absolute imports
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/lib/api/client';

// 4. Relative imports
import { LocalComponent } from './LocalComponent';

// 5. Types
import type { User } from '@/types';
```

## 4. Component Creation

ALWAYS use this workflow:
```bash
/cc ui ComponentName    # Creates with validation
/vd                    # Verify design compliance
```

NEVER create components manually without validation.

## 5. Error Handling Pattern

ALWAYS implement try-catch with specific error handling:
```typescript
try {
  const result = await apiCall();
  // Success path
} catch (error) {
  if (error instanceof ApiError) {
    setError(error.message);
  } else if (error instanceof NetworkError) {
    setError('Connection failed. Please try again.');
  } else {
    setError('Something went wrong');
    console.error('Unexpected error:', error);
  }
}
```

## 6. State Management Rules

1. Local component state → useState
2. Shared between few components → Props
3. Global app state → Zustand store
4. Server state → React Query
5. URL state → URLSearchParams

NEVER use Context for frequent updates.

## 7. Testing Claims

Before saying "done", "fixed", or "should work":

1. Actually run the code
2. Check browser console for errors
3. Verify the expected output appears
4. Test at least one edge case
5. Run /btf for UI changes

The "Actually Works" protocol is ENFORCED by hooks.

## 8. Git Commit Messages

Format: type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code change without fix/feature
- style: Formatting only
- test: Adding tests
- docs: Documentation only
- chore: Maintenance

Example:
```bash
git commit -m "feat(auth): add password reset flow"
git commit -m "fix(ui): correct button spacing on mobile"
```

## 9. PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Added X component
- Fixed Y bug
- Refactored Z function

## Testing
- [ ] Manual testing completed
- [ ] Unit tests added/updated
- [ ] E2E tests pass
- [ ] Design system validated

## Screenshots
[If UI changes]

Closes #[issue-number]
```

## 10. Performance Considerations

ALWAYS:
- Lazy load heavy components
- Optimize images (next/image)
- Use React.memo for expensive renders
- Implement pagination for lists
- Add loading states

NEVER:
- Load entire datasets
- Use inline functions in renders
- Forget cleanup in useEffect
- Block the main thread

## 11. Accessibility Requirements

Every component MUST:
- Have proper ARIA labels
- Support keyboard navigation
- Maintain focus management
- Provide alt text for images
- Meet WCAG 2.1 AA standards

## 12. Documentation

For every feature, create:
1. PRD in docs/project/features/
2. Technical spec in docs/technical/
3. Component docs inline
4. API documentation
5. Update README if needed
```

### Common Pitfalls to Avoid

```markdown
# COMMON PITFALLS - MEMORIZE THESE

## 1. Design System Violations
❌ WRONG:
<div className="text-lg font-bold p-5">

✅ CORRECT:
<div className="text-size-2 font-semibold p-4">

## 2. Unhandled Loading States
❌ WRONG:
const { data } = useQuery(...);
return <div>{data.name}</div>;

✅ CORRECT:
const { data, isLoading, error } = useQuery(...);
if (isLoading) return <LoadingSpinner />;
if (error) return <ErrorMessage error={error} />;
return <div>{data?.name}</div>;

## 3. Direct DOM Manipulation
❌ WRONG:
document.getElementById('myDiv').style.color = 'red';

✅ CORRECT:
const [color, setColor] = useState('black');
return <div style={{ color }}>

## 4. Unvalidated User Input
❌ WRONG:
const handleSubmit = (data) => {
  apiClient.post('/api/user', data);
};

✅ CORRECT:
const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2)
});

const handleSubmit = (data) => {
  const validated = schema.parse(data);
  apiClient.post('/api/user', validated);
};

## 5. Console Logs in Production
❌ WRONG:
console.log('user data:', userData);

✅ CORRECT:
if (process.env.NODE_ENV === 'development') {
  console.log('user data:', userData);
}

## 6. Hardcoded Values
❌ WRONG:
const API_URL = 'https://api.example.com';

✅ CORRECT:
const API_URL = process.env.NEXT_PUBLIC_API_URL;

## 7. Missing Error Boundaries
❌ WRONG:
<ComplexComponent />

✅ CORRECT:
<ErrorBoundary fallback={<ErrorFallback />}>
  <ComplexComponent />
</ErrorBoundary>

## 8. Inefficient Re-renders
❌ WRONG:
<Button onClick={() => handleClick(item.id)}>

✅ CORRECT:
const handleClick = useCallback((id) => {
  // handle click
}, []);

<Button onClick={() => handleClick(item.id)}>

## 9. Synchronous Heavy Operations
❌ WRONG:
const sorted = hugeArray.sort((a, b) => complexSort(a, b));

✅ CORRECT:
const sorted = useMemo(
  () => hugeArray.sort((a, b) => complexSort(a, b)),
  [hugeArray]
);

## 10. Forgetting Mobile
❌ WRONG:
<div className="w-[800px]">

✅ CORRECT:
<div className="w-full max-w-[800px]">
```

---

## Part 9: MCP Integration & Service Access

### 🎯 CRITICAL: Use MCPs, Not CLIs

**ALWAYS use MCP (Model Context Protocol) when available**. MCPs provide direct integration with services without leaving Claude Code.

### Available MCPs

```markdown
# SUPABASE MCP
✅ USE FOR:
- Database queries: supabase:execute_sql
- Table management: supabase:list_tables
- Migrations: supabase:apply_migration
- Edge functions: supabase:deploy_edge_function
- Logs: supabase:get_logs

❌ DON'T USE:
- supabase CLI commands
- npx supabase (unless for local dev)

# GITHUB MCP
✅ USE FOR:
- Issues: github:create_issue, github:list_issues
- PRs: github:create_pull_request
- Files: github:get_file_contents
- Repos: github:create_repository

❌ DON'T USE:
- gh CLI commands (unless MCP unavailable)

# UPSTASH REDIS MCP
✅ USE FOR:
- Cache operations: upstash:get, upstash:set
- Counters: upstash:incr
- TTL: upstash:expire

❌ DON'T USE:
- redis-cli (unless for complex scripts)

# BIGQUERY MCP (Google Toolbox)
✅ USE FOR:
- Queries: google:bigquery_query
- Schema: google:bigquery_get_schema

⚠️ LIMITATION - USE CLI FOR:
- Data loading: bq load
- Table creation: bq mk
- Dataset management: bq mk -d
```

### MCP Usage Examples

```typescript
// ✅ CORRECT - Using Supabase MCP
const result = await supabase:execute_sql({
  project_id: "abc-123",
  query: "SELECT * FROM users WHERE active = true"
});

// ❌ WRONG - Using CLI when MCP available
await shell_command("supabase db execute 'SELECT * FROM users'");

// ✅ CORRECT - Using GitHub MCP
await github:create_issue({
  owner: "myorg",
  repo: "myrepo",
  title: "Bug: Login fails",
  body: "Description here"
});

// ❌ WRONG - Using gh CLI
await shell_command("gh issue create --title 'Bug'");

// ✅ CORRECT - BigQuery read via MCP
const data = await google:bigquery_query({
  query: "SELECT * FROM dataset.table LIMIT 100"
});

// ✅ CORRECT - BigQuery write via CLI (MCP can't write)
await shell_command("bq load --source_format=CSV dataset.table gs://bucket/data.csv");
```

### MCP Limitations & Fallbacks

| Service | MCP Can Do | Must Use CLI For |
|---------|------------|------------------|
| Supabase | Query, migrate, deploy | Local dev server |
| GitHub | Issues, PRs, files | Complex git operations |
| BigQuery | Read data | Write data, create tables |
| Redis | Basic operations | Lua scripts, clustering |
| Sentry | View issues, alerts | Deploy releases |
| DBT | Run models | Create models, init |

### Integration Decision Flow

```mermaid
Start → Is MCP available? 
  ├─ Yes → Use MCP
  └─ No → Is it a known limitation?
      ├─ Yes → Use CLI/API
      └─ No → Check docs first
```

---

## Summary & Implementation Checklist

### For AI Agents Starting a New Project:

1. **Initial Setup**
   ```bash
   # Run setup script
   ./setup-enhanced-boilerplate.sh
   
   # Install dependencies
   npm install
   
   # Start Claude Code
   claude-code .
   
   # Initialize project
   /init
   ```

2. **Configure MCPs**
   ```bash
   # Check available MCPs
   # Use autocomplete to see functions
   
   # Example: Set up Supabase
   supabase:list_projects
   supabase:get_project { id: "your-project" }
   ```

3. **Start Development**
   ```bash
   # Begin with PRD
   /prd user-authentication
   
   # Generate tasks
   /gt user-authentication
   
   # Process tasks
   /pt user-authentication
   
   # Validate as you go
   /vd
   ```

4. **Use MCPs Throughout**
   ```typescript
   // Database operations
   await supabase:execute_sql({ ... })
   
   // GitHub operations  
   await github:create_issue({ ... })
   
   // Cache operations
   await upstash:set({ ... })
   ```

5. **Daily Workflow**
   ```bash
   # Always start with
   /sr
   
   # Check status
   /ts
   
   # Continue work
   /pt
   
   # Before breaks
   /checkpoint create
   ```

6. **Quality Checks**
   - Design validation runs automatically
   - "Actually Works" protocol enforced
   - Team conflicts prevented
   - Context never lost
   - MCPs used for all operations

### Success Metrics

When properly implemented, this system delivers:
- ✅ 70% faster development
- ✅ Zero design inconsistencies  
- ✅ Perfect team coordination
- ✅ 100% context preservation
- ✅ Verified working code
- ✅ Direct service integration via MCPs

### Remember

This is not just a boilerplate - it's a complete development operating system that:
- Enforces quality automatically
- Preserves knowledge permanently
- Coordinates team efforts seamlessly
- Validates everything continuously
- Integrates services directly via MCPs

The developer provides strategy (WHAT to build).
The system ensures quality (HOW it's built).
MCPs provide the tools (HOW to integrate).

Welcome to the future of AI-assisted development! 🚀
