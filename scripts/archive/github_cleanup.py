#!/usr/bin/env python3
"""
Delete unnecessary files from the public Python boilerplate repository.
This script uses the GitHub CLI to remove internal documentation and JavaScript-related files.
"""

import subprocess
import sys

# Repository details
REPO = "bearingfruitco/cc-boiler-python-public"

# Files to delete
FILES_TO_DELETE = [
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
    
    # Prisma
    "prisma/schema.prisma",
    
    # JavaScript tests
    "tests/system-check.test.ts",
    "tests/test-imports.tsx",
    "tests/test-setup.ts",
    
    # JavaScript types
    "types/global.d.ts",
    "types/index.ts",
    "types/rudderstack.d.ts",
    "types/tracking.ts",
]

def delete_file(repo, file_path):
    """Delete a file from the repository using GitHub CLI."""
    cmd = ["gh", "api", f"/repos/{repo}/contents/{file_path}", "-X", "DELETE"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Deleted: {file_path}")
        else:
            print(f"❌ Failed to delete {file_path}: {result.stderr}")
    except Exception as e:
        print(f"❌ Error deleting {file_path}: {e}")

def main():
    print("🧹 Cleaning up Python boilerplate repository")
    print("=" * 50)
    print()
    
    print(f"Repository: {REPO}")
    print(f"Files to delete: {len(FILES_TO_DELETE)}")
    print()
    
    # Check if gh CLI is installed
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except:
        print("❌ GitHub CLI (gh) is not installed!")
        print("Install it from: https://cli.github.com/")
        sys.exit(1)
    
    # Delete each file
    for file_path in FILES_TO_DELETE:
        delete_file(REPO, file_path)
    
    print()
    print("✅ Cleanup complete!")

if __name__ == "__main__":
    main()
