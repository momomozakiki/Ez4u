# Skill & Rule Structure Examples

## Skill Folder Structure

This is the mandatory folder structure for any new skill.

```
.trae/
└── skills/
    └── your-skill-name/       ← Folder name: lowercase with hyphens
        ├── SKILL.md           ← Main skill definition with frontmatter
        ├── examples/          ← Optional: Purpose-specific example files
        │   ├── README.md
        │   ├── pattern-1.md
        │   └── pattern-2.md
        ├── templates/         ← Optional: Reusable code templates
        └── resources/         ← Optional: Supporting documentation or assets
```

### Example: `planner-architect` Skill Structure
```
.trae/
└── skills/
    └── planner-architect/
        ├── SKILL.md
        └── examples/
            ├── README.md
            ├── execution-templates.md
            ├── failure-scenarios.md
            ├── planning-patterns.md
            └── validation-examples.md
```

## Rule File Structure

Rules are single markdown files and do not have a folder structure.

```
.trae/
└── rules/
    └── your-rule-name.md      ← File name: lowercase with hyphens
```

### Example: `project_rules.md`
```
.trae/
└── rules/
    └── project_rules.md
```

## README.md for Examples

When splitting examples, always include a `README.md` inside the `examples` folder to explain the purpose of each file.

### Example: `examples/README.md`
```markdown
# Skill Examples

This directory contains purpose-specific examples for this skill.

## Available Examples

- **[pattern-1.md](pattern-1.md)** - Description of what this file contains.
- **[pattern-2.md](pattern-2.md)** - Description of what this file contains.

## Quick Reference

| Scenario | File | Purpose |
|---|---|---|
| Use Case 1 | `pattern-1.md` | Brief description |
| Use Case 2 | `pattern-2.md` | Brief description |
```