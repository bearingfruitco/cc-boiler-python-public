# Supabase Integration Guide for Claude Code

## 🚀 Quick Setup

```bash
# 1. Install Supabase
npm install @supabase/supabase-js @supabase/ssr

# 2. Set environment variables
NEXT_PUBLIC_SUPABASE_URL=your_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_key
```

## 📁 File Structure

```
lib/
├── supabase/
│   ├── client.ts         # Browser client
│   ├── server.ts         # Server client
│   ├── middleware.ts     # Auth middleware
│   └── types.ts          # Generated types
```

## 🔧 Client Setup

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'
import type { Database } from './types'

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

## 🔐 Server Setup

```typescript
// lib/supabase/server.ts
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'
import type { Database } from './types'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          cookieStore.set({ name, value, ...options })
        },
        remove(name: string, options: CookieOptions) {
          cookieStore.set({ name, value: '', ...options })
        },
      },
    }
  )
}
```

## 🎯 Common Patterns

### Authentication Hook

```typescript
// hooks/use-auth.ts
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { User } from '@supabase/supabase-js'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    // Listen for changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [supabase])

  return { user, loading }
}
```

### Protected Route

```typescript
// app/(protected)/layout.tsx
import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return <>{children}</>
}
```

### Data Fetching with React Query

```typescript
// hooks/queries/use-posts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/client'

export function usePosts() {
  const supabase = createClient()
  
  return useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('posts')
        .select('*, author:profiles(*)')
        .order('created_at', { ascending: false })
      
      if (error) throw error
      return data
    },
  })
}

export function useCreatePost() {
  const supabase = createClient()
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (post: { title: string; content: string }) => {
      const { data, error } = await supabase
        .from('posts')
        .insert(post)
        .select()
        .single()
      
      if (error) throw error
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] })
    },
  })
}
```

### Real-time Subscriptions

```typescript
// hooks/use-realtime-posts.ts
import { useEffect } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/client'

export function useRealtimePosts() {
  const supabase = createClient()
  const queryClient = useQueryClient()

  useEffect(() => {
    const channel = supabase
      .channel('posts-changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'posts' },
        (payload) => {
          // Invalidate and refetch posts
          queryClient.invalidateQueries({ queryKey: ['posts'] })
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase, queryClient])
}
```

### File Upload

```typescript
// components/upload/AvatarUpload.tsx
import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Button } from '@/components/ui/Button'

export function AvatarUpload({ userId }: { userId: string }) {
  const [uploading, setUploading] = useState(false)
  const supabase = createClient()

  const uploadAvatar = async (event: React.ChangeEvent<HTMLInputElement>) => {
    try {
      setUploading(true)

      if (!event.target.files || event.target.files.length === 0) {
        throw new Error('You must select an image to upload.')
      }

      const file = event.target.files[0]
      const fileExt = file.name.split('.').pop()
      const filePath = `${userId}-${Math.random()}.${fileExt}`

      const { error: uploadError } = await supabase.storage
        .from('avatars')
        .upload(filePath, file)

      if (uploadError) throw uploadError

      // Update user profile
      const { error: updateError } = await supabase
        .from('profiles')
        .update({ avatar_url: filePath })
        .eq('id', userId)

      if (updateError) throw updateError

      alert('Avatar uploaded!')
    } catch (error) {
      alert('Error uploading avatar!')
      console.error(error)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="space-y-4">
      <input
        type="file"
        id="avatar"
        accept="image/*"
        onChange={uploadAvatar}
        disabled={uploading}
        className="hidden"
      />
      <label htmlFor="avatar">
        <Button
          as="span"
          loading={uploading}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Upload Avatar'}
        </Button>
      </label>
    </div>
  )
}
```

## 🗄️ Database Types

```bash
# Generate TypeScript types from your database
npx supabase gen types typescript --project-id your-project-id > lib/supabase/types.ts
```

## 🔒 Row Level Security (RLS)

```sql
-- Enable RLS on tables
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own posts
CREATE POLICY "Users can view own posts" ON posts
  FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own posts
CREATE POLICY "Users can insert own posts" ON posts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own posts
CREATE POLICY "Users can update own posts" ON posts
  FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own posts
CREATE POLICY "Users can delete own posts" ON posts
  FOR DELETE USING (auth.uid() = user_id);
```

## 🚨 Common Patterns & Best Practices

### Error Handling

```typescript
// lib/supabase/errors.ts
export class SupabaseError extends Error {
  constructor(
    message: string,
    public code?: string,
    public status?: number
  ) {
    super(message)
    this.name = 'SupabaseError'
  }
}

export function handleSupabaseError(error: any): never {
  if (error.code === 'PGRST116') {
    throw new SupabaseError('Record not found', error.code, 404)
  }
  if (error.code === '23505') {
    throw new SupabaseError('Duplicate entry', error.code, 409)
  }
  throw new SupabaseError(error.message || 'Database error', error.code)
}
```

