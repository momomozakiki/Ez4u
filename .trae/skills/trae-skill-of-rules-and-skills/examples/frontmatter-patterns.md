# Frontmatter Patterns

## Skill Frontmatter

The `SKILL.md` file for every skill **MUST** begin with the following frontmatter:

```yaml
---
name: "your-skill-name"
description: "A brief, one-sentence description of what this skill does."
---
```

### ✅ Valid Skill Frontmatter
```yaml
---
name: "planner-architect"
description: "Analyzes project architecture and generates detailed implementation plans."
---
```

### ❌ Invalid Skill Frontmatter

- **Missing `name`**:
  ```yaml
  ---
  description: "This is invalid because the name is missing."
  ---
  ```
- **Missing `description`**:
  ```yaml
  ---
  name: "invalid-skill"
  ---
  ```
- **Extra fields**:
  ```yaml
  ---
  name: "another-invalid-skill"
  description: "This is also invalid."
  author: "John Doe" # This field is not allowed
  ---
  ```

## Rule Frontmatter

Rule files **MUST** begin with frontmatter containing a `description` and may optionally include `alwaysApply` or `globs`.

```yaml
---
description: "A brief, one-sentence description of what this rule enforces."
alwaysApply: true # Optional: defaults to false
globs: # Optional: list of file patterns to apply the rule to
  - "src/**/*.ts"
---
```

### ✅ Valid Rule Frontmatter

- **With `alwaysApply`**:
  ```yaml
  ---
  description: "Enforces that all files have a license header."
  alwaysApply: true
  ---
  ```
- **With `globs`**:
  ```yaml
  ---
  description: "Checks for correct formatting in TypeScript files."
  globs:
    - "src/**/*.ts"
    - "tests/**/*.ts"
  ---
  ```
- **Minimal**:
  ```yaml
  ---
  description: "A rule that is applied manually."
  ---
  ```

### ❌ Invalid Rule Frontmatter

- **Missing `description`**:
  ```yaml
  ---
  alwaysApply: true
  ---
  ```
- **`name` field is not allowed**:
  ```yaml
  ---
  name: "my-rule" # Rules do not have names, only descriptions
  description: "This is an invalid rule."
  ---
  ```