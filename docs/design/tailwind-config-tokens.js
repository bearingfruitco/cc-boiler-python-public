// tailwind-tokens.js
// FreshSlate Design System Tokens for Tailwind Config

export const freshSlateTokens = {
  // Typography - 4 sizes only
  fontSize: {
    'size-1': ['32px', { lineHeight: '1.25' }],      // Large headings
    'size-1-mobile': ['28px', { lineHeight: '1.25' }], // Mobile large headings
    'size-2': ['24px', { lineHeight: '1.375' }],     // Subheadings
    'size-2-mobile': ['20px', { lineHeight: '1.375' }], // Mobile subheadings
    'size-3': ['16px', { lineHeight: '1.5' }],       // Body text
    'size-4': ['12px', { lineHeight: '1.5' }],       // Small text
    'display': ['48px', { lineHeight: '1' }],        // Special income display
  },
  
  // Font weights - 2 only
  fontWeight: {
    regular: '400',
    semibold: '600',
    // Remove all other weights
  },
  
  // Spacing - 4px grid
  spacing: {
    '0': '0px',
    '1': '4px',
    '2': '8px',
    '3': '12px',
    '4': '16px',
    '5': '20px',
    '6': '24px',
    '7': '28px',
    '8': '32px',
    '9': '36px',
    '10': '40px',
    '11': '44px',  // Min touch target
    '12': '48px',  // Preferred touch target
    '14': '56px',
    '16': '64px',
    '18': '72px',
    '20': '80px',
    '24': '96px',
    '32': '128px',
  },
  
  // Border radius - 4px grid aligned
  borderRadius: {
    'none': '0px',
    'sm': '4px',
    'DEFAULT': '8px',
    'md': '8px',
    'lg': '12px',
    'xl': '16px',
    '2xl': '24px',
    'full': '9999px',
  },
  
  // Colors - Semantic palette
  colors: {
    // Income/Positive (Green)
    positive: {
      50: '#f0fdf4',
      100: '#dcfce7',
      200: '#bbf7d0',
      300: '#86efac',
      400: '#4ade80',
      500: '#22c55e',
      600: '#16a34a',
      700: '#15803d',
      800: '#166534',
      900: '#14532d',
    },
    
    // Debt/Negative (Red)
    negative: {
      50: '#fef2f2',
      100: '#fee2e2',
      200: '#fecaca',
      300: '#fca5a5',
      400: '#f87171',
      500: '#ef4444',
      600: '#dc2626',
      700: '#b91c1c',
      800: '#991b1b',
      900: '#7f1d1d',
    },
    
    // Primary action (Blue)
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93c5fd',
      400: '#60a5fa',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      800: '#1e40af',
      900: '#1e3a8a',
    },
  },
  
  // Animation durations
  transitionDuration: {
    '100': '100ms',  // Instant
    '200': '200ms',  // Fast
    '300': '300ms',  // Normal
    '500': '500ms',  // Slow
    '800': '800ms',  // Slower
  },
  
  // Animation timing functions
  transitionTimingFunction: {
    'out': 'cubic-bezier(0, 0, 0.2, 1)',
    'in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
    'bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    'elastic': 'cubic-bezier(0.68, -0.55, 0.265, 1.85)',
  },
  
  // Container max widths
  maxWidth: {
    'xs': '320px',   // Minimum phone
    'sm': '384px',   // Standard phone
    'md': '448px',   // Large phone
    'lg': '512px',   // Tablet
    'xl': '640px',   // Small desktop
  },
}

// Tailwind config extension
export const tailwindConfig = {
  theme: {
    extend: {
      ...freshSlateTokens,
      
      // Custom utilities
      height: {
        '11': '44px',  // Min touch target
        '14': '56px',
        '18': '72px',
      },
      
      // Custom animations
      keyframes: {
        fadeIn: {
          from: { opacity: '0', transform: 'translateY(10px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          from: { opacity: '0', transform: 'translateX(20px)' },
          to: { opacity: '1', transform: 'translateX(0)' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-10px)' },
          '75%': { transform: 'translateX(10px)' },
        },
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
      },
      
      animation: {
        fadeIn: 'fadeIn 0.3s ease-out',
        slideIn: 'slideIn 0.3s ease-out',
        shake: 'shake 0.4s ease-out',
        pulse: 'pulse 2s ease-in-out infinite',
      },
    },
  },
}

// Export for use in tailwind.config.js:
// import { tailwindConfig } from './tailwind-tokens.js'
// module.exports = tailwindConfig