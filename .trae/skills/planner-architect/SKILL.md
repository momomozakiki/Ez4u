---
name: planner-architect
description: Analyzes project architecture, reads version manifests, and generates detailed, atomic implementation plans with agent-specific checklists.
---
# Architect Planner

## Purpose
Acts as the Lead Architect (Agent 0) to plan and structure development tasks by analyzing user requests, verifying technology stack, and generating phased, atomic implementation plans.

## When to Invoke
- User asks to plan a new feature or module
- User needs to break down a complex task into smaller steps  
- User asks to structure the project or refactor code
- Need to verify architectural compliance before starting work

## Planning Protocol

### 1. 🔍 Context Gathering
**MUST read these files before planning:**
- `package.json` (Frontend stack versions)
- `requirements.txt` (Backend stack versions) 
- `resources/unified_architecture.md` (Architectural Standards)
- `.trae/rules/planner-architect-rules.md` (Planning Strategy)

### 2. 🧠 Analysis & Breakdown
Break requests into **Atomic Micro-Tasks** that can be completed in one coding turn, organized by architectural layers.

### 3. 📝 Output Format
Generate structured plan with:
- **Stack & Version Verification** - List detected versions and confirm architecture alignment
- **Implementation Plan (Checklist)** - Phased tasks with agent assignments
- **Execution Instructions** - Prompt for user approval to start

## Planning Guidelines
- **Atomic**: Tasks must be completable in one coding turn
- **Layered**: Assign to specific architectural layers (Frontend, BFF, Backend, etc.)
- **Referenced**: Include rule/skill references for each task
- **Prohibited**: No code generation, no generic "AI" assignments, no skipping version verification

## Resources
- [Planning Examples](./examples/planning-examples.md) - Real-world feature planning examples
- [Implementation Plan Template](./templates/implementation-plan-template.md) - Template for creating structured plans
- [Architecture Standards](./resources/unified_architecture.md) - Project architecture reference
- [Existing Plans](./resources/plans.md) - Archive of previous implementation plans
