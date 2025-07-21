# React Query (TanStack Query) Guide

## Overview

This guide covers data fetching patterns using React Query (TanStack Query) for FreshSlate applications. React Query provides powerful server state management with features like caching, synchronization, and background updates.

## Setup and Configuration

### Installation

```bash
pnpm add @tanstack/react-query @tanstack/react-query-devtools
```

### Global Configuration

The query client is configured in `lib/query/client.ts`:

```typescript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      gcTime: 5 * 60 * 1000, // 5 minutes (garbage collection)
      retry: (failureCount, error: any) => {
        // Don't retry on 4xx errors
        if (error?.status >= 400 && error?.status < 500) return false;
        return failureCount < 3;
      },
      refetchOnWindowFocus: false, // Disable for lead forms
    },
    mutations: {
      retry: false,
    },
  },
});
```

### Provider Setup

Wrap your app with the QueryClientProvider in `app/providers.tsx`:

```typescript
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## Query Keys Pattern

Use a consistent query key factory pattern for cache management:

```typescript
// lib/query/client.ts
export const queryKeys = {
  all: ['data'] as const,
  users: () => [...queryKeys.all, 'users'] as const,
  user: (id: string) => [...queryKeys.users(), id] as const,
  userPosts: (userId: string) => [...queryKeys.user(userId), 'posts'] as const,
  
  leads: () => [...queryKeys.all, 'leads'] as const,
  lead: (id: string) => [...queryKeys.leads(), id] as const,
  
  quiz: () => [...queryKeys.all, 'quiz'] as const,
  quizResults: (userId: string) => [...queryKeys.quiz(), 'results', userId] as const,
} as const;
```

## Basic Query Hook

```typescript
// hooks/queries/use-user.ts
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { queryKeys } from '@/lib/query/client';

export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string;
}

export function useUser(userId?: string) {
  return useQuery({
    queryKey: queryKeys.user(userId!),
    queryFn: () => apiClient<User>(`/users/${userId}`),
    enabled: !!userId, // Only run if userId exists
    staleTime: 5 * 60 * 1000, // Consider fresh for 5 minutes
  });
}
```

## Mutation Hook with Optimistic Updates

```typescript
// hooks/queries/use-update-user.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { queryKeys } from '@/lib/query/client';

interface UpdateUserData {
  name?: string;
  email?: string;
}