### Optimistic Updates

```typescript
// hooks/mutations/use-update-profile.ts
export function useUpdateProfile() {
  const supabase = createClient()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ 
      userId, 
      updates 
    }: { 
      userId: string
      updates: Partial<Profile> 
    }) => {
      const { data, error } = await supabase
        .from('profiles')
        .update(updates)
        .eq('id', userId)
        .select()
        .single()

      if (error) throw error
      return data
    },
    onMutate: async ({ userId, updates }) => {
      // Cancel in-flight queries
      await queryClient.cancelQueries({ queryKey: ['profile', userId] })

      // Snapshot previous value
      const previousProfile = queryClient.getQueryData(['profile', userId])

      // Optimistically update
      queryClient.setQueryData(['profile', userId], (old: any) => ({
        ...old,
        ...updates,
      }))

      return { previousProfile }
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousProfile) {
        queryClient.setQueryData(
          ['profile', variables.userId],
          context.previousProfile
        )
      }
    },
    onSettled: (data, error, variables) => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ 
        queryKey: ['profile', variables.userId] 
      })
    },
  })
}
```

### Server Actions

```typescript
// app/actions/posts.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
})

export async function createPost(formData: FormData) {
  const supabase = await createClient()
  
  // Validate input
  const validatedFields = createPostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  })

  if (!validatedFields.success) {
    return {
      error: 'Invalid fields',
      issues: validatedFields.error.flatten().fieldErrors,
    }
  }

  // Check auth
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return { error: 'Unauthorized' }
  }

  // Insert post
  const { data, error } = await supabase
    .from('posts')
    .insert({
      ...validatedFields.data,
      user_id: user.id,
    })
    .select()
    .single()

  if (error) {
    return { error: 'Failed to create post' }
  }

  revalidatePath('/posts')
  return { data }
}
```

## 🎯 Design System Compliant Components

### Login Form

```typescript
// components/auth/LoginForm.tsx
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Card } from '@/components/ui/Card'

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
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })

      if (error) throw error
      router.push('/dashboard')
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to login')
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
        />

        <Input
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
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

        <p className="text-size-3 text-gray-600 text-center">
          Don't have an account?{' '}
          <a href="/signup" className="text-blue-600 hover:text-blue-700">
            Sign up
          </a>
        </p>
      </form>
    </Card>
  )
}
```

## 📝 Migration Example

```sql
-- Create profiles table
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE,
  full_name TEXT,
  avatar_url TEXT,
  bio TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Public profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can insert their own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- Create function to handle new user
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username, full_name, avatar_url)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'username',
    NEW.raw_user_meta_data->>'full_name',
    NEW.raw_user_meta_data->>'avatar_url'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
```

## 🔍 Debugging Tips

```typescript
// Enable debug mode in development
if (process.env.NODE_ENV === 'development') {
  const supabase = createClient()
  
  // Log all queries
  supabase.channel('debug').subscribe((status) => {
    console.log('Supabase status:', status)
  })
}

// Helper to log Supabase errors
export function logSupabaseError(
  operation: string,
  error: any,
  context?: Record<string, any>
) {
  console.error(`Supabase ${operation} error:`, {
    message: error.message,
    code: error.code,
    details: error.details,
    hint: error.hint,
    context,
  })
}
```

## 🚀 Performance Tips

1. **Use select() wisely**
   ```typescript
   // Bad - fetches all columns
   const { data } = await supabase.from('posts').select('*')
   
   // Good - fetch only needed columns
   const { data } = await supabase.from('posts').select('id, title, created_at')
   ```

2. **Implement pagination**
   ```typescript
   const PAGE_SIZE = 10
   
   const { data, count } = await supabase
     .from('posts')
     .select('*', { count: 'exact' })
     .range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1)
   ```

3. **Use database views for complex queries**
   ```sql
   CREATE VIEW post_with_author AS
   SELECT 
     p.*,
     profiles.username as author_name,
     profiles.avatar_url as author_avatar
   FROM posts p
   JOIN profiles ON p.user_id = profiles.id;
   ```

4. **Cache with React Query**
   ```typescript
   // Set stale time for data that doesn't change often
   useQuery({
     queryKey: ['profile', userId],
     queryFn: fetchProfile,
     staleTime: 5 * 60 * 1000, // 5 minutes
   })
   ```

## 🎓 Remember

- Always use RLS for security
- Generate TypeScript types for type safety
- Handle errors gracefully
- Use React Query for caching
- Follow the design system in all components
- Test authentication flows thoroughly
