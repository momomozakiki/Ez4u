# Seed Validation Protocol (CRITICAL)

## What is a "Seed"?
A minimal, verifiable unit of change that can be:
- ✅ Validated against existing patterns BEFORE full implementation
- ✅ Reverted instantly if validation fails
- ✅ Used as foundation for next task

## Seed Examples

| Request | BAD Seed (too big) | GOOD Seed (atomic) |
|---------|-------------------|-------------------|
| "Add icon to Button" | Full icon implementation with positioning logic | Add `icon?: ReactNode` prop type ONLY |
| "Make responsive" | Rewrite entire layout with media queries | Add single `sm:` breakpoint to ONE element |
| "Add dark mode" | Full theme switcher + CSS variables | Add `dark:` prefix to ONE utility class |

## Validation Questions for Every Seed
BEFORE executing seed task:
1. Does this seed preserve existing styling patterns? (Tailwind vs custom CSS)
2. Does this seed preserve existing composition patterns? (clsx usage)
3. Does this seed preserve existing API surface? (additive vs breaking)
4. Can this seed be reverted in <10 seconds if validation fails?
5. Does this seed affect ≤1 file OR ≤1 logical unit?

IF any answer = NO → REJECT seed and replan smaller task
