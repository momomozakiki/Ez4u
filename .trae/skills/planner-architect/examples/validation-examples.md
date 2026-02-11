# Task Validation Examples

## Validation Checkpoint Templates

### Interface/Type Validation
```
[TASK 1 VALIDATION]
• Target: src/components/Button/types.ts
• Current: interface ButtonProps { children: ReactNode; variant?: string; ... }
• Proposed: Add `icon?: ReactNode; iconPosition?: 'left' | 'right'`
• Pattern preservation: ✅ Additive only (no breaking changes)
• Risk: Low
Confirm "TASK 1" to proceed
```

### Function Validation
```
[TASK 2 VALIDATION]
• Target: src/components/Button/utils.ts
• Current: variantClasses extracts base + variant classes
• Proposed: Add iconSpacingClasses for icon positioning
• Pattern preservation: ✅ Extends existing clsx pattern
• Risk: Low
Confirm "TASK 2" to proceed
```

### Component Render Validation
```
[TASK 3 VALIDATION]
• Target: src/components/Button/Button.tsx
• Current: Simple button with children render
• Proposed: Conditional icon rendering with positioning
• Pattern preservation: ✅ Preserves existing render pattern
• Risk: Low
Confirm "TASK 3" to proceed
```

## Validation Decision Points

### When to Validate
- Before modifying existing interfaces/types
- Before changing function signatures
- Before modifying component render logic
- Before updating state management
- Before changing file structure

### What to Check
1. **Pattern Preservation**: Does this maintain existing patterns?
2. **Breaking Changes**: Will this break existing consumers?
3. **Additive vs Destructive**: Is this extending or replacing?
4. **Risk Assessment**: What's the impact scope?

### Validation Response Patterns

#### ✅ Safe to Proceed
```
Confirm "TASK X" to proceed
```

#### ⚠️ Requires Confirmation
```
[DESTRUCTIVE CHANGE WARNING] This replaces existing [pattern]
Confirm: "Yes, replace existing pattern" to proceed
```

#### ❌ Abort
```
[VALIDATION FAILED] Pattern preservation impossible
Recommend: [alternative approach]
```