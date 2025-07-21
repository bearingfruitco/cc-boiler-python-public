# State Management Guide with Zustand

## Overview

This guide covers state management patterns using Zustand for FreshSlate applications, focusing on lead generation flows, quiz state, and attribution tracking.

## Why Zustand?

- **Lightweight**: ~8KB bundle size
- **TypeScript First**: Excellent type inference
- **No Providers**: Cleaner component trees
- **Persistence**: Built-in localStorage/sessionStorage support
- **DevTools**: Redux DevTools compatibility

## Core Stores

### 1. Lead Store

```typescript
// stores/lead-store.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface LeadState {
  // Form data
  formData: {
    name?: string;
    email?: string;
    phone?: string;
    debtAmount?: number;
    debtTypes?: string[];
    state?: string;
    creditScore?: string;
    monthlyPayment?: number;
  };
  
  // Attribution data
  attribution: {
    utm_source?: string;
    utm_medium?: string;
    utm_campaign?: string;
    utm_term?: string;
    utm_content?: string;
    gclid?: string;
    fbclid?: string;
    ttclid?: string;
    landing_page?: string;
    referrer?: string;
    ip_address?: string;
    user_agent?: string;
  };
  
  // Interaction tracking
  interactions: {
    started_at: number;
    field_touches: Record<string, number>;
    abandoned_fields: string[];
    time_per_field: Record<string, number>;
    validation_errors: Record<string, string[]>;
  };
  
  // Actions
  updateField: (field: string, value: any) => void;
  setAttribution: (attribution: Partial<LeadState['attribution']>) => void;
  trackFieldInteraction: (field: string) => void;
  trackValidationError: (field: string, error: string) => void;
  reset: () => void;
  getCompletionPercentage: () => number;
}

export const useLeadStore = create<LeadState>()(
  persist(
    immer((set, get) => ({
      // Initial state
      formData: {},
      attribution: {},
      interactions: {
        started_at: Date.now(),
        field_touches: {},
        abandoned_fields: [],
        time_per_field: {},
        validation_errors: {},
      },
      
      // Actions
      updateField: (field, value) => set((state) => {
        state.formData[field] = value;
        
        // Track interaction
        if (!state.interactions.field_touches[field]) {
          state.interactions.field_touches[field] = 0;
        }
        state.interactions.field_touches[field]++;
        
        // Remove from abandoned if it was there
        state.interactions.abandoned_fields = 
          state.interactions.abandoned_fields.filter(f => f !== field);
      }),
      
      setAttribution: (attribution) => set((state) => {
        state.attribution = { ...state.attribution, ...attribution };
      }),
      
      trackFieldInteraction: (field) => set((state) => {
        const now = Date.now();
        if (!state.interactions.time_per_field[field]) {
          state.interactions.time_per_field[field] = 0;
        }
        state.interactions.time_per_field[field] = now;
      }),
      
      trackValidationError: (field, error) => set((state) => {
        if (!state.interactions.validation_errors[field]) {
          state.interactions.validation_errors[field] = [];
        }
        state.interactions.validation_errors[field].push(error);
      }),
      
      reset: () => set((state) => {
        state.formData = {};
        state.interactions = {
          started_at: Date.now(),
          field_touches: {},
          abandoned_fields: [],
          time_per_field: {},
          validation_errors: {},
        };
      }),
      
      getCompletionPercentage: () => {
        const state = get();
        const requiredFields = ['name', 'email', 'phone', 'debtAmount', 'state'];
        const completedFields = requiredFields.filter(
          field => state.formData[field] !== undefined
        );
        return (completedFields.length / requiredFields.length) * 100;
      },
    })),
    {
      name: 'lead-storage',
      storage: createJSONStorage(() => sessionStorage),
      partialize: (state) => ({
        formData: state.formData,
        attribution: state.attribution,
      }),
    }
  )
);
```

### 2. Quiz Store

