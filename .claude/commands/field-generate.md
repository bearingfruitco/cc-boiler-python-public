---
name: field-generate
aliases: [fg, gen-fields]
description: Generate code from field registry definitions
category: forms
---

Generate various code artifacts from field registry definitions.

## Arguments:
- $TYPE: types|schemas|factories|masking|all
- $OUTPUT: (optional) output directory

## Generation Types:

### Types (TypeScript interfaces)
```bash
/field-generate types
```
Generates:
- Field type definitions
- Validation interfaces
- Form data types

### Schemas (Zod/Yup validation)
```bash
/field-generate schemas
```
Generates:
- Validation schemas
- Field-level validators
- Form schemas

### Factories (Test data)
```bash
/field-generate factories
```
Generates:
- Test data factories
- Mock generators
- Fixture builders

### Masking (PII protection)
```bash
/field-generate masking
```
Generates:
- Field masking utilities
- PII detection functions
- Display formatters

## Field Registry Structure:
```yaml
# field-registry/contact.yaml
fields:
  email:
    type: string
    validation: email
    required: true
    pii: true
    mask: partial
    
  phone:
    type: string
    validation: phone
    required: false
    pii: true
    mask: last4
    
  name:
    type: string
    validation: minLength(2)
    required: true
    pii: false
```

## Generated Output Examples:

### Types
```typescript
// generated/field-types.ts
export interface ContactFields {
  email: string;
  phone?: string;
  name: string;
}
```

### Schemas
```typescript
// generated/field-schemas.ts
export const contactSchema = z.object({
  email: z.string().email(),
  phone: z.string().regex(/^\d{10}$/).optional(),
  name: z.string().min(2)
});
```

### Factories
```typescript
// generated/field-factories.ts
export const contactFactory = {
  email: () => faker.internet.email(),
  phone: () => faker.phone.number(),
  name: () => faker.person.fullName()
};
```

### Masking
```typescript
// generated/field-masking.ts
export const maskContact = {
  email: (val) => maskEmail(val), // j***@example.com
  phone: (val) => maskPhone(val), // ***-**-1234
  name: (val) => val // no masking
};
```

## Usage in Project:
1. Define fields in `field-registry/`
2. Run `/field-generate all`
3. Import generated code
4. Use in forms/validation

## Chain Integration:
Part of `field-sync` chain for updating all generated code at once.
