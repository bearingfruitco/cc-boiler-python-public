---
command: tcpa-setup
aliases: [tcpa, compliance-setup, tcpa-config]
description: Configure TCPA compliance for lead generation forms
category: compliance
---

# TCPA Compliance Setup

Configure TrustedForm and/or Jornaya for TCPA compliance in your lead generation forms.

## Usage

```bash
/tcpa-setup              # Interactive setup
/tcpa-setup trustedform  # Setup TrustedForm only
/tcpa-setup jornaya      # Setup Jornaya only
/tcpa-setup both         # Setup both providers
/tcpa-setup status       # Check current configuration
/tcpa-setup disable      # Disable TCPA features
```

## Implementation

```bash
#!/bin/bash

TCPA_CONFIG=".claude/tcpa.config.json"

case "$1" in
    "status")
        if [ -f "$TCPA_CONFIG" ]; then
            echo "📊 TCPA Configuration Status"
            echo "============================"
            
            # Check if enabled
            ENABLED=$(python3 -c "import json; print(json.load(open('$TCPA_CONFIG'))['enabled'])")
            echo "TCPA Module: $([ "$ENABLED" = "True" ] && echo "✅ Enabled" || echo "❌ Disabled")"
            
            # Check providers
            TF_ENABLED=$(python3 -c "import json; print(json.load(open('$TCPA_CONFIG'))['providers']['trustedform']['enabled'])")
            JY_ENABLED=$(python3 -c "import json; print(json.load(open('$TCPA_CONFIG'))['providers']['jornaya']['enabled'])")
            
            echo ""
            echo "Providers:"
            echo "  TrustedForm: $([ "$TF_ENABLED" = "True" ] && echo "✅ Enabled" || echo "❌ Disabled")"
            echo "  Jornaya:     $([ "$JY_ENABLED" = "True" ] && echo "✅ Enabled" || echo "❌ Disabled")"
            
            # Check API keys
            TF_KEY=$(python3 -c "import json; print(json.load(open('$TCPA_CONFIG'))['providers']['trustedform']['apiKey'])")
            JY_ID=$(python3 -c "import json; print(json.load(open('$TCPA_CONFIG'))['providers']['jornaya']['accountId'])")
            
            echo ""
            echo "Configuration:"
            echo "  TrustedForm API Key: $([ -n "$TF_KEY" ] && echo "✅ Set" || echo "❌ Missing")"
            echo "  Jornaya Account ID:  $([ -n "$JY_ID" ] && echo "✅ Set" || echo "❌ Missing")"
        else
            echo "❌ TCPA not configured. Run: /tcpa-setup"
        fi
        ;;
        
    "disable")
        if [ -f "$TCPA_CONFIG" ]; then
            # Disable TCPA
            python3 -c "
import json
with open('$TCPA_CONFIG', 'r') as f:
    config = json.load(f)
config['enabled'] = False
with open('$TCPA_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
"
            echo "❌ TCPA compliance disabled"
        else
            echo "TCPA already disabled"
        fi
        ;;
        
    "trustedform"|"jornaya"|"both")
        # Enable TCPA if not already
        if [ ! -f "$TCPA_CONFIG" ]; then
            echo "Creating TCPA configuration..."
            # Config would be created by the hook
        fi
        
        # Enable main module
        python3 -c "
import json
with open('$TCPA_CONFIG', 'r') as f:
    config = json.load(f)
config['enabled'] = True
with open('$TCPA_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
"
        
        # Configure providers
        case "$1" in
            "trustedform")
                echo "🔐 Setting up TrustedForm..."
                read -p "TrustedForm Account ID: " TF_ACCOUNT
                read -p "TrustedForm API Key: " TF_KEY
                
                python3 -c "
import json
with open('$TCPA_CONFIG', 'r') as f:
    config = json.load(f)
config['providers']['trustedform']['enabled'] = True
config['providers']['trustedform']['accountId'] = '$TF_ACCOUNT'
config['providers']['trustedform']['apiKey'] = '$TF_KEY'
with open('$TCPA_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
"
                echo "✅ TrustedForm configured"
                ;;
                
            "jornaya")
                echo "🔐 Setting up Jornaya..."
                read -p "Jornaya Account ID: " JY_ACCOUNT
                read -p "Jornaya Campaign ID: " JY_CAMPAIGN
                read -p "Jornaya Site ID: " JY_SITE
                
                python3 -c "
import json
with open('$TCPA_CONFIG', 'r') as f:
    config = json.load(f)
config['providers']['jornaya']['enabled'] = True
config['providers']['jornaya']['accountId'] = '$JY_ACCOUNT'
config['providers']['jornaya']['campaignId'] = '$JY_CAMPAIGN'
config['providers']['jornaya']['siteId'] = '$JY_SITE'
with open('$TCPA_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
"
                echo "✅ Jornaya configured"
                ;;
                
            "both")
                # Run both setups
                $0 trustedform
                $0 jornaya
                ;;
        esac
        
        # Update .env.example
        if ! grep -q "TRUSTEDFORM_API_KEY" .env.example 2>/dev/null; then
            cat >> .env.example << 'EOF'

# TCPA Compliance
TRUSTEDFORM_API_KEY=
TRUSTEDFORM_ACCOUNT_ID=
JORNAYA_ACCOUNT_ID=
JORNAYA_CAMPAIGN_ID=
JORNAYA_SITE_ID=
EOF
        fi
        
        # Generate example form
        echo ""
        echo "✅ TCPA setup complete!"
        echo ""
        echo "Next steps:"
        echo "1. Add API keys to .env.local"
        echo "2. Run database migration: bun run db:push"
        echo "3. Use TCPALeadForm component for compliant forms"
        echo ""
        echo "Example usage:"
        echo "  import { TCPALeadForm } from '@/components/forms/tcpa/tcpa-lead-form';"
        echo "  <TCPALeadForm onSubmit={handleSubmit} />"
        ;;
        
    *)
        # Interactive setup
        echo "🔐 TCPA Compliance Setup"
        echo "======================="
        echo ""
        echo "This will configure TCPA compliance for lead generation."
        echo ""
        
        read -p "Do you need TCPA compliance? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            $0 disable
            exit 0
        fi
        
        echo ""
        echo "Which providers do you need?"
        echo "1) TrustedForm only"
        echo "2) Jornaya only"
        echo "3) Both providers"
        echo ""
        read -p "Select (1-3): " -n 1 -r PROVIDER_CHOICE
        echo
        
        case "$PROVIDER_CHOICE" in
            1) $0 trustedform ;;
            2) $0 jornaya ;;
            3) $0 both ;;
            *) echo "Invalid choice"; exit 1 ;;
        esac
        ;;
esac
```