```typescript
// stores/quiz-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { subscribeWithSelector } from 'zustand/middleware';

interface QuizState {
  // Quiz state
  currentStep: number;
  totalSteps: number;
  answers: Record<string, any>;
  
  // Progress tracking
  progress: {
    started_at: number;
    completed_at?: number;
    time_per_step: Record<number, number>;
    abandoned_step?: number;
  };
  
  // Calculated values
  debtAnalysis?: {
    total_debt: number;
    monthly_payment: number;
    debt_to_income: number;
    qualification_status: 'qualified' | 'not_qualified' | 'needs_review';
    recommended_solution: string;
  };
  
  // Actions
  setAnswer: (step: number, answer: any) => void;
  nextStep: () => void;
  previousStep: () => void;
  goToStep: (step: number) => void;
  calculateDebtAnalysis: () => void;
  completeQuiz: () => void;
  resetQuiz: () => void;
}

export const useQuizStore = create<QuizState>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        // Initial state
        currentStep: 1,
        totalSteps: 7,
        answers: {},
        progress: {
          started_at: Date.now(),
          time_per_step: {},
        },
        
        // Actions
        setAnswer: (step, answer) => set((state) => ({
          answers: { ...state.answers, [step]: answer },
          progress: {
            ...state.progress,
            time_per_step: {
              ...state.progress.time_per_step,
              [step]: Date.now() - state.progress.started_at,
            },
          },
        })),
        
        nextStep: () => set((state) => ({
          currentStep: Math.min(state.currentStep + 1, state.totalSteps),
        })),
        
        previousStep: () => set((state) => ({
          currentStep: Math.max(state.currentStep - 1, 1),
        })),
        
        goToStep: (step) => set({ currentStep: step }),
        
        calculateDebtAnalysis: () => {
          const state = get();
          const totalDebt = state.answers.debtAmount || 0;
          const monthlyIncome = state.answers.monthlyIncome || 0;
          const monthlyPayment = totalDebt * 0.025; // 2.5% minimum payment
          const debtToIncome = monthlyIncome > 0 ? (monthlyPayment / monthlyIncome) * 100 : 0;
          
          let qualificationStatus: QuizState['debtAnalysis']['qualification_status'] = 'needs_review';
          let recommendedSolution = 'Credit counseling';
          
          if (totalDebt >= 10000 && debtToIncome > 20) {
            qualificationStatus = 'qualified';
            recommendedSolution = 'Debt settlement program';
          } else if (totalDebt < 5000) {
            qualificationStatus = 'not_qualified';
            recommendedSolution = 'DIY debt payoff plan';
          }
          
          set({
            debtAnalysis: {
              total_debt: totalDebt,
              monthly_payment: monthlyPayment,
              debt_to_income: debtToIncome,
              qualification_status: qualificationStatus,
              recommended_solution: recommendedSolution,
            },
          });
        },
        
        completeQuiz: () => set((state) => ({
          progress: {
            ...state.progress,
            completed_at: Date.now(),
          },
        })),
        
        resetQuiz: () => set({
          currentStep: 1,
          answers: {},
          progress: {
            started_at: Date.now(),
            time_per_step: {},
          },
          debtAnalysis: undefined,
        }),
      }),
      {
        name: 'quiz-storage',
        partialize: (state) => ({
          currentStep: state.currentStep,
          answers: state.answers,
          progress: state.progress,
        }),
      }
    )
  )
);

// Middleware to track analytics on step changes
useQuizStore.subscribe(
  (state) => state.currentStep,
  (currentStep) => {
    // Track step view in analytics
    if (typeof window !== 'undefined' && window.analytics) {
      window.analytics.track('Quiz Step Viewed', {
        step: currentStep,
        timestamp: new Date().toISOString(),
      });
    }
  }
);
```

### 3. Analytics Store

