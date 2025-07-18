# FreshSlate Database & ORM Guide

## Overview

We use PostgreSQL via Supabase with Drizzle ORM as our primary database interface, and Prisma for schema management and migrations.

## Technology Stack

- **PostgreSQL 15+** - Primary database (via Supabase)
- **Drizzle ORM** - Type-safe SQL queries and performance
- **Prisma** - Schema management and migrations
- **Bun** - Running migrations and scripts

## Database Architecture

### Why This Stack?

1. **PostgreSQL**: Battle-tested, full-featured RDBMS
2. **Drizzle**: Lightweight, type-safe, excellent performance
3. **Prisma**: Best-in-class migrations and schema management
4. **Supabase**: Managed PostgreSQL with realtime, auth, and RLS

## Drizzle Setup

### Installation

```bash
# Install Drizzle and PostgreSQL driver
pnpm add drizzle-orm postgres
pnpm add -D drizzle-kit

# Or with Bun
bun add drizzle-orm postgres
bun add -d drizzle-kit
```

### Configuration

```typescript
// drizzle.config.ts
import type { Config } from 'drizzle-kit';

export default {
  schema: './db/schema/*',
  out: './db/migrations',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
  verbose: true,
  strict: true,
} satisfies Config;
```

### Schema Definition

```typescript
// db/schema/leads.ts
import { pgTable, uuid, text, decimal, timestamp, jsonb, boolean, varchar, inet } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

export const leads = pgTable('leads', {
  id: uuid('id').defaultRandom().primaryKey(),
  // Personal info
  name: text('name').notNull(),
  email: text('email').notNull(),
  phone: text('phone').notNull(),
  state: varchar('state', { length: 2 }).notNull(),
  
  // Financial info
  debtAmount: decimal('debt_amount', { precision: 10, scale: 2 }).notNull(),
  debtTypes: text('debt_types').array().default([]),
  monthlyPayment: decimal('monthly_payment', { precision: 10, scale: 2 }),
  creditScoreRange: varchar('credit_score_range', { length: 50 }),
  
  // Attribution
  utmSource: text('utm_source'),
  utmMedium: text('utm_medium'),
  utmCampaign: text('utm_campaign'),
  gclid: text('gclid'),
  fbclid: text('fbclid'),
  
  // Metadata
  ipAddress: inet('ip_address'),
  userAgent: text('user_agent'),
  sessionId: text('session_id'),
  quizAnswers: jsonb('quiz_answers').default({}),
  
  // Status
  status: varchar('status', { length: 50 }).default('new'),
  qualificationStatus: varchar('qualification_status', { length: 50 }),
  partnerMatched: boolean('partner_matched').default(false),
  partnerId: uuid('partner_id'),
  
  // Timestamps
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
  contactedAt: timestamp('contacted_at'),
  convertedAt: timestamp('converted_at'),
});

// Relations
export const leadsRelations = relations(leads, ({ one, many }) => ({
  partner: one(partners, {
    fields: [leads.partnerId],
    references: [partners.id],
  }),
  events: many(analyticsEvents),
}));

// Type exports
export type Lead = typeof leads.$inferSelect;
export type NewLead = typeof leads.$inferInsert;
```

### Database Client

```typescript
// db/client.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

// For query purposes
const queryClient = postgres(process.env.DATABASE_URL!);
export const db = drizzle(queryClient, { schema });

// For migrations
const migrationClient = postgres(process.env.DATABASE_URL!, { max: 1 });
export const migrationDb = drizzle(migrationClient);
```

### Query Examples

