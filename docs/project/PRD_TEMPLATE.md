# [Project Name] - Product Requirements Document Template

## Executive Summary
[One paragraph: What is this product/feature and why does it matter?]

## Problem Statement
- **Problem**: [What specific problem are we solving?]
- **Impact**: [What happens if we don't solve this?]
- **Current Solutions**: [How are users solving this today?]
- **Why Now**: [Why is this the right time to build this?]

## Target Users
### Primary User
- **Who**: [Specific user type/role]
- **Needs**: [What they need to accomplish]
- **Pain Points**: [Current frustrations]

### Secondary Users
- **Who**: [Other user types]
- **Needs**: [Their specific needs]

## Core Features (MVP)

### 1. [Feature Name]
- **Description**: [What it does]
- **User Value**: [Why users need this]
- **Success Criteria**: [How we know it works]

### 2. [Feature Name]
- **Description**: [What it does]
- **User Value**: [Why users need this]
- **Success Criteria**: [How we know it works]

## User Stories
- As a [user type], I want to [action] so that [benefit]
- As a [user type], I want to [action] so that [benefit]
- As a [user type], I want to [action] so that [benefit]

## User Flow
1. User arrives at [entry point]
2. User sees [what they see]
3. User performs [action]
4. System responds with [response]
5. User achieves [goal]

## Technical Requirements
- **Performance**: Page load < 3 seconds
- **Availability**: 99.9% uptime
- **Security**: [Specific requirements]
- **Scalability**: Support [X] concurrent users
- **Browser Support**: Chrome, Safari, Firefox, Edge (latest 2 versions)
- **Mobile**: Fully responsive, touch-optimized

## External Documentation & RAG Integration

### MCP Servers to Use
- [ ] **Supabase MCP**: Database schemas, RLS policies, auth patterns
  - Focus areas: [specific tables/features]
- [ ] **GitHub MCP**: Similar implementations, code examples
  - Repositories: [list relevant repos]
- [ ] **Web Search**: Latest best practices, framework updates
  - Topics: [specific search areas]

### Documentation Resources
- [ ] **Official Docs**: [Framework/library documentation URLs]
- [ ] **API References**: [Specific API documentation]
- [ ] **Internal Docs**: [Company/project documentation]
- [ ] **Blog Posts/Guides**: [Helpful articles/tutorials]

### Example Code & Patterns
- [ ] **Similar Features**: See `docs/examples/patterns/[pattern-name].md`
- [ ] **Anti-patterns**: Review `docs/examples/anti-patterns/` to avoid common mistakes
- [ ] **Integration Examples**: Check `docs/examples/integrations/[service-name].md`

## Success Metrics
- **Adoption**: [X]% of users use feature within 30 days
- **Engagement**: [Y] actions per user per week
- **Performance**: [Z]% improvement in [metric]
- **Business**: [Specific business metric]

## Constraints & Assumptions
### Constraints
- Must work within existing infrastructure
- Cannot break existing features
- Must comply with [regulations/standards]

### Assumptions
- Users have [basic knowledge/access]
- [Technical assumption]
- [Business assumption]

## Dependencies
- [Internal system/team]
- [External service/API]
- [Design assets]

## Context & State Requirements

### Required Context
- [ ] Previous implementation patterns
- [ ] Team decisions and rationale
- [ ] Common errors and solutions
- [ ] Performance benchmarks

### State Tracking
- [ ] Feature flags
- [ ] User preferences
- [ ] Session data
- [ ] Analytics events

## Timeline Considerations
- **MVP Target**: [Date]
- **Critical Milestones**: [List key dates]
- **Launch Considerations**: [Any specific timing needs]

## Out of Scope (v1)
- [Feature/functionality not included in MVP]
- [Another deferred feature]
- [Future enhancement]

## Open Questions
- [ ] [Question needing answer]
- [ ] [Decision to be made]
- [ ] [Clarification needed]

## Appendix
### Mockups/Wireframes
[Links or references to design assets]

### Technical Architecture
[High-level technical approach]

### Competitive Analysis
[How competitors solve this problem]

### Pattern References
- Authentication: See `docs/examples/patterns/auth-flow.md`
- Data Fetching: See `docs/examples/patterns/data-fetching.md`
- Error Handling: See `docs/examples/patterns/error-handling.md`
- Form Validation: See `docs/examples/patterns/form-validation.md`
