# Performance Monitor

Track and optimize performance metrics during development.

## Arguments:
- $ACTION: check|baseline|compare|report
- $TARGET: build|runtime|lighthouse|all

## Why This Command:
- Catch performance regressions early
- Track metrics per feature
- Ensure mobile performance
- Maintain performance budget

## Steps:

### Action: CHECK
Quick performance check:

```bash
# Build metrics
echo "## ⚡ Performance Check"
echo ""

# Bundle size
echo "### 📦 Bundle Size"
BUNDLE_SIZE=$(npm run build 2>&1 | grep -E "First Load JS" | \
  awk '{print $NF}')
echo "First Load JS: $BUNDLE_SIZE"

LIMIT="75kB"
if [[ "$BUNDLE_SIZE" > "$LIMIT" ]]; then
  echo "❌ Exceeds limit ($LIMIT)"
  echo "Run: npm run analyze"
else
  echo "✅ Under limit"
fi

# Component count
echo -e "\n### 🧩 Component Metrics"
COMPONENTS=$(find components -name "*.tsx" | wc -l)
echo "Total components: $COMPONENTS"

# Image optimization
echo -e "\n### 🖼️ Images"
UNOPTIMIZED=$(find public -name "*.jpg" -o -name "*.png" | \
  xargs -I {} identify {} | grep -c "sRGB")
echo "Unoptimized images: $UNOPTIMIZED"

# Runtime checks
echo -e "\n### 🏃 Runtime Performance"
cat > perf-check.js << 'EOF'
// Check for common issues
const issues = [];

// Large lists without virtualization
if (document.querySelectorAll('li').length > 100) {
  issues.push('Large list detected - consider virtualization');
}

// Unoptimized images
const images = Array.from(document.querySelectorAll('img'));
images.forEach(img => {
  if (!img.loading || img.loading !== 'lazy') {
    issues.push(`Image not lazy loaded: ${img.src}`);
  }
});

console.log(issues);
EOF
```

### Action: BASELINE
Create performance baseline:

```bash
# Run Lighthouse
npx lighthouse http://localhost:3000 \
  --output=json \
  --output-path=.claude/perf/baseline.json \
  --only-categories=performance,accessibility,best-practices

# Extract key metrics
METRICS=$(cat .claude/perf/baseline.json | jq '{
  performance: .categories.performance.score,
  fcp: .audits["first-contentful-paint"].numericValue,
  lcp: .audits["largest-contentful-paint"].numericValue,
  cls: .audits["cumulative-layout-shift"].numericValue,
  fid: .audits["max-potential-fid"].numericValue
}')

# Save with issue context
echo "$METRICS" > .claude/perf/baseline-issue-${ISSUE}.json

echo "✅ Baseline saved for Issue #$ISSUE"
```

### Action: COMPARE
Compare against baseline:

```bash
# Run current check
npx lighthouse http://localhost:3000 \
  --output=json \
  --output-path=.claude/perf/current.json \
  --only-categories=performance

# Compare
BASELINE=$(cat .claude/perf/baseline-issue-${ISSUE}.json)
CURRENT=$(cat .claude/perf/current.json | jq '.categories.performance.score')

echo "## 📊 Performance Comparison"
echo ""
echo "Baseline: $(echo $BASELINE | jq '.performance')"
echo "Current: $CURRENT"
echo ""

# Detailed comparison
node -e "
const baseline = $BASELINE;
const current = require('.claude/perf/current.json');

const metrics = ['fcp', 'lcp', 'cls', 'fid'];
metrics.forEach(metric => {
  const baseValue = baseline[metric];
  const currValue = current.audits[metric]?.numericValue || 0;
  const diff = ((currValue - baseValue) / baseValue * 100).toFixed(1);
  const emoji = diff > 10 ? '❌' : diff > 0 ? '⚠️' : '✅';
  console.log(`${emoji} ${metric}: ${diff}%`);
});
"
```

### Action: REPORT
Generate performance report:

```markdown
## 🚀 Performance Report - Issue #23

### Summary
- Performance Score: 92/100 (↓ 3 from baseline)
- Build Size: 72kB (↑ 5kB)
- Status: ⚠️ Minor regression

### Core Web Vitals
| Metric | Baseline | Current | Change | Status |
|--------|----------|---------|---------|--------|
| FCP | 1.2s | 1.3s | +8.3% | ⚠️ |
| LCP | 2.1s | 2.0s | -4.8% | ✅ |
| CLS | 0.05 | 0.05 | 0% | ✅ |
| FID | 45ms | 48ms | +6.7% | ✅ |

### Recommendations
1. **FCP Regression**: Check new fonts/CSS
2. **Bundle Size**: Run bundle analyzer
3. **Images**: 2 images need optimization

### Component Performance
- LoginForm: 45ms render (acceptable)
- RegisterForm: 52ms render (investigate)

### Next Steps
```bash
# Analyze bundle
npm run analyze

# Optimize images
npm run optimize:images
```
```

## Performance Budget Config:

```json
{
  "performance": {
    "budgets": {
      "firstLoad": "75kB",
      "performance": 90,
      "fcp": 1500,
      "lcp": 2500,
      "cls": 0.1,
      "fid": 100
    },
    "monitoring": {
      "enabled": true,
      "failBuild": true,
      "warnOnly": false
    }
  }
}
```

## Integration:

```bash
# During development
/performance-monitor check
> "Bundle: 72kB ✅"
> "Performance: 92/100 ✅"

# Before PR
/feature-workflow complete 23
> "Running performance check..."
> "❌ FCP regression detected"
> "Fix before creating PR"
```
