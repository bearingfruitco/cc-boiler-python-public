# Data Fetching Pattern with React Query

## Overview
Comprehensive data fetching pattern using React Query (TanStack Query) with Supabase, including caching, optimistic updates, and error handling.

## Implementation Pattern

### 1. Query Client Setup
```typescript
// app/providers.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useState } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Stale time: How long until data is considered stale
            staleTime: 1000 * 60 * 5, // 5 minutes
            // Cache time: How long to keep data in cache
            cacheTime: 1000 * 60 * 10, // 10 minutes
            // Retry configuration
            retry: (failureCount, error: any) => {
              // Don't retry on 4xx errors
              if (error?.status >= 400 && error?.status < 500) {
                return false
              }
              // Retry up to 3 times for other errors
              return failureCount < 3
            },
            // Refetch on window focus
            refetchOnWindowFocus: false,
          },
          mutations: {
            // Always retry mutations once
            retry: 1,
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

### 2. Data Fetching Hooks
```typescript
// hooks/queries/use-posts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/client'
import type { Post } from '@/types'

// Query Keys Factory
export const postKeys = {
  all: ['posts'] as const,
  lists: () => [...postKeys.all, 'list'] as const,
  list: (filters: string) => [...postKeys.lists(), { filters }] as const,
  details: () => [...postKeys.all, 'detail'] as const,
  detail: (id: string) => [...postKeys.details(), id] as const,
}

// Fetch all posts
export function usePosts(filters?: { status?: string; userId?: string }) {
  const supabase = createClient()
  
  return useQuery({
    queryKey: postKeys.list(JSON.stringify(filters || {})),
    queryFn: async () => {
      let query = supabase
        .from('posts')
        .select(`
          *,
          author:profiles(id, username, avatar_url),
          categories(id, name),
          _count:comments(count)
        `)
        .order('created_at', { ascending: false })

      // Apply filters
      if (filters?.status) {
        query = query.eq('status', filters.status)
      }
      if (filters?.userId) {
        query = query.eq('user_id', filters.userId)
      }

      const { data, error } = await query

      if (error) {
        throw new Error(`Failed to fetch posts: ${error.message}`)
      }

      return data as Post[]
    },
    // This query is considered fresh for 1 minute
    staleTime: 1000 * 60,
  })
}

// Fetch single post
export function usePost(id: string) {
  const supabase = createClient()
  
  return useQuery({
    queryKey: postKeys.detail(id),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('posts')
        .select(`
          *,
          author:profiles(*),
          categories(*),
          comments(
            *,
            user:profiles(id, username, avatar_url)
          )
        `)
        .eq('id', id)
        .single()

      if (error) {
        if (error.code === 'PGRST116') {
          throw new Error('Post not found')
        }
        throw error
      }

      return data as Post
    },
    // Keep post data fresh for 30 seconds
    staleTime: 30 * 1000,
  })
}
```

### 3. Mutations with Optimistic Updates
```typescript
// hooks/mutations/use-create-post.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/client'
import { postKeys } from '../queries/use-posts'
import type { Post, CreatePostInput } from '@/types'

export function useCreatePost() {
  const supabase = createClient()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (input: CreatePostInput) => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) throw new Error('Must be authenticated')

      const { data, error } = await supabase
        .from('posts')
        .insert({
          ...input,
          user_id: user.id,
        })
        .select(`
          *,
          author:profiles(id, username, avatar_url),
          categories(id, name),
          _count:comments(count)
        `)
        .single()

      if (error) throw error
      return data as Post
    },
    
    // Optimistic update
    onMutate: async (newPost) => {
      // Cancel in-flight queries
      await queryClient.cancelQueries({ queryKey: postKeys.lists() })

      // Get current data
      const previousPosts = queryClient.getQueryData(postKeys.lists())

      // Optimistically update
      queryClient.setQueryData(postKeys.lists(), (old: Post[] = []) => {
        const optimisticPost: Partial<Post> = {
          id: `temp-${Date.now()}`,
          ...newPost,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          author: { 
            id: 'temp',
            username: 'You',
            avatar_url: null 
          },
          categories: [],
          _count: { comments: 0 },
        }
        return [optimisticPost as Post, ...old]
      })

      return { previousPosts }
    },
    
    // On error, rollback
    onError: (err, newPost, context) => {
      if (context?.previousPosts) {
        queryClient.setQueryData(postKeys.lists(), context.previousPosts)
      }
      console.error('Failed to create post:', err)
    },
    
    // Always refetch after error or success
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: postKeys.lists() })
    },
  })
}