```typescript
// lib/db/queries/leads.ts
import { db } from '@/db/client';
import { leads } from '@/db/schema/leads';
import { eq, desc, and, gte, sql } from 'drizzle-orm';

// Simple select
export async function getLeadById(id: string) {
  const result = await db
    .select()
    .from(leads)
    .where(eq(leads.id, id))
    .limit(1);
    
  return result[0];
}

// Complex query with joins
export async function getQualifiedLeadsWithPartners() {
  return await db
    .select({
      lead: leads,
      partnerName: partners.name,
      partnerAcceptanceRate: partners.acceptanceRate,
    })
    .from(leads)
    .leftJoin(partners, eq(leads.partnerId, partners.id))
    .where(
      and(
        eq(leads.qualificationStatus, 'qualified'),
        gte(leads.debtAmount, '10000')
      )
    )
    .orderBy(desc(leads.createdAt))
    .limit(100);
}

// Aggregation
export async function getLeadStats(startDate: Date) {
  const stats = await db
    .select({
      totalLeads: sql<number>`count(*)`,
      avgDebtAmount: sql<number>`avg(${leads.debtAmount})`,
      qualifiedCount: sql<number>`count(*) filter (where ${leads.qualificationStatus} = 'qualified')`,
      states: sql<string[]>`array_agg(distinct ${leads.state})`,
    })
    .from(leads)
    .where(gte(leads.createdAt, startDate));
    
  return stats[0];
}

// Transaction example
export async function createLeadWithEvents(leadData: NewLead, events: NewEvent[]) {
  return await db.transaction(async (tx) => {
    const [lead] = await tx
      .insert(leads)
      .values(leadData)
      .returning();
      
    const eventData = events.map(event => ({
      ...event,
      leadId: lead.id,
    }));
    
    await tx.insert(analyticsEvents).values(eventData);
    
    return lead;
  });
}

// Prepared statements for performance
const preparedGetByEmail = db
  .select()
  .from(leads)
  .where(eq(leads.email, sql.placeholder('email')))
  .prepare('getLeadByEmail');

export async function getLeadByEmail(email: string) {
  const result = await preparedGetByEmail.execute({ email });
  return result[0];
}
```

## Prisma Setup (For Migrations)

### Installation

```bash
# Install Prisma
pnpm add -D prisma
pnpm add @prisma/client

# Or with Bun
bun add -d prisma
bun add @prisma/client
```

### Schema Definition

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Lead {
  id                   String    @id @default(uuid())
  // Personal info
  name                 String
  email                String
  phone                String
  state                String    @db.VarChar(2)
  
  // Financial info
  debtAmount          Decimal   @map("debt_amount") @db.Decimal(10, 2)
  debtTypes           String[]  @map("debt_types")
  monthlyPayment      Decimal?  @map("monthly_payment") @db.Decimal(10, 2)
  creditScoreRange    String?   @map("credit_score_range") @db.VarChar(50)
  
  // Attribution
  utmSource           String?   @map("utm_source")
  utmMedium           String?   @map("utm_medium")
  utmCampaign         String?   @map("utm_campaign")
  gclid               String?
  fbclid              String?
  
  // Metadata
  ipAddress           String?   @map("ip_address") @db.Inet
  userAgent           String?   @map("user_agent")
  sessionId           String?   @map("session_id")
  quizAnswers         Json?     @map("quiz_answers")
  
  // Status
  status              String    @default("new") @db.VarChar(50)
  qualificationStatus String?   @map("qualification_status") @db.VarChar(50)
  partnerMatched      Boolean   @default(false) @map("partner_matched")
  partnerId           String?   @map("partner_id") @db.Uuid
  
  // Timestamps
  createdAt           DateTime  @default(now()) @map("created_at")
  updatedAt           DateTime  @updatedAt @map("updated_at")
  contactedAt         DateTime? @map("contacted_at")
  convertedAt         DateTime? @map("converted_at")
  
  // Relations
  partner             Partner?  @relation(fields: [partnerId], references: [id])
  events              AnalyticsEvent[]
  
  @@index([createdAt(sort: Desc)])
  @@index([email])
  @@index([phone])
  @@index([status])
  @@index([partnerId])
  @@map("leads")
}
```

### Migration Workflow

```bash
# Create migration from schema changes
pnpm prisma migrate dev --name add_lead_scoring

# Apply migrations in production
pnpm prisma migrate deploy

# Generate Prisma Client (for type checking)
pnpm prisma generate

# Open Prisma Studio
pnpm prisma studio
```

## Bun Scripts

### Database Scripts

```typescript
// scripts/migrate.ts
#!/usr/bin/env bun
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import { migrationDb } from '@/db/client';

async function runMigrations() {
  console.log('Running migrations...');
  
  await migrate(migrationDb, {
    migrationsFolder: './db/migrations',
  });
  
  console.log('Migrations complete!');
  process.exit(0);
}

runMigrations().catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
```

```typescript
// scripts/seed.ts
#!/usr/bin/env bun
import { db } from '@/db/client';
import { leads, partners } from '@/db/schema';

