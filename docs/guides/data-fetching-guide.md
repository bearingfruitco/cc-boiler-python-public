# Data Fetching Guide with SWR

## Overview

This guide covers data fetching patterns using SWR (stale-while-revalidate) for FreshSlate applications. SWR provides powerful data synchronization with features like caching, revalidation, focus tracking, and refetching.

## Why SWR?

- **Built-in Cache**: Automatic deduplication and caching
- **Real-time**: Revalidation on focus, network recovery
- **Optimistic UI**: Update UI immediately, sync with server
- **Error Handling**: Built-in error retry with exponential backoff
- **TypeScript**: First-class TypeScript support
- **React Suspense**: Ready for concurrent features

## Setup and Configuration

### Installation

```bash
pnpm add swr
```

### Global Configuration

```typescript
// app/providers.tsx
import { SWRConfig } from 'swr';

const fetcher = async (url: string) => {
  const res = await fetch(url);
  
  if (!res.ok) {
    const error = new Error('An error occurred while fetching the data.');
    error.info = await res.json();
    error.status = res.status;
    throw error;
  }
  
  return res.json();
};

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SWRConfig
      value={{
        fetcher,
        revalidateOnFocus: false, // Disable for lead forms
        revalidateOnReconnect: true,
        refreshInterval: 0, // No automatic refresh
        errorRetryCount: 3,
        errorRetryInterval: 5000,
        shouldRetryOnError: (error) => {
          // Don't retry on 4xx errors
          return error.status >= 500;
        },
        onError: (error, key) => {
          // Log to error tracking
          console.error(`SWR Error for ${key}:`, error);
        },
      }}
    >
      {children}
    </SWRConfig>
  );
}
```

## Core Patterns

### 1. Basic Data Fetching

```typescript
// hooks/queries/useLeads.ts
import useSWR from 'swr';

interface Lead {
  id: string;
  name: string;
  email: string;
  debt_amount: number;
  status: string;
  created_at: string;
}

interface LeadsResponse {
  data: Lead[];
  total: number;
  page: number;
  per_page: number;
}

export function useLeads(page = 1, filters?: Record<string, any>) {
  const params = new URLSearchParams({
    page: page.toString(),
    ...filters,
  });
  
  const { data, error, isLoading, isValidating, mutate } = useSWR<LeadsResponse>(
    `/api/leads?${params}`,
    {
      revalidateOnMount: true,
      dedupingInterval: 2000,
    }
  );
  
  return {
    leads: data?.data ?? [],
    total: data?.total ?? 0,
    isLoading,
    isValidating,
    isError: error,
    refresh: mutate,
  };
}
```

### 2. Dependent Fetching

```typescript
// hooks/queries/useLeadDetails.ts
export function useLeadDetails(leadId: string | null) {
  const { data: lead, error: leadError } = useSWR(
    leadId ? `/api/leads/${leadId}` : null
  );
  
  const { data: interactions } = useSWR(
    lead ? `/api/leads/${leadId}/interactions` : null
  );
  
  const { data: qualificationStatus } = useSWR(
    lead ? `/api/leads/${leadId}/qualification` : null
  );
  
  return {
    lead,
    interactions,
    qualificationStatus,
    isLoading: !lead && !leadError && leadId !== null,
    isError: leadError,
  };
}
```

### 3. Pagination with SWR

```typescript
// hooks/queries/usePaginatedLeads.ts
import { useSWRInfinite } from 'swr/infinite';

export function usePaginatedLeads(filters?: Record<string, any>) {
  const getKey = (pageIndex: number, previousPageData: LeadsResponse) => {
    // Return null to stop fetching
    if (previousPageData && !previousPageData.data.length) return null;
    
    const params = new URLSearchParams({
      page: (pageIndex + 1).toString(),
      limit: '20',
      ...filters,
    });
    
    return `/api/leads?${params}`;
  };
  
  const {
    data,
    error,
    size,
    setSize,
    isValidating,
    isLoading,
    mutate,
  } = useSWRInfinite<LeadsResponse>(getKey, {
    revalidateFirstPage: false,
    revalidateAll: false,
  });
  
  const leads = data ? data.flatMap(page => page.data) : [];
  const isLoadingMore = isLoading || (size > 0 && data && typeof data[size - 1] === 'undefined');
  const isEmpty = data?.[0]?.data.length === 0;
  const isReachingEnd = isEmpty || (data && data[data.length - 1]?.data.length < 20);
  
  return {
    leads,
    error,
    isLoading,
    isLoadingMore,
    isReachingEnd,
    size,
    setSize,
    mutate,
  };
}
```

