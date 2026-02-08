---
name: "trae-skill-of-rules-and-skills"
description: "Categorizes guidance into rules vs skills. Invoke when adding/modifying guidance or deciding placement."
---

# TRAE Skills: Guidance Categorization

## Purpose
- Apply categorization protocol to place content in rules or skills.
- Enforce correct skill folder structure and frontmatter.

## When to Invoke
- Before creating or updating `.trae/rules/*.md` or `.trae/skills/*/SKILL.md`.
- When deciding where new guidance belongs (rule vs skill).

## Decision Flow
1. Non‑negotiable constraint → place in rules (ALWAYS/NEVER, no examples).
2. Pattern/example/workflow → place in skills (descriptive + code).
3. Mixed content → split between rules and skills.
4. Neither → abort with `[GUIDANCE UNCATEGORIZABLE]` notice.

## Structure Enforcement
- Path: `.trae/skills/<skill-name>/SKILL.md`
- Frontmatter must include:
  - `name`: equals `<skill-name>`
  - `description`: what the skill does AND when to invoke
- Allowed subfolders: `resources/`, `examples/`, `templates/`
- Keep all skill assets inside the skill directory.
 - Keep SKILL.md concise (purpose, guidance, checklist). Place extended code samples in `examples/` and scaffolds in `templates/`.

## Examples (Categorization Rationale)
```
[CATEGORIZATION] Placing in rules.md because this is a non‑negotiable security constraint.
[CATEGORIZATION] Placing in skills.md because this demonstrates a reusable implementation pattern.
```

## Verification Checklist
- Placement matches decision flow (rules vs skills).
- `.trae/skills/<name>/SKILL.md` exists; `name` equals folder.
- Description includes explicit invoke triggers (<200 chars).
- Subfolders exist if referenced: `resources/`, `examples/`, `templates/`.

## Rule Frontmatter Setup
- Always Apply:
```yaml
---
alwaysApply: true
---
```
- Apply Intelligently:
```yaml
---
alwaysApply: false
description: "Applies when editing Tailwind-styled React/Next components"
---
```
- Apply to Specific Files:
```yaml
---
alwaysApply: false
globs:
  - "src/**/*.tsx"
  - "styles/**/*.css"
---
```
- Checklist:
- Confirm `alwaysApply` matches the intended mode.
- Provide concise `description` for intelligent mode.
- Define `globs` for specific-file mode.