async function seed() {
  console.log('Seeding database...');
  
  // Create test partners
  const testPartners = await db
    .insert(partners)
    .values([
      {
        name: 'ABC Debt Relief',
        type: 'settlement',
        statesLicensed: ['CA', 'TX', 'FL'],
        minDebtAmount: '10000',
        maxDebtAmount: '100000',
      },
      {
        name: 'Credit Counseling Corp',
        type: 'counseling',
        statesLicensed: ['ALL'],
        minDebtAmount: '5000',
        maxDebtAmount: '50000',
      },
    ])
    .returning();
    
  // Create test leads
  const testLeads = await db
    .insert(leads)
    .values([
      {
        name: 'Test User 1',
        email: 'test1@example.com',
        phone: '5555551234',
        state: 'CA',
        debtAmount: '25000',
        debtTypes: ['credit_card', 'medical'],
      },
      {
        name: 'Test User 2',
        email: 'test2@example.com',
        phone: '5555555678',
        state: 'TX',
        debtAmount: '15000',
        debtTypes: ['credit_card'],
      },
    ])
    .returning();
    
  console.log(`Created ${testPartners.length} partners and ${testLeads.length} leads`);
}

seed()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error('Seeding failed:', err);
    process.exit(1);
  });
```

## Performance Optimization

### Connection Pooling

```typescript
// db/pool.ts
import postgres from 'postgres';

// Create connection pool
const sql = postgres({
  max: 20,                    // Max connections
  idle_timeout: 20,           // Seconds
  connect_timeout: 10,        // Seconds
  max_lifetime: 60 * 30,      // 30 minutes
  
  // SSL for production
  ssl: process.env.NODE_ENV === 'production' ? 'require' : false,
  
  // Connection string
  connection: {
    application_name: 'freshslate-app',
  },
  
  // Transform keys to camelCase
  transform: postgres.camel,
});

export default sql;
```

### Query Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_leads_created_at_desc ON leads(created_at DESC);
CREATE INDEX idx_leads_email_lower ON leads(LOWER(email));
CREATE INDEX idx_leads_status_qualified ON leads(status) WHERE status = 'qualified';
CREATE INDEX idx_leads_debt_amount ON leads(debt_amount);
CREATE INDEX idx_leads_state_debt ON leads(state, debt_amount);

-- Partial indexes for performance
CREATE INDEX idx_active_leads ON leads(created_at DESC) 
WHERE status != 'archived' AND partner_matched = false;

-- Composite indexes for partner matching
CREATE INDEX idx_partner_matching ON leads(state, debt_amount, qualification_status)
WHERE partner_matched = false;
```

## Best Practices

1. **Use Drizzle for queries**: Better performance and type safety
2. **Use Prisma for migrations**: Better migration tooling
3. **Always use transactions**: For related operations
4. **Prepare statements**: For frequently used queries
5. **Use connection pooling**: Manage connections efficiently
6. **Index strategically**: Based on query patterns
7. **Monitor slow queries**: Use pg_stat_statements

## Common Patterns

### Soft Deletes

```typescript
// Add deleted_at column
export const leads = pgTable('leads', {
  // ... other columns
  deletedAt: timestamp('deleted_at'),
});

// Query only active records
export async function getActiveLeads() {
  return await db
    .select()
    .from(leads)
    .where(isNull(leads.deletedAt));
}

// Soft delete
export async function softDeleteLead(id: string) {
  return await db
    .update(leads)
    .set({ deletedAt: new Date() })
    .where(eq(leads.id, id));
}
```

### Audit Logging

```typescript
// Trigger for updated_at
const updateTimestampTrigger = sql`
  CREATE OR REPLACE FUNCTION update_updated_at()
  RETURNS TRIGGER AS $$
  BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;

  CREATE TRIGGER update_leads_updated_at
  BEFORE UPDATE ON leads
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
`;
```

### Full-Text Search

```typescript
// Add search vector
export const leads = pgTable('leads', {
  // ... other columns
  searchVector: text('search_vector'),
});

// Search query
export async function searchLeads(query: string) {
  return await db
    .select()
    .from(leads)
    .where(
      sql`${leads.searchVector} @@ plainto_tsquery('english', ${query})`
    )
    .orderBy(
      sql`ts_rank(${leads.searchVector}, plainto_tsquery('english', ${query})) DESC`
    );
}
```

## Troubleshooting

### Common Issues

1. **Connection timeout**: Increase pool size or connection timeout
2. **Type errors**: Regenerate types after schema changes
3. **Migration conflicts**: Use `prisma migrate resolve`
4. **Performance issues**: Check query plans with EXPLAIN ANALYZE

### Debug Mode

```typescript
// Enable query logging
const db = drizzle(queryClient, {
  logger: true,
});

// Or custom logger
const db = drizzle(queryClient, {
  logger: {
    logQuery(query, params) {
      console.log('Query:', query);
      console.log('Params:', params);
    },
  },
});
```