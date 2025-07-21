# Boilerplate Template Files

## Directory Structure
```
templates/
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   └── index.ts
│   └── layout/
│       ├── Header.tsx
│       ├── Footer.tsx
│       └── Container.tsx
├── hooks/
│   ├── useAnalytics.ts
│   ├── useTracking.ts
│   └── index.ts
├── lib/
│   ├── analytics.ts
│   ├── api-client.ts
│   ├── auth.ts
│   ├── validation.ts
│   └── utils.ts
└── app/
    ├── layout.tsx
    ├── page.tsx
    └── global.css
```

## Template Files

### components/ui/Button.tsx
```typescript
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}

export function Button({ 
  children, 
  variant = 'primary', 
  size = 'md',
  disabled,
  onClick,
  className = ''
}: ButtonProps) {
  const baseClasses = 'rounded-xl font-semibold transition-all flex items-center justify-center gap-2';
  
  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 disabled:bg-gray-200 disabled:text-gray-400',
    secondary: 'bg-gray-800 text-white hover:bg-gray-900 disabled:bg-gray-200 disabled:text-gray-400',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 disabled:text-gray-400'
  };
  
  const sizeClasses = {
    sm: 'h-8 px-3 text-size-4',
    md: 'h-10 px-4 text-size-3',
    lg: 'h-12 px-6 text-size-3'
  };
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
    >
      {children}
    </button>
  );
}
```

### components/ui/Card.tsx
```typescript
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`bg-white border border-gray-200 rounded-xl p-4 space-y-3 ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '' }: CardProps) {
  return (
    <div className={`space-y-1 ${className}`}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className = '' }: CardProps) {
  return (
    <h3 className={`text-size-2 font-semibold text-gray-900 ${className}`}>
      {children}
    </h3>
  );
}

export function CardContent({ children, className = '' }: CardProps) {
  return (
    <div className={`text-size-3 font-regular text-gray-600 ${className}`}>
      {children}
    </div>
  );
}
```

### lib/analytics.ts
```typescript
// Generic analytics setup
interface AnalyticsConfig {
  debug?: boolean;
  provider?: 'rudderstack' | 'segment' | 'custom';
}

class Analytics {
  private initialized = false;
  
  init(config: AnalyticsConfig) {
    if (this.initialized) return;
    
    // Initialize your analytics provider
    if (typeof window !== 'undefined') {
      // Client-side initialization
      console.log('Analytics initialized', config);
    }
    
    this.initialized = true;
  }
  
  track(event: string, properties?: Record<string, any>) {
    if (!this.initialized) {
      console.warn('Analytics not initialized');
      return;
    }
    
    // Send to your analytics provider
    console.log('Track:', event, properties);
  }
  
  page(properties?: Record<string, any>) {
    this.track('Page Viewed', {
      page_path: window.location.pathname,
      page_title: document.title,
      ...properties
    });
  }
}

export const analytics = new Analytics();
```

### lib/validation.ts
```typescript
import { z } from 'zod';

// Common validation schemas
export const emailSchema = z.string().email('Invalid email address');

export const phoneSchema = z.string().regex(
  /^\+?[1-9]\d{1,14}$/,
  'Invalid phone number'
);

export const requiredString = z.string().min(1, 'This field is required');

// Form schemas
export const contactFormSchema = z.object({
  name: requiredString,
  email: emailSchema,
  message: requiredString.min(10, 'Message must be at least 10 characters'),
});

// Utility functions
export function validateEmail(email: string): boolean {
  return emailSchema.safeParse(email).success;
}

export function validatePhone(phone: string): boolean {
  return phoneSchema.safeParse(phone).success;
}
```

### hooks/useTracking.ts
```typescript
import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';

export interface TrackingParams {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  [key: string]: string | undefined;
}

export function useTracking() {
  const searchParams = useSearchParams();
  const [params, setParams] = useState<TrackingParams>({});
  
  useEffect(() => {
    const trackingParams: TrackingParams = {};
    
    // Capture URL parameters
    searchParams.forEach((value, key) => {
      trackingParams[key] = value;
    });
    
    // Store in session
    if (Object.keys(trackingParams).length > 0) {
      sessionStorage.setItem('tracking_params', JSON.stringify(trackingParams));
      setParams(trackingParams);
    } else {
      // Retrieve from session
      const stored = sessionStorage.getItem('tracking_params');
      if (stored) {
        setParams(JSON.parse(stored));
      }
    }
  }, [searchParams]);
  
  return { params };
}
```

### app/layout.tsx
```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'Your App Name',
  description: 'Your app description',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
```

### app/globals.css
```css
@import "tailwindcss";

@theme {
  /* Custom theme tokens */
  --font-sans: var(--font-inter), system-ui, sans-serif;
  
  /* Override Tailwind defaults to match design system */
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;
  
  /* Ensure our spacing system */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-6: 24px;
  --spacing-8: 32px;
  --spacing-12: 48px;
}

/* Custom utilities */
.text-size-1 {
  font-size: 32px;
  line-height: 1.25;
}

.text-size-2 {
  font-size: 24px;
  line-height: 1.375;
}

.text-size-3 {
  font-size: 16px;
  line-height: 1.5;
}

.text-size-4 {
  font-size: 12px;
  line-height: 1.5;
}

@media (max-width: 640px) {
  .text-size-1 {
    font-size: 28px;
  }
  
  .text-size-2 {
    font-size: 20px;
  }
}
```