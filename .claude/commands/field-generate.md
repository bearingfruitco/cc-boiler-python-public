# Field Generate - Generate Code from Field Registry

Generates Zod schemas, TypeScript types, test factories, and more from your field registry definitions.

## Usage

```bash
/field-generate [type] [options]
/fg [type]  # alias

# Types: schemas, factories, masking, all
# Options: --vertical=debt, --output=path
```

## Generation Types

### 1. Schemas - Zod Validation
```bash
/field-generate schemas
/fg schemas --vertical=debt
```

Generates from field registry:
```typescript
// generated/schemas/contact-form.ts
import { z } from 'zod';

export const contactFormSchema = z.object({
  // From field-registry/core/personal.json
  firstName: z.string()
    .min(2, 'First name must be at least 2 characters')
    .max(50, 'First name must be less than 50 characters'),
  
  lastName: z.string()
    .min(2, 'Last name must be at least 2 characters')
    .max(50, 'Last name must be less than 50 characters'),
  
  email: z.string()
    .email('Invalid email address')
    .toLowerCase(),
  
  phone: z.string()
    .regex(/^\d{10}$/, 'Phone must be 10 digits')
    .transform(val => val.replace(/\D/g, '')),
  
  // From field-registry/verticals/debt/contact.json
  debtAmount: z.number()
    .min(1000, 'Minimum debt amount is $1,000')
    .max(1000000, 'Maximum debt amount is $1,000,000'),
  
  creditorCount: z.number()
    .int()
    .min(1, 'Must have at least 1 creditor')
    .max(50, 'Maximum 50 creditors')
});

export type ContactFormData = z.infer<typeof contactFormSchema>;
```

### 2. Factories - Test Data Generation
```bash
/field-generate factories
```

Generates test data factories:
```typescript
// generated/factories/contact-form.factory.ts
import { faker } from '@faker-js/faker';
import type { ContactFormData } from '../schemas/contact-form';

export const contactFormFactory = {
  build: (overrides?: Partial<ContactFormData>): ContactFormData => ({
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    email: faker.internet.email().toLowerCase(),
    phone: faker.string.numeric(10),
    debtAmount: faker.number.int({ min: 1000, max: 100000 }),
    creditorCount: faker.number.int({ min: 1, max: 10 }),
    ...overrides
  }),
  
  buildMany: (count: number, overrides?: Partial<ContactFormData>): ContactFormData[] => {
    return Array.from({ length: count }, () => 
      contactFormFactory.build(overrides)
    );
  },
  
  // Special variants
  buildWithHighDebt: () => contactFormFactory.build({
    debtAmount: faker.number.int({ min: 50000, max: 100000 }),
    creditorCount: faker.number.int({ min: 5, max: 15 })
  }),
  
  buildWithPII: () => ({
    ...contactFormFactory.build(),
    ssn: faker.string.numeric(9), // Only in test env!
    dateOfBirth: faker.date.birthdate({ min: 18, max: 80 })
  })
};
```

### 3. Masking - Display Functions
```bash
/field-generate masking
```

Generates PII masking utilities:
```typescript
// generated/masking/field-masking.ts
export const fieldMasking = {
  email: (email: string): string => {
    const [name, domain] = email.split('@');
    return `${name.slice(0, 2)}****@${domain}`;
  },
  
  phone: (phone: string): string => {
    const cleaned = phone.replace(/\D/g, '');
    return `(***) ***-${cleaned.slice(-4)}`;
  },
  
  ssn: (ssn: string): string => {
    return `***-**-${ssn.slice(-4)}`;
  },
  
  name: (name: string): string => {
    return name.charAt(0) + '*'.repeat(name.length - 1);
  },
  
  // Currency formatting
  currency: (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  },
  
  // Conditional masking based on user role
  maskForRole: (value: string, field: string, userRole: string) => {
    if (userRole === 'admin') return value;
    if (field in fieldMasking) {
      return fieldMasking[field](value);
    }
    return value;
  }
};
```

### 4. All - Complete Generation
```bash
/field-generate all
```

Generates everything:
- Zod schemas
- TypeScript types  
- Test factories
- Masking functions
- Form field configs
- API request/response types
- Database seed functions

## Output Structure

```
lib/generated/
├── schemas/
│   ├── index.ts
│   ├── contact-form.ts
│   └── user-profile.ts
├── factories/
│   ├── index.ts
│   └── *.factory.ts
├── masking/
│   ├── index.ts
│   └── field-masking.ts
└── types/
    ├── fields.ts
    └── api.ts
```

## Integration Example

```typescript
// In your form component
import { contactFormSchema } from '@/lib/generated/schemas/contact-form';
import { fieldMasking } from '@/lib/generated/masking/field-masking';

// Validation
const form = useForm({
  resolver: zodResolver(contactFormSchema)
});

// Display
<div>{fieldMasking.email(user.email)}</div>

// Testing
import { contactFormFactory } from '@/lib/generated/factories/contact-form.factory';

test('form submission', () => {
  const testData = contactFormFactory.build();
  // ...
});
```

## Options

- `--vertical=debt` - Include vertical-specific fields
- `--output=lib/generated` - Custom output directory
- `--dry-run` - Preview without writing files

This ensures all field handling is consistent and type-safe across your application!