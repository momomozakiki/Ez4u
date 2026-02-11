# Planning Pattern Examples

## Monolithic vs Incremental Planning

### ❌ Monolithic Execution (Anti-Pattern)
**User**: "Add icon support to Button component"

**AI Response** (Breaking):
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

### ✅ Incremental Planning (Correct Pattern)
**User**: "Add icon support to Button component"

**AI Response** (Preserving):
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

## Different Planning Scenarios

### Feature Addition Pattern
```
[PLAN]
1. Audit existing pattern (styling, props, composition)
2. Add new prop/interface definitions
3. Extend existing utility functions
4. Modify component render logic
5. Update tests/stories
6. Verify backward compatibility
```

### Bug Fix Pattern
```
[PLAN]
1. Reproduce the issue
2. Identify root cause
3. Create minimal fix
4. Add regression test
5. Verify fix doesn't break other functionality
6. Document the change
```

### Refactoring Pattern
```
[PLAN]
1. Document current implementation
2. Identify improvement opportunities
3. Plan incremental migration steps
4. Create backward compatibility layer
5. Migrate consumers incrementally
6. Remove deprecated code
```

## Planning Decision Matrix

| Request Type | Planning Approach | Validation Points |
|-------------|------------------|-------------------|
| Add feature | Incremental extension | Pattern preservation |
| Fix bug | Minimal targeted fix | Regression prevention |
| Refactor | Migration strategy | Compatibility maintenance |
| Update dependency | Compatibility check | Breaking change assessment |
| Performance optimization | Benchmark-driven | Measurement verification |