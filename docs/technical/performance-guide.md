# Performance Optimization Guide

## Overview

Performance directly impacts user experience and conversion rates. This guide covers optimization strategies for Next.js applications targeting sub-2.5s page loads and perfect Core Web Vitals.

## Performance Targets

```yaml
Core Web Vitals:
  LCP: < 2.5s        # Largest Contentful Paint
  FID: < 100ms       # First Input Delay  
  CLS: < 0.1         # Cumulative Layout Shift
  INP: < 200ms       # Interaction to Next Paint

Additional Metrics:
  TTFB: < 600ms      # Time to First Byte
  FCP: < 1.8s        # First Contentful Paint
  TTI: < 3.8s        # Time to Interactive
  Bundle Size: < 300KB (gzipped)
```

## Next.js 15 Optimizations

### 1. App Router Optimizations

```typescript
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* Preconnect to critical third-party domains */}
        <link rel="preconnect" href="https://cdn.example.com" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://analytics.example.com" />
        
        {/* Preload critical assets */}
        <link 
          rel="preload" 
          href="/fonts/inter-var.woff2" 
          as="font" 
          type="font/woff2" 
          crossOrigin="anonymous" 
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### 2. Partial Prerendering (PPR)

```typescript
// app/page.tsx
export const experimental_ppr = true;

export default async function HomePage() {
  return (
    <>
      {/* Static shell - renders immediately */}
      <HeroSection />
      
      {/* Dynamic content - streams in */}
      <Suspense fallback={<ContentSkeleton />}>
        <DynamicContent />
      </Suspense>
    </>
  )
}
```

### 3. React Server Components

```typescript
// components/DataDisplay.tsx
// This runs on the server, no JS sent to client
async function DataDisplay() {
  const data = await fetchData(); // Direct DB query
  
  return (
    <div className="grid grid-cols-3 gap-4">
      {data.map(item => (
        <Card key={item.id} {...item} />
      ))}
    </div>
  );
}

// Mark client components explicitly
'use client';

// components/InteractiveWidget.tsx
export function InteractiveWidget({ data }) {
  // This ships JS to the client
  return <InteractiveChart data={data} />;
}
```

## Bundle Size Optimization

### 1. Code Splitting

```typescript
// Dynamic imports for heavy components
const HeavyComponent = dynamic(
  () => import('@/components/HeavyComponent'),
  { 
    loading: () => <div>Loading...</div>,
    ssr: false // Don't SSR if not needed
  }
);

// Route-based splitting happens automatically with App Router
// app/feature/page.tsx - only loads when /feature is visited
```

### 2. Tree Shaking

```typescript
// ❌ Bad - imports entire library
import _ from 'lodash';
const grouped = _.groupBy(data, 'category');

// ✅ Good - imports only what's needed
import groupBy from 'lodash/groupBy';
const grouped = groupBy(data, 'category');

// Even better - use native methods when possible
const grouped = data.reduce((acc, item) => {
  (acc[item.category] = acc[item.category] || []).push(item);
  return acc;
}, {});
```

### 3. Bundle Analysis

```json
// package.json
{
  "scripts": {
    "analyze": "ANALYZE=true next build",
    "analyze:server": "BUNDLE_ANALYZE=server next build",
    "analyze:browser": "BUNDLE_ANALYZE=browser next build"
  }
}
```

```typescript
// next.config.ts
import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer';

const config: NextConfig = {
  webpack: (config, { isServer }) => {
    if (process.env.ANALYZE) {
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'server',
          analyzerPort: isServer ? 8888 : 8889,
        })
      );
    }
    return config;
  },
};
```

## Image Optimization

### 1. Next.js Image Component

```typescript
// ❌ Bad
<img src="/hero.jpg" alt="Hero" />

// ✅ Good
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Description for accessibility"
  width={1200}
  height={600}
  priority // For above-the-fold images
  placeholder="blur"
  blurDataURL={heroBlurDataUrl}
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
/>
```

### 2. Image Formats & Sizing

```typescript
// lib/images.ts
export const imageLoader = ({ src, width, quality }) => {
  // Use image CDN for on-demand optimization
  return `https://cdn.example.com/image/upload/w_${width},q_${quality || 75},f_auto/${src}`;
};

