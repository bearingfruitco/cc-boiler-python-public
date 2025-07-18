# AI Agent Training Scenarios

## 🎓 Introduction

These scenarios train AI agents to use the Claude Code boilerplate system effectively. Each scenario builds on previous ones, introducing concepts gradually.

---

## Scenario 1: First Day Setup
**Goal**: Initialize a new project and understand basic commands

### Instructions for AI Agent:

```markdown
You're starting a new project for a task management app. Follow these steps:

1. Initialize the project:
   ```bash
   ./setup-enhanced-boilerplate.sh
   npm install
   ```

2. Start Claude Code and run:
   ```bash
   /init
   ```

3. Create your first PRD:
   ```bash
   /prd task-management
   ```

4. Generate tasks from the PRD:
   ```bash
   /gt task-management
   ```

5. Check your task status:
   ```bash
   /ts
   ```

Expected Outcome:
- Project structure created
- PRD saved to docs/project/features/
- Task list generated with 15-20 tasks
- Ready to start development
```

### Key Learnings:
- Project initialization workflow
- PRD-driven development approach
- Task decomposition methodology

---

## Scenario 2: Component Creation with Design Validation
**Goal**: Create components following the design system

### Instructions for AI Agent:

```markdown
Create a TaskCard component that displays a task with title, description, and status.

1. Use the component creation command:
   ```bash
   /cc ui TaskCard
   ```

2. The component should include:
   - Title (text-size-2, font-semibold)
   - Description (text-size-3, font-regular)
   - Status badge (colored background)
   - Due date (text-size-4)
   - Edit and Delete buttons

3. Validate the design:
   ```bash
   /vd
   ```

Expected Component Structure:
```typescript
export function TaskCard({ task }: { task: Task }) {
  return (
    <Card className="space-y-3">
      <div className="flex justify-between items-start">
        <h3 className="text-size-2 font-semibold text-gray-900">
          {task.title}
        </h3>
        <StatusBadge status={task.status} />
      </div>
      
      <p className="text-size-3 font-regular text-gray-600">
        {task.description}
      </p>
      
      <div className="flex justify-between items-center">
        <span className="text-size-4 text-gray-500">
          Due: {formatDate(task.dueDate)}
        </span>
        <div className="flex gap-2">
          <Button size="small" variant="secondary">Edit</Button>
          <Button size="small" variant="danger">Delete</Button>
        </div>
      </div>
    </Card>
  )
}
```

Common Mistakes to Avoid:
- ❌ Using text-lg or text-sm
- ❌ Using font-bold or font-medium
- ❌ Using p-5 or gap-5 (not on 4px grid)
- ✅ Only text-size-[1-4] and font-regular/semibold
- ✅ Only spacing divisible by 4
```

### Key Learnings:
- Design system compliance
- Component creation workflow
- Validation process

---

## Scenario 3: Task Processing Workflow
**Goal**: Work through tasks systematically

### Instructions for AI Agent:

```markdown
Process the first 3 tasks from your task list.

1. Start task processing:
   ```bash
   /pt task-management
   ```

2. For Task 1.1 (Create database schema):
   - Create file: lib/db/schema.ts
   - Define tables: tasks, categories, users
   - Add proper TypeScript types
   - Verify with: `tsc --noEmit`

3. For Task 1.2 (Set up API routes):
   - Create: app/api/tasks/route.ts
   - Implement GET and POST handlers
   - Add validation with Zod
   - Test with: `curl http://localhost:3000/api/tasks`

4. For Task 1.3 (Implement data models):
   - Create: lib/models/task.ts
   - Define interfaces and validation schemas
   - Export for use in components

5. After each task:
   ```bash
   /vt  # Verify task completion
   ```

6. Create checkpoint:
   ```bash
   /checkpoint create "completed database setup"
   ```

Expected Verification:
- Each task produces working code
- All files in correct directories
- Types compile without errors
- Manual testing confirms functionality
```

### Key Learnings:
- Task-by-task development
- Verification importance
- Progress tracking

---

## Scenario 4: Handling Design Violations
**Goal**: Understand how hooks prevent violations

### Instructions for AI Agent:

```markdown
Attempt to create a component with design violations and see how the system responds.

1. Try to create a component with banned classes:
   ```typescript
   // This will be blocked
   <div className="text-lg font-bold p-5">
     <h1 className="text-xl">Header</h1>
   </div>
   ```

2. You'll see:
   ```
   DESIGN VIOLATION DETECTED:
   - text-lg found: use text-size-2
   - font-bold found: use font-semibold
   - p-5 found: use p-4 or p-6 (4px grid)
   - text-xl found: use text-size-1
   
   Auto-fix available. Accept? (y/n)
   ```

