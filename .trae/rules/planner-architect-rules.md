---
alwaysApply: true
---

# Planner Architect Rules

## ✅ MUST DO
1. **Inherit Context**: Always read the existing plan (if any) before generating a new one.
2. **Evolution over Revolution**:
    *   **Expand**: Add granularity to existing steps (e.g., break "Build Login" into "UI", "API", "Auth").
    *   **Refine**: Clarify descriptions or add technical references.
    *   **Adjust**: specific errors or outdated steps.
3. **Preserve Structure**: Maintain the high-level Phases (Foundation -> Core Logic -> Interface) unless architectural requirements fundamentally change.
4. **Traceability**: Link new detailed tasks back to their parent items in the General Plan.

## ❌ PROHIBITED
1. **Total Rewrites**: Do not discard the existing plan to create a "better" one from scratch.
2. **Context Amnesia**: Do not ignore previously completed or in-progress steps.
3. **Scope Creep**: Do not add phases or major goals unrelated to the original General Plan without explicit user confirmation.
