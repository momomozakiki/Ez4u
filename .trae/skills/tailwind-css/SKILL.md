---
name: "tailwind-css"
description: "Provides Tailwind v4 patterns and component snippets. Invoke when building UI or composing classes."
---

# Tailwind Patterns

## Purpose
- Teach correct usage of Tailwind v4 with project tokens from globals.css @theme.
- Provide reusable patterns for layout, state variants, and components.

## Guidance
- Follow tailwind-css rules for constraints and validation.
- Compose className with clsx and dedupe via tailwind-merge.
- Extract conditional/variant logic before the JSX return.

## Common Utility Patterns
- Responsive grid: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`
- Flex layout: `flex items-center justify-between gap-2`
- Container: `max-w-7xl mx-auto p-6`
- Tokens: `bg-background text-foreground border-border text-muted-foreground`
- Ring/focus: `focus:outline-none focus:ring-2 focus:ring-ring`

## Components & Patterns
- See detailed examples under `examples/tailwind-examples.md` for buttons, cards, inputs, popover triggers, and layout sections.

## Notes
- Prefer project tokens from globals.css @theme over raw hex values.
- Use responsive prefixes (sm:, md:, lg:) and pseudo-class variants (hover:, focus:, disabled:).

## See Also
- Examples: `examples/tailwind-examples.md`
- Templates: `templates/tailwind-component-template.md`, `templates/tailwind-utility-patterns-template.md`
- Resources: `resources/tailwind-reference.md`
