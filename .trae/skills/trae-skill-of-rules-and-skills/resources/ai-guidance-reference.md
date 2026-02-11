# AI Guidance Reference

## Local References (Verified)
- Rule: `.trae/rules/trae-rule-of-rules-and-skills.md`
- Skill: `.trae/skills/trae-skill-of-rules-and-skills/SKILL.md`

## Quick Reference
- Decision flow summary: constraint → rules; pattern/workflow → skills; mixed → split.
- Skill structure: `.trae/skills/<name>/SKILL.md` and create `examples/`, `templates/`, `resources/`.
- Verify: placement rationale, frontmatter correctness, folder/name match.

## Decision Checklist
- If it contains ALWAYS/NEVER and is enforceable, put it in a rule.
- If it teaches how to do something (patterns, examples, workflows), put it in a skill.
- If it contains both enforcement + example code, split it across rule + skill.
- If it depends on project context, cite the project file(s) it comes from.

## Common Patterns
- Security constraints → Always apply rules
- UI component patterns → Skills with examples
- API endpoint conventions → Skills with templates
- Database schema rules → Specific file globs

## Rule Shape
Use rules for constraints and prohibitions.

- Frontmatter (rule): keep it minimal (see existing `.trae/rules/*.md` files).
- Body: prefer `## ✅ MUST DO` and `## ❌ PROHIBITED` sections.

## Skill Shape
Use skills for reusable guidance.

- Folder name: lowercase-hyphen (example: `my-skill-name`)
- Required layout:
  - `.trae/skills/<name>/SKILL.md`
  - `.trae/skills/<name>/examples/`
  - `.trae/skills/<name>/templates/`
  - `.trae/skills/<name>/resources/`

## Naming Conventions
- Skill folders: lowercase-hyphen format (`my-skill-name`)
- Rule files: descriptive-hyphen format (`security-rules.md`)
- Template placeholders: `{{placeholder-name}}` format
