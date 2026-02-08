---
alwaysApply: false
description: Tailwind CSS Standards
---
# Tailwind CSS Standards

## ✅ MUST DO
- Exhaustively use built-in Tailwind utilities before any custom CSS (Primitive-First).
- Use Tailwind’s predefined utilities; extend centrally when truly necessary.
- Prefer theme tokens from config (e.g., bg-brand-primary) over hex literals.
- Use clsx (or cn) to compose className; keep JSX returns minimal.
- Extract complex class logic into constants before the return.
- Use object syntax in clsx for conditional classes.
- Use tailwind-merge when composing classes to deduplicate and resolve conflicts.
- Prefer project tokens defined in globals.css @theme (e.g., bg-background, text-muted-foreground).
- Allow inline style only for dynamic runtime values (e.g., computed widths).

## ❌ PROHIBITED
- Writing custom CSS in component <style> tags for cases covered by Tailwind.
- Concatenating className with template literals or + operator.
- Creating ad-hoc colors/spacing not declared in tailwind.config.js.
- Defining conditional class logic inline inside JSX elements.
- Using Client Components to inject non-deterministic styling that breaks SSR.
- Reinventing existing utilities (spacing, flex/grid, colors, responsive variants).

## 🔧 Configuration Rules
- Project design tokens live in globals.css @theme (Tailwind v4), or tailwind.config.js if present.
- Add variants/plugins centrally; do not define per-file utility hacks.
- Keep config changes additive and documented via theme.extend.
- When utilities are insufficient, extend via config with minimal, reusable tokens; avoid per-component CSS.

## 🧪 Validation Checklist
- Classes use project tokens (no raw hex unless temporary).
- clsx present; no string concatenation patterns.
- tailwind-merge used when combining dynamic/variant classes.
- No inline style except for necessary dynamic values.
- No local <style> blocks for general styling.
- No conditional class logic embedded in JSX.
- No ad-hoc utilities reinventing Tailwind primitives.

## 📌 Edge Cases
- If a required pattern is not expressible with existing utilities, add a token or variant centrally and document usage in the Tailwind skills file.

## 📌 Notes
- For animations not supported by Tailwind, define keyframes and utilities via config or a shared CSS module, not inline per component.
- Accessibility states (focus-visible, aria-*) should be handled via Tailwind variants or config extensions.
