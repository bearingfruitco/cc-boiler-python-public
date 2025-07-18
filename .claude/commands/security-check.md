# Security Check

Scan for security vulnerabilities and compliance issues.

## Arguments:
- $TARGET: deps|code|secrets|all
- $FIX: auto|manual|report

## Why This Command:
- Catch vulnerabilities early
- Prevent secret exposure
- Ensure secure coding
- Maintain compliance

## Steps:

### Target: DEPS
Check dependency vulnerabilities:

```bash
echo "## 🔒 Security Scan - Dependencies"
echo ""

# npm audit
echo "### NPM Audit"
npm audit --json > .claude/security/npm-audit.json
VULNS=$(cat .claude/security/npm-audit.json | jq '.metadata.vulnerabilities')

echo "Found vulnerabilities:"
echo "- Critical: $(echo $VULNS | jq '.critical')"
echo "- High: $(echo $VULNS | jq '.high')"
echo "- Moderate: $(echo $VULNS | jq '.moderate')"
echo "- Low: $(echo $VULNS | jq '.low')"

# Auto-fix if requested
if [ "$FIX" = "auto" ]; then
  echo -e "\n### Auto-fixing..."
  npm audit fix
  
  # Check if any remain
  npm audit --json > .claude/security/npm-audit-after.json
  REMAINING=$(cat .claude/security/npm-audit-after.json | \
    jq '.metadata.vulnerabilities.critical + .metadata.vulnerabilities.high')
  
  if [ $REMAINING -gt 0 ]; then
    echo "⚠️ $REMAINING critical/high vulnerabilities require manual review"
    npm audit
  fi
fi

# Check for outdated packages
echo -e "\n### Outdated Packages"
npx npm-check-updates -u --dep prod
```

### Target: SECRETS
Scan for exposed secrets:

```bash
echo "## 🔑 Secret Scanning"

# Common patterns
PATTERNS=(
  "sk_live_"
  "pk_live_"
  "ghp_"
  "ghs_"
  "mongodb+srv://"
  "postgres://"
  "mysql://"
  "redis://"
  "PRIVATE KEY"
  "BEGIN RSA"
  "AWS_SECRET"
  "SUPABASE_SERVICE_ROLE"
)

# Scan files
for pattern in "${PATTERNS[@]}"; do
  FOUND=$(grep -r "$pattern" --exclude-dir=node_modules \
    --exclude-dir=.next --exclude="*.log" . 2>/dev/null | wc -l)
  
  if [ $FOUND -gt 0 ]; then
    echo "❌ Found exposed secret pattern: $pattern"
    grep -r "$pattern" --exclude-dir=node_modules . | head -3
  fi
done

# Check .env files
echo -e "\n### Environment Files"
for env_file in .env*; do
  if [ -f "$env_file" ]; then
    # Check if in .gitignore
    if ! grep -q "^$env_file" .gitignore; then
      echo "❌ $env_file not in .gitignore!"
    else
      echo "✅ $env_file properly ignored"
    fi
  fi
done

# Scan git history
echo -e "\n### Git History"
git log -p -S"sk_live_\|pk_live_\|password" --all | grep -E "^[\+\-].*sk_live_|^[\+\-].*password" | head -5
```

### Target: CODE
Security code analysis:

```bash
echo "## 🛡️ Code Security Analysis"

# Check for common vulnerabilities
echo "### Potential Issues"

# SQL Injection risks
echo -e "\n#### SQL Injection Risks"
grep -r "query.*\${" --include="*.ts" --include="*.tsx" . | \
  grep -v "prepared" | head -5

# XSS risks
echo -e "\n#### XSS Risks"
grep -r "dangerouslySetInnerHTML" --include="*.tsx" . | head -5

# Unvalidated redirects
echo -e "\n#### Open Redirects"
grep -r "redirect.*req\." --include="*.ts" . | head -5

# Missing auth checks
echo -e "\n#### Missing Auth Checks"
find app/api -name "*.ts" -exec grep -L "auth\|session\|token" {} \; | head -10

# CORS issues
echo -e "\n#### CORS Configuration"
grep -r "Access-Control-Allow-Origin.*\*" . | head -5
```

### Generate Security Report
```markdown
## 🔐 Security Report - $(date +%Y-%m-%d)

### Summary
- Status: ⚠️ Issues Found
- Dependencies: 2 high, 5 moderate
- Secrets: 0 exposed
- Code Issues: 3 potential risks

### Critical Issues
1. **Dependency**: lodash@4.17.20 - Prototype pollution
   - Severity: High
   - Fix: Update to 4.17.21
   
2. **Code**: Unvalidated redirect in `/api/auth/callback`
   - Risk: Open redirect vulnerability
   - Fix: Validate redirect URLs against whitelist

### Recommendations
1. Run `npm audit fix --force` for dependencies
2. Add input validation to API routes
3. Enable CSP headers
4. Review authentication middleware

### Compliance Checklist
- [ ] No high/critical vulnerabilities
- [ ] All secrets in env files
- [ ] Input validation on all forms
- [ ] Auth checks on protected routes
- [ ] HTTPS enforced
- [ ] Security headers configured

### Next Steps
```bash
# Fix dependencies
/security-check deps auto

# Review code issues
/security-check code manual
```
```

## Integration with CI/CD:

```json
{
  "security": {
    "preCommit": {
      "enabled": true,
      "checks": ["secrets", "deps"]
    },
    "preBuild": {
      "enabled": true,
      "failOn": ["critical", "high"],
      "checks": ["all"]
    }
  }
}
```

## Git Hooks Integration:

```bash
# .husky/pre-commit
#!/bin/sh
/security-check secrets report
if [ $? -ne 0 ]; then
  echo "❌ Security check failed"
  exit 1
fi
```

This ensures security is checked at every stage of development!
