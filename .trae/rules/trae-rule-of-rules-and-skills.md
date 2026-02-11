alwaysApply: false
description: "Meta-rule for .trae guidance only; applies when creating/updating rules or skills, never to project code."
globs:
  - ".trae/rules/*.md"
  - ".trae/skills/*/SKILL.md"
  - ".trae/skills/*/examples/*.md"
  - ".trae/skills/*/templates/*.md"
  - ".trae/skills/*/resources/*.md"
---
# TRAE Rule: Guidance Categorization

## ✅ MUST DO
- Place constraints in rules using imperative language (ALWAYS/NEVER).
- Place patterns/examples/workflows in skills using descriptive language.
- Split mixed guidance: constraints to rules; patterns/examples to skills.
- Use skill folder structure: `.trae/skills/<skill-name>/SKILL.md`.
- ALWAYS create `examples/`, `templates/`, and `resources/` subfolders.
- Include frontmatter: `name` equals folder name, `description` with invoke triggers.
- Split skill examples by purpose: `styling-patterns.md`, `component-patterns.md`, `destructive-changes.md`, `verification-output.md`.
- Reference examples from SKILL.md using relative links to purpose-specific files.
 - Apply this rule ONLY to `.trae/rules/*.md` and `.trae/skills/**` guidance files, not to project code (e.g. `src/**`, `app/**`).

## ❌ PROHIBITED
- Place examples in rules.md.
- Place constraints in skills.md.
- Create skills as single files (must be folder + SKILL.md).
- Mismatch skill folder and `name` field.
- Omit frontmatter or use empty `description`.
