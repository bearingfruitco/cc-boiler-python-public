# Generate AI Agent Documentation

Generate comprehensive documentation package for AI coding assistants.

## Steps:

1. **Analyze Requirements**
   - Read INITIAL.md for project type and requirements
   - Identify key features and components needed
   - Determine appropriate boilerplate components

2. **Create Design System Documentation**
   ```
   - DESIGN_RULES.md (quick reference)
   - design-system.md (comprehensive guide)
   - Component patterns with examples
   ```

3. **Generate Boilerplate Library**
   ```
   /components/ui/
     - Button.tsx (with all variants)
     - Card.tsx (with sub-components)
     - Input.tsx (with validation states)
     - Select.tsx (mobile-optimized)
     - Modal.tsx (accessible)
   
   /components/forms/
     - FormField.tsx (with error handling)
     - FormSection.tsx (with spacing)
     - ValidationMessage.tsx
   
   /components/layout/
     - Container.tsx (responsive)
     - PageLayout.tsx (with SEO)
     - Section.tsx (with proper spacing)
   ```

4. **Create Utility Functions**
   ```
   /lib/
     - api-client.ts (with error handling)
     - validation.ts (common schemas)
     - utils.ts (formatting, etc.)
     - cn.ts (classname utility)
   ```

5. **Generate Setup Scripts**
   ```bash
   setup-project.sh
   setup-env.sh
   setup-database.sh
   ```

6. **Create AI Instructions**
   - project-instructions.md (for AI agents)
   - validation-rules.md (for checking)
   - common-patterns.md (for reference)

7. **Add VSCode Snippets**
   - Create project-snippets.json
   - Include all common patterns
   - Add to .vscode/snippets/

8. **Generate Validation Tools**
   - Design system checker
   - Typography validator
   - Spacing grid checker
   - Color distribution analyzer

## Validation:
- All components follow 4-size typography
- All spacing on 4px grid
- Color distribution is 60/30/10
- Mobile-first with 44px+ touch targets
- Includes error handling patterns

## Output:
Create artifacts for each major file with complete, production-ready code.
