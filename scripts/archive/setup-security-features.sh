#!/bin/bash
# setup-security-features.sh - Initialize security and field registry

echo "🔒 Setting up security features and field registry..."

# Create environment variables template
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local template..."
    cat > .env.local << EOL
# Security Keys (REQUIRED - Generate strong keys)
FORM_ENCRYPTION_KEY=
AUDIT_LOG_KEY=

# API Keys for tracking
NEXT_PUBLIC_GA_ID=
NEXT_PUBLIC_FB_PIXEL_ID=

# Database encryption
DATABASE_ENCRYPTION_KEY=

# Session configuration
SESSION_SECRET=
SESSION_DURATION=86400

# Rate limiting
RATE_LIMIT_WINDOW=3600
RATE_LIMIT_MAX_REQUESTS=100

# Compliance mode (standard, hipaa, gdpr)
COMPLIANCE_MODE=standard

# Data retention (days)
PII_RETENTION_DAYS=90
AUDIT_LOG_RETENTION_DAYS=2555
EOL
    echo "✅ Created .env.local - Please fill in the values"
else
    echo "⚠️  .env.local already exists - skipping"
fi

# Generate encryption keys if openssl is available
if command -v openssl &> /dev/null; then
    echo ""
    echo "🔑 Generating secure keys..."
    echo "FORM_ENCRYPTION_KEY: $(openssl rand -base64 32)"
    echo "AUDIT_LOG_KEY: $(openssl rand -base64 32)"
    echo "DATABASE_ENCRYPTION_KEY: $(openssl rand -base64 32)"
    echo "SESSION_SECRET: $(openssl rand -base64 32)"
    echo ""
    echo "Copy these keys to your .env.local file!"
fi

# Create types directory if it doesn't exist
mkdir -p types/generated

# Make Python hooks executable
echo "🔧 Making security hooks executable..."
chmod +x .claude/hooks/pre-tool-use/07-pii-protection.py

# Install additional dependencies
echo "📦 Installing security dependencies..."
npm install --save crypto-js jsonwebtoken rate-limiter-flexible

# Generate initial field types
echo "🏗️ Generating TypeScript types from field registry..."
cat > types/generated/field-types.ts << 'EOL'
// Auto-generated from field-registry
// Run /gft to regenerate

export interface TrackingFields {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_term?: string;
  utm_content?: string;
  gclid?: string;
  fbclid?: string;
  partner_id?: string;
  campaign_id?: string;
}

export interface FormFields {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  zip_code: string;
  consent_tcpa: boolean;
}

export const PII_FIELDS = [
  'first_name',
  'last_name',
  'email',
  'phone',
  'ssn',
  'date_of_birth',
  'ip_address',
] as const;

export const PREPOP_WHITELIST = [
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'gclid',
  'fbclid',
  'partner_id',
] as const;
EOL

echo ""
echo "✅ Security features setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Fill in the encryption keys in .env.local"
echo "2. Run: /gft to generate complete field types"
echo "3. Run: /ctf MyForm --vertical=debt to create secure forms"
echo "4. Run: /afs components/forms/MyForm.tsx to audit security"
echo ""
echo "🔒 Security rules enforced:"
echo "  • NO PII in console.log"
echo "  • NO PII in localStorage"
echo "  • NO PII in URLs"
echo "  • All PII encrypted at rest"
echo "  • All form submissions audit logged"
echo ""
echo "📚 See field-registry/README.md for documentation"
