# Failure Scenario Examples

## What Happens When Planning Fails

### Pattern Recognition Failure
```
[ERROR] Unable to detect existing pattern
• File: src/components/CustomButton.tsx
• Issue: Mixed styling approaches (Tailwind + Styled Components)
• Recommendation: Ask user to clarify preferred approach

USER RESPONSE: "Use Tailwind only"
[PLAN ADJUSTED] Migrate to Tailwind-only approach incrementally
```

### Validation Rejection
```
[TASK 3 VALIDATION FAILED]
• Reason: Would break 8 existing consumers
• Impact: Removes required 'onClick' prop
• User Response: "I meant add onPress, not replace onClick"
[PLAN REVISED] Add onPress prop alongside existing onClick
```

### Execution Failure
```
[TASK 2 EXECUTION FAILED]
• Error: TypeScript compilation error
• Cause: Icon type conflicts with existing SVG component
• Rollback: Restored working state from task 1
• Next: Revise icon type definition
```

### User Abort
```
[USER ABORTED]
• Stopped at: Task 4 of 6
• Reason: "This is taking too long, let's simplify"
• State: Preserved from task 3 completion
• Next: Create simplified plan with fewer tasks
```

## Recovery Patterns

### Auto-Rollback
```
[ROLLBACK INITIATED]
• Failed task: Task 5 (Button render modification)
• Restored state: Task 4 completion
• Preserved work: Tasks 1-4 remain intact
• Ready for: Alternative approach or manual fix
```

### Plan Revision
```
[PLAN REVISION REQUIRED]
• Original plan: 8 tasks (too granular)
• User feedback: "Can we combine some steps?"
• Revised plan: 4 consolidated tasks
• Maintains: All validation checkpoints
```

### Alternative Approach
```
[ALTERNATIVE APPROACH]
• Original approach: Breaking change required
• User rejection: "No breaking changes allowed"
• Alternative: Backward-compatible wrapper approach
• Trade-off: Slightly more complex but preserves compatibility
```