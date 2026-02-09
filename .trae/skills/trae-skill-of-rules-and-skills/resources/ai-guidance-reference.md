# AI Guidance Reference

## TRAE Documentation Links
- [Official TRAE Rules Documentation](https://docs.trae.com/rules) - Core rule system overview
- [TRAE Skills Framework](https://docs.trae.com/skills) - Skill creation and management
- [Frontmatter Specification](https://docs.trae.com/rules/frontmatter) - Complete frontmatter reference

## Quick Reference
- Decision flow summary: constraint → rules; pattern → skills; mixed → split.
- Structure requirements: `.trae/skills/<name>/SKILL.md` with `resources/`, `examples/`, `templates/` as needed.
- Verification: placement rationale, frontmatter correctness, folder/name match.

## Common Patterns
- Security constraints → Always apply rules
- UI component patterns → Skills with examples
- API endpoint conventions → Skills with templates
- Database schema rules → Specific file globs

## Naming Conventions
- Skill folders: lowercase-hyphen format (`my-skill-name`)
- Rule files: descriptive-hyphen format (`security-rules.md`)
- Template placeholders: `{{placeholder-name}}` format
