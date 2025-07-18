#!/bin/bash
# Setup script for TCPA compliance module

echo "🔐 TCPA Compliance Module Setup"
echo "=============================="
echo ""

# Check if TCPA config exists
if [ -f ".claude/tcpa.config.json" ]; then
    ENABLED=$(python3 -c "import json; print(json.load(open('.claude/tcpa.config.json'))['enabled'])" 2>/dev/null || echo "False")
    if [ "$ENABLED" = "True" ]; then
        echo "✅ TCPA module is already configured"
        echo "Run: /tcpa-setup status - to check current settings"
        exit 0
    fi
fi

# Ask if TCPA is needed
read -p "Do you need TCPA compliance for lead generation forms? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Skipping TCPA setup."
    exit 0
fi

echo ""
echo "TCPA compliance is critical for:"
echo "• Lead generation forms"
echo "• Marketing campaigns"
echo "• Call centers"
echo "• Any form collecting phone numbers for sales"
echo ""

# Provider selection
echo "Which TCPA providers will you use?"
echo "1) TrustedForm only"
echo "2) Jornaya (LeadiD) only"
echo "3) Both providers (recommended)"
echo ""
read -p "Select (1-3): " -n 1 -r PROVIDER
echo

# Enable TCPA in config
python3 -c "
import json
config_path = '.claude/tcpa.config.json'
with open(config_path, 'r') as f:
    config = json.load(f)
config['enabled'] = True
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print('✅ TCPA module enabled')
"

# Configure providers
case "$PROVIDER" in
    1)
        echo ""
        echo "Setting up TrustedForm..."
        read -p "TrustedForm Account ID: " TF_ACCOUNT
        read -s -p "TrustedForm API Key: " TF_KEY
        echo
        
        python3 -c "
import json
with open('.claude/tcpa.config.json', 'r') as f:
    config = json.load(f)
config['providers']['trustedform']['enabled'] = True
config['providers']['trustedform']['accountId'] = '$TF_ACCOUNT'
config['providers']['trustedform']['apiKey'] = '$TF_KEY'
with open('.claude/tcpa.config.json', 'w') as f:
    json.dump(config, f, indent=2)
"
        ;;
    2)
        echo ""
        echo "Setting up Jornaya..."
        read -p "Jornaya Account ID: " JY_ACCOUNT
        read -p "Jornaya Campaign ID: " JY_CAMPAIGN
        
        python3 -c "
import json
with open('.claude/tcpa.config.json', 'r') as f:
    config = json.load(f)
config['providers']['jornaya']['enabled'] = True
config['providers']['jornaya']['accountId'] = '$JY_ACCOUNT'
config['providers']['jornaya']['campaignId'] = '$JY_CAMPAIGN'
with open('.claude/tcpa.config.json', 'w') as f:
    json.dump(config, f, indent=2)
"
        ;;
    3)
        # Setup both
        $0 1
        $0 2
        ;;
esac

# Add to .env.example if not present
if ! grep -q "TRUSTEDFORM_API_KEY" .env.example 2>/dev/null; then
    cat >> .env.example << 'EOL'

# TCPA Compliance
TRUSTEDFORM_API_KEY=
TRUSTEDFORM_ACCOUNT_ID=
JORNAYA_ACCOUNT_ID=
JORNAYA_CAMPAIGN_ID=
JORNAYA_SITE_ID=
EOL
    echo "✅ Added TCPA variables to .env.example"
fi

# Create database migration
echo ""
echo "Creating database migration for TCPA tables..."
cat > lib/db/migrations/add-tcpa-tables.sql << 'EOL'
-- TCPA Certificates table
CREATE TABLE IF NOT EXISTS tcpa_certificates (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    lead_id TEXT NOT NULL,
    cert_url TEXT NOT NULL,
    cert_type TEXT NOT NULL CHECK (cert_type IN ('trustedform', 'jornaya')),
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    verification_data JSONB,
    ip_address TEXT,
    user_agent TEXT,
    page_url TEXT
);

-- TCPA Consents table
CREATE TABLE IF NOT EXISTS tcpa_consents (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    lead_id TEXT NOT NULL,
    consent_text TEXT NOT NULL,
    consented_at TIMESTAMP NOT NULL,
    ip_address TEXT NOT NULL,
    user_agent TEXT,
    page_url TEXT NOT NULL,
    certificate_id TEXT REFERENCES tcpa_certificates(id),
    session_id TEXT,
    form_id TEXT
);

-- TCPA Verifications table
CREATE TABLE IF NOT EXISTS tcpa_verifications (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    certificate_id TEXT NOT NULL,
    verified_at TIMESTAMP DEFAULT NOW() NOT NULL,
    valid BOOLEAN NOT NULL,
    provider TEXT NOT NULL CHECK (provider IN ('trustedform', 'jornaya')),
    response_data JSONB NOT NULL,
    error_message TEXT,
    api_version TEXT,
    response_time INTEGER
);

-- Indexes for performance
CREATE INDEX idx_tcpa_certificates_lead_id ON tcpa_certificates(lead_id);
CREATE INDEX idx_tcpa_certificates_expires_at ON tcpa_certificates(expires_at);
CREATE INDEX idx_tcpa_consents_lead_id ON tcpa_consents(lead_id);
CREATE INDEX idx_tcpa_verifications_certificate_id ON tcpa_verifications(certificate_id);
EOL

echo "✅ Migration created at: lib/db/migrations/add-tcpa-tables.sql"
echo ""
echo "🎉 TCPA Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Add API keys to .env.local"
echo "2. Run database migration: bun run db:push"
echo "3. Use TCPALeadForm component in your forms:"
echo ""
echo "   import { TCPALeadForm } from '@/components/forms/tcpa/tcpa-lead-form';"
echo "   <TCPALeadForm onSubmit={handleSubmit} />"
echo ""
echo "For more information, run: /tcpa-setup status"
