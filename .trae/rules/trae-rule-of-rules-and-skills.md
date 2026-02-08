# Project Rules: AI Guidance Categorization

## ✅ MUST DO
- Apply the decision flow before generating or modifying guidance.
- Place non-negotiable constraints in rules using imperative language (ALWAYS/NEVER).
- Place patterns, examples, and workflows in skills using descriptive language.
- Split mixed guidance: constraints to rules; patterns/examples to skills.
- Confirm placement matches the decision flow and state categorization rationale.
 - Enforce SKILL structure: `.trae/skills/<skill-name>/SKILL.md` with required frontmatter.
 - Ensure `description` includes what the skill does AND when to invoke it (trigger conditions).
 - Use allowed subfolders under each skill: `resources/`, `examples/`, `templates/` for supplementary content.
 - Keep skill content self-contained; reference files must reside within the skill folder.

## Rule Application Modes (Constraints)
- ALWAYS configure project rule application mode explicitly via frontmatter when supported.
- ALWAYS set `alwaysApply: true` for “Always Apply”.
- ALWAYS set `alwaysApply: false` and provide a concise `description` for “Apply Intelligently”.
- ALWAYS set `alwaysApply: false` and define `globs` for “Apply to Specific Files”.
- NEVER leave `alwaysApply` unspecified when frontmatter is used.

## ❌ PROHIBITED
- NEVER place examples in rules.md (dilutes enforcement).
- NEVER place constraints in skills.md (makes them ignorable).
- Outputting guidance without categorization verification.
 - Creating skills as single files (e.g., `.trae/skills/<name>.md`) instead of folder + `SKILL.md`.
 - Mismatching skill folder and `name` field (they must be identical).
 - Placing skill assets outside the skill folder (e.g., in project root or other skills).
 - Omitting frontmatter or using empty `description` without invoke triggers.

## Decision Flow
1. Ask: Is this a non-negotiable constraint?
   - Yes → Put in rules with imperative language.
   - No → Go to step 2.
2. Ask: Is this a pattern, example, or workflow?
   - Yes → Put in skills with descriptive language and code snippets.
   - No → Go to step 3.
3. Ask: Is it both constraint and pattern?
   - Yes → Split: constraint to rules; pattern/example to skills.
   - No → Abort and notify using the standardized message defined in skills templates.

## Verification
- Before output, ensure placement matches the decision flow.
- Always include a brief rationale for the chosen category and file.
 - Validate SKILL path and naming:
   - Directory exists: `.trae/skills/<skill-name>/`
   - File exists: `SKILL.md` inside the directory
   - Optional folders: `resources/`, `examples/`, `templates/` (if referenced)
   - Frontmatter present with:
     - `name`: must equal `<skill-name>`
     - `description`: must state what the skill does AND when to invoke (explicit trigger cues), under ~200 chars
   - `name` equals `<skill-name>`
   - `description` contains explicit invoke cues ("Invoke when ..."), under ~200 chars
 - Confirm rules contain only constraints; skills contain patterns/examples.