```typescript
// stores/analytics-store.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface AnalyticsEvent {
  event: string;
  properties: Record<string, any>;
  timestamp: number;
}

interface AnalyticsState {
  // Session data
  sessionId: string;
  userId?: string;
  
  // Events queue
  events: AnalyticsEvent[];
  queuedEvents: AnalyticsEvent[];
  
  // Page tracking
  pageViews: Array<{
    path: string;
    timestamp: number;
    duration?: number;
  }>;
  
  // Actions
  track: (event: string, properties?: Record<string, any>) => void;
  identify: (userId: string, traits?: Record<string, any>) => void;
  page: (pageName?: string, properties?: Record<string, any>) => void;
  flush: () => Promise<void>;
  reset: () => void;
}

export const useAnalyticsStore = create<AnalyticsState>()(
  devtools(
    (set, get) => ({
      // Initial state
      sessionId: generateSessionId(),
      events: [],
      queuedEvents: [],
      pageViews: [],
      
      // Actions
      track: (event, properties = {}) => {
        const analyticsEvent: AnalyticsEvent = {
          event,
          properties: {
            ...properties,
            session_id: get().sessionId,
            timestamp: new Date().toISOString(),
          },
          timestamp: Date.now(),
        };
        
        set((state) => ({
          events: [...state.events, analyticsEvent],
          queuedEvents: [...state.queuedEvents, analyticsEvent],
        }));
        
        // Send to analytics
        if (window.analytics) {
          window.analytics.track(event, analyticsEvent.properties);
        }
      },
      
      identify: (userId, traits = {}) => {
        set({ userId });
        
        if (window.analytics) {
          window.analytics.identify(userId, traits);
        }
      },
      
      page: (pageName, properties = {}) => {
        const pageView = {
          path: window.location.pathname,
          timestamp: Date.now(),
        };
        
        set((state) => ({
          pageViews: [...state.pageViews, pageView],
        }));
        
        if (window.analytics) {
          window.analytics.page(pageName, properties);
        }
      },
      
      flush: async () => {
        const { queuedEvents } = get();
        
        if (queuedEvents.length === 0) return;
        
        try {
          // Send to your analytics endpoint
          await fetch('/api/analytics/batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ events: queuedEvents }),
          });
          
          // Clear queue on success
          set({ queuedEvents: [] });
        } catch (error) {
          console.error('Failed to flush analytics:', error);
        }
      },
      
      reset: () => set({
        sessionId: generateSessionId(),
        events: [],
        queuedEvents: [],
        pageViews: [],
        userId: undefined,
      }),
    }),
    {
      name: 'analytics-store',
    }
  )
);

function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
```

## Zustand + SWR Integration Patterns

### 1. Form with Real-time Validation

```typescript
// components/forms/LeadFormWithZustand.tsx
import { useEffect } from 'react';
import { useLeadStore } from '@/stores/lead-store';
import { useSWRMutation } from 'swr/mutation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { leadSchema } from '@/lib/validation/schemas';

async function createLead(url: string, { arg }: { arg: any }) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(arg),
  });
  
  if (!response.ok) throw new Error('Failed to create lead');
  return response.json();
}

export function LeadForm() {
  const { formData, attribution, updateField, getCompletionPercentage } = useLeadStore();
  const { trigger, isMutating } = useSWRMutation('/api/leads', createLead);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm({
    resolver: zodResolver(leadSchema),
    defaultValues: formData,
  });
  
  // Sync form changes to Zustand
  useEffect(() => {
    const subscription = watch((value, { name }) => {
      if (name) {
        updateField(name, value[name]);
      }
    });
    return () => subscription.unsubscribe();
  }, [watch, updateField]);
  
  const onSubmit = async (data) => {
    try {
      const result = await trigger({
        ...data,
        attribution,
        completion_percentage: getCompletionPercentage(),
      });
      
      // Handle success
      window.location.href = `/thank-you?id=${result.id}`;
    } catch (error) {
      // Handle error
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Progress indicator */}
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className="bg-blue-600 h-2 rounded-full transition-all"
          style={{ width: `${getCompletionPercentage()}%` }}
        />
      </div>
      
      {/* Form fields */}
      <div className="space-y-4">
        <input
          {...register('name')}
          placeholder="Full Name"
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl"
        />
        {errors.name && (
          <p className="text-size-4 text-red-600">{errors.name.message}</p>
        )}
        
        {/* More fields... */}
      </div>
      
      <button
        type="submit"
        disabled={isMutating}
        className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 bg-blue-600 text-white"
      >
        {isMutating ? 'Submitting...' : 'Get Your Free Consultation'}
      </button>
    </form>
  );
}
```

### 2. Quiz with State Persistence

