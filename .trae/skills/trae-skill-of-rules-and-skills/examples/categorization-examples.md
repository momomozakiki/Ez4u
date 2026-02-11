# Categorization Examples

Use these examples when deciding whether guidance belongs in a rule or a skill.

## Rule Categorization (Constraints)
Put non-negotiable constraints in a rule.

```
[CATEGORIZATION] Rule: non-negotiable constraint (enforced behavior).
[RULE EXAMPLE]
## ✅ MUST DO
- ALWAYS validate input payloads before persisting.

## ❌ PROHIBITED
- NEVER log secrets or tokens.
```

## Skill Categorization (Patterns / Workflows)
Put reusable patterns, examples, templates, and step-by-step workflows in a skill.

```
[CATEGORIZATION] Skill: reusable pattern/workflow with examples and templates.
[SKILL EXAMPLE]
---
name: "request-validation"
description: "Shows request validation patterns. Invoke when adding API validation."
---

## Guidance
- Use a schema to validate and normalize input.

## Examples
- Minimal schema usage example (kept in examples/).
```

## Mixed Guidance (Split It)
If a single paragraph mixes constraints + patterns, split it across rule + skill.

```
[INPUT]
"Always validate requests with a Zod schema; here is the code snippet you should copy."

[SPLIT RESULT]
Rule:
- ALWAYS validate requests.

Skill:
- Provide a Zod validation pattern + copyable snippet in examples/.
```

## Misplacements (Avoid)
```
[BAD] Putting copy-paste snippets inside rules.md
[BAD] Putting "ALWAYS/NEVER" constraints inside SKILL.md
```
