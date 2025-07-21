# PRP: Payment Integration System

## Metadata
- **Created**: 2024-01-15
- **Author**: AI Development Team
- **Confidence**: 9/10
- **Complexity**: High
- **Type**: Full-Stack Integration

## Goal
Build a complete payment processing system integrating Stripe for credit card payments, supporting subscriptions, one-time payments, and refunds with full PCI compliance.

## Why
- **Business Value**: Enable monetization with 2% transaction fee revenue
- **Technical Need**: Current system lacks payment processing
- **Priority**: Critical - blocking launch

## What
Complete payment system with:
- Stripe integration for card processing
- Subscription management
- Payment history tracking
- Webhook handling for async events
- PCI-compliant card tokenization
- Admin dashboard for refunds

### Success Criteria
- [ ] Process test payment successfully
- [ ] Handle all Stripe webhook events
- [ ] 99.9% uptime for payment processing
- [ ] PCI DSS compliance verified
- [ ] < 3 second payment confirmation
- [ ] 100% test coverage for payment flows

## All Needed Context

### Documentation & References
```yaml
# Stripe Integration
- url: https://stripe.com/docs/api
  why: Official Stripe API documentation
  sections: ["charges", "customers", "subscriptions", "webhooks"]
  critical: Webhook signature verification

- url: https://stripe.com/docs/webhooks/signatures
  why: Webhook security implementation
  gotcha: Signatures expire after 5 minutes

# Existing Code
- file: src/api/billing.py
  why: Current billing structure to extend
  pattern: Decorator-based route registration

- file: src/models/user.py
  why: User model needs payment fields
  extend: Add stripe_customer_id, subscription_status

# Security Patterns
- docfile: PRPs/ai_docs/pci_compliance.md
  why: PCI compliance requirements
  critical: Never store raw card numbers

- file: src/utils/encryption.py
  why: Field-level encryption utilities
  pattern: Use for storing payment metadata
```

### Current Codebase Structure
```bash
src/
├── api/
│   ├── __init__.py
│   ├── auth.py          # Has JWT patterns to follow
│   └── billing.py       # Extend this
├── models/
│   ├── __init__.py
│   └── user.py          # Add payment fields
└── utils/
    ├── validators.py    # Add payment validators
    └── encryption.py    # Use for sensitive data
```

### Desired Structure After Implementation
```bash
src/
├── api/
│   ├── endpoints/
│   │   ├── payments.py      # [NEW] Payment endpoints
│   │   └── webhooks.py      # [NEW] Stripe webhooks
│   └── billing.py           # [UPDATED] With Stripe
├── models/
│   ├── payment.py           # [NEW] Payment models
│   ├── subscription.py      # [NEW] Subscription models
│   └── user.py              # [UPDATED] Payment fields
├── services/
│   ├── stripe_service.py    # [NEW] Stripe wrapper
│   └── payment_service.py   # [NEW] Payment logic
├── utils/
│   └── stripe_helpers.py    # [NEW] Stripe utilities
└── workers/
    └── payment_worker.py    # [NEW] Async payment tasks
```

### Known Gotchas & Critical Patterns
```python
# CRITICAL: Always use Stripe's libraries for PCI compliance
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# GOTCHA: Webhook signatures expire after 5 minutes
def verify_webhook_signature(payload: bytes, signature: str):
    try:
        stripe.Webhook.construct_event(
            payload, signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

# PATTERN: Idempotency for payment operations
@router.post("/charge")
async def create_charge(
    request: ChargeRequest,
    idempotency_key: str = Header(...)
):
    # Stripe automatically handles idempotency
    
# WARNING: Test mode vs Live mode
# Always check stripe.api_key before operations

# CRITICAL: Store minimal payment data
class PaymentRecord(BaseModel):
    # Good: Store Stripe IDs
    stripe_payment_intent_id: str
    stripe_customer_id: str
    
    # Bad: Never store these
    # card_number: str  # NEVER!
    # cvv: str         # NEVER!
```

## Implementation Blueprint

### Task Breakdown
```yaml
Task 1 - Payment Models:
  CREATE src/models/payment.py:
    - PaymentIntent model
    - PaymentMethod model  
    - RefundRequest model
    
  CREATE src/models/subscription.py:
    - Subscription model
    - SubscriptionPlan model
    - BillingHistory model
    
  UPDATE src/models/user.py:
    - Add stripe_customer_id
    - Add subscription_status
    - Add payment_method_id

Task 2 - Stripe Service Layer:
  CREATE src/services/stripe_service.py:
    - Customer management
    - Payment intent creation
    - Subscription handling
    - Webhook processing
    
  CREATE src/services/payment_service.py:
    - Payment orchestration
    - Business logic layer
    - Audit logging

Task 3 - API Endpoints:
  CREATE src/api/endpoints/payments.py:
    - POST /payments/create-intent
    - POST /payments/confirm
    - GET /payments/history
    - POST /payments/refund
    
  CREATE src/api/endpoints/webhooks.py:
    - POST /webhooks/stripe
    - Signature verification
    - Event processing

Task 4 - Webhook Handlers:
  CREATE src/workers/payment_worker.py:
    - payment_intent.succeeded
    - payment_intent.failed
    - subscription.created
    - subscription.updated
    - invoice.payment_failed

Task 5 - Frontend Integration:
  CREATE src/static/js/payment.js:
    - Stripe Elements setup
    - Card tokenization
    - 3D Secure handling
    
  CREATE templates/payment_form.html:
    - PCI-compliant form
    - Error handling
    - Loading states

Task 6 - Testing:
  CREATE tests/test_payment_flow.py:
    - End-to-end payment test
    - Webhook simulation
    - Error scenarios
    
  CREATE tests/test_stripe_service.py:
    - Mock Stripe API
    - Edge cases
    - Idempotency tests
```

