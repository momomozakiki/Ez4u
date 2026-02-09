---
alwaysApply: false
description: "Applies when adding/modifying guidance; enforces placement: constraints → rules, patterns/examples/workflows → skills."
---
# TRAE Rule: Guidance Categorization

## ✅ MUST DO
- Place constraints in rules using imperative language (ALWAYS/NEVER).
- Place patterns/examples/workflows in skills using descriptive language.
- Split mixed guidance: constraints to rules; patterns/examples to skills.
- Use skill folder structure: `.trae/skills/<skill-name>/SKILL.md`.
- Include frontmatter: `name` equals folder name, `description` with invoke triggers.

## ❌ PROHIBITED
- Place examples in rules.md.
- Place constraints in skills.md.
- Create skills as single files (must be folder + SKILL.md).
- Mismatch skill folder and `name` field.
- Omit frontmatter or use empty `description`.