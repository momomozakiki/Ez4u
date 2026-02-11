---
name: "planner-architect"
description: "Breaks requests into validated micro-tasks. Invoke when user requests updates/modifications to existing code."
---
# Planner-Architect Skill

## Purpose
Prevent design system corruption by decomposing requests into atomic, validated tasks executed incrementally.

## When to Invoke
- User requests "update", "modify", "change", "improve" existing components
- Request involves >1 file or complex feature addition
- User shares existing code for modification

## Execution Protocol (MANDATORY FLOW)

### PHASE 1: Pattern Audit (BEFORE PLANNING)
Analyze existing implementation to detect:
✅ Styling approach (Tailwind primitives vs custom CSS)
✅ Composition pattern (clsx usage, base class extraction)
✅ Props API surface (existing props/interfaces)
✅ Dependencies (components/files consuming this pattern)
✅ File organization convention (feature-based vs type-based)

Output audit result:
```
[PATTERN AUDIT]
• Component: Button
• Styling: Tailwind primitives only (no custom CSS)
• Composition: clsx with base/variant/size classes extracted
• Props: { children, variant, size, disabled }
• Dependencies: 12 components in src/features/
• Convention: PascalCase components, kebab-case files
```

### PHASE 2: Task Decomposition
Break request into atomic tasks (≤1 file OR ≤1 logical unit per task):

❌ BAD (monolithic):
```
[PLAN] Update Button component with icon support, new variants, and responsive sizing
```

✅ GOOD (atomic):
```
[PLAN]
1. Audit Button component pattern (styling, props, composition)
2. Add `icon` prop type to ButtonProps interface (src/components/Button/types.ts)
3. Extend variantClasses to support icon positioning (src/components/Button/utils.ts)
4. Modify Button render to accept/iconLeft/iconRight props (src/components/Button.tsx)
5. Update Storybook stories with icon examples (src/components/Button/Button.stories.tsx)
6. Verify all 12 consumers still work with new API (additive only)
```

### PHASE 3: Validation Checkpoints
BEFORE each task execution:
```
[TASK 2 VALIDATION]
• Target: src/components/Button/types.ts
• Current: interface ButtonProps { children: ReactNode; variant?: 'primary' | 'secondary'; ... }
• Proposed: Add `icon?: ReactNode; iconPosition?: 'left' | 'right'`
• Pattern preservation: ✅ Additive only (no breaking changes)
• Risk: Low
Confirm "TASK 2" to proceed
```

### PHASE 4: Incremental Execution
- Execute ONLY confirmed task
- Show diff of changes (before/after)
- Verify functionality preserved
- WAIT for explicit confirmation before next task

### PHASE 5: Rollback Protocol
IF validation fails OR user rejects task:
```
[ROLLBACK]
• Reverted task 3 changes to src/components/Button/utils.ts
• Restored working state from task 2
• Awaiting replan for icon positioning approach
```

## Atomic Task Templates

### ✅ ADDITIVE TASK (Preferred)
```
TASK: Add [feature] to [component] preserving existing [pattern]
• Target file: [path]
• Current API: [describe]
• Proposed change: [describe additive change]
• Pattern preserved: ✅ [list preserved patterns]
• Breaking changes: None
```

### ⚠️ REPLACEMENT TASK (Requires Approval)
```
TASK: Replace [old pattern] with [new pattern] in [component]
• Target file: [path]
• Current pattern: [describe]
• Proposed replacement: [describe]
• Dependencies affected: [list]
• Breaking changes: [list]
⚠️ Requires explicit "CONFIRM REPLACEMENT" before proceeding
```

## Verification Checklist (After Each Task)
```
[TASK COMPLETE]
✓ Pattern preserved: [Tailwind primitives / clsx composition]
✓ Additive change only: [new prop added, existing API intact]
✓ Dependencies unaffected: [0 breaking changes]
✓ Next task ready: [TASK 3 description]
Confirm "TASK 3" to proceed OR "ABORT" to stop
```

## Seed Validation Protocol (CRITICAL)

### What is a "Seed"?
A minimal, verifiable unit of change that can be:
- ✅ Validated against existing patterns BEFORE full implementation
- ✅ Reverted instantly if validation fails
- ✅ Used as foundation for next task

### Seed Examples

| Request | BAD Seed (too big) | GOOD Seed (atomic) |
|---------|-------------------|-------------------|
| "Add icon to Button" | Full icon implementation with positioning logic | Add `icon?: ReactNode` prop type ONLY |
| "Make responsive" | Rewrite entire layout with media queries | Add single `sm:` breakpoint to ONE element |
| "Add dark mode" | Full theme switcher + CSS variables | Add `dark:` prefix to ONE utility class |

### Validation Questions for Every Seed
BEFORE executing seed task:
1. Does this seed preserve existing styling patterns? (Tailwind vs custom CSS)
2. Does this seed preserve existing composition patterns? (clsx usage)
3. Does this seed preserve existing API surface? (additive vs breaking)
4. Can this seed be reverted in <10 seconds if validation fails?
5. Does this seed affect ≤1 file OR ≤1 logical unit?

IF any answer = NO → REJECT seed and replan smaller task
