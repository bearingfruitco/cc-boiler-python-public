# Analyze Project Requirements

Analyze a project's needs and create a comprehensive documentation plan.

## Arguments:
- $PROJECT_TYPE: Type of project (SaaS, e-commerce, etc.)
- $REQUIREMENTS: Path to requirements file or inline description

## Steps:

1. **Analyze Project Type**
   ```typescript
   // Determine component needs based on project type
   const projectProfiles = {
     'saas': ['auth', 'dashboard', 'billing', 'teams'],
     'ecommerce': ['catalog', 'cart', 'checkout', 'orders'],
     'marketing': ['hero', 'features', 'testimonials', 'cta'],
     'internal': ['tables', 'forms', 'reports', 'admin']
   };
   ```

2. **Scan Existing Code** (if any)
   - Check for existing patterns
   - Identify design system violations
   - Note commonly used components

3. **Research Best Practices**
   - Look up industry standards for project type
   - Check accessibility requirements
   - Note performance considerations

4. **Generate Documentation Plan**
   ```markdown
   # Documentation Plan for [Project Name]
   
   ## Required Components (Priority Order)
   1. Authentication System
      - Login/Register forms
      - Password reset flow
      - Session management
   
   2. Dashboard Layout
      - Navigation structure
      - Widget system
      - Responsive grid
   
   ## Design Patterns Needed
   - Form validation strategy
   - Error handling patterns
   - Loading state management
   
   ## Boilerplate Structure
   - 15 UI components
   - 8 utility functions
   - 5 layout templates
   - 3 example features
   
   ## Validation Requirements
   - All components must pass design system check
   - Mobile-first implementation
   - Accessibility WCAG 2.1 AA
   ```

5. **Create Execution Plan**
   - Order components by dependency
   - Group related components
   - Estimate documentation size

## Output:
Creates `DOCUMENTATION_PLAN.md` with:
- Complete component list
- Implementation order
- Design pattern requirements
- Validation criteria

## Next Step:
Run `/generate-docs DOCUMENTATION_PLAN.md` to create the actual documentation.