```typescript
// components/quiz/QuizFlow.tsx
import { useQuizStore } from '@/stores/quiz-store';
import { useLeadStore } from '@/stores/lead-store';
import { motion, AnimatePresence } from 'framer-motion';

const quizSteps = [
  { id: 1, question: 'How much debt do you have?', field: 'debtAmount' },
  { id: 2, question: 'What types of debt?', field: 'debtTypes' },
  // ... more steps
];

export function QuizFlow() {
  const { 
    currentStep, 
    totalSteps, 
    answers, 
    setAnswer, 
    nextStep, 
    previousStep,
    calculateDebtAnalysis 
  } = useQuizStore();
  
  const { updateField } = useLeadStore();
  
  const handleAnswer = (value: any) => {
    const step = quizSteps[currentStep - 1];
    
    // Update quiz store
    setAnswer(currentStep, value);
    
    // Sync to lead store
    updateField(step.field, value);
    
    // Auto-advance for certain steps
    if (currentStep < totalSteps) {
      nextStep();
    } else {
      calculateDebtAnalysis();
    }
  };
  
  return (
    <div className="max-w-md mx-auto p-4">
      {/* Progress bar */}
      <div className="mb-8">
        <div className="flex justify-between text-size-4 text-gray-600 mb-2">
          <span>Step {currentStep} of {totalSteps}</span>
          <span>{Math.round((currentStep / totalSteps) * 100)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className="bg-blue-600 h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${(currentStep / totalSteps) * 100}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>
      
      {/* Question */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.3 }}
        >
          <QuizStep
            step={quizSteps[currentStep - 1]}
            value={answers[currentStep]}
            onAnswer={handleAnswer}
          />
        </motion.div>
      </AnimatePresence>
      
      {/* Navigation */}
      <div className="flex gap-4 mt-8">
        {currentStep > 1 && (
          <button
            onClick={previousStep}
            className="flex-1 h-12 px-4 rounded-xl border-2 border-gray-200"
          >
            Back
          </button>
        )}
      </div>
    </div>
  );
}
```

## Best Practices

### 1. Store Organization

```typescript
// stores/index.ts
// Export all stores from a central location
export { useLeadStore } from './lead-store';
export { useQuizStore } from './quiz-store';
export { useAnalyticsStore } from './analytics-store';
export { useAppStore } from './app-store';

// Create store hooks with selectors
export const useLeadFormData = () => useLeadStore((state) => state.formData);
export const useAttribution = () => useLeadStore((state) => state.attribution);
export const useQuizProgress = () => useQuizStore((state) => ({
  current: state.currentStep,
  total: state.totalSteps,
  percentage: (state.currentStep / state.totalSteps) * 100,
}));
```

### 2. TypeScript Integration

```typescript
// types/stores.ts
import { StateCreator } from 'zustand';

// Define slices for complex stores
export interface FormSlice {
  formData: Record<string, any>;
  updateField: (field: string, value: any) => void;
}

export interface AttributionSlice {
  attribution: Record<string, string>;
  setAttribution: (data: Record<string, string>) => void;
}

// Combine slices
export type LeadStore = FormSlice & AttributionSlice;

// Create typed store creator
export const createLeadStore: StateCreator<LeadStore> = (set) => ({
  // Implementation
});
```

### 3. Testing Stores

```typescript
// __tests__/stores/lead-store.test.ts
import { renderHook, act } from '@testing-library/react';
import { useLeadStore } from '@/stores/lead-store';

describe('Lead Store', () => {
  beforeEach(() => {
    useLeadStore.setState({
      formData: {},
      attribution: {},
    });
  });
  
  it('updates form fields', () => {
    const { result } = renderHook(() => useLeadStore());
    
    act(() => {
      result.current.updateField('email', 'test@example.com');
    });
    
    expect(result.current.formData.email).toBe('test@example.com');
  });
  
  it('tracks field interactions', () => {
    const { result } = renderHook(() => useLeadStore());
    
    act(() => {
      result.current.trackFieldInteraction('email');
    });
    
    expect(result.current.interactions.field_touches.email).toBeDefined();
  });
});
```

## Migration Guide

### From Context to Zustand

```typescript
// Before (Context)
const LeadContext = createContext();

export function LeadProvider({ children }) {
  const [formData, setFormData] = useState({});
  
  return (
    <LeadContext.Provider value={{ formData, setFormData }}>
      {children}
    </LeadContext.Provider>
  );
}

// After (Zustand)
// No provider needed! Just use the hook
export function MyComponent() {
  const { formData, updateField } = useLeadStore();
  // Use directly
}
```

### From SessionStorage to Zustand

```typescript
// Before
const saveToSession = (data) => {
  sessionStorage.setItem('lead_data', JSON.stringify(data));
};

const loadFromSession = () => {
  return JSON.parse(sessionStorage.getItem('lead_data') || '{}');
};

// After
// Automatic persistence with Zustand!
const { formData } = useLeadStore(); // Already persisted
```

## Performance Optimizations

### 1. Selective Subscriptions

```typescript
// Only re-render when specific fields change
const email = useLeadStore((state) => state.formData.email);
const phone = useLeadStore((state) => state.formData.phone);

// Or use shallow comparison
import { shallow } from 'zustand/shallow';

const { name, email } = useLeadStore(
  (state) => ({ name: state.formData.name, email: state.formData.email }),
  shallow
);
```

### 2. Computed Values

```typescript
// Add computed values to store
const useLeadStore = create((set, get) => ({
  // ... state
  
  // Computed getters
  get isComplete() {
    const { formData } = get();
    return !!(formData.name && formData.email && formData.phone);
  },
  
  get progress() {
    const { formData } = get();
    const fields = ['name', 'email', 'phone', 'debtAmount'];
    const completed = fields.filter(f => formData[f]);
    return (completed.length / fields.length) * 100;
  },
}));
```

### 3. Middleware Composition

```typescript
// Combine multiple middleware
const useLeadStore = create()(
  devtools(
    persist(
      immer((set) => ({
        // Your store implementation
      })),
      {
        name: 'lead-store',
      }
    ),
    {
      name: 'Lead Store',
    }
  )
);
```

## Common Patterns

### 1. Form Field Sync

```typescript
// Custom hook to sync form field with store
export function useFormField(fieldName: string) {
  const value = useLeadStore((state) => state.formData[fieldName]);
  const updateField = useLeadStore((state) => state.updateField);
  
  const setValue = useCallback(
    (newValue: any) => updateField(fieldName, newValue),
    [fieldName, updateField]
  );
  
  return [value, setValue] as const;
}

// Usage
const [email, setEmail] = useFormField('email');
```

### 2. Auto-save with Debounce

```typescript
// Hook for auto-saving form data
export function useAutoSave() {
  const formData = useLeadStore((state) => state.formData);
  const { trigger } = useSWRMutation('/api/leads/draft', updateDraft);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      if (Object.keys(formData).length > 0) {
        trigger(formData);
      }
    }, 2000); // 2 second debounce
    
    return () => clearTimeout(timer);
  }, [formData, trigger]);
}
```

### 3. Multi-step Form State

```typescript
// Complex multi-step form store
interface MultiStepFormStore {
  steps: Array<{
    id: string;
    title: string;
    fields: string[];
    validation: z.ZodSchema;
  }>;
  currentStepIndex: number;
  stepData: Record<string, any>;
  errors: Record<string, string[]>;
  
  // Navigation
  nextStep: () => boolean;
  previousStep: () => void;
  goToStep: (index: number) => void;
  
  // Validation
  validateCurrentStep: () => boolean;
  validateField: (field: string, value: any) => string[];
  
  // Data
  updateStepData: (data: Record<string, any>) => void;
  getStepProgress: () => number;
  isStepComplete: (stepIndex: number) => boolean;
}
```

## Troubleshooting

### Common Issues

1. **State not persisting**: Check storage permissions and middleware order
2. **Hydration mismatch**: Use `useEffect` for client-only state
3. **Performance issues**: Use selectors and shallow comparison
4. **TypeScript errors**: Ensure proper type definitions

### Debug Tools

```typescript
// Enable Redux DevTools
const useStore = create(
  devtools(
    (set) => ({
      // Your store
    }),
    {
      name: 'MyStore',
      trace: true,
    }
  )
);

// Log state changes
useStore.subscribe(
  (state) => console.log('State updated:', state)
);
```

## Resources

- [Zustand Documentation](https://docs.pmnd.rs/zustand/getting-started/introduction)
- [SWR Documentation](https://swr.vercel.app/)
- [Zustand Recipes](https://docs.pmnd.rs/zustand/recipes/recipes)
- [TypeScript Guide](https://docs.pmnd.rs/zustand/guides/typescript)