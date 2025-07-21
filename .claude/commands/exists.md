# Exists - Check if Something Already Exists

Quick check to see if a component, function, type, or route already exists before creating it.

## Usage

```bash
/exists [name]
/exists LoginForm
/exists useAuth
/exists /api/user
```

## What It Checks

1. **Components** - Searches components/* for matching files
2. **Hooks** - Searches hooks/* for custom hooks
3. **API Routes** - Checks app/api/* for endpoints
4. **Types** - Searches types/* for type definitions
5. **Functions** - Grep for function declarations
6. **Database Tables** - Checks schema files
7. **Environment Variables** - Checks .env.example

## Example Output

### Found Example:
```bash
/exists LoginForm

✅ FOUND: LoginForm

📍 Location: components/auth/LoginForm.tsx
📦 Type: React Component
📤 Exports: 
   - LoginForm (default export)
   - LoginFormProps (named export)

📊 Usage (3 locations):
   - app/login/page.tsx (line 12)
   - app/register/page.tsx (line 8) 
   - tests/auth/login.test.tsx (line 5)

🔧 Props Interface:
   - onSubmit: (data: LoginData) => Promise<void>
   - initialValues?: Partial<LoginData>
   - loading?: boolean

⚡ Related:
   - Types: LoginData (types/auth.ts)
   - Hook: useAuth (hooks/useAuth.ts)
   - API: POST /api/auth/login

⚠️ This component ALREADY EXISTS. Do not recreate.
To modify, edit: components/auth/LoginForm.tsx
```

### Not Found Example:
```bash
/exists UserDashboard

❌ NOT FOUND: UserDashboard

🔍 Did you mean?
   - UserProfile (components/user/UserProfile.tsx)
   - Dashboard (components/layout/Dashboard.tsx)
   - UserStats (components/user/UserStats.tsx)

✅ Safe to create this component.
Suggested location: components/user/UserDashboard.tsx

💡 Quick create: /cc user UserDashboard
```

## Smart Detection

The command uses multiple strategies:

1. **Exact Match** - Direct file/export name match
2. **Fuzzy Match** - Similar names (typo detection)
3. **Context Search** - Checks if functionality exists under different name
4. **Usage Search** - Finds where it might be imported

## Integration with Workflow

```bash
# Before creating anything
/exists MyComponent

# If not found
/cc ui MyComponent

# If found
# Edit the existing file instead
```

## Prevents Common Mistakes

- Creating duplicate components
- Recreating existing utilities
- Duplicate API endpoints
- Conflicting type definitions
- Redundant hooks

## Implementation

```python
def check_exists(name):
    results = {
        'components': search_components(name),
        'hooks': search_hooks(name),
        'api_routes': search_api_routes(name),
        'types': search_types(name),
        'functions': search_functions(name),
        'database': search_schema(name),
        'env_vars': search_env_vars(name)
    }
    
    # Also check for usage
    usage = find_usage_locations(name)
    
    # Fuzzy match for typos
    suggestions = find_similar_names(name)
    
    return format_results(results, usage, suggestions)
```

Always run this before creating new code to avoid duplicates!