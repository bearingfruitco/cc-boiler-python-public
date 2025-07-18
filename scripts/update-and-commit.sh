#!/bin/bash
# Update all documentation files and commit changes

echo "🔄 Updating documentation from NextJS to Python..."

# Function to update a file
update_file() {
    local file="$1"
    echo "  Updating: $(basename "$file")"
    
    # Create backup
    cp "$file" "$file.bak"
    
    # Perform replacements
    sed -i '' \
        -e 's/npm install/poetry install/g' \
        -e 's/pnpm install/poetry install/g' \
        -e 's/yarn install/poetry install/g' \
        -e 's/npm run/poetry run/g' \
        -e 's/pnpm run/poetry run/g' \
        -e 's/npm test/pytest/g' \
        -e 's/pnpm test/pytest/g' \
        -e 's/npm/poetry/g' \
        -e 's/pnpm/poetry/g' \
        -e 's/yarn/poetry/g' \
        -e 's/Node\.js 22+/Python 3.11+/g' \
        -e 's/Node\.js/Python/g' \
        -e 's/Next\.js/FastAPI/g' \
        -e 's/NextJS/FastAPI/g' \
        -e 's/React/Pydantic/g' \
        -e 's/TypeScript/Python/g' \
        -e 's/JavaScript/Python/g' \
        -e 's/\.tsx\?/\.py/g' \
        -e 's/\.jsx\?/\.py/g' \
        -e 's/\.ts/\.py/g' \
        -e 's/\.js/\.py/g' \
        -e 's/components\//src\//g' \
        -e 's/component/module/g' \
        -e 's/Component/Module/g' \
        -e 's/package\.json/pyproject.toml/g' \
        -e 's/node_modules/\.venv/g' \
        -e 's/tsconfig\.json/pyproject.toml/g' \
        -e 's/tailwind\.config\.js/ruff.toml/g' \
        -e 's/\.eslintrc/\.ruff.toml/g' \
        -e 's/prettier/black/g' \
        -e 's/Jest/Pytest/g' \
        -e 's/Vitest/Pytest/g' \
        -e 's/frontend/API/g' \
        -e 's/Frontend/API/g' \
        -e 's/UI components/Python modules/g' \
        -e 's/design system/coding standards/g' \
        -e 's/Design System/Coding Standards/g' \
        -e 's/Tailwind/Type hints/g' \
        -e 's/Vercel/Railway\/Fly.io/g' \
        -e 's/my-awesome-app/my-ai-agent-system/g' \
        -e 's/claude-code-boilerplate/boilerplate-python/g' \
        "$file"
    
    # Remove backup if successful
    if [ $? -eq 0 ]; then
        rm "$file.bak"
    else
        echo "    ❌ Error updating $file"
        mv "$file.bak" "$file"
    fi
}

# Update all markdown files in docs/setup
echo "📁 Updating docs/setup..."
for file in docs/setup/*.md; do
    if [ -f "$file" ]; then
        update_file "$file"
    fi
done

# Update all markdown files in docs/workflow
echo "📁 Updating docs/workflow..."
for file in docs/workflow/*.md; do
    if [ -f "$file" ]; then
        update_file "$file"
    fi
done

# Update CodeRabbit references to be optional
echo "📝 Making CodeRabbit optional..."
find docs -name "*.md" -exec sed -i '' \
    -e '/CodeRabbit.*AI Code Reviews/,/^###/{s/CodeRabbit (AI Code Reviews)/CodeRabbit (AI Code Reviews) - Optional/; s/Choose "Pro" plan/Choose plan that fits your needs/; /Choose "Pro" plan/a\
- Note: This is optional but recommended for AI-powered code reviews
}' {} \;

# Create git commit
echo "📦 Creating git commit..."
git add docs/
git add scripts/update-docs-to-python.py
git add SHARING_CHECKLIST.md

git commit -m "docs: Update all documentation from NextJS to Python

- Convert package manager references (npm/pnpm → poetry)
- Update language/framework references (NextJS → FastAPI, React → Pydantic)
- Change file extensions (.tsx/.jsx → .py)
- Update directory structures (components → src)
- Make CodeRabbit optional throughout
- Add Python-specific setup guide
- Update all examples and commands for Python context"

echo "✅ Documentation updated and committed!"
echo ""
echo "📋 Next steps:"
echo "1. Review changes: git diff HEAD~1"
echo "2. Push to GitHub: git push origin main"
echo "3. Share repository with your brother"
