/**
 * Test file to verify all async/event imports work correctly
 */

import { eventQueue, LEAD_EVENTS, emitAsync, emitCritical } from '@/lib/events';
import { useLeadFormEvents, useEventEmitter, useEventListener } from '@/hooks/use-event-system';
import { LoadingState, ErrorState, EmptyState } from '@/components/ui/async-states';
import { parallelSettle, retryWithBackoff, withTimeout } from '@/lib/utils/async-helpers';
import { waitForEvent, expectEventSequence } from '@/lib/testing/async-test-utils';
import { initializeApp, trackFormConversion } from '@/lib/analytics';

// Test that types are working
const testEventEmission = () => {
  eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
    formId: 'test-form',
    sessionId: 'test-session',
    timestamp: new Date().toISOString(),
    source: 'test',
    data: {}
  });
};

// Test parallel operations
const testParallelOps = async () => {
  const results = await parallelSettle({
    user: fetch('/api/user'),
    prefs: fetch('/api/preferences'),
    perms: fetch('/api/permissions')
  }, {
    timeout: 5000,
    critical: ['user']
  });
  
  return results;
};

// Test form tracking
const TestFormComponent = () => {
  const { trackFormSubmit, trackSubmissionResult } = useLeadFormEvents('test-form');
  
  const handleSubmit = async (data: any) => {
    const startTime = await trackFormSubmit(data);
    // ... submit logic
    trackSubmissionResult(true, startTime);
  };
  
  return null;
};

console.log('All imports verified successfully!');