// Update mutation with optimistic updates
export function useUpdatePost() {
  const supabase = createClient()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ 
      id, 
      updates 
    }: { 
      id: string
      updates: Partial<Post> 
    }) => {
      const { data, error } = await supabase
        .from('posts')
        .update(updates)
        .eq('id', id)
        .select()
        .single()

      if (error) throw error
      return data as Post
    },
    
    // Optimistic update for both list and detail views
    onMutate: async ({ id, updates }) => {
      await queryClient.cancelQueries({ queryKey: postKeys.detail(id) })
      await queryClient.cancelQueries({ queryKey: postKeys.lists() })

      const previousPost = queryClient.getQueryData(postKeys.detail(id))
      const previousPosts = queryClient.getQueryData(postKeys.lists())

      // Update single post
      queryClient.setQueryData(postKeys.detail(id), (old: Post | undefined) => {
        if (!old) return old
        return { ...old, ...updates }
      })

      // Update in lists
      queryClient.setQueriesData(
        { queryKey: postKeys.lists() },
        (old: Post[] | undefined) => {
          if (!old) return old
          return old.map(post => 
            post.id === id ? { ...post, ...updates } : post
          )
        }
      )

      return { previousPost, previousPosts }
    },
    
    onError: (err, variables, context) => {
      if (context?.previousPost) {
        queryClient.setQueryData(
          postKeys.detail(variables.id),
          context.previousPost
        )
      }
      if (context?.previousPosts) {
        queryClient.setQueryData(postKeys.lists(), context.previousPosts)
      }
    },
    
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: postKeys.detail(variables.id) })
      queryClient.invalidateQueries({ queryKey: postKeys.lists() })
    },
  })
}
```

### 4. Infinite Scroll Pattern
```typescript
// hooks/queries/use-infinite-posts.ts
import { useInfiniteQuery } from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/client'

const PAGE_SIZE = 10

export function useInfinitePosts() {
  const supabase = createClient()

  return useInfiniteQuery({
    queryKey: ['posts', 'infinite'],
    queryFn: async ({ pageParam = 0 }) => {
      const from = pageParam * PAGE_SIZE
      const to = from + PAGE_SIZE - 1

      const { data, error, count } = await supabase
        .from('posts')
        .select('*, author:profiles(username)', { count: 'exact' })
        .order('created_at', { ascending: false })
        .range(from, to)

      if (error) throw error

      return {
        posts: data,
        nextPage: to < (count || 0) ? pageParam + 1 : undefined,
        totalCount: count,
      }
    },
    getNextPageParam: (lastPage) => lastPage.nextPage,
    // Keep pages in cache for 5 minutes
    staleTime: 5 * 60 * 1000,
  })
}

// Usage in component
export function InfinitePostList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    isError,
    error,
  } = useInfinitePosts()

  // Intersection observer for infinite scroll
  const observerRef = useRef<IntersectionObserver>()
  const loadMoreRef = useCallback(
    (node: HTMLDivElement | null) => {
      if (isLoading) return
      if (observerRef.current) observerRef.current.disconnect()
      
      observerRef.current = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && hasNextPage) {
          fetchNextPage()
        }
      })
      
      if (node) observerRef.current.observe(node)
    },
    [isLoading, hasNextPage, fetchNextPage]
  )

  if (isLoading) return <LoadingSpinner />
  if (isError) return <ErrorMessage error={error} />

  return (
    <div className="space-y-4">
      {data?.pages.map((page, i) => (
        <Fragment key={i}>
          {page.posts.map(post => (
            <PostCard key={post.id} post={post} />
          ))}
        </Fragment>
      ))}
      
      {hasNextPage && (
        <div ref={loadMoreRef} className="py-4 text-center">
          {isFetchingNextPage ? <LoadingSpinner /> : 'Load more'}
        </div>
      )}
    </div>
  )
}
```

### 5. Prefetching Pattern
```typescript
// hooks/queries/use-prefetch.ts
export function usePrefetchPost() {
  const queryClient = useQueryClient()
  const supabase = createClient()

  const prefetchPost = async (id: string) => {
    await queryClient.prefetchQuery({
      queryKey: postKeys.detail(id),
      queryFn: async () => {
        const { data, error } = await supabase
          .from('posts')
          .select('*')
          .eq('id', id)
          .single()

        if (error) throw error
        return data
      },
      // Prefetch data stays fresh for 10 seconds
      staleTime: 10 * 1000,
    })
  }

  return prefetchPost
}

// Usage in list component
export function PostList() {
  const { data: posts } = usePosts()
  const prefetchPost = usePrefetchPost()

  return (
    <div className="space-y-4">
      {posts?.map(post => (
        <div
          key={post.id}
          onMouseEnter={() => prefetchPost(post.id)}
        >
          <PostCard post={post} />
        </div>
      ))}
    </div>
  )
}
```

## Best Practices

1. **Use query key factories** - Consistent, type-safe query keys
2. **Handle loading and error states** - Never assume data exists
3. **Configure stale times appropriately** - Balance freshness vs performance
4. **Implement optimistic updates** - Better UX for mutations
5. **Cancel in-flight queries** - Prevent race conditions
6. **Use prefetching** - Anticipate user actions
7. **Handle pagination properly** - Use infinite queries for feeds

## Common Mistakes to Avoid

1. ❌ Not handling loading states
2. ❌ Forgetting error boundaries
3. ❌ Over-fetching with no pagination
4. ❌ Not canceling queries on unmount
5. ❌ Inconsistent query keys
6. ❌ Not using optimistic updates
7. ❌ Fetching in useEffect instead of React Query

## Performance Tips

1. **Set appropriate stale times** based on data volatility
2. **Use `select` to transform data** and avoid re-renders
3. **Implement proper pagination** for large datasets
4. **Prefetch on hover** for instant navigation
5. **Use `enabled` option** to conditionally fetch
6. **Background refetch** for real-time feel

## Testing Checklist

- [ ] Data loads successfully
- [ ] Error states display correctly
- [ ] Loading states show appropriately
- [ ] Optimistic updates work
- [ ] Rollback works on error
- [ ] Pagination/infinite scroll works
- [ ] Prefetching improves performance
- [ ] Cache invalidation works correctly
- [ ] Offline behavior is handled
