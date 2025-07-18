# Claude Code Quick Reference Cards

## 🎯 Essential Commands Card

```bash
# SESSION MANAGEMENT
/sr                    # Smart Resume - start EVERY session
/init                  # One-time setup (first time only)
/checkpoint create     # Save progress anytime
/help                  # Get contextual help

# PRD WORKFLOW
/prd auth             # Create Product Requirements Doc
/gt auth              # Generate tasks from PRD
/pt auth              # Process tasks one-by-one
/ts                   # Task status overview
/vt                   # Verify current task

# DEVELOPMENT
/cc ui Button         # Create validated component
/vd                   # Validate design compliance
/fw start 23          # Start feature #23
/fw complete 23       # Finish with PR

# TESTING
/btf auth            # Browser test flow
/tr                  # Run all tests
/pp                  # Pre-PR validation

# ALIASES
/sr = smart-resume    /prd = create-prd
/cc = create-component    /vd = validate-design
/fw = feature-workflow    /gt = generate-tasks
/pt = process-tasks      /ts = task-status
```

---

## 🎨 Design System Card

```css
/* TYPOGRAPHY - ONLY THESE */
text-size-1: 32px (28px mobile)    /* Major headings */
text-size-2: 24px (20px mobile)    /* Section headers */
text-size-3: 16px                  /* Body, buttons, inputs */
text-size-4: 12px                  /* Small text */

font-regular: 400                  /* Body text */
font-semibold: 600                 /* Headers, buttons */

/* SPACING - 4px GRID ONLY */
p-1=4px   p-2=8px   p-3=12px   p-4=16px   p-6=24px   p-8=32px
m-1=4px   m-2=8px   m-3=12px   m-4=16px   m-6=24px   m-8=32px
gap-1=4px gap-2=8px gap-3=12px gap-4=16px gap-6=24px gap-8=32px

/* BANNED CSS */
❌ text-sm, text-lg, text-xl, font-bold, font-medium
❌ p-5, m-7, gap-10 (not on 4px grid)

/* COLOR RULES */
60% Neutral (white, gray-50)
30% Text/UI (gray-700, borders)
10% Actions (blue-600, red-600)

/* MOBILE */
Min touch: 44px (h-11)
Min text: 16px (text-size-3)
```

---

## 🔄 Daily Workflow Card

```bash
# MORNING START
/sr                   # Restore all context
/ts                   # Check task status
/team-status          # See team activity

# WORKING ON TASKS
/pt auth              # Process next task
/vd                   # Validate after changes
/vt                   # Verify task complete
/checkpoint create    # Save progress

# BEFORE LUNCH/BREAK
/checkpoint create lunch
/todo add "Review API error handling"
/ws                   # Work status

# END OF DAY
/fw validate 23       # Check feature
/pp                   # Pre-PR checks
/checkpoint create eod
/handoff prepare      # For team

# QUICK CHAINS
/ms = morning-setup (sr + checks)
/pp = pre-pr (validate + test + security)
/ds = daily-startup (sr + status + todos)
```

---

## 🧩 Component Patterns Card

```typescript
// STANDARD BUTTON
<button className="w-full h-12 px-4 rounded-xl font-semibold 
  text-size-3 bg-blue-600 text-white hover:bg-blue-700 
  transition-all disabled:bg-gray-200">
  Label
</button>

// STANDARD INPUT
<input className="w-full h-12 px-4 border-2 border-gray-200 
  rounded-xl focus:border-blue-500 focus:outline-none 
  transition-colors" />

// STANDARD CARD
<div className="bg-white border border-gray-200 rounded-xl 
  p-4 space-y-3">
  {content}
</div>

// PAGE CONTAINER
<div className="min-h-screen bg-gray-50">
  <div className="max-w-md mx-auto p-4">
    {content}
  </div>
</div>

// FORM FIELD
<div className="space-y-2">
  <label className="text-size-3 font-semibold text-gray-700">
    Label
  </label>
  {input}
  {error && <p className="text-size-4 text-red-600">{error}</p>}
</div>
```

---

## 🚨 Testing Protocol Card

