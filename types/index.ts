// types/index.ts - Global type definitions

// User types
export interface User {
  id: string;
  email: string;
  createdAt: Date;
  updatedAt: Date;
}

// Common response types
export interface ApiResponse<T = unknown> {
  data?: T;
  error?: string;
  success: boolean;
}

// Form types (for tracked forms)
export interface FormField {
  name: string;
  value: string | number | boolean;
  type: 'text' | 'email' | 'tel' | 'number' | 'select' | 'checkbox';
  required?: boolean;
  pii?: boolean;
  phi?: boolean;
}

// Add more types as needed