3. Accept the auto-fix and observe corrections:
   ```typescript
   <div className="text-size-2 font-semibold p-4">
     <h1 className="text-size-1">Header</h1>
   </div>
   ```

4. Run validation to confirm:
   ```bash
   /vd
   ```

Key Understanding:
- Hooks run automatically before file saves
- Violations are caught immediately
- Auto-fix helps maintain compliance
- No manual review needed
```

### Key Learnings:
- Hook system automation
- Design enforcement mechanism
- Auto-fix capabilities

---

## Scenario 5: Team Collaboration
**Goal**: Experience multi-agent coordination

### Instructions for AI Agent:

```markdown
Simulate working with another developer on the same feature.

1. Check team status:
   ```bash
   /team-status
   ```

2. You'll see:
   ```
   Team Activity:
   - nikki: editing components/ui/TaskList.tsx (5m ago)
   - nikki: last commit "Add task filtering" (12m ago)
   ```

3. Before editing related files:
   ```bash
   /collab-sync nikki
   ```

4. You'll see:
   ```
   Syncing with nikki's work...
   ✓ Pulled latest changes
   ✓ No conflicts detected
   ✓ Updated components/ui/TaskList.tsx
   ```

5. Create your component to work with theirs:
   ```bash
   /cc features TaskFilter
   ```

6. The system coordinates:
   - Auto-saves your work every 60s
   - Updates team registry
   - Prevents conflicts
   - Enables perfect handoffs

7. Prepare handoff:
   ```bash
   /handoff prepare
   ```

Result:
- Work saved to GitHub gist
- Team registry updated
- Next developer can pick up seamlessly
```

### Key Learnings:
- Multi-agent coordination
- Automatic synchronization
- Conflict prevention

---

## Scenario 6: Error Recovery and Testing
**Goal**: Handle errors gracefully and ensure code works

### Instructions for AI Agent:

```markdown
Create a form with proper error handling and test it.

1. Create a task creation form:
   ```bash
   /cc forms CreateTaskForm
   ```

2. Implement with error handling:
   ```typescript
   const [error, setError] = useState<string | null>(null)
   
   const handleSubmit = async (data: TaskData) => {
     try {
       const result = await createTask(data)
       router.push(`/tasks/${result.id}`)
     } catch (err) {
       if (err instanceof ApiError) {
         setError(err.message)
       } else {
         setError('Something went wrong')
       }
     }
   }
   ```

3. Test the form:
   ```bash
   /btf create-task-form
   ```

4. The browser test will:
   - Open the form
   - Try valid submission
   - Try invalid data
   - Check error displays
   - Verify success flow

5. If test fails, check:
   - Console for errors
   - Network tab for API issues
   - Form validation logic

Never say "should work" - always verify!
```

### Key Learnings:
- Error handling patterns
- Testing importance
- "Actually Works" protocol

---

## Scenario 7: Performance Optimization
**Goal**: Optimize component performance

### Instructions for AI Agent:

```markdown
Optimize a task list that's rendering slowly.

1. Identify the issue:
   ```typescript
   // Slow version
   function TaskList({ tasks }) {
     return tasks.map(task => (
       <TaskCard 
         key={task.id} 
         task={task}
         onUpdate={() => handleUpdate(task.id)}  // Creates new function each render
       />
     ))
   }
   ```

2. Apply optimizations:
   ```typescript
   // Optimized version
   const TaskList = memo(function TaskList({ tasks }) {
     const handleUpdate = useCallback((taskId: string) => {
       // Update logic
     }, [])
     
     return tasks.map(task => (
       <TaskCard 
         key={task.id} 
         task={task}
         onUpdate={handleUpdate}
       />
     ))
   })
   ```

3. Add pagination:
   ```typescript
   const ITEMS_PER_PAGE = 10
   const [page, setPage] = useState(0)
   
   const paginatedTasks = useMemo(
     () => tasks.slice(page * ITEMS_PER_PAGE, (page + 1) * ITEMS_PER_PAGE),
     [tasks, page]
   )
   ```

4. Measure improvement:
   ```bash
   /pm check
   ```

Results:
- Reduced re-renders
- Faster interaction
- Better user experience
```

### Key Learnings:
- Performance patterns
- React optimization techniques
- Measurement importance

---

## Scenario 8: Full Feature Implementation
**Goal**: Complete an entire feature from PRD to deployment

### Instructions for AI Agent:

```markdown
Implement a complete task filtering feature.

