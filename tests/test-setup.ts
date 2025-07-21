import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';

// Extend Vitest matchers
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () =>
          `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true,
      };
    } else {
      return {
        message: () =>
          `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false,
      };
    }
  },
});

// Set test environment
globalThis.process = globalThis.process || { env: {} };
(globalThis.process.env as any).NODE_ENV = 'test';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
});

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Add custom test helpers
(globalThis as any).testHelpers = {
  waitFor: (ms: number) => new Promise(resolve => setTimeout(resolve, ms)),
  mockFetch: (data: any, options: { status?: number; ok?: boolean } = {}) => {
    const { status = 200, ok = true } = options;
    return vi.fn(() =>
      Promise.resolve({
        ok,
        status,
        json: () => Promise.resolve(data),
        text: () => Promise.resolve(JSON.stringify(data)),
      })
    );
  },
};

// Declare custom matchers
declare module 'vitest' {
  interface Assertion<T = any> {
    toBeWithinRange(floor: number, ceiling: number): T;
  }
  interface AsymmetricMatchersContaining {
    toBeWithinRange(floor: number, ceiling: number): any;
  }
}
