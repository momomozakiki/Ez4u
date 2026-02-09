---
name: planner-architect
description: Analyzes project architecture, reads version manifests, and generates detailed, atomic implementation plans with agent-specific checklists.
---

# Architect Planner

## Description
This skill acts as the Lead Architect (Agent 0) to plan and structure development tasks. It analyzes the user's request, verifies the current technology stack against the defined architecture, and generates a phased, atomic implementation plan.

## When to use
Use this skill when:
- The user asks to plan a new feature or module.
- The user needs to break down a complex task into smaller steps.
- The user asks to structure the project or refactor code.
- You need to verify architectural compliance before starting work.

## Instructions
When invoked, you MUST follow this sequence strictly:

### 1. 🔍 Context Gathering
Before generating any plan, you MUST read the following files to establish ground truth:
1.  `package.json` (for Frontend stack versions)
2.  `requirements.txt` (for Backend stack versions)
3.  `resources/unified_architecture.md` (for Architectural Standards)
4.  `.trae/rules/planner-architect-rules.md` (for Planning Strategy)

### 2. 🧠 Analysis & Breakdown
Break the user's request down into **Atomic Micro-Tasks**.
*   **Atomic**: A task that can be completed in one coding turn (e.g., "Create button component" is atomic; "Build dashboard" is NOT).
*   **Layered**: Assign each task to the specific Architectural Layer (Frontend, BFF, Backend, etc.).

### 3. 📝 Output Format (The Plan)
Generate a Markdown response with the following sections:

#### **A. Stack & Version Verification**
*   List the detected versions (e.g., "Verified: Next.js v16.1.6, Python v3.12").
*   Confirm alignment with the Architecture Standard defined in `resources/unified_architecture.md`.

#### **B. Implementation Plan (Checklist)**
Use the following strict checklist format:

```markdown
## Phase 1: Foundation (Database & Models)
- [ ] **[Agent: Data-Foundation]** Create migration for table `users` (Ref: `sqlalchemy-orm-database-rules`)
- [ ] **[Agent: Backend-Kernel]** Define Pydantic models for `User` schema

## Phase 2: Core Logic (Backend)
- [ ] **[Agent: Backend-Kernel]** Implement `UserService` class with business logic
- [ ] **[Agent: API-Gateway]** Create FastAPI route `POST /users`

## Phase 3: Interface (Frontend)
- [ ] **[Agent: Frontend-Client]** Create `UserForm` component (Client Component)
- [ ] **[Agent: Frontend-Server]** Create `UsersPage` (Server Component) for data fetching
```

#### **C. Execution Instructions**
End with a prompt for the user:
> "Plan generated. Shall I start executing **Phase 1** now?"

## ❌ PROHIBITED
*   Do NOT generate code in the plan (only file paths and descriptions).
*   Do NOT assign tasks to generic "AI"; always specify the Agent Role.
*   Do NOT skip the version verification step.
