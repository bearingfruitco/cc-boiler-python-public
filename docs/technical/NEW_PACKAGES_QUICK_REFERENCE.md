# 🚀 New Package Quick Reference

Quick reference for the new packages added in v2.0.0 based on 2025 ecosystem research.

## 🔐 Authentication Setup

### Auth.js (next-auth) v5
```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from "next-auth"
import { authConfig } from "@/lib/auth"

const handler = NextAuth(authConfig)
export { handler as GET, handler as POST }

// lib/auth.ts
import type { NextAuthConfig } from "next-auth"
import Credentials from "next-auth/providers/credentials"

export const authConfig: NextAuthConfig = {
  providers: [
    Credentials({
      // Your credentials config
    })
  ],
  // Use jose for JWT
  jwt: {
    encode: async ({ token }) => {
      // Custom JWT encoding with jose
    }
  }
}
```

## 🎨 Radix UI Components

### Dialog Example
```tsx
import * as Dialog from '@radix-ui/react-dialog';

<Dialog.Root>
  <Dialog.Trigger asChild>
    <button className="Button">Open</button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="DialogOverlay" />
    <Dialog.Content className="DialogContent">
      <Dialog.Title>Title</Dialog.Title>
      <Dialog.Description>Description</Dialog.Description>
      <Dialog.Close asChild>
        <button className="IconButton">X</button>
      </Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

### Dropdown Menu
```tsx
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

<DropdownMenu.Root>
  <DropdownMenu.Trigger>Options</DropdownMenu.Trigger>
  <DropdownMenu.Portal>
    <DropdownMenu.Content>
      <DropdownMenu.Item>Edit</DropdownMenu.Item>
      <DropdownMenu.Item>Delete</DropdownMenu.Item>
    </DropdownMenu.Content>
  </DropdownMenu.Portal>
</DropdownMenu.Root>
```

## 📅 Date-fns v4 with Timezones

### Basic Usage
```typescript
import { format, parseISO } from 'date-fns';
import { toZonedTime } from '@date-fns/tz';

// Format date
const formatted = format(new Date(), 'yyyy-MM-dd');

// Work with timezones
const utcDate = new Date();
const nyTime = toZonedTime(utcDate, 'America/New_York');
```

## 🧪 Testing with MSW

### API Mocking
```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/user', () => {
    return HttpResponse.json({
      id: '123',
      name: 'John Doe'
    });
  }),
];

// mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);
```

### Test Data with Faker
```typescript
import { faker } from '@faker-js/faker';

const user = {
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  avatar: faker.image.avatar(),
};
```

## 🛠️ Developer Tools

### Concurrently
```json
// package.json
{
  "scripts": {
    "dev:all": "concurrently \"npm:dev\" \"npm:db:studio\"",
    "dev": "next dev --turbopack",
    "db:studio": "drizzle-kit studio"
  }
}
```

### TSX for Scripts
```bash
# Run TypeScript directly
tsx scripts/migrate.ts

# Watch mode
tsx watch scripts/seed.ts
```

## 🚀 Turbopack Dev

Already configured in package.json:
```json
{
  "scripts": {
    "dev": "next dev --turbopack"
  }
}
```

Benefits:
- 76.7% faster startup
- Better HMR performance
- Improved memory usage

## 📦 Bundle Size Impact

New packages add minimal overhead:
- Radix UI: ~5-10kb per component (tree-shakeable)
- date-fns v4: 1.6kb min (tree-shakeable)
- Auth.js: ~50kb (auth pages only)
- MSW: Dev only (0kb in production)
- faker: Dev only (0kb in production)

## 🎯 Next Steps

1. **Set up Auth.js**:
   ```bash
   npm exec auth secret
   ```

2. **Style Radix components** with Tailwind:
   ```css
   /* styles/radix.css */
   .DialogOverlay {
     @apply fixed inset-0 bg-black/50;
   }
   
   .DialogContent {
     @apply fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2;
     @apply bg-white rounded-xl p-6 shadow-xl;
   }
   ```

3. **Initialize MSW** for development:
   ```bash
   npx msw init public/ --save
   ```

Remember: These are the packages developers are actually using in 2025, based on real NPM statistics!