// Responsive images
export const generateImageSizes = (maxWidth: number) => {
  const sizes = [640, 750, 828, 1080, 1200, 1920, 2048, 3840];
  return sizes.filter(s => s <= maxWidth * 2);
};
```

### 3. Lazy Loading

```typescript
// components/ImageGallery.tsx
'use client';

import { useIntersectionObserver } from '@/hooks/useIntersectionObserver';

export function ImageGallery({ images }) {
  const { ref, isIntersecting } = useIntersectionObserver({
    threshold: 0.1,
    rootMargin: '50px',
  });

  return (
    <div ref={ref}>
      {isIntersecting ? (
        images.map(img => (
          <Image key={img.id} {...img} loading="lazy" />
        ))
      ) : (
        <ImageGallerySkeleton />
      )}
    </div>
  );
}
```

## Font Optimization

### 1. Next.js Font Optimization

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
  preload: true,
  fallback: ['system-ui', 'arial'],
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

### 2. Font Subsetting

```css
/* Only load the characters you need */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC;
}
```

## CSS Optimization

### 1. Critical CSS

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <style dangerouslySetInnerHTML={{
          __html: `
            /* Critical CSS for above-the-fold content */
            body { margin: 0; font-family: system-ui; }
            .hero { min-height: 60vh; display: flex; align-items: center; }
            .btn-primary { background: #2563eb; color: white; padding: 12px 24px; }
          `
        }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 2. Tailwind Optimization

```typescript
// tailwind.config.ts
export default {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      // Only extend what you need
    },
  },
  plugins: [
    // Only essential plugins
  ],
};
```

## JavaScript Optimization

### 1. Reduce Main Thread Work

```typescript
// Use Web Workers for heavy computations
// lib/workers/heavy-computation.worker.ts
self.addEventListener('message', (event) => {
  const { data } = event.data;
  
  // Heavy calculation off main thread
  const result = performHeavyCalculation(data);
  
  self.postMessage({ result });
});

// Usage
const worker = new Worker('/workers/heavy-computation.worker.js');
worker.postMessage({ data });
worker.onmessage = (e) => setResult(e.data.result);
```

### 2. Debouncing & Throttling

```typescript
// hooks/useDebounce.ts
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage in search
const SearchInput = () => {
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 300);
  
  useEffect(() => {
    if (debouncedSearch) {
      performSearch(debouncedSearch);
    }
  }, [debouncedSearch]);
};
```

### 3. Lazy Load Heavy Libraries

```typescript
// Only load analytics after interaction
let analyticsLoaded = false;

const loadAnalytics = async () => {
  if (analyticsLoaded) return;
  
  const { initAnalytics } = await import('@/lib/analytics');
  initAnalytics();
  analyticsLoaded = true;
};

// Load on first interaction
document.addEventListener('click', loadAnalytics, { once: true });
document.addEventListener('scroll', loadAnalytics, { once: true });
```

## Caching Strategies

### 1. Static Generation

```typescript
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export default async function BlogPost({ params }) {
  const post = await getPost(params.slug);
  return <Article {...post} />;
}
```

### 2. Edge Caching

```typescript
// app/api/data/route.ts
export async function GET() {
  const data = await fetchData();
  
  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
      'CDN-Cache-Control': 'max-age=600',
    },
  });
}
```

### 3. Client-Side Caching

```typescript
// lib/api-client.ts
const cache = new Map();

export async function fetchWithCache(url: string, ttl = 300000) {
  const cached = cache.get(url);
  
  if (cached && Date.now() - cached.timestamp < ttl) {
    return cached.data;
  }
  
  const response = await fetch(url);
  const data = await response.json();
  
  cache.set(url, { data, timestamp: Date.now() });
  return data;
}
```

## Database Optimization

### 1. Query Optimization

```typescript
// ❌ Bad - N+1 query
const items = await db.select('*').from('items');
for (const item of items) {
  const category = await db
    .select('*')
    .from('categories')
    .where('id', item.category_id)
    .single();
}

// ✅ Good - Single query with join
const items = await db
  .select(`
    items.*,
    categories.name as category_name
  `)
  .from('items')
  .leftJoin('categories', 'items.category_id', 'categories.id');
