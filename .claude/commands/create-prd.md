Create a comprehensive Product Requirements Document for: $ARGUMENTS

Structure the PRD with:

## 1. Feature Overview
- What is this feature?
- Why are we building it?
- Who will use it?

## 2. User Stories
Generate 3-5 user stories in format:
"As a [type of user], I want to [action] so that [benefit]"

## 3. Functional Requirements
List specific functionalities needed:
- Must have features
- Nice to have features
- Out of scope for v1

## 4. UI/UX Requirements
- Key screens/components needed
- User flow description
- Mobile considerations

## 5. Technical Requirements
- API endpoints needed
- Database changes
- Performance requirements
- Security considerations

## 6. Success Metrics
- How will we measure success?
- What are the KPIs?

## 7. Edge Cases & Error Handling
- What could go wrong?
- How should the system respond?

## 8. Documentation & Context Requirements
### Must Read Documentation
List with reasons why each is critical:
```
- url: [official API docs] 
  why: [specific methods/patterns we'll use]
- file: [existing code example]
  why: [pattern to follow or gotcha to avoid]
- doc: [library guide]
  section: [specific section]
  critical: [key insight that prevents errors]
```

### Research Needed
Technologies requiring documentation research:
- [ ] Technology 1 - focus areas
- [ ] Technology 2 - focus areas

Run `/research-docs "[tech1], [tech2]"` before implementation
Then cache with `/doc-cache cache "[tech1], [tech2]"`

## 9. Implementation Phases with Stage Gates

### Phase 1: Foundation (Backend/Data)
**Objective**: Establish solid technical foundation

Tasks:
- Database schema and models
- Core business logic
- Basic API structure
- Authentication setup
- Environment configuration

**Exit Criteria** (Automated validation):
- [ ] All database migrations run successfully
- [ ] API endpoints return expected status codes
- [ ] Authentication flow complete
- [ ] Test data available
- [ ] No TypeScript errors
- [ ] Unit tests passing

**Validate with**: `/stage-validate check 1`

### Phase 2: Core Features
**Objective**: Implement all user-facing functionality

Tasks:
- Complete API implementation
- Frontend components
- Form validation
- Integration testing
- Error states
- Loading states

**Exit Criteria**:
- [ ] All PRD features implemented
- [ ] Forms validate properly
- [ ] API integration complete
- [ ] Mobile responsive
- [ ] Error handling works
- [ ] 80% test coverage

**Validate with**: `/stage-validate check 2`

### Phase 3: Polish & Production
**Objective**: Production-ready quality

Tasks:
- Performance optimization
- Security hardening
- Final testing
- Documentation
- Deployment setup
- Monitoring

**Exit Criteria**:
- [ ] Lighthouse score > 90
- [ ] Security audit passed
- [ ] All tests green
- [ ] Documentation complete
- [ ] Deployment automated
- [ ] Error tracking active

**Validate with**: `/stage-validate check 3`

## 10. Context Management Strategy

### Recommended Context Profiles
```bash
# Create profiles for this feature
/context-profile create "$ARGUMENTS-backend"  # For Phase 1
/context-profile create "$ARGUMENTS-frontend" # For Phase 2
/context-profile create "$ARGUMENTS-testing"  # For Phase 3
```

### Documentation to Cache
```bash
# Cache relevant docs after PRD approval
/doc-cache cache "[primary framework docs]"
/doc-cache cache "[authentication library]"
/doc-cache cache "[testing framework]"
```

Save as docs/project/features/$ARGUMENTS-PRD.md

After creation:
1. Run `/research-docs` for documentation
2. Run `/gt $ARGUMENTS` to generate tasks
3. Run `/stage-validate require 1` to enforce gates