## Features

### Provider Configuration
- Interactive setup wizard
- Secure API key storage
- Environment variable management
- Automatic form field injection

### Compliance Features
- Certificate retention (90 days default)
- Consent tracking
- IP/timestamp recording
- Audit trail generation

### Development Tools
- Status checking
- Test certificate generation
- Compliance validation
- Debug mode

## Example Form

After setup, create TCPA-compliant forms:

```tsx
// Using the TCPA-enhanced form
import { TCPALeadForm } from '@/components/forms/tcpa/tcpa-lead-form';

export function ContactPage() {
  const handleSubmit = async (data) => {
    // Data includes TCPA certificates automatically
    console.log('Form data:', data);
    // data.trustedform_cert
    // data.jornaya_leadid
    // data.consent_tcpa
  };
  
  return (
    <TCPALeadForm 
      onSubmit={handleSubmit}
      className="max-w-md mx-auto"
    />
  );
}
```

## Database Migration

After setup, run migration to create TCPA tables:

```bash
# Generate migration
bun run db:generate

# Apply migration
bun run db:push
```

## Testing

Test your TCPA integration:

```bash
# Check if scripts load
/tcpa-test scripts

# Validate certificate generation
/tcpa-test certificate

# Test form submission
/tcpa-test submit
```

## Best Practices

1. **Always test in development first**
2. **Verify certificates are being generated**
3. **Check retention policies**
4. **Monitor API usage/costs**
5. **Keep consent language updated**

## Troubleshooting

### Certificates not generating?
- Check if scripts are loading
- Verify account IDs are correct
- Check browser console for errors

### Forms not submitting?
- Ensure consent checkbox is checked
- Verify API keys are set
- Check server logs

## Related Commands

- `/create-form` - Create forms with TCPA
- `/audit-form-security` - Check compliance
- `/facts` - Protected compliance values

## Resources

- [TrustedForm Docs](https://activeprospect.com/trustedform)
- [Jornaya Docs](https://docs.jornaya.com)
- [TCPA Guidelines](https://www.fcc.gov/tcpa)