```

### 2. Connection Pooling

```typescript
// lib/db.ts
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export default pool;
```

### 3. Indexed Fields

```sql
-- Ensure proper indexes
CREATE INDEX idx_items_created_at ON items(created_at DESC);
CREATE INDEX idx_items_status ON items(status) WHERE status != 'archived';
CREATE INDEX idx_items_user_id ON items(user_id);
```

## Third-Party Script Optimization

### 1. Script Loading Strategy

```typescript
// components/Analytics.tsx
import Script from 'next/script';

export function Analytics() {
  return (
    <>
      {/* Load critical scripts after hydration */}
      <Script
        id="analytics"
        strategy="afterInteractive"
        src="https://analytics.example.com/script.js"
      />
      
      {/* Load non-critical scripts when idle */}
      <Script
        id="chat-widget"
        strategy="lazyOnload"
        src="https://chat.example.com/widget.js"
      />
      
      {/* Load in web worker if possible */}
      <Script
        id="heavy-script"
        strategy="worker"
        src="/scripts/heavy-computation.js"
      />
    </>
  );
}
```

### 2. Facade Pattern

```typescript
// components/VideoEmbed.tsx
'use client';

import { useState } from 'react';

export function VideoEmbed({ videoId, title }) {
  const [loaded, setLoaded] = useState(false);
  
  if (!loaded) {
    return (
      <div 
        className="relative aspect-video cursor-pointer"
        onClick={() => setLoaded(true)}
      >
        <img 
          src={`https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`}
          alt={title}
          loading="lazy"
        />
        <PlayButton />
      </div>
    );
  }
  
  return (
    <iframe
      src={`https://www.youtube.com/embed/${videoId}?autoplay=1`}
      title={title}
      allow="autoplay"
      className="aspect-video w-full"
    />
  );
}
```

## Monitoring & Measurement

### 1. Real User Monitoring

```typescript
// lib/web-vitals.ts
import { onCLS, onFID, onLCP, onINP, onTTFB } from 'web-vitals';

export function reportWebVitals() {
  onCLS(sendToAnalytics);
  onFID(sendToAnalytics);
  onLCP(sendToAnalytics);
  onINP(sendToAnalytics);
  onTTFB(sendToAnalytics);
}

function sendToAnalytics(metric) {
  // Send to your analytics service
  window.analytics?.track('Web Vitals', {
    metric_name: metric.name,
    metric_value: metric.value,
    metric_rating: metric.rating,
    page_path: window.location.pathname,
  });
  
  // Log poor performance
  if (metric.rating === 'poor') {
    console.warn(`Poor ${metric.name}:`, metric.value);
  }
}
```

### 2. Performance Budget

```javascript
// performance-budget.json
{
  "resourceSizes": [
    {
      "resourceType": "script",
      "budget": 300
    },
    {
      "resourceType": "stylesheet",
      "budget": 100
    },
    {
      "resourceType": "image",
      "budget": 500
    },
    {
      "resourceType": "total",
      "budget": 1000
    }
  ],
  "timings": [
    {
      "metric": "first-contentful-paint",
      "budget": 1800
    },
    {
      "metric": "largest-contentful-paint",
      "budget": 2500
    }
  ]
}
```

## Performance Checklist

### Before Deploy
- [ ] Bundle size < 300KB gzipped
- [ ] All images optimized and lazy loaded
- [ ] Critical CSS inlined
- [ ] Third-party scripts deferred
- [ ] Database queries optimized
- [ ] Caching headers configured

### After Deploy
- [ ] Run Lighthouse audit
- [ ] Check Core Web Vitals
- [ ] Monitor error rates
- [ ] Verify CDN caching
- [ ] Test on 3G connection
- [ ] Check mobile performance

## Common Performance Issues

1. **Large Bundle Size**
   - Solution: Code split, tree shake, analyze bundle

2. **Slow Initial Load**
   - Solution: SSG/SSR, optimize critical path, preload resources

3. **Layout Shifts**
   - Solution: Set dimensions, use skeleton screens, font-display: swap

4. **Slow Interactions**
   - Solution: Debounce, virtualize lists, optimize re-renders

5. **Memory Leaks**
   - Solution: Clean up listeners, cancel requests, clear timers

Remember: Performance is a feature. Every millisecond counts in user experience.