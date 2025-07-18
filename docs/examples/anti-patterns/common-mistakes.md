# Common AI Coding Mistakes & Anti-Patterns

## Overview
This document catalogues common mistakes AI coding assistants make and how to avoid them. Use this as a reference to prevent these issues in your implementations.

## 1. State Management Anti-Patterns

### ❌ WRONG: Mutating State Directly
```typescript
// AI often tries to mutate state
const [items, setItems] = useState([{id: 1, name: 'Item'}])

// WRONG
const updateItem = (id: number, name: string) => {
  items[0].name = name  // Direct mutation!
  setItems(items)       // React won't re-render
}
```

### ✅ CORRECT: Create New State
```typescript
const updateItem = (id: number, name: string) => {
  setItems(items.map(item => 
    item.id === id ? { ...item, name } : item
  ))
}
```

## 2. Async/Await Anti-Patterns

### ❌ WRONG: Forgetting to Await
```typescript
// AI frequently forgets await
const saveData = async () => {
  try {
    // Missing await - error won't be caught!
    apiClient.post('/api/save', data)
    toast.success('Saved!')  // Shows before save completes
  } catch (error) {
    // This won't catch API errors
    toast.error('Failed')
  }
}
```

### ✅ CORRECT: Always Await Async Calls
```typescript
const saveData = async () => {
  try {
    await apiClient.post('/api/save', data)
    toast.success('Saved!')
  } catch (error) {
    toast.error('Failed to save')
  }
}
```

## 3. useEffect Anti-Patterns

### ❌ WRONG: Missing Dependencies
```typescript
// AI often misses dependencies
useEffect(() => {
  fetchUserData(userId)  // userId not in deps!
}, [])  // Will never re-fetch when userId changes
```

### ✅ CORRECT: Include All Dependencies
```typescript
useEffect(() => {
  fetchUserData(userId)
}, [userId])  // Re-fetches when userId changes

// Or better - use React Query instead of useEffect for data fetching
```

### ❌ WRONG: Not Cleaning Up
```typescript
useEffect(() => {
  const timer = setInterval(() => {
    // Do something
  }, 1000)
  // Missing cleanup!
}, [])
```

### ✅ CORRECT: Always Clean Up
```typescript
useEffect(() => {
  const timer = setInterval(() => {
    // Do something
  }, 1000)
  
  return () => clearInterval(timer)  // Cleanup
}, [])
```

## 4. Error Handling Anti-Patterns

### ❌ WRONG: Generic Error Messages
```typescript
try {
  await someOperation()
} catch (error) {
  // Unhelpful generic message
  setError('An error occurred')
}
```

### ✅ CORRECT: Specific Error Handling
```typescript
try {
  await someOperation()
} catch (error) {
  if (error instanceof NetworkError) {
    setError('Connection failed. Please check your internet.')
  } else if (error instanceof ValidationError) {
    setError(error.message)
  } else {
    setError('Something went wrong. Please try again.')
    console.error('Unexpected error:', error)
  }
}
```

## 5. Loading State Anti-Patterns

### ❌ WRONG: No Loading States
```typescript
function UserProfile() {
  const { data } = useQuery(['user'])
  
  // Crashes when data is undefined!
  return <div>{data.name}</div>
}
```

### ✅ CORRECT: Handle All States
```typescript
function UserProfile() {
  const { data, isLoading, error } = useQuery(['user'])
  
  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage error={error} />
  if (!data) return <EmptyState />
  
  return <div>{data.name}</div>
}
```

## 6. Performance Anti-Patterns

### ❌ WRONG: Functions in Render
```typescript
// Creates new function every render
<Button onClick={() => handleClick(item.id)}>
  Click
</Button>

// Causes infinite re-renders
useEffect(() => {
  setData(processData(rawData))
}, [processData])  // processData recreated every render!
```

### ✅ CORRECT: Memoize Functions
```typescript
const handleItemClick = useCallback((id: string) => {
  // Handle click
}, [])

<Button onClick={() => handleItemClick(item.id)}>
  Click
</Button>

// Or for the effect
const processedData = useMemo(() => 
  processData(rawData), 
  [rawData]
)
```

## 7. TypeScript Anti-Patterns

### ❌ WRONG: Using 'any'
```typescript
// AI often falls back to any
const processData = (data: any) => {
  return data.map((item: any) => item.name)
}
```

### ✅ CORRECT: Proper Types
```typescript
interface DataItem {
  id: string
  name: string
}

const processData = (data: DataItem[]) => {
  return data.map(item => item.name)
}
```

## 8. Component Structure Anti-Patterns

### ❌ WRONG: Everything in One Component
```typescript
// 500+ line component with everything
function Dashboard() {
  // Authentication logic
  // Data fetching
  // Complex business logic
  // Multiple forms
  // All UI rendering
}
```

### ✅ CORRECT: Separate Concerns
```typescript
// Split into logical components
function Dashboard() {
  return (
    <DashboardLayout>
      <DashboardHeader />
      <DashboardMetrics />
      <DashboardActivity />
    </DashboardLayout>
  )
}
```

## 9. API Integration Anti-Patterns

### ❌ WRONG: Hardcoded URLs
```typescript
// AI often hardcodes URLs
fetch('http://localhost:3000/api/users')
```

### ✅ CORRECT: Environment Variables
```typescript
fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users`)
```

## 10. Form Handling Anti-Patterns

### ❌ WRONG: Uncontrolled Forms Without Validation
```typescript
const handleSubmit = (e) => {
  e.preventDefault()
  const formData = new FormData(e.target)
  // No validation!
  apiClient.post('/api/submit', formData)
}
```

### ✅ CORRECT: Controlled with Validation
```typescript
const {
  register,
  handleSubmit,
  formState: { errors }
} = useForm({
  resolver: zodResolver(schema)
})

const onSubmit = async (data: FormData) => {
  // Data is validated by Zod
  await apiClient.post('/api/submit', data)
}
```

## 11. Security Anti-Patterns

### ❌ WRONG: Client-Side Only Validation
```typescript
// Only validating on client
if (email.includes('@')) {
  // Proceed with operation
}
```

### ✅ CORRECT: Client + Server Validation
```typescript
// Client side for UX
const isValid = emailSchema.safeParse(email).success

// Server side for security
// app/api/route.ts
const validated = emailSchema.parse(request.body.email)
```

## 12. Mobile Responsiveness Anti-Patterns

### ❌ WRONG: Fixed Widths
```typescript
<div className="w-[800px]">
  Content that breaks on mobile
</div>
```

### ✅ CORRECT: Responsive Design
```typescript
<div className="w-full max-w-[800px]">
  Content that works on all devices
</div>
```

## Key Takeaways

1. **Always handle loading and error states**
2. **Never mutate state directly**
3. **Always await async operations**
4. **Include all useEffect dependencies**
5. **Avoid 'any' types**
6. **Validate on client AND server**
7. **Use environment variables**
8. **Design mobile-first**
9. **Split large components**
10. **Memoize expensive operations**

## Red Flags in AI-Generated Code

Watch for these warning signs:
- Missing error handling
- No loading states
- Direct state mutations
- Hardcoded values
- Missing TypeScript types
- No input validation
- Forgetting to await
- Not cleaning up effects
- Fixed pixel widths
- Everything in one file

When you see these patterns, stop and refactor before proceeding!
