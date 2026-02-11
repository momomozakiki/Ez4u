---
name: "<skill-name>"
description: "<does X. Invoke when Y or user asks Z>"
---

# <Skill Title>

## Purpose
- <what this skill teaches>

## When to Invoke
- <trigger phrases or situations>

## Required Structure
- Folder: `.trae/skills/<skill-name>/`
- File: `.trae/skills/<skill-name>/SKILL.md`
- Subfolders: `examples/`, `templates/`, `resources/`
- Examples split by purpose: `styling-patterns.md`, `component-patterns.md`, `destructive-changes.md`, `verification-output.md`

## Guidance
- <how to apply patterns>

## Examples
- Split examples by purpose in `examples/` folder:
  - `styling-patterns.md` - Pattern detection examples
  - `component-patterns.md` - API and composition examples
  - `destructive-changes.md` - Breaking change warnings
  - `verification-output.md` - User message templates
- Reference examples using relative links: `[styling examples](examples/styling-patterns.md)`

## Templates
- Put scaffolds with `{{placeholders}}` in `templates/`.

## Resources
- Put supporting notes, checklists, and references in `resources/`.
