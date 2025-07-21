import json
import subprocess
import sys

# Files to delete from the public repository
files_to_delete = [
    # Internal documentation
    "COMMIT_MESSAGE.md",
    "DOCUMENTATION_UPDATE_COMPLETE.md", 
    "GIT_COMMIT_GUIDE.md",
    "GO_PUBLIC_TODO.md",
    "INITIAL.md",
    "PYTHON_DEVELOPMENT_PLAN.md",
    "SECURITY_SWEEP_RESULTS.md",
    "SHARING_CHECKLIST.md",
    "UPDATE_SUMMARY.md",
    
    # JavaScript/Next.js related files
    "biome.json",
    "bunfig.toml",
    "check-dependencies.sh",
    "components.json",
    ".npmrc",
    ".coderabbit.yaml",
    
    # Directories (need to be handled differently)
    "prisma/schema.prisma",
    
    # Test files that are JavaScript
    "tests/system-check.test.ts",
    "tests/test-imports.tsx",
    "tests/test-setup.ts",
    
    # Types directory files
    "types/global.d.ts",
    "types/index.ts",
    "types/rudderstack.d.ts",
    "types/tracking.ts"
]

print("🧹 Cleaning up public Python boilerplate repository")
print("=" * 50)
print()

# Group files by type for better organization
internal_docs = [f for f in files_to_delete if f.endswith('.md') and f not in ['README.md', 'SECURITY.md', 'CHANGELOG.md', 'CLAUDE.md']]
js_configs = [f for f in files_to_delete if f.endswith(('.json', '.toml', '.yaml')) or f in ['.npmrc', 'check-dependencies.sh']]
js_code = [f for f in files_to_delete if f.endswith(('.ts', '.tsx', '.prisma'))]

print("📄 Internal documentation to remove:")
for f in internal_docs:
    print(f"  - {f}")

print("\n⚙️ JavaScript/Next.js config files to remove:")
for f in js_configs:
    print(f"  - {f}")

print("\n📦 JavaScript code files to remove:")
for f in js_code:
    print(f"  - {f}")

print(f"\n📊 Total files to remove: {len(files_to_delete)}")
print("\nThese files are not needed for a Python-focused boilerplate.")