export function useUpdateUser(userId: string) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: UpdateUserData) => 
      apiClient<User>(`/users/${userId}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
      
    // Optimistic update
    onMutate: async (newData) => {
      // Cancel in-flight queries
      await queryClient.cancelQueries({ 
        queryKey: queryKeys.user(userId) 
      });
      
      // Get current data
      const previousUser = queryClient.getQueryData<User>(
        queryKeys.user(userId)
      );
      
      // Optimistically update
      queryClient.setQueryData<User>(
        queryKeys.user(userId),
        (old) => old ? { ...old, ...newData } : old
      );
      
      return { previousUser };
    },
    
    // Rollback on error
    onError: (err, newData, context) => {
      if (context?.previousUser) {
        queryClient.setQueryData(
          queryKeys.user(userId),
          context.previousUser
        );
      }
    },
    
    // Refetch after success
    onSettled: () => {
      queryClient.invalidateQueries({ 
        queryKey: queryKeys.user(userId) 
      });
    },
  });
}
```

## Infinite Query (Pagination)

```typescript
// hooks/queries/use-leads.ts
import { useInfiniteQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { queryKeys } from '@/lib/query/client';

interface LeadsResponse {
  data: Lead[];
  nextCursor?: string;
  hasMore: boolean;
}

export function useInfiniteLeads() {
  return useInfiniteQuery({
    queryKey: queryKeys.leads(),
    queryFn: ({ pageParam }) => 
      apiClient<LeadsResponse>(`/leads?cursor=${pageParam ?? ''}`),
    initialPageParam: '',
    getNextPageParam: (lastPage) => 
      lastPage.hasMore ? lastPage.nextCursor : undefined,
  });
}

// Usage in component:
function LeadsList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteLeads();
  
  const allLeads = data?.pages.flatMap(page => page.data) ?? [];
  
  return (
    <>
      {allLeads.map(lead => (
        <LeadCard key={lead.id} lead={lead} />
      ))}
      <Button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? 'Loading...' : 'Load More'}
      </Button>
    </>
  );
}
```

## Dependent Queries

```typescript
// hooks/queries/use-user-posts.ts
export function useUserWithPosts(userId?: string) {
  // First query: get user
  const userQuery = useQuery({
    queryKey: queryKeys.user(userId!),
    queryFn: () => apiClient<User>(`/users/${userId}`),
    enabled: !!userId,
  });
  
  // Second query: get posts (depends on user)
  const postsQuery = useQuery({
    queryKey: queryKeys.userPosts(userId!),
    queryFn: () => apiClient<Post[]>(`/users/${userId}/posts`),
    enabled: !!userQuery.data, // Only run after user loads
  });
  
  return {
    user: userQuery.data,
    posts: postsQuery.data,
    isLoading: userQuery.isLoading || postsQuery.isLoading,
    error: userQuery.error || postsQuery.error,
  };
}
```

## Prefetching

```typescript
// Prefetch on hover
function UserLink({ userId }: { userId: string }) {
  const queryClient = useQueryClient();
  
  const prefetchUser = () => {
    queryClient.prefetchQuery({
      queryKey: queryKeys.user(userId),
      queryFn: () => apiClient<User>(`/users/${userId}`),
      staleTime: 10 * 1000, // Only prefetch if older than 10s
    });
  };
  
  return (
    <Link 
      href={`/users/${userId}`}
      onMouseEnter={prefetchUser}
      onFocus={prefetchUser}
    >
      View Profile
    </Link>
  );
}
```

## Error Handling

```typescript
// Global error handling in component
function UserProfile({ userId }: { userId: string }) {
  const { data, error, isLoading } = useUser(userId);
  
  if (isLoading) {
    return <LoadingSpinner />;
  }
  
  if (error) {
    if (error.status === 404) {
      return <NotFound message="User not found" />;
    }
    return <ErrorMessage error={error} />;
  }
  
  return <UserDetails user={data} />;
}

// With error boundaries
import { QueryErrorResetBoundary } from '@tanstack/react-query';
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          fallbackRender={({ error, resetErrorBoundary }) => (
            <div>
              <p>Something went wrong: {error.message}</p>
              <Button onClick={resetErrorBoundary}>Try again</Button>
            </div>
          )}
        >
          <UserProfile userId="123" />
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}
```

## Form Integration

```typescript
// Using with React Hook Form
function EditUserForm({ userId }: { userId: string }) {
  const { data: user } = useUser(userId);
  const updateUser = useUpdateUser(userId);
  
  const form = useForm<UpdateUserData>({
    defaultValues: {
      name: user?.name ?? '',
      email: user?.email ?? '',
    },
  });
  
  const onSubmit = async (data: UpdateUserData) => {
    try {
      await updateUser.mutateAsync(data);
      toast.success('Profile updated!');
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };
  
  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
      <Button
        type="submit"
        disabled={updateUser.isPending}
      >
        {updateUser.isPending ? 'Saving...' : 'Save'}
      </Button>
    </form>
  );
}
```

## Cache Management

```typescript
// Manual cache updates
function useCreateLead() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateLeadData) => 
      apiClient<Lead>('/leads', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
      
    onSuccess: (newLead) => {
      // Add to list cache
      queryClient.setQueryData<Lead[]>(
        queryKeys.leads(),
        (old) => old ? [...old, newLead] : [newLead]
      );
      
      // Set individual cache
      queryClient.setQueryData(
        queryKeys.lead(newLead.id),
        newLead
      );
    },
  });
}

// Invalidate related queries
function useDeleteLead() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (leadId: string) => 
      apiClient(`/leads/${leadId}`, { method: 'DELETE' }),
      
    onSuccess: (_, leadId) => {
      // Remove from cache
      queryClient.removeQueries({ 
        queryKey: queryKeys.lead(leadId) 
      });
      
      // Invalidate list
      queryClient.invalidateQueries({ 
        queryKey: queryKeys.leads() 
      });
    },
  });
}
```

## Best Practices

1. **Use Query Key Factories**: Centralize query keys for consistency
2. **Set Appropriate Stale Times**: Balance freshness vs performance
3. **Handle Loading States**: Show skeletons or spinners
4. **Handle Error States**: Provide meaningful error messages
5. **Use Optimistic Updates**: For better UX on mutations
6. **Prefetch Critical Data**: Improve perceived performance
7. **Clean Up Cache**: Remove unused data to prevent memory leaks

## Common Patterns

### Background Refetch
```typescript
// Refetch in background every 30 seconds
useQuery({
  queryKey: ['dashboard-stats'],
  queryFn: fetchDashboardStats,
  refetchInterval: 30 * 1000, // 30 seconds
  refetchIntervalInBackground: true,
});
```

### Polling with Pause
```typescript
function usePollingData(shouldPoll: boolean) {
  return useQuery({
    queryKey: ['polling-data'],
    queryFn: fetchData,
    refetchInterval: shouldPoll ? 5000 : false,
  });
}
```

### Retry with Backoff
```typescript
useQuery({
  queryKey: ['flaky-api'],
  queryFn: fetchFromFlakyAPI,
  retry: 3,
  retryDelay: (attemptIndex) => 
    Math.min(1000 * 2 ** attemptIndex, 30000),
});
```