1. Create PRD:
   ```bash
   /prd task-filtering
   ```

2. Generate and review tasks:
   ```bash
   /gt task-filtering
   /tb  # View task board
   ```

3. Process all tasks:
   ```bash
   /pt task-filtering
   ```
   
   Work through:
   - Database: Add filter columns
   - API: Add query parameters
   - UI: Create filter components
   - State: Manage filter state
   - Tests: Verify all paths

4. Regular checkpoints:
   ```bash
   /checkpoint create "filters backend done"
   /checkpoint create "filters UI complete"
   ```

5. Test thoroughly:
   ```bash
   /btf task-filtering
   /tr  # Run all tests
   ```

6. Validate and complete:
   ```bash
   /pp  # Pre-PR checks
   /fw complete 45  # Create PR
   ```

Success Criteria:
- All tasks completed
- Tests passing
- Design validated
- No console errors
- Performance acceptable
```

### Key Learnings:
- End-to-end feature development
- Systematic approach
- Quality gates

---

## Scenario 9: Debugging Production Issues
**Goal**: Debug and fix a reported issue

### Instructions for AI Agent:

```markdown
Users report tasks aren't saving. Debug and fix.

1. Start with smart resume:
   ```bash
   /sr
   ```

2. Check recent changes:
   ```bash
   git log --oneline -10
   ```

3. Run error recovery:
   ```bash
   /er deps  # Check dependencies
   /er build # Check build errors
   ```

4. Use browser testing to reproduce:
   ```bash
   /btf task-save-issue
   ```

5. Check console and network:
   - Look for red errors
   - Check API responses
   - Verify payloads

6. Common issues to check:
   - Missing await on async calls
   - Incorrect API endpoints
   - Validation mismatches
   - State not updating

7. Fix and verify:
   ```typescript
   // Found: missing await
   const saveTask = async (task) => {
     await apiClient.post('/api/tasks', task)  // Added await
     refetch()  // Refresh list
   }
   ```

8. Test the fix:
   ```bash
   /btf task-save-fixed
   ```

Resolution: Always verify fixes work!
```

### Key Learnings:
- Debugging methodology
- Common issue patterns
- Fix verification

---

## Scenario 10: Advanced Patterns
**Goal**: Implement advanced features using all system capabilities

### Instructions for AI Agent:

```markdown
Implement real-time collaborative task editing.

1. Design the feature:
   ```bash
   /prd real-time-collaboration
   ```

2. Key implementation points:
   - WebSocket connection
   - Optimistic updates
   - Conflict resolution
   - Presence indicators

3. Use Supabase real-time:
   ```typescript
   useEffect(() => {
     const channel = supabase
       .channel(`task:${taskId}`)
       .on('presence', { event: 'sync' }, () => {
         // Show who's editing
       })
       .on('broadcast', { event: 'update' }, (payload) => {
         // Apply changes
       })
       .subscribe()
       
     return () => supabase.removeChannel(channel)
   }, [taskId])
   ```

4. Handle edge cases:
   - Network disconnection
   - Conflicting edits
   - User leaves suddenly
   - Data sync issues

5. Test collaboration:
   ```bash
   # Open two browser windows
   /btf collaboration-test
   ```

6. Monitor performance:
   ```bash
   /pm check collaboration
   ```

Advanced Considerations:
- State synchronization
- Network efficiency
- User experience
- Error recovery
```

### Key Learnings:
- Complex feature implementation
- Real-time patterns
- System integration

---

## 📊 Progress Tracking

As AI agents complete scenarios, they should:

1. **Document learnings**:
   ```bash
   /todo add "Learned: Design system auto-enforcement"
   /todo add "Learned: PRD-driven task generation"
   ```

2. **Create knowledge base entries**:
   ```bash
   /checkpoint create "training-scenario-X-complete"
   ```

3. **Share patterns**:
   - Successful implementations
   - Common pitfalls avoided
   - Optimization techniques

---

## 🎯 Graduation Criteria

An AI agent is considered proficient when they can:

- [ ] Initialize projects without guidance
- [ ] Create PRDs and generate tasks
- [ ] Build components with zero design violations
- [ ] Handle errors gracefully
- [ ] Collaborate with team members
- [ ] Debug and fix issues systematically
- [ ] Implement complex features
- [ ] Optimize performance
- [ ] Test thoroughly
- [ ] Never claim "should work" without verification

---

## 🚀 Next Steps

After completing these scenarios:

1. **Practice on real projects**
2. **Contribute to the command library**
3. **Share learnings with team**
4. **Suggest system improvements**

Remember: The system handles HOW, you decide WHAT to build!
