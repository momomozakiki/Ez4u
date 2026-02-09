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
- Required subfolders and their purposes:
  - `examples/` - Reference snippets demonstrating the skill in action (runnable code samples, usage patterns)
  - `templates/` - Scaffolds with `{{placeholders}}` for quick creation (standardized formats with fill-in fields)
  - `resources/` - Supporting assets and reference materials (external references, documentation)
- Keep all skill assets inside the skill directory.
- Keep SKILL.md concise (purpose, guidance, checklist). Place extended code samples in `examples/` and scaffolds in `templates/`.

## Examples (Categorization Rationale)
```
[CATEGORIZATION] Placing in rules.md because this is a non‑negotiable security constraint.
[CATEGORIZATION] Placing in skills.md because this demonstrates a reusable implementation pattern.
```

## Template Usage Instructions

### Using Skill Templates
1. Copy `templates/skill-template.md` to your new skill directory
2. Replace `<skill-name>` with your actual skill folder name (lowercase-hyphen format)
3. Replace `<does X. Invoke when Y or user asks Z>` with specific invoke triggers
4. Fill in `<Skill Title>`, `<what this skill teaches>`, and `<how to apply patterns>`
5. Add runnable code examples in the Examples section

### Using Rule Templates  
1. Copy `templates/rules-template.md` to your new rule file
2. Add appropriate frontmatter (see Rule Frontmatter Setup section above)
3. Replace constraint placeholders with your specific rules
4. Ensure MUST DO/PROHIBITED sections are actionable and specific

### Template Checklist
- Templates contain `{{placeholders}}` for easy identification
- Skill templates include required frontmatter fields
- Rule templates follow the MUST DO/PROHIBITED format
- All placeholders are replaced before finalizing

## Rule Frontmatter Setup

### Three Application Modes

1. **Always Apply Mode** - Rule applies to all files, all the time
```yaml
---
alwaysApply: true
---
```
**Use when**: Universal constraints like security, formatting, or core architectural rules.

2. **Apply Intelligently Mode** - Rule applies based on context/description matching
```yaml
---
alwaysApply: false
description: "Applies when editing Tailwind-styled React/Next components"
---
```
**Use when**: Domain-specific guidance that should trigger contextually.

3. **Apply to Specific Files Mode** - Rule applies only to matched file patterns
```yaml
---
alwaysApply: false
globs:
  - "src/**/*.tsx"
  - "styles/**/*.css"
---
```
**Use when**: File-type or location-specific rules.

### Frontmatter Checklist
- Confirm `alwaysApply` matches the intended mode (true/false)
- For intelligent mode: Provide concise `description` with invoke triggers (<200 chars)
- For specific-files mode: Define `globs` with proper file patterns
- Never use both `description` and `globs` together