```bash
# BEFORE CLAIMING "FIXED" OR "DONE"

1. RUN THE CODE
   - npm run dev
   - Open browser
   - Navigate to feature

2. CHECK CONSOLE
   - Open DevTools (F12)
   - Check for red errors
   - Check network tab

3. VERIFY OUTPUT
   - Does it look right?
   - Click all buttons
   - Submit forms
   - Check error states

4. EDGE CASES
   - Empty data
   - Network offline
   - Invalid input
   - Rapid clicks

5. VALIDATION
   /vd                  # Design check
   /btf feature-name    # Browser test

# NEVER SAY:
❌ "Should work"
❌ "Probably fixed"
❌ "Might be done"

# ALWAYS SAY:
✅ "Tested and working"
✅ "Verified in browser"
✅ "Console shows no errors"
```

---

## 📁 File Organization Card

```
COMPONENT LOCATIONS:
✅ components/ui/         → Button, Card, Input
✅ components/forms/      → FormField, ContactForm
✅ components/layout/     → Header, Footer, Container
✅ components/features/   → UserProfile, Dashboard

API LOCATIONS:
✅ app/api/auth/         → Auth endpoints
✅ app/api/users/        → User CRUD
✅ lib/api/              → API client, utils

UTILITIES:
✅ lib/utils/            → Helpers, formatters
✅ lib/db/               → Database queries
✅ hooks/                → useAuth, useUser
✅ stores/               → Zustand stores

DOCS:
✅ docs/project/features/  → PRDs
✅ docs/design/           → Design system
✅ docs/technical/        → Architecture

NEVER:
❌ Root directory files
❌ components/ (too general)
❌ Random locations
```

---

## 🔧 Error Handling Card

```typescript
// API ERROR HANDLING
try {
  const data = await apiClient('/api/users');
  setUsers(data);
} catch (error) {
  if (error instanceof ApiError) {
    if (error.status === 404) {
      setError('User not found');
    } else if (error.status === 401) {
      setError('Please login');
    } else {
      setError(error.message);
    }
  } else if (error instanceof NetworkError) {
    setError('Connection failed. Try again.');
  } else {
    setError('Something went wrong');
    console.error('Unexpected:', error);
  }
} finally {
  setLoading(false);
}

// FORM VALIDATION
const schema = z.object({
  email: z.string().email('Invalid email'),
  age: z.number().min(18, 'Must be 18+')
});

// LOADING STATES
if (isLoading) return <Spinner />;
if (error) return <ErrorMessage />;
if (!data) return <EmptyState />;
```

---

## 🚀 PRD Task Breakdown Card

```markdown
# TASK STRUCTURE (5-15 min each)

## Phase 1: Backend
1.1 [ ] Database schema      → CREATE TABLE, indexes
1.2 [ ] API routes          → /api/feature structure
1.3 [ ] Data models         → Types & validation
1.4 [ ] Service layer       → Business logic

## Phase 2: Frontend
2.1 [ ] UI components       → With design system
2.2 [ ] Forms              → Validation, loading
2.3 [ ] State management    → Zustand/React Query
2.4 [ ] Error handling      → User feedback

## Phase 3: Integration
3.1 [ ] Connect UI to API   → Fetch data
3.2 [ ] Real-time updates   → If needed
3.3 [ ] Optimizations       → Performance
3.4 [ ] Testing            → Unit, integration

## VERIFICATION
Each task must:
✓ Take 5-15 minutes
✓ Have clear output
✓ Be testable
✓ Follow design system
```

---

## 🎭 State Management Card

```typescript
// LOCAL STATE (useState)
const [count, setCount] = useState(0);

// SHARED STATE (Props)
<Parent data={data}>
  <Child data={data} />
</Parent>

// GLOBAL STATE (Zustand)
const useAuthStore = create((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null })
}));

// SERVER STATE (React Query)
const { data, error, isLoading } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers
});

// URL STATE (URLSearchParams)
const [params, setParams] = useSearchParams();
const page = params.get('page') || '1';

// FORM STATE (React Hook Form)
const { register, handleSubmit } = useForm({
  resolver: zodResolver(schema)
});
```

---

## 🛡️ Security Checklist Card

```typescript
// INPUT VALIDATION
✅ Zod schemas for all inputs
✅ Sanitize user content
✅ Validate on client AND server
✅ SQL injection prevention

// AUTHENTICATION
✅ Supabase Auth setup
✅ Protected routes
✅ Session management
✅ Secure cookies

// API SECURITY
✅ Rate limiting
✅ CORS configuration
✅ Input validation
✅ Error message sanitization

// DATA PROTECTION
✅ No sensitive data in logs
✅ Env vars for secrets
✅ HTTPS only
✅ XSS prevention

// COMMON MISTAKES
❌ console.log(userData)
❌ Hardcoded API keys
❌ Direct SQL queries
❌ Exposing stack traces
```
