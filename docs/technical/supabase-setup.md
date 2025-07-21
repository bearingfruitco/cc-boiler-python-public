# Supabase Setup Guide

**Official Documentation**: https://supabase.com/docs

## Overview

Supabase provides PostgreSQL database, real-time subscriptions, authentication, and edge functions. This guide covers setup and common patterns.

## MCP Tool Usage

When using Claude with Supabase MCP:
```typescript
// @mcp-tool: supabase
// Available commands:
// - Query tables
// - Insert/update data
// - Manage schemas
// - Execute SQL
```

## Database Schema

### Core Tables Example

```sql
-- Users table
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  -- Basic info
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE,
  full_name TEXT,
  avatar_url TEXT,
  
  -- Metadata
  metadata JSONB DEFAULT '{}',
  preferences JSONB DEFAULT '{}',
  
  -- Status
  status VARCHAR(50) DEFAULT 'active',
  role VARCHAR(50) DEFAULT 'user',
  
  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  last_seen_at TIMESTAMPTZ
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
CREATE INDEX idx_users_status ON users(status);

-- Content table example
CREATE TABLE content (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  body TEXT,
  metadata JSONB DEFAULT '{}',
  
  -- Status
  status VARCHAR(50) DEFAULT 'draft',
  published_at TIMESTAMPTZ,
  
  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Analytics events table
CREATE TABLE analytics_events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  event_name TEXT NOT NULL,
  user_id UUID REFERENCES users(id),
  session_id TEXT,
  properties JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Settings/configuration table
CREATE TABLE settings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  key TEXT UNIQUE NOT NULL,
  value JSONB NOT NULL,
  description TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Row Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE content ENABLE ROW LEVEL SECURITY;

-- Service role can do everything
CREATE POLICY "Service role has full access" ON users
  FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- Users can view their own data
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (id = auth.uid());

-- Users can update their own data
CREATE POLICY "Users can update own data" ON users
  FOR UPDATE USING (id = auth.uid());

-- Content policies
CREATE POLICY "Anyone can view published content" ON content
  FOR SELECT USING (status = 'published');

CREATE POLICY "Users can manage own content" ON content
  FOR ALL USING (user_id = auth.uid());
```

## Supabase Client Setup

### Initialize Client
```typescript
// lib/supabase/client.ts
import { createClient } from '@supabase/supabase-js';
import type { Database } from '@/types/supabase';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  },
});

// For server-side operations
export const supabaseAdmin = createClient<Database>(
  supabaseUrl,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  }
);
```

### Type Generation
```bash
# Generate TypeScript types from database
npx supabase gen types typescript --project-id YOUR_PROJECT_ID > types/supabase.ts
```

## Common Query Patterns

### CRUD Operations
```typescript
// lib/db/queries/users.ts
import { supabase } from '@/lib/supabase/client';

// Simple select
export async function getUserById(id: string) {
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', id)
    .single();
    
  if (error) throw error;
  return data;
}

// Select with pagination
export async function getUsers(page = 1, limit = 20) {
  const from = (page - 1) * limit;
  const to = from + limit - 1;
  
  const { data, error, count } = await supabase
    .from('users')
    .select('*', { count: 'exact' })
    .order('created_at', { ascending: false })
    .range(from, to);
    
  if (error) throw error;
  
  return {
    users: data || [],
    total: count || 0,
    page,
    totalPages: Math.ceil((count || 0) / limit),
  };
}

// Insert
export async function createUser(userData: any) {
  const { data, error } = await supabase
    .from('users')
    .insert(userData)
    .select()
    .single();
    
  if (error) throw error;
  return data;
}

// Update
export async function updateUser(id: string, updates: any) {
  const { data, error } = await supabase
    .from('users')
    .update(updates)
    .eq('id', id)
    .select()
    .single();
    
  if (error) throw error;
  return data;
}

// Delete (soft delete recommended)
export async function deleteUser(id: string) {
  const { error } = await supabase
    .from('users')
    .update({ status: 'deleted' })
    .eq('id', id);
    
  if (error) throw error;
}
```

### Advanced Queries
```typescript
// Complex filtering
export async function searchUsers(query: string, filters: any = {}) {
  let supabaseQuery = supabase
    .from('users')
    .select('*');
    
  // Text search
  if (query) {
    supabaseQuery = supabaseQuery.or(
      `email.ilike.%${query}%,username.ilike.%${query}%,full_name.ilike.%${query}%`
    );
  }
  
  // Apply filters
  if (filters.status) {
    supabaseQuery = supabaseQuery.eq('status', filters.status);
  }
  
  if (filters.role) {
    supabaseQuery = supabaseQuery.eq('role', filters.role);
  }
  
  if (filters.dateFrom) {
    supabaseQuery = supabaseQuery.gte('created_at', filters.dateFrom);
  }
  
  const { data, error } = await supabaseQuery
    .order('created_at', { ascending: false })
    .limit(50);
    
  if (error) throw error;
  return data;
}

// Joins
export async function getUsersWithContent() {
  const { data, error } = await supabase
    .from('users')
    .select(`
      *,
      content (
        id,
        title,
        status,
        created_at
      )
    `)
    .order('created_at', { ascending: false });
    
  if (error) throw error;
  return data;
}

// Aggregations
export async function getUserStats() {
  const { data, error } = await supabase
    .rpc('get_user_stats'); // Call a database function
    
  if (error) throw error;
  return data;
}
```

