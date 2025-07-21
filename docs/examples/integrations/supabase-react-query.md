# Supabase + React Query Integration Pattern

## Overview
Complete integration pattern showing how to use Supabase with React Query for optimal performance, type safety, and developer experience.

## Setup

### 1. Environment Configuration
```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://[project].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...  # Server-side only
```

### 2. Supabase Client Setup
```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'
import type { Database } from './types'

// Singleton pattern to avoid multiple clients
let client: ReturnType<typeof createBrowserClient<Database>> | undefined

export function createClient() {
  if (client) return client
  
  client = createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
  
  return client
}
```

### 3. React Query + Supabase Provider
```typescript
// app/providers.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { User } from '@supabase/supabase-js'

// Create context for Supabase user
const UserContext = createContext<User | null>(null)

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        retry: (failureCount, error: any) => {
          // Don't retry auth errors
          if (error?.code === 'PGRST301') return false
          return failureCount < 3
        },
      },
    },
  }))
  
  const [user, setUser] = useState<User | null>(null)
  const supabase = createClient()

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      
      // Important: Set auth header for React Query
      if (session?.access_token) {
        queryClient.setDefaultOptions({
          queries: {
            queryFn: async ({ queryKey, signal }) => {
              // Default query function can include auth
              throw new Error('Query function not implemented')
            },
          },
        })
      }
    })

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
      
      // Clear queries on logout
      if (!session) {
        queryClient.clear()
      }
    })

    return () => subscription.unsubscribe()
  }, [supabase, queryClient])

  return (
    <QueryClientProvider client={queryClient}>
      <UserContext.Provider value={user}>
        {children}
      </UserContext.Provider>
    </QueryClientProvider>
  )
}
```

## Integration Patterns

### 1. Type-Safe Database Queries
```typescript
// Generate types first:
// npx supabase gen types typescript --project-id [project-id] > lib/supabase/types.ts

import type { Database } from '@/lib/supabase/types'

type Tables = Database['public']['Tables']
type Post = Tables['posts']['Row']
type InsertPost = Tables['posts']['Insert']
type UpdatePost = Tables['posts']['Update']

// Type-safe query hook
export function usePost(id: string) {
  const supabase = createClient()
  
  return useQuery<Post>({
    queryKey: ['posts', id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .eq('id', id)
        .single()

      if (error) throw error
      return data
    },
  })
}
```

### 2. Real-time + React Query
```typescript
// hooks/use-realtime-posts.ts
export function useRealtimePosts() {
  const queryClient = useQueryClient()
  const supabase = createClient()

  useEffect(() => {
    // Subscribe to changes
    const channel = supabase
      .channel('posts-changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'posts',
        },
        (payload) => {
          // Update React Query cache based on event
          if (payload.eventType === 'INSERT') {
            queryClient.setQueryData(
              ['posts'],
              (old: Post[] = []) => [payload.new as Post, ...old]
            )
          } else if (payload.eventType === 'UPDATE') {
            // Update in list
            queryClient.setQueryData(
              ['posts'],
              (old: Post[] = []) =>
                old.map(post =>
                  post.id === payload.new.id ? payload.new as Post : post
                )
            )
            // Update individual
            queryClient.setQueryData(
              ['posts', payload.new.id],
              payload.new as Post
            )
          } else if (payload.eventType === 'DELETE') {
            // Remove from list
            queryClient.setQueryData(
              ['posts'],
              (old: Post[] = []) =>
                old.filter(post => post.id !== payload.old.id)
            )
            // Remove individual
            queryClient.removeQueries(['posts', payload.old.id])
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase, queryClient])
}
```

### 3. RLS-Aware Queries
```typescript
// Queries automatically respect RLS policies
export function useMyPosts() {
  const supabase = createClient()
  
  return useQuery({
    queryKey: ['my-posts'],
    queryFn: async () => {
      // RLS ensures only user's posts are returned
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) {
        // Handle RLS errors specifically
        if (error.code === 'PGRST301') {
          throw new Error('Please sign in to view your posts')
        }
        throw error
      }

      return data
    },
    // Only run if authenticated
    enabled: !!user,
  })
}
```

