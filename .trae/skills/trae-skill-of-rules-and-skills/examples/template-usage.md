# Template Usage Examples

## Skill Template (`templates/skill-template.md`)

When creating a new skill, use the `skill-template.md` as a starting point.

```markdown
---
name: "{{skill-name}}"
description: "{{description}}"
---

# {{Skill Name}}

## Purpose
- {{purpose-1}}
- {{purpose-2}}

## Guidance
- {{guidance-1}}
- {{guidance-2}}

## Core Patterns
- **Pattern 1**: {{pattern-1-description}}
  ```
  {{pattern-1-code-example}}
  ```
- **Pattern 2**: {{pattern-2-description}}
  ```
  {{pattern-2-code-example}}
  ```

## Resources
- [Example 1](./examples/example-1.md)
- [Example 2](./examples/example-2.md)
```

### How to Use
1. Copy `templates/skill-template.md` to a new `SKILL.md` file.
2. Replace all `{{...}}` placeholders with your skill's specific information.
3. Create the corresponding example files in the `examples/` directory.

## Rule Template (`templates/rules-template.md`)

When creating a new rule, use the `rules-template.md` as a starting point.

```markdown
---
description: "{{description}}"
alwaysApply: {{alwaysApply | default: false}}
globs:
  - "{{glob-1}}"
---

# {{Rule Name}}

## Constraint
{{constraint-description}}

## Rationale
{{rationale}}

## Examples

### ✅ Correct Usage
```
{{correct-usage-example}}
```

### ❌ Incorrect Usage
```
{{incorrect-usage-example}}
```
```

### How to Use
1. Copy `templates/rules-template.md` to a new `.md` file in the `rules/` directory.
2. Replace all `{{...}}` placeholders with your rule's specific information.
3. Set `alwaysApply` to `true` or `false`.
4. Define the `globs` if the rule is not global.