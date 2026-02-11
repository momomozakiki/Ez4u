# Atomic Task Templates

## ✅ ADDITIVE TASK (Preferred)
Use this template for extending functionality without breaking existing patterns.

```
TASK: Add {{feature}} to {{component}} preserving existing {{pattern}}
• Target file: {{file_path}}
• Current API: {{current_api_description}}
• Proposed change: {{proposed_change_description}}
• Pattern preserved: ✅ {{preserved_patterns}}
• Breaking changes: None
```

## ⚠️ REPLACEMENT TASK (Requires Approval)
Use this template when replacing patterns is unavoidable.

```
TASK: Replace {{old_pattern}} with {{new_pattern}} in {{component}}
• Target file: {{file_path}}
• Current pattern: {{current_pattern_description}}
• Proposed replacement: {{proposed_replacement_description}}
• Dependencies affected: {{list_of_dependencies}}
• Breaking changes: {{list_of_breaking_changes}}
⚠️ Requires explicit "CONFIRM REPLACEMENT" before proceeding
```

## PLAN STRUCTURE
```
[PLAN]
1. {{Task 1: atomic action}}
2. {{Task 2: atomic action}}
...

[VALIDATION REQUIRED] Confirm plan before execution? (Reply "YES" to proceed step-by-step)
```
