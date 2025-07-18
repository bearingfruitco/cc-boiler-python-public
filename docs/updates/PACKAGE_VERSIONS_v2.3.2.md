# Package Version Updates - v2.3.2

## Overview

Updated all package versions in the boilerplate to their latest stable versions that are confirmed to work together.

## Key Version Fixes

### Production Dependencies
- `@supabase/ssr`: `^0.5.0` → `^0.5.2`
- `drizzle-zod`: `^0.5.0` → `^0.5.1`
- `postgres`: `^3.5.0` → `^3.4.7` (3.5.0 not released yet)

### Development Dependencies
- `@types/node`: `^22.10.0` → `^22.16.3`
- `drizzle-kit`: `^0.32.0` → `^0.31.4` (0.32.0 not released yet)
- `husky`: `^9.2.0` → `^9.1.7` (9.2.0 not released yet)
- `prettier`: `^3.4.0` → `^3.6.2`
- `concurrently`: `^8.2.0` → `^8.2.2`
- `tsx`: `^4.19.0` → `^4.20.3`

### Package Manager
- `pnpm`: `10.0.0` → `10.13.1`

### Script Updates
- `prepare`: `"husky install"` → `"husky"` (new husky v9 syntax)

## Important Notes

1. **Tailwind CSS v4**: We're using the stable v4.1.0 release
2. **Version Constraints**: Some packages had versions specified that haven't been released yet
3. **Compatibility**: All versions have been tested together and work correctly

## Installation

```bash
# Clean install with updated versions
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## Verification

```bash
# Verify key packages
pnpm ls drizzle-kit husky postgres tailwindcss
```

## Breaking Changes

None - all updates are backward compatible.

## Future Updates

These packages have newer versions available but are not critical:
- `jose`: 5.10.0 → 6.0.11 (major version bump, needs testing)
- `@types/node`: Could go to 24.x but staying on 22.x for stability
- `concurrently`: Could go to 9.x but 8.x is stable

## Boilerplate Sync

The main boilerplate repository has been updated with all these version fixes to ensure new projects start with working versions.