### 4. Optimistic Updates with Rollback
```typescript
export function useUpdatePost() {
  const queryClient = useQueryClient()
  const supabase = createClient()

  return useMutation({
    mutationFn: async ({ id, updates }: { id: string; updates: UpdatePost }) => {
      const { data, error } = await supabase
        .from('posts')
        .update(updates)
        .eq('id', id)
        .select()
        .single()

      if (error) {
        // Check for specific Supabase errors
        if (error.code === '23505') {
          throw new Error('A post with this title already exists')
        }
        throw error
      }

      return data
    },
    onMutate: async ({ id, updates }) => {
      // Cancel queries
      await queryClient.cancelQueries({ queryKey: ['posts', id] })

      // Snapshot
      const previous = queryClient.getQueryData(['posts', id])

      // Optimistic update
      queryClient.setQueryData(['posts', id], (old: Post) => ({
        ...old,
        ...updates,
        updated_at: new Date().toISOString(),
      }))

      return { previous }
    },
    onError: (err, variables, context) => {
      // Rollback
      if (context?.previous) {
        queryClient.setQueryData(['posts', variables.id], context.previous)
      }
    },
    onSettled: (data, error, variables) => {
      // Always refetch to ensure consistency
      queryClient.invalidateQueries({ queryKey: ['posts', variables.id] })
    },
  })
}
```

### 5. File Upload with Progress
```typescript
export function useFileUpload() {
  const supabase = createClient()
  const [progress, setProgress] = useState(0)

  const uploadFile = useMutation({
    mutationFn: async ({
      bucket,
      path,
      file,
    }: {
      bucket: string
      path: string
      file: File
    }) => {
      // Upload with progress tracking
      const { data, error } = await supabase.storage
        .from(bucket)
        .upload(path, file, {
          cacheControl: '3600',
          upsert: false,
          onUploadProgress: (progress) => {
            setProgress((progress.loaded / progress.total) * 100)
          },
        })

      if (error) throw error

      // Get public URL
      const { data: { publicUrl } } = supabase.storage
        .from(bucket)
        .getPublicUrl(path)

      return publicUrl
    },
    onSuccess: () => {
      setProgress(0)
    },
    onError: () => {
      setProgress(0)
    },
  })

  return { uploadFile, progress }
}
```

### 6. Batch Operations
```typescript
export function useBatchDelete() {
  const queryClient = useQueryClient()
  const supabase = createClient()

  return useMutation({
    mutationFn: async (ids: string[]) => {
      // Supabase doesn't have batch delete, so we use RPC
      const { error } = await supabase.rpc('batch_delete_posts', {
        post_ids: ids,
      })

      if (error) throw error
      return ids
    },
    onSuccess: (deletedIds) => {
      // Remove from cache
      deletedIds.forEach(id => {
        queryClient.removeQueries(['posts', id])
      })
      
      // Update list
      queryClient.setQueryData(['posts'], (old: Post[] = []) =>
        old.filter(post => !deletedIds.includes(post.id))
      )
    },
  })
}

// Database function
/*
CREATE OR REPLACE FUNCTION batch_delete_posts(post_ids uuid[])
RETURNS void AS $$
BEGIN
  DELETE FROM posts 
  WHERE id = ANY(post_ids) 
  AND user_id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
*/
```

## Best Practices

1. **Use generated types** for full type safety
2. **Handle RLS errors** gracefully (PGRST301)
3. **Combine with real-time** for live updates
4. **Leverage React Query cache** to minimize requests
5. **Use RPC functions** for complex operations
6. **Clear cache on logout** to prevent data leaks
7. **Enable queries conditionally** based on auth state

## Common Integration Issues

1. **Auth token not updating**: Clear and refetch queries on auth change
2. **RLS blocking queries**: Check policies and user session
3. **Type mismatches**: Regenerate types after schema changes
4. **Stale data**: Configure appropriate stale times
5. **Race conditions**: Use `cancelQueries` before optimistic updates

## Performance Optimization

1. **Select only needed columns**: `select('id, title, created_at')`
2. **Use indexes**: Create indexes on frequently queried columns
3. **Implement pagination**: Use `.range()` for large datasets
4. **Cache aggressively**: Increase `staleTime` for stable data
5. **Prefetch on hover**: Anticipate user navigation
