---
name: "design-preserver"
description: "Analyzes existing code patterns before modifications. Invoke when user requests updates to existing components/features."
---
# Design Preservation Skill

## Purpose
Prevent breaking changes by recognizing and preserving existing project patterns during updates.

## When to Invoke
- User requests "update", "modify", "change", or "improve" existing code
- User shares existing code snippet for modification
- Request implies refactoring without explicit "refactor" keyword

## Pattern Recognition Checklist

### 1. Styling Pattern Detection
Check existing component for:
✅ Tailwind primitives only → Preserve primitive-first approach
✅ Custom CSS classes → Preserve custom approach; don't replace with Tailwind
✅ clsx usage → Continue using clsx for class composition
✅ Inline styles → Only replace if explicitly requested

### 2. Component Pattern Detection
Check for:
✅ Props-based configuration → Preserve prop API; extend don't replace
✅ Context/state management → Preserve data flow pattern
✅ Render composition → Match existing pattern
✅ Error boundaries/loading states → Preserve existing UX patterns

### 3. File Structure Detection
Check project for:
✅ Feature-based organization → Add new files to same structure
✅ Type-based organization → Match existing taxonomy
✅ Naming conventions → Match PascalCase/kebab-case patterns

## Safe Modification Approach
1. **ALWAYS prefer additive changes** (extending existing functionality)
2. **NEVER replace working patterns** without explicit user approval
3. **REQUIRE confirmation** for destructive changes
4. **VERIFY preservation** after modifications

## Resources
- [Styling Patterns](./examples/styling-patterns.md) - How to detect and preserve Tailwind vs custom CSS
- [Component Patterns](./examples/component-patterns.md) - Props API, composition, and naming conventions
- [Destructive Changes](./examples/destructive-changes.md) - When changes must break patterns and approval requirements
- [Verification Output](./examples/verification-output.md) - Copy-paste templates for user messages
- [Preservation Templates](./templates/preservation-plan-template.md) - Templates for documenting changes
- [Common Patterns Reference](./resources/common-patterns.md) - Reference for common project patterns