### 4. Mutations with SWR

```typescript
// hooks/mutations/useCreateLead.ts
import useSWRMutation from 'swr/mutation';

async function createLead(url: string, { arg }: { arg: any }) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(arg),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create lead');
  }
  
  return response.json();
}

export function useCreateLead() {
  const { trigger, isMutating, error } = useSWRMutation(
    '/api/leads',
    createLead,
    {
      onSuccess: (data) => {
        // Optimistically update the cache
        mutate(
          (key) => typeof key === 'string' && key.startsWith('/api/leads'),
          undefined,
          { revalidate: true }
        );
      },
      onError: (err) => {
        console.error('Failed to create lead:', err);
      },
    }
  );
  
  return {
    createLead: trigger,
    isCreating: isMutating,
    error,
  };
}
```

### 5. Optimistic Updates

```typescript
// hooks/mutations/useUpdateLead.ts
import useSWRMutation from 'swr/mutation';
import { mutate } from 'swr';

async function updateLead(url: string, { arg }: { arg: { id: string; data: any } }) {
  const response = await fetch(`/api/leads/${arg.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(arg.data),
  });
  
  if (!response.ok) {
    throw new Error('Failed to update lead');
  }
  
  return response.json();
}

export function useUpdateLead() {
  const { trigger, isMutating } = useSWRMutation(
    '/api/leads',
    updateLead,
    {
      onSuccess: async (data, variables) => {
        // Update specific lead in cache
        await mutate(`/api/leads/${variables.arg.id}`, data, false);
        
        // Revalidate list views
        await mutate(
          (key) => typeof key === 'string' && key.startsWith('/api/leads?'),
          undefined,
          { revalidate: true }
        );
      },
      optimisticData: (current, variables) => {
        // Immediately update UI
        return { ...current, ...variables.arg.data };
      },
      rollbackOnError: true,
    }
  );
  
  return {
    updateLead: trigger,
    isUpdating: isMutating,
  };
}
```

## Advanced Patterns

### 1. Real-time Data Sync

```typescript
// hooks/queries/useRealtimeLeads.ts
import useSWR from 'swr';
import { useEffect } from 'react';

export function useRealtimeLeads() {
  const { data, mutate } = useSWR('/api/leads', {
    refreshInterval: 5000, // Poll every 5 seconds
  });
  
  useEffect(() => {
    // WebSocket connection for real-time updates
    const ws = new WebSocket(process.env.NEXT_PUBLIC_WS_URL);
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      
      if (update.type === 'lead_created' || update.type === 'lead_updated') {
        // Revalidate data
        mutate();
      }
    };
    
    return () => ws.close();
  }, [mutate]);
  
  return { leads: data?.data ?? [] };
}
```

### 2. Request Deduplication

```typescript
// hooks/queries/useLeadStats.ts
const STATS_KEY = '/api/stats/leads';

export function useLeadStats() {
  return useSWR(STATS_KEY, {
    dedupingInterval: 60000, // Dedupe requests within 1 minute
    focusThrottleInterval: 60000, // Throttle revalidation on focus
  });
}

// Multiple components can call this hook
// SWR will only make one request
export function useDashboardStats() {
  const { data: leadStats } = useLeadStats();
  const { data: conversionStats } = useConversionStats();
  
  return {
    totalLeads: leadStats?.total ?? 0,
    conversionRate: conversionStats?.rate ?? 0,
  };
}
```

### 3. Cache Management

```typescript
// lib/swr-cache.ts
import { mutate } from 'swr';

