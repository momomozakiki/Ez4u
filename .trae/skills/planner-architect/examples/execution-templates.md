# Execution Output Templates

## Task Completion Templates

### Successful Task Completion
```
[TASK 1 COMPLETE]
✓ Added `icon?: ReactNode` to ButtonProps
✓ No breaking changes to existing API
✓ All 12 consumers continue working
✓ Next: TASK 2 (add iconPosition prop)
Confirm "TASK 2" to proceed OR "ABORT" to stop
```

### Multi-Task Completion
```
[TASK 3 COMPLETE]
✓ Extended variantClasses with icon spacing utilities
✓ Preserved clsx composition pattern
✓ Added support for iconPosition variants
✓ Next: TASK 4 (modify Button render logic)
Confirm "TASK 4" to proceed OR "ABORT" to stop
```

### Final Completion
```
[PLAN COMPLETE]
✅ All tasks executed successfully
✅ Icon support added to Button component
✅ Existing patterns preserved (Tailwind + clsx)
✅ All 12 consumers verified working
✅ Stories updated with icon examples

SUMMARY:
• Added icon and iconPosition props
• Extended variantClasses for icon spacing
• Maintained backward compatibility
• Zero breaking changes introduced
```

## Rollback Templates

### Task Rollback
```
[ROLLBACK]
• Reverted task 3 changes to src/components/Button/utils.ts
• Restored working state from task 2
• Awaiting replan for icon positioning approach
```

### Plan Abort
```
[PLAN ABORTED]
• Stopped at task 2 of 6
• Working state preserved from task 1
• No partial changes committed
• Ready for alternative approach
```

## Error Templates

### Validation Error
```
[VALIDATION ERROR]
• Task 4 validation failed
• Reason: Would break existing render pattern
• Recommendation: Use additive approach instead
• Awaiting revised plan
```

### Execution Error
```
[EXECUTION ERROR]
• Task 3 failed during execution
• Error: TypeScript compilation failed
• Rollback initiated automatically
• Restored working state from task 2
```