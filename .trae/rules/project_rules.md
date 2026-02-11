---
alwaysApply: true
---
# Project Rules: Design Preservation & Incremental Execution Protocol

## Hallucination Prevention (MANDATORY)
- NEVER modify existing code patterns without first analyzing current implementation
- WHEN uncertain about existing patterns → ABORT with:
  ```
  [UNCERTAIN] Cannot verify existing implementation pattern. 
  Please share current code snippet before requesting updates.
  ```

## Preservation-First Principle (NON-NEGOTIABLE)
- ALWAYS preserve existing architectural patterns, naming conventions, and styling approaches UNLESS explicitly instructed to refactor
- ALWAYS match existing code style (indentation, quotes, line breaks) in modifications
- NEVER replace working implementations with "better" alternatives without explicit user approval
- ALWAYS prefer additive changes (extending) over destructive changes (replacing)

## Impact Assessment Requirement
BEFORE any modification:
1. ANALYZE existing implementation pattern
2. IDENTIFY all dependencies/consumers of the target code
3. STATE impact assessment explicitly:
   ```
   [IMPACT ASSESSMENT] 
   • Current pattern: [describe existing approach]
   • Dependencies: [list components/files using this pattern]
   • Change scope: [minimal/additive/destructive]
   • Risk level: [low/medium/high]
   ```
4. FOR destructive changes (replacing patterns): REQUIRE explicit user confirmation:
   ```
   [DESTRUCTIVE CHANGE WARNING] This update replaces existing [pattern] used by [X components].
   Confirm: "Yes, replace existing pattern" to proceed.
   ```

## Mandatory Planning Enforcement (NON-NEGOTIABLE)
- ALWAYS generate explicit task list BEFORE executing ANY modification request
- NEVER execute monolithic changes (>3 file modifications in single response)
- ALWAYS structure responses as:
  ```
  [PLAN]
  1. [Task 1: atomic action]
  2. [Task 2: atomic action]
  ...
  
  [VALIDATION REQUIRED] Confirm plan before execution? (Reply "YES" to proceed step-by-step)
  ```

## Atomic Task Definition
- EACH task MUST modify ≤1 file OR ≤1 logical unit (e.g., "add prop to Button interface")
- EACH task MUST preserve existing patterns (styling, naming, composition)
- NEVER combine pattern changes with feature additions in same task

## Validation Protocol (MANDATORY BEFORE EACH TASK)
BEFORE executing task N:
1. AUDIT current state of target file/component
2. STATE expected outcome of task N
3. VERIFY no conflicts with existing patterns
4. REQUIRE explicit confirmation:
   ```
   [TASK 1 VALIDATION]
   • Target: src/components/Button.tsx
   • Current pattern: Tailwind primitives + clsx composition
   • Proposed change: Add `icon` prop preserving existing variant API
   • Risk: Low (additive only)
   Confirm "TASK 1" to proceed
   ```

## Rollback Requirement
- WHEN task validation fails → ABORT and revert any partial changes
- NEVER proceed to task N+1 if task N validation fails
- ALWAYS preserve working state between tasks

## Pattern Recognition Enforcement
- ALWAYS detect and adopt existing project patterns BEFORE generating new code:
  • Styling approach (Tailwind primitives vs custom CSS)
  • Component composition (props vs context vs state management)
  • File organization (feature-based vs type-based)
  • Naming conventions (PascalCase components, kebab-case files)
- WHEN multiple patterns exist → PRESERVE the pattern used in the target file/component
- NEVER introduce new patterns that conflict with existing conventions

## Verification Protocol (Post-Execution)
AFTER generating modifications:
- ALWAYS include before/after comparison showing ONLY changed lines
- ALWAYS preserve all existing functionality (no breaking changes without approval)
- ALWAYS maintain 100% of existing props/interfaces unless explicitly deprecated

## Pre-Modification Audit (MANDATORY BEFORE ANY CHANGE)
WHEN user requests update to existing code:
1. REQUEST current implementation if not provided:
   ```
   [AUDIT REQUIRED] Please share current implementation of [component/feature] before requesting updates.
   ```
2. IF implementation provided → ANALYZE and STATE findings:
   ```
   [PATTERN AUDIT]
   • Current styling: Tailwind primitives only (no custom CSS)
   • Composition: clsx for variants, base classes extracted
   • Props API: { children, variant, size, disabled }
   • Dependencies: Used by 8 components in src/features/
   ```
3. PROPOSE change WITH preservation rationale:
   ```
   [PRESERVATION PLAN]
   • Change: Add icon prop to Button component
   • Preservation: Maintain existing variant/size API; extend don't replace
   • Styling: Use existing icon utility classes from project
   • Risk: Low (additive change, no breaking changes)
   ```
4. FOR destructive changes → REQUIRE explicit approval BEFORE proceeding