export const swrCache = {
  // Clear all cache
  clearAll: () => mutate(() => true, undefined, { revalidate: false }),
  
  // Clear specific pattern
  clearPattern: (pattern: string) => {
    mutate(
      (key) => typeof key === 'string' && key.includes(pattern),
      undefined,
      { revalidate: false }
    );
  },
  
  // Revalidate pattern
  revalidatePattern: (pattern: string) => {
    mutate(
      (key) => typeof key === 'string' && key.includes(pattern),
      undefined,
      { revalidate: true }
    );
  },
  
  // Prefetch data
  prefetch: async (key: string, fetcher: () => Promise<any>) => {
    const data = await fetcher();
    mutate(key, data, { revalidate: false });
  },
};
```

### 4. Error Handling & Retry

```typescript
// hooks/queries/useLeadsWithRetry.ts
export function useLeadsWithRetry() {
  const { data, error, mutate } = useSWR('/api/leads', {
    onErrorRetry: (error, key, config, revalidate, { retryCount }) => {
      // Never retry on 404
      if (error.status === 404) return;
      
      // Only retry up to 3 times
      if (retryCount >= 3) return;
      
      // Retry after 5 seconds
      setTimeout(() => revalidate({ retryCount }), 5000);
    },
  });
  
  const retry = () => mutate();
  
  return {
    leads: data?.data ?? [],
    error,
    retry,
  };
}
```

### 5. Suspense Mode

```typescript
// hooks/queries/useLeadsSuspense.ts
import useSWR from 'swr';

export function useLeadsSuspense() {
  const { data } = useSWR('/api/leads', {
    suspense: true, // Enable suspense mode
  });
  
  // Data is guaranteed to be defined in suspense mode
  return { leads: data.data };
}

// Usage with Suspense
export function LeadsPage() {
  return (
    <Suspense fallback={<LeadsSkeletonLoader />}>
      <LeadsList />
    </Suspense>
  );
}
```

## Integration with Zustand

### Syncing SWR with Zustand Store

```typescript
// hooks/useSyncLeadStore.ts
import { useEffect } from 'react';
import { useLeadStore } from '@/stores/lead-store';
import useSWR from 'swr';

export function useSyncLeadStore(leadId: string) {
  const { data: lead } = useSWR(`/api/leads/${leadId}`);
  const setFormData = useLeadStore((state) => state.setFormData);
  
  useEffect(() => {
    if (lead) {
      setFormData({
        name: lead.name,
        email: lead.email,
        phone: lead.phone,
        debtAmount: lead.debt_amount,
      });
    }
  }, [lead, setFormData]);
  
  return { lead };
}
```

## Testing SWR Hooks

```typescript
// __tests__/hooks/useLeads.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { SWRConfig } from 'swr';
import { useLeads } from '@/hooks/queries/useLeads';

const wrapper = ({ children }) => (
  <SWRConfig value={{ dedupingInterval: 0 }}>
    {children}
  </SWRConfig>
);

describe('useLeads', () => {
  it('fetches leads successfully', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          data: [{ id: '1', name: 'Test Lead' }],
          total: 1,
        }),
      })
    );
    
    const { result } = renderHook(() => useLeads(), { wrapper });
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.leads).toHaveLength(1);
    expect(result.current.leads[0].name).toBe('Test Lead');
  });
});
```

## Performance Optimization

### 1. Preloading Data

```typescript
// lib/swr-preload.ts
import { preload } from 'swr';

// Preload data before navigation
export function preloadLeadDetails(leadId: string) {
  preload(`/api/leads/${leadId}`, fetcher);
}

// Usage in Link component
<Link 
  href={`/leads/${lead.id}`}
  onMouseEnter={() => preloadLeadDetails(lead.id)}
>
  View Details
</Link>
```

### 2. Request Batching

```typescript
// lib/batch-fetcher.ts
let batchQueue: Array<{ key: string; resolve: (data: any) => void }> = [];
let batchTimer: NodeJS.Timeout | null = null;

async function executeBatch() {
  const batch = [...batchQueue];
  batchQueue = [];
  
  const keys = batch.map(item => item.key);
  const response = await fetch('/api/batch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ keys }),
  });
  
  const results = await response.json();
  
  batch.forEach((item, index) => {
    item.resolve(results[index]);
  });
}

export function batchFetcher(key: string): Promise<any> {
  return new Promise((resolve) => {
    batchQueue.push({ key, resolve });
    
    if (batchTimer) clearTimeout(batchTimer);
    batchTimer = setTimeout(executeBatch, 10);
  });
}
```

### 3. Partial Data Updates

```typescript
// hooks/mutations/usePartialUpdate.ts
export function usePartialUpdate() {
  const { trigger } = useSWRMutation('/api/leads', updateLead);
  
  const updateField = async (id: string, field: string, value: any) => {
    // Optimistically update only the changed field
    await mutate(
      `/api/leads/${id}`,
      (current) => ({
        ...current,
        [field]: value,
      }),
      false
    );
    
    // Send update to server
    await trigger({ id, data: { [field]: value } });
  };
  
  return { updateField };
}
```

## Common Patterns for Lead Generation

### 1. Lead List with Filters

```typescript
// components/leads/LeadsList.tsx
export function LeadsList() {
  const [filters, setFilters] = useState({
    status: 'all',
    dateRange: 'today',
  });
  
  const { leads, isLoading, error } = useLeads(1, filters);
  
  if (error) return <ErrorMessage error={error} />;
  if (isLoading) return <LeadsSkeletonLoader />;
  
  return (
    <div>
      <LeadFilters filters={filters} onChange={setFilters} />
      <div className="space-y-4">
        {leads.map(lead => (
          <LeadCard key={lead.id} lead={lead} />
        ))}
      </div>
    </div>
  );
}
```

### 2. Auto-refresh Dashboard

```typescript
// components/dashboard/LeadsDashboard.tsx
export function LeadsDashboard() {
  const { data: stats } = useSWR('/api/stats/leads', {
    refreshInterval: 30000, // Refresh every 30 seconds
    revalidateOnFocus: true,
  });
  
  const { data: recentLeads } = useSWR('/api/leads?limit=5&sort=created_at', {
    refreshInterval: 10000, // Refresh every 10 seconds
  });
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <StatsCard title="Total Leads" value={stats?.total ?? 0} />
      <StatsCard title="Conversion Rate" value={`${stats?.conversionRate ?? 0}%`} />
      <RecentLeadsList leads={recentLeads?.data ?? []} />
    </div>
  );
}
```

### 3. Lead Form with Draft Saving

```typescript
// components/forms/LeadFormWithDraft.tsx
export function LeadFormWithDraft() {
  const { formData, updateField } = useLeadStore();
  const { trigger: saveDraft } = useSWRMutation('/api/leads/draft', createDraft);
  
  // Auto-save draft every 5 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      if (Object.keys(formData).length > 0) {
        saveDraft(formData);
      }
    }, 5000);
    
    return () => clearInterval(timer);
  }, [formData, saveDraft]);
  
  return (
    <form>
      {/* Form fields */}
    </form>
  );
}
```

## Best Practices

1. **Use Error Boundaries**: Wrap SWR components with error boundaries
2. **Set Proper Cache Keys**: Use consistent, unique keys
3. **Handle Loading States**: Always show loading indicators
4. **Optimize Revalidation**: Disable unnecessary revalidation
5. **Use Suspense Carefully**: Only for non-critical data
6. **Prefetch Important Data**: Improve perceived performance
7. **Clean Up Subscriptions**: Cancel requests on unmount

## Resources

- [SWR Documentation](https://swr.vercel.app/)
- [SWR GitHub](https://github.com/vercel/swr)
- [Data Fetching Patterns](https://swr.vercel.app/docs/advanced/patterns)
- [SWR DevTools](https://swr-devtools.vercel.app/)