## Real-time Subscriptions

```typescript
// components/RealtimeComponent.tsx
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase/client';

export function RealtimeComponent() {
  const [items, setItems] = useState<any[]>([]);
  
  useEffect(() => {
    // Initial fetch
    fetchItems();
    
    // Subscribe to changes
    const subscription = supabase
      .channel('items-channel')
      .on(
        'postgres_changes',
        {
          event: '*', // INSERT, UPDATE, DELETE
          schema: 'public',
          table: 'items',
        },
        (payload) => {
          console.log('Change received!', payload);
          
          if (payload.eventType === 'INSERT') {
            setItems(current => [payload.new, ...current]);
          } else if (payload.eventType === 'UPDATE') {
            setItems(current => 
              current.map(item => 
                item.id === payload.new.id ? payload.new : item
              )
            );
          } else if (payload.eventType === 'DELETE') {
            setItems(current => 
              current.filter(item => item.id !== payload.old.id)
            );
          }
        }
      )
      .subscribe();
    
    return () => {
      subscription.unsubscribe();
    };
  }, []);
  
  const fetchItems = async () => {
    const { data } = await supabase
      .from('items')
      .select('*')
      .order('created_at', { ascending: false });
      
    if (data) setItems(data);
  };
  
  return (
    <div>
      {items.map((item) => (
        <ItemCard key={item.id} item={item} />
      ))}
    </div>
  );
}
```

## Database Functions

### Creating Functions
```sql
-- Function to calculate statistics
CREATE OR REPLACE FUNCTION get_user_stats()
RETURNS TABLE (
  total_users BIGINT,
  active_users BIGINT,
  new_users_today BIGINT
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(*)::BIGINT as total_users,
    COUNT(CASE WHEN status = 'active' THEN 1 END)::BIGINT as active_users,
    COUNT(CASE WHEN created_at >= CURRENT_DATE THEN 1 END)::BIGINT as new_users_today
  FROM users;
END;
$$ LANGUAGE plpgsql;

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();
```

## Edge Functions

### Edge Function Example
```typescript
// supabase/functions/process-data/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const { data } = await req.json();
    
    // Process data
    const processed = processData(data);
    
    // Create Supabase client
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );
    
    // Store results
    const { error } = await supabase
      .from('processed_data')
      .insert(processed);
      
    if (error) throw error;
    
    return new Response(
      JSON.stringify({ success: true, data: processed }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
});

function processData(data: any) {
  // Your processing logic
  return {
    ...data,
    processed_at: new Date().toISOString(),
  };
}
```

## Authentication

### Auth Setup
```typescript
// lib/auth.ts
import { supabase } from './supabase/client';

export async function signUp(email: string, password: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  });
  
  if (error) throw error;
  return data;
}

export async function signIn(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  
  if (error) throw error;
  return data;
}

export async function signOut() {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}

export async function getSession() {
  const { data: { session } } = await supabase.auth.getSession();
  return session;
}
```

## Best Practices

1. **Use RLS**: Always enable Row Level Security
2. **Type Safety**: Generate and use TypeScript types
3. **Error Handling**: Always handle errors appropriately
4. **Connection Pooling**: Use appropriate client for context
5. **Indexes**: Add indexes for frequently queried columns
6. **Soft Deletes**: Prefer soft deletes over hard deletes
7. **Migrations**: Use migrations for schema changes

## Common Patterns

### Pagination
```typescript
const pageSize = 20;
const { data, count } = await supabase
  .from('items')
  .select('*', { count: 'exact' })
  .range((page - 1) * pageSize, page * pageSize - 1)
  .order('created_at', { ascending: false });
```

### Full-text Search
```sql
-- Add search vector
ALTER TABLE content ADD COLUMN search_vector tsvector;

-- Update search vector
UPDATE content SET search_vector = 
  to_tsvector('english', title || ' ' || coalesce(body, ''));

-- Create index
CREATE INDEX idx_content_search ON content USING gin(search_vector);
```

### Soft Delete
```typescript
// Don't delete, mark as deleted
await supabase
  .from('items')
  .update({ deleted_at: new Date().toISOString() })
  .eq('id', itemId);
```

## Testing Locally

```bash
# Start Supabase locally
npx supabase start

# Run migrations
npx supabase migration up

# Generate types
npx supabase gen types typescript --local > types/supabase.ts

# Test edge functions
npx supabase functions serve process-data --env-file .env.local
```