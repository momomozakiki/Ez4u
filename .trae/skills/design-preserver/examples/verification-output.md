# Verification Output Templates

## Successful Preservation Output

```
[PRESERVATION VERIFIED]
✓ Existing pattern preserved: Tailwind primitives with hover states
✓ Naming conventions matched: PascalCase components, kebab-case files
✓ Dependencies unaffected: 0 breaking changes
✓ Additive change only: New 'icon' prop added, existing API preserved
```

## Pattern Audit Output

```
[PATTERN AUDIT]
• Component: Button
• Styling: Tailwind primitives only (no custom CSS)
• Composition: clsx with base/variant/size classes extracted
• Props: { children, variant, size, disabled }
• Dependencies: 12 components in src/features/
• Convention: PascalCase components, kebab-case files
```

## Impact Assessment Output

```
[IMPACT ASSESSMENT]
• Current pattern: Tailwind utilities with clsx composition
• Dependencies: 8 components in src/components/
• Change scope: Additive (new icon prop)
• Risk level: Low (no breaking changes)
```

## Task Validation Output

```
[TASK 1 VALIDATION]
• Target: src/components/Button/types.ts
• Current: interface ButtonProps { children: ReactNode; variant?: string; ... }
• Proposed: Add `icon?: ReactNode; iconPosition?: 'left' | 'right'`
• Pattern preservation: ✅ Additive only (no breaking changes)
• Risk: Low
Confirm "TASK 1" to proceed
```

## Task Completion Output

```
[TASK COMPLETE]
✓ Pattern preserved: Tailwind primitives + clsx composition
✓ Additive change only: new prop added, existing API intact
✓ Dependencies unaffected: 0 breaking changes
✓ Next task ready: TASK 2 (extend variantClasses)
Confirm "TASK 2" to proceed OR "ABORT" to stop
```

## Rollback Output

```
[ROLLBACK]
• Reverted task 3 changes to src/components/Button/utils.ts
• Restored working state from task 2
• Awaiting replan for icon positioning approach
```

## Template Variables

Replace these placeholders with actual values:
- `{component}` - Component name
- `{pattern}` - Pattern type (Tailwind, custom CSS, etc.)
- `{dependencies}` - Number of affected components
- `{file_path}` - Target file path
- `{change_description}` - Specific change being made
- `{risk_level}` - Low/Medium/High assessment