import { NextResponse } from 'next/server';
import { headers } from 'next/headers';
import { SecureFormHandler } from '@/lib/forms/secure-form-handler';
import { AuditLogger } from '@/lib/security/audit-logger';
import { PIIDetector } from '@/lib/security/pii-detector';

// Rate limiting (implement with Redis in production)
const submissionCache = new Map<string, number>();

export async function POST(request: Request) {
  try {
    // Get request metadata
    const headersList = await headers();
    const ipAddress = headersList.get('x-forwarded-for') || 
                     headersList.get('x-real-ip') || 
                     'unknown';
    const userAgent = headersList.get('user-agent') || '';
    const sessionId = headersList.get('x-session-id') || '';
    
    // Rate limiting check
    const rateLimitKey = `${ipAddress}:${new Date().toISOString().slice(0, 13)}`;
    const submissions = submissionCache.get(rateLimitKey) || 0;
    
    if (submissions >= 10) {
      await AuditLogger.logSecurityEvent({
        event: 'blocked_rate_limit',
        sessionId,
        ipAddress,
        userAgent,
        details: { submissions, limit: 10 }
      });
      
      return NextResponse.json(
        { error: 'Too many submissions. Please try again later.' },
        { status: 429 }
      );
    }
    
    // Parse request body
    const body = await request.json();
    const { formId, data } = body;
    
    // Validate form ID
    if (!formId || typeof formId !== 'string') {
      return NextResponse.json(
        { error: 'Invalid form submission' },
        { status: 400 }
      );
    }
    
    // Check for PII in places it shouldn't be
    const urlPiiCheck = PIIDetector.detectPII(request.url);
    if (urlPiiCheck.hasPII) {
      await AuditLogger.logSecurityEvent({
        event: 'blocked_pii_in_url',
        sessionId,
        ipAddress,
        userAgent,
        details: { 
          piiTypes: urlPiiCheck.types,
          formId 
        }
      });
      
      return NextResponse.json(
        { error: 'Invalid request parameters' },
        { status: 400 }
      );
    }
    
    // Process the form submission securely
    const submission = {
      formData: data,
      metadata: {
        formId,
        sessionId,
        ipAddress,
        userAgent,
      }
    };
    
    // Get encryption key from environment
    const encryptionKey = process.env.FORM_ENCRYPTION_KEY;
    if (!encryptionKey) {
      console.error('Missing FORM_ENCRYPTION_KEY environment variable');
      return NextResponse.json(
        { error: 'Server configuration error' },
        { status: 500 }
      );
    }
    
    // Process with full security
    const result = await SecureFormHandler.processFormSubmission(
      submission,
      encryptionKey
    );
    
    if (!result.success) {
      return NextResponse.json(
        { errors: result.errors },
        { status: 400 }
      );
    }
    
    // Update rate limit
    submissionCache.set(rateLimitKey, submissions + 1);
    
    // Clean old rate limit entries periodically
    if (Math.random() < 0.01) {
      const hourAgo = new Date();
      hourAgo.setHours(hourAgo.getHours() - 1);
      const cutoff = hourAgo.toISOString().slice(0, 13);
      
      for (const [key] of submissionCache.entries()) {
        if (key.split(':')[1] < cutoff) {
          submissionCache.delete(key);
        }
      }
    }
    
    // Return success with minimal information
    return NextResponse.json({
      success: true,
      message: 'Thank you for your submission.',
      // Never return the actual lead ID or any PII
      reference: `REF-${Date.now().toString(36).toUpperCase()}`,
    });
    
  } catch (error) {
    // Log error safely (no PII)
    console.error('Form submission error:', {
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString(),
    });
    
    // Generic error response
    return NextResponse.json(
      { error: 'An error occurred processing your submission.' },
      { status: 500 }
    );
  }
}

// Only allow POST
export async function GET() {
  return NextResponse.json(
    { error: 'Method not allowed' },
    { status: 405 }
  );
}
