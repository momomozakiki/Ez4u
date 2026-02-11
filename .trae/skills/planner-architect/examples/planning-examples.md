# Real-World Planning Examples

## Example 1: Add icon support to Button

### ❌ Monolithic Execution (Current Failure Mode)
User: "Add icon support to Button component"

AI response:
```
✅ Here's the updated Button component with full icon support:
[Generates 200-line rewrite replacing clsx with emotion, adding icon positioning logic, 
 modifying 3 files simultaneously]

RESULT: 
• Breaks Tailwind primitive pattern
• Breaks clsx composition used by 12 components
• Introduces emotion dependency unexpectedly
• All 12 consumers broken → design system corrupted
```

### ✅ Incremental Planning (Correct Approach)
User: "Add icon support to Button component"

AI response:
```
[PATTERN AUDIT]
• Component: Button
• Styling: Tailwind primitives only
• Composition: clsx with base/variant/size extraction
• Props: { children, variant, size, disabled }
• Dependencies: 12 components

[PLAN]
1. Add `icon?: ReactNode` prop type to ButtonProps interface
2. Add `iconPosition?: 'left' | 'right'` prop type
3. Extend variantClasses to support icon spacing utilities
4. Modify render to conditionally render icon with spacing
5. Update stories with icon examples
6. Verify all 12 consumers still work

[VALIDATION REQUIRED] Confirm plan? Reply "YES" to proceed step-by-step.
```

User: YES

```
[TASK 1 VALIDATION]
• Target: src/components/Button/types.ts
• Current: interface ButtonProps { children: ReactNode; variant?: string; ... }
• Proposed: Add `icon?: ReactNode;`
• Pattern preserved: ✅ Additive only (no breaking changes)
• Risk: Low
Confirm "TASK 1" to proceed
```

User: TASK 1

```
[TASK 1 COMPLETE]
✓ Added `icon?: ReactNode` to ButtonProps
✓ No breaking changes
✓ Next: TASK 2 (add iconPosition prop)
Confirm "TASK 2" to proceed
```

[... continues incrementally ...]

**RESULT**: 
✅ Icon support added WITHOUT breaking existing patterns  
✅ All 12 consumers continue working  
✅ Full rollback capability at each step  
✅ Zero design system corruption
