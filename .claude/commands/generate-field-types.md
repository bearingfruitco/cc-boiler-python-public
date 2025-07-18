Generate TypeScript types from field registry for: $ARGUMENTS

Parse arguments:
- Vertical name (optional, defaults to all)
- Output location (--output=path)

Steps:

1. Load field definitions:
   - Core fields from field-registry/core/
   - Vertical fields if specified
   - Merge all definitions

2. Generate TypeScript interfaces:

```typescript
// Generated from field-registry
// DO NOT EDIT - Generated on [date]

// Tracking Fields
export interface TrackingFields {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_term?: string;
  utm_content?: string;
  gclid?: string;
  fbclid?: string;
  ttclid?: string;
  partner_id?: string;
  campaign_id?: string;
}

// Device Information
export interface DeviceFields {
  browser_name?: string;
  browser_version?: string;
  os_name?: string;
  os_version?: string;
  device_type?: 'desktop' | 'mobile' | 'tablet';
  screen_width?: number;
  screen_height?: number;
}

// Geographic Data
export interface GeographicFields {
  ip_country?: string;
  ip_region?: string;
  ip_city?: string;
  ip_timezone?: string;
}

// Form Fields (vertical-specific)
export interface FormFields {
  // Required fields
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  zip_code: string;
  
  // Optional fields
  enrolled_debt_amount?: number;
  employment_status?: 'employed' | 'self_employed' | 'unemployed' | 'retired';
  consent_tcpa: boolean;
}

// Complete submission type
export interface LeadSubmission extends TrackingFields, FormFields {
  id: string;
  journey_id: string;
  session_id: string;
  created_at: string;
  updated_at: string;
  
  // Related data
  dim_device?: DeviceFields;
  dim_cookie?: CookieFields;
  dim_geoip?: GeographicFields;
}

// Field metadata for runtime validation
export const FIELD_METADATA = {
  email: {
    type: 'string',
    pii: true,
    encryption: 'field',
    validation: {
      required: true,
      pattern: 'email'
    }
  },
  // ... more field metadata
} as const;

// Validation schemas
export const fieldValidation = {
  email: z.string().email(),
  phone: z.string().regex(/^\d{10}$/),
  zip_code: z.string().regex(/^\d{5}(-\d{4})?$/),
  enrolled_debt_amount: z.number().min(5000).max(1000000),
  // ... more validations
};

// PII field list for security checks
export const PII_FIELDS = [
  'first_name',
  'last_name',
  'email',
  'phone',
  'ssn',
  'date_of_birth',
  'ip_address',
  'enrolled_debt_amount',
] as const;

// Prepopulation whitelist
export const PREPOP_WHITELIST = [
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'gclid',
  'fbclid',
  'partner_id',
] as const;
```

3. Generate Zod schemas:

```typescript
import { z } from 'zod';

// Auto-generated Zod schemas
export const trackingSchema = z.object({
  utm_source: z.string().optional(),
  utm_medium: z.string().optional(),
  // ...
});

export const formSchema = z.object({
  first_name: z.string().min(2).max(50),
  last_name: z.string().min(2).max(50),
  email: z.string().email(),
  phone: z.string().regex(/^\d{10}$/),
  // ...
});

export const completeSubmissionSchema = trackingSchema
  .merge(formSchema)
  .extend({
    consent_tcpa: z.boolean().refine(val => val === true, {
      message: 'Consent is required'
    })
  });
```

4. Generate utility functions:

```typescript
// Field utilities
export const fieldUtils = {
  isPII(fieldName: string): boolean {
    return PII_FIELDS.includes(fieldName as any);
  },
  
  requiresEncryption(fieldName: string): boolean {
    return FIELD_METADATA[fieldName]?.encryption === 'field';
  },
  
  canPrepopulate(fieldName: string): boolean {
    return PREPOP_WHITELIST.includes(fieldName as any);
  },
  
  getMaskPattern(fieldName: string): string | null {
    const patterns = {
      phone: '(XXX) XXX-##XX',
      ssn: 'XXX-XX-####',
      email: 'u***@domain.com',
    };
    return patterns[fieldName] || null;
  }
};
```

5. Save generated files:
   - types/generated/field-types.ts
   - types/generated/field-schemas.ts
   - types/generated/field-utils.ts

6. Update tsconfig paths:
   ```json
   {
     "paths": {
       "@/field-types": ["./types/generated/field-types"],
       "@/field-schemas": ["./types/generated/field-schemas"]
     }
   }
   ```

Note: Re-run this command when field registry is updated
