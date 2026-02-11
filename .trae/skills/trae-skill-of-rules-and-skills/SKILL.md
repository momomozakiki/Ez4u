name: "trae-skill-of-rules-and-skills"
description: "Meta-skill for .trae guidance only. Invoke when creating/updating rules or skills, never for project code."
---

# TRAE Skills: Guidance Categorization

## Purpose
- Apply categorization protocol to place content in rules or skills.
- Enforce correct skill folder structure and frontmatter.
- Act ONLY on `.trae/rules/**` and `.trae/skills/**` guidance files, not on project code paths like `src/**` or `app/**`.

## When to Invoke
- Before creating or updating `.trae/rules/*.md` or any files under `.trae/skills/**`.
- When deciding where new guidance belongs (rule vs skill).
- NEVER invoke this skill to make changes directly in application code (e.g. `src/**`, `app/**`).

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
- Required subfolders and their purposes:
  - `examples/` - Reference snippets demonstrating the skill in action (runnable code samples, usage patterns)
  - `templates/` - Scaffolds with `{{placeholders}}` for quick creation (standardized formats with fill-in fields)
  - `resources/` - Supporting assets and reference materials (external references, documentation)
- Split skill examples by purpose for clarity:
  - `styling-patterns.md` - Pattern detection for different styling approaches
  - `component-patterns.md` - Component composition and API patterns
  - `destructive-changes.md` - When changes must break patterns and approval requirements
  - `verification-output.md` - Copy-paste templates for user-facing messages
- Reference examples from SKILL.md using relative links to purpose-specific files.
- Keep all skill assets inside the skill directory.
- Keep SKILL.md concise (purpose, guidance, checklist). Place extended code samples in `examples/` and scaffolds in `templates/`.

## Resources
- [Categorization Examples](./examples/categorization-examples.md) - How to decide between creating a rule or a skill.
- [Structure Examples](./examples/structure-examples.md) - The mandatory folder and file structure for skills and rules.
- [Frontmatter Patterns](./examples/frontmatter-patterns.md) - Correct and incorrect frontmatter for skills and rules.
- [Template Usage](./examples/template-usage.md) - How to use the provided templates to create new skills and rules.
- [AI Guidance Reference](./resources/ai-guidance-reference.md) - Deeper reference on AI behavior.
- [Rule Template](./templates/rules-template.md) - Template for creating new rules.
- [Skill Template](./templates/skill-template.md) - Template for creating new skills.