### Implementation Patterns

```python
# Pattern 1: Stripe Service Wrapper
class StripeService:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self._customer_cache = {}
    
    async def create_customer(self, user: User) -> str:
        """Create or retrieve Stripe customer"""
        if user.stripe_customer_id:
            return user.stripe_customer_id
            
        customer = stripe.Customer.create(
            email=user.email,
            metadata={"user_id": str(user.id)}
        )
        
        # Update user record
        await user.update(stripe_customer_id=customer.id)
        return customer.id
    
    async def create_payment_intent(
        self,
        amount: int,  # in cents
        customer_id: str,
        metadata: dict = None
    ) -> PaymentIntent:
        """Create payment intent with retry logic"""
        @retry(stop=stop_after_attempt(3))
        async def _create():
            return stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                customer=customer_id,
                metadata=metadata or {},
                capture_method="automatic"
            )
        
        intent = await _create()
        
        # Store in database
        await PaymentRecord.create(
            stripe_payment_intent_id=intent.id,
            customer_id=customer_id,
            amount=amount,
            status="pending"
        )
        
        return intent

# Pattern 2: Webhook Handler
@router.post("/webhooks/stripe")
async def handle_stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None)
):
    """Process Stripe webhooks with verification"""
    payload = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    
    # Process events asynchronously
    await process_webhook_event.delay(event)
    
    return {"status": "success"}

# Pattern 3: Payment Processing with Audit
async def process_payment(
    user: User,
    amount: int,
    payment_method_id: str,
    description: str = None
) -> PaymentResult:
    """Process payment with full audit trail"""
    
    # Create audit entry
    audit = await PaymentAudit.create(
        user_id=user.id,
        amount=amount,
        action="payment_initiated",
        ip_address=request.client.host
    )
    
    try:
        # Create payment intent
        stripe_service = StripeService()
        customer_id = await stripe_service.create_customer(user)
        
        intent = await stripe_service.create_payment_intent(
            amount=amount,
            customer_id=customer_id,
            metadata={
                "user_id": str(user.id),
                "audit_id": str(audit.id),
                "description": description
            }
        )
        
        # Confirm payment
        confirmed = stripe.PaymentIntent.confirm(
            intent.id,
            payment_method=payment_method_id
        )
        
        # Update audit
        await audit.update(
            action="payment_confirmed",
            stripe_payment_intent_id=confirmed.id
        )
        
        return PaymentResult(
            success=True,
            payment_intent_id=confirmed.id,
            client_secret=confirmed.client_secret
        )
        
    except stripe.error.CardError as e:
        await audit.update(
            action="payment_failed",
            error=str(e)
        )
        raise PaymentError(e.user_message)
```

## Validation Loops

### Level 1: Syntax & Style
```bash
# Python style checks
ruff check src/ --fix
black src/
mypy src/ --strict

# Security scan for payment code
bandit -r src/services/stripe_service.py src/api/endpoints/payments.py
# Must have 0 high-severity issues
```

### Level 2: Unit Tests
```bash
# Test models
pytest tests/models/test_payment_models.py -v
pytest tests/models/test_subscription_models.py -v

# Test services
pytest tests/services/test_stripe_service.py -v
pytest tests/services/test_payment_service.py -v

# Coverage check
pytest tests/ --cov=src/services --cov=src/api/endpoints --cov-report=term-missing
# Required: >95% coverage for payment code
```

### Level 3: Integration Tests
```bash
# Test with Stripe test mode
export STRIPE_TEST_MODE=true
pytest tests/integration/test_payment_flow.py -v

# Test webhook handling
pytest tests/integration/test_webhook_processing.py -v

# Test error scenarios
pytest tests/integration/test_payment_errors.py -v

# Load test payment endpoints
locust -f tests/load/payment_load_test.py --headless \
  --users 100 --spawn-rate 10 --run-time 300s
```

### Level 4: Security & Compliance
```bash
# PCI compliance check
python scripts/pci_compliance_check.py
# All checks must pass

# Security headers test
python scripts/security_headers_test.py
# Must include: Strict-Transport-Security, X-Frame-Options

# Penetration testing
python scripts/payment_pentest.py
# No vulnerabilities allowed

# Webhook signature test
python scripts/test_webhook_signatures.py
# Must handle expired signatures correctly
```

## Deployment Checklist
- [ ] Stripe API keys in environment variables
- [ ] Webhook endpoint registered in Stripe dashboard
- [ ] Database migrations for payment tables
- [ ] Redis configured for idempotency keys
- [ ] SSL certificate valid (required for PCI)
- [ ] Rate limiting on payment endpoints
- [ ] Monitoring alerts for failed payments
- [ ] Backup payment processor configured
- [ ] PCI compliance scan passed
- [ ] Load testing completed

## Anti-Patterns to Avoid
- ❌ Don't store card numbers or CVV
- ❌ Don't log sensitive payment data
- ❌ Don't process payments synchronously
- ❌ Don't skip webhook signature verification
- ❌ Don't reuse idempotency keys
- ❌ Don't mix test and live Stripe keys
- ❌ Don't forget to handle 3D Secure
- ❌ Don't process webhooks synchronously

## Confidence Score: 9/10

### Scoring Rationale:
- Documentation completeness: 2/2 (Stripe docs comprehensive)
- Pattern examples: 2/2 (All critical patterns shown)
- Gotchas identified: 2/2 (Security and compliance covered)
- Test coverage: 2/2 (All levels defined)
- Automation readiness: 1/2 (Needs manual Stripe setup)

### Notes:
The one point deduction is because Stripe webhook endpoints must be manually configured in the Stripe dashboard, which cannot be fully automated. Everything else can be executed via the PRP runner.
