# Authentication Flow Pattern

## Overview
Standard authentication flow using Supabase with proper error handling, loading states, and session management.

## Implementation Pattern

### 1. Authentication Hook
```typescript
// hooks/use-auth.ts
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { User } from '@supabase/supabase-js'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const supabase = createClient()

  useEffect(() => {
    // Get initial session
    const initAuth = async () => {
      try {
        const { data: { session }, error } = await supabase.auth.getSession()
        if (error) throw error
        setUser(session?.user ?? null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Auth initialization failed')
      } finally {
        setLoading(false)
      }
    }

    initAuth()

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setUser(session?.user ?? null)
        
        // Handle specific events
        if (event === 'SIGNED_OUT') {
          // Clear any app state
          window.location.href = '/login'
        }
        if (event === 'TOKEN_REFRESHED') {
          // Token was refreshed successfully
        }
        if (event === 'USER_UPDATED') {
          // Profile was updated
        }
      }
    )

    return () => subscription.unsubscribe()
  }, [supabase])

  return { user, loading, error }
}
```

### 2. Login Form Component
```typescript
// components/auth/LoginForm.tsx
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Card } from '@/components/ui/Card'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters')
})

export function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      // Validate inputs
      const validated = loginSchema.parse({ email, password })
      
      // Attempt login
      const { data, error } = await supabase.auth.signInWithPassword({
        email: validated.email,
        password: validated.password,
      })

      if (error) {
        // Handle specific error types
        if (error.message.includes('Invalid login credentials')) {
          throw new Error('Email or password is incorrect')
        }
        throw error
      }

      // Success - router will handle redirect via middleware
      router.push('/dashboard')
      
    } catch (err) {
      if (err instanceof z.ZodError) {
        setError(err.errors[0].message)
      } else if (err instanceof Error) {
        setError(err.message)
      } else {
        setError('An unexpected error occurred')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md">
      <form onSubmit={handleLogin} className="space-y-4">
        <div>
          <h2 className="text-size-2 font-semibold text-gray-900">
            Welcome back
          </h2>
          <p className="text-size-3 text-gray-600 mt-1">
            Sign in to your account
          </p>
        </div>

        <Input
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={loading}
          autoComplete="email"
        />

        <Input
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          disabled={loading}
          autoComplete="current-password"
        />

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-3">
            <p className="text-size-3 text-red-700">{error}</p>
          </div>
        )}

        <Button
          type="submit"
          loading={loading}
          disabled={loading}
          className="w-full"
        >
          Sign In
        </Button>

        <div className="text-center space-y-2">
          <p className="text-size-3 text-gray-600">
            <a href="/forgot-password" className="text-blue-600 hover:text-blue-700">
              Forgot your password?
            </a>
          </p>
          <p className="text-size-3 text-gray-600">
            Don't have an account?{' '}
            <a href="/signup" className="text-blue-600 hover:text-blue-700">
              Sign up
            </a>
          </p>
        </div>
      </form>
    </Card>
  )
}
```

### 3. Protected Route Middleware
```typescript
// middleware.ts
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value,
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value,
            ...options,
          })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value: '',
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value: '',
            ...options,
          })
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard') && !user) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Auth routes (redirect if already logged in)
  if (['/login', '/signup'].includes(request.nextUrl.pathname) && user) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/signup']
}
```

### 4. Session Refresh Pattern
```typescript
// lib/supabase/session-manager.ts
export class SessionManager {
  private refreshTimer: NodeJS.Timeout | null = null
  private supabase = createClient()

  startAutoRefresh() {
    // Refresh token 5 minutes before expiry
    this.refreshTimer = setInterval(async () => {
      const { data: { session } } = await this.supabase.auth.getSession()
      
      if (session?.expires_at) {
        const expiresAt = new Date(session.expires_at * 1000)
        const now = new Date()
        const timeUntilExpiry = expiresAt.getTime() - now.getTime()
        
        // If less than 5 minutes until expiry
        if (timeUntilExpiry < 5 * 60 * 1000) {
          await this.supabase.auth.refreshSession()
        }
      }
    }, 60 * 1000) // Check every minute
  }

  stopAutoRefresh() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
      this.refreshTimer = null
    }
  }
}
```

## Best Practices

1. **Always handle loading states** - Users need feedback
2. **Validate inputs on client AND server** - Never trust client-only validation
3. **Handle specific error cases** - Generic errors are unhelpful
4. **Use proper TypeScript types** - Avoid `any` types
5. **Implement session refresh** - Don't let users get logged out unexpectedly
6. **Clear app state on logout** - Prevent data leaks
7. **Use middleware for route protection** - Centralized auth checks

## Common Mistakes to Avoid

1. ❌ Storing sensitive data in localStorage
2. ❌ Not handling token refresh
3. ❌ Forgetting to unsubscribe from auth listeners
4. ❌ Using client-side only route protection
5. ❌ Not validating email format
6. ❌ Showing raw error messages to users
7. ❌ Not handling network errors

## Testing Checklist

- [ ] Login with valid credentials
- [ ] Login with invalid email
- [ ] Login with wrong password
- [ ] Login with network disconnected
- [ ] Navigate to protected route without auth
- [ ] Navigate to login when already authenticated
- [ ] Logout clears all user data
- [ ] Session persists on page refresh
- [ ] Token refresh works automatically
