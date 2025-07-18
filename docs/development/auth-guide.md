# Authentication Guide

## Overview

This guide covers authentication implementation using either Supabase Auth or Better Auth, depending on your project needs.

## Choosing an Auth Provider

### Use Supabase Auth when:
- Already using Supabase for database
- Need built-in user management UI
- Want email/SMS verification out of the box
- Need Row Level Security (RLS) integration

### Use Better Auth when:
- Want more control over auth flow
- Need custom authentication methods
- Using a different database provider
- Want a lighter auth solution

## Supabase Auth Implementation

### Setup

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

```typescript
// lib/supabase/server.ts
import { createServerClient, type CookieOptions } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createClient() {
  const cookieStore = cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          cookieStore.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          cookieStore.set({ name, value: '', ...options });
        },
      },
    }
  );
}
```

### Authentication Components

```typescript
// components/auth/LoginForm.tsx
'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const supabase = createClient();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    router.push('/dashboard');
    router.refresh();
  }

  return (
    <form onSubmit={handleLogin} className="space-y-4">
      <div>
        <label htmlFor="email" className="text-size-3 font-semibold">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl"
          required
        />
      </div>

      <div>
        <label htmlFor="password" className="text-size-3 font-semibold">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl"
          required
        />
      </div>

      {error && (
        <div className="text-red-600 text-size-3">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full h-12 bg-primary-600 text-white rounded-xl font-semibold"
      >
        {loading ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  );
}
```

### Protected Routes

```typescript
// app/(protected)/layout.tsx
import { redirect } from 'next/navigation';
import { createClient } from '@/lib/supabase/server';

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    redirect('/login');
  }

  return <>{children}</>;
}
```

### Sign Out

```typescript
// components/auth/SignOutButton.tsx
'use client';

import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';

export function SignOutButton() {
  const router = useRouter();
  const supabase = createClient();

  async function handleSignOut() {
    await supabase.auth.signOut();
    router.push('/');
    router.refresh();
  }

  return (
    <button onClick={handleSignOut} className="text-size-3">
      Sign Out
    </button>
  );
}
```

## Better Auth Implementation

### Installation

```bash
pnpm add better-auth
```

### Setup

```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { db } from './db';

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'pg',
  }),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
});
```

### Client Setup

```typescript
// lib/auth-client.ts
import { createAuthClient } from 'better-auth/react';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL!,
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient;
```

### Authentication Hook

```typescript
// hooks/useAuth.ts
import { useSession } from '@/lib/auth-client';

export function useAuth() {
  const { data: session, error, isLoading } = useSession();

  return {
    user: session?.user,
    session,
    isLoading,
    isAuthenticated: !!session?.user,
    error,
  };
}
```

### Login Component

```typescript
// components/auth/BetterAuthLogin.tsx
'use client';

import { useState } from 'react';
import { signIn } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await signIn.email({
      email,
      password,
      callbackURL: '/dashboard',
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    router.push('/dashboard');
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Same form fields as above */}
    </form>
  );
}
```

### Protected Route Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { auth } from '@/lib/auth';

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
};
```

## Social Authentication

### OAuth Providers (Supabase)

```typescript
// components/auth/SocialAuth.tsx
'use client';

import { createClient } from '@/lib/supabase/client';

export function SocialAuth() {
  const supabase = createClient();

  async function signInWithGoogle() {
    await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
  }

  async function signInWithGitHub() {
    await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
  }

  return (
    <div className="space-y-2">
      <button
        onClick={signInWithGoogle}
        className="w-full h-12 border-2 border-gray-200 rounded-xl flex items-center justify-center gap-2"
      >
        <GoogleIcon />
        Continue with Google
      </button>
      
      <button
        onClick={signInWithGitHub}
        className="w-full h-12 border-2 border-gray-200 rounded-xl flex items-center justify-center gap-2"
      >
        <GitHubIcon />
        Continue with GitHub
      </button>
    </div>
  );
}
```

## Session Management

### Server-Side Session Check

```typescript
// lib/auth/session.ts
import { cookies } from 'next/headers';
import { createClient } from '@/lib/supabase/server';

export async function getSession() {
  const supabase = createClient();
  const { data: { session } } = await supabase.auth.getSession();
  return session;
}

export async function getUser() {
  const session = await getSession();
  return session?.user || null;
}
```

### Client-Side Session Hook

```typescript
// hooks/useSession.ts
import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import type { User } from '@supabase/supabase-js';

export function useUser() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const supabase = createClient();

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, [supabase]);

  return { user, loading };
}
```

## Authorization

### Role-Based Access Control

```typescript
// lib/auth/rbac.ts
export const ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  MODERATOR: 'moderator',
} as const;

export type Role = typeof ROLES[keyof typeof ROLES];

export async function hasRole(userId: string, role: Role): Promise<boolean> {
  // Check user role in database
  const userRole = await getUserRole(userId);
  return userRole === role;
}

export async function requireRole(userId: string, role: Role) {
  const hasAccess = await hasRole(userId, role);
  if (!hasAccess) {
    throw new Error('Insufficient permissions');
  }
}
```

### Protected API Routes

```typescript
// app/api/admin/route.ts
import { NextRequest } from 'next/server';
import { getUser } from '@/lib/auth/session';
import { requireRole, ROLES } from '@/lib/auth/rbac';

export async function GET(request: NextRequest) {
  const user = await getUser();
  
  if (!user) {
    return new Response('Unauthorized', { status: 401 });
  }
  
  try {
    await requireRole(user.id, ROLES.ADMIN);
  } catch {
    return new Response('Forbidden', { status: 403 });
  }
  
  // Admin-only logic here
  return Response.json({ data: 'Admin data' });
}
```

## Security Best Practices

1. **Always validate sessions server-side**
2. **Use HTTPS in production**
3. **Implement CSRF protection**
4. **Set secure cookie options**
5. **Implement rate limiting for auth endpoints**
6. **Use strong password requirements**
7. **Enable 2FA when possible**
8. **Log authentication events**
9. **Implement session timeout**
10. **Sanitize all user inputs**

## Testing Authentication

```typescript
// __tests__/auth.test.ts
import { vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from '@/components/auth/LoginForm';

vi.mock('@/lib/supabase/client', () => ({
  createClient: () => ({
    auth: {
      signInWithPassword: vi.fn().mockResolvedValue({ error: null }),
    },
  }),
}));

describe('LoginForm', () => {
  it('submits login credentials', async () => {
    render(<LoginForm />);
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' },
    });
    
    fireEvent.click(screen.getByText('Sign In'));
    
    await waitFor(() => {
      expect(screen.getByText('Signing in...')).toBeInTheDocument();
    });
  });
});
```