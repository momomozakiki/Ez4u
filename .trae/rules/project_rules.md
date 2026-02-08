# Project Rules: AI Guidance Categorization Protocol

## Hallucination Prevention Protocol (MANDATORY)

### Source Verification Before Categorization
- BEFORE categorizing ANY guidance request, ALWAYS verify:
  • The feature/API exists in official documentation
  • Version compatibility with project dependencies (package.json/requirements.txt)
- WHEN confidence <90% → ABORT categorization and notify using the standardized message defined in skills templates.

## Meta-Rule: Guidance Categorization Decision Flow

### Purpose
This rule governs HOW the AI decides where to place guidance content.
VIOLATION = mis-categorized guidance that breaks project consistency.

### Decision Flow (Execute in Strict Order)

#### STEP 1: Is this a NON-NEGOTIABLE CONSTRAINT?
Definition: Violation causes security risk, architectural breakage, or critical failure.
Constraints include (non-exhaustive):
- NEVER use eval()
- ALWAYS validate user input before processing
- NEVER hardcode secrets in source code
- ALWAYS use clsx for Tailwind className composition

→ IF YES: Categorize as RULE
- Place in .trae/rules/project_rules.md
- Use imperative language: ALWAYS... / NEVER...
- NO code examples allowed (dilutes enforcement)

→ IF NO: Proceed to STEP 2

#### STEP 2: Is this a PATTERN, EXAMPLE, or WORKFLOW?
Definition: Shows HOW to implement something correctly using existing tools.
Examples of patterns:
- Button component snippet with variants
- API call pattern with error handling
- Deployment workflow steps
- Responsive layout example using Tailwind grid

→ IF YES: Categorize as SKILL
- Place in .trae/skills/<skill-name>/SKILL.md (folder structure required)
- Use descriptive language + executable code snippets
- Include official documentation references

→ IF NO: Proceed to STEP 3

#### STEP 3: Is this MIXED (constraint + pattern)?
→ IF YES: SPLIT content
- Constraint portion → .trae/rules/project_rules.md (imperative)
- Pattern/example portion → .trae/skills/<skill-name>/SKILL.md (descriptive)

→ IF NO: ABORT categorization and notify using the standardized message defined in skills templates.

### Mandatory Verification Before Output
BEFORE outputting any guidance content:
- STATE categorization rationale explicitly using the `[CATEGORIZATION]` tag.
- CONFIRM rules contain ONLY constraints (no examples)
- CONFIRM skills contain ONLY patterns/examples (no mandates)

### Prohibited Actions (Violations)
- NEVER place examples in rules.md (dilutes enforcement authority)
- NEVER place constraints in skills.md (makes them ignorable)
- NEVER output guidance without stating [CATEGORIZATION] rationale
- NEVER categorize guidance without completing Phase 0 verification

## Why This Belongs in rules.md (Not skills.md)

| Question | Answer |
|----------|--------|
| Is this a constraint on AI behavior? | YES – It mandates HOW the AI must think before acting |
| Does violation cause project harm? | YES – Mis-categorized guidance breaks consistency |
| Is it non-negotiable? | YES – No exceptions allowed (must always verify first) |
| Does it teach "how to do something"? | NO – It doesn't show implementation patterns |
| Can it be ignored safely? | NO – Ignoring it causes systemic categorization errors |

→ Conclusion: This is a RULE, not a skill. It belongs in .trae/rules/project_rules.md.

## Critical Fixes Applied to Your Draft

| Your Draft Issue | Fixed In Meta-Rule | Why It Matters |
|------------------|-------------------|----------------|
| YAML frontmatter in rules file | REMOVED entirely | Rules must not include name/description frontmatter |
| Decision flow without verification | Added Phase 0: Source Verification | Prevents categorizing hallucinated guidance |
| Ambiguous "constraint" definition | Added explicit definition + examples | Prevents misclassification of weak preferences |
| No uncertainty signaling | Added [UNCERTAIN] abort protocol | Stops broken guidance before categorization |
| Examples/templates in rules content | REMOVED all examples | Rules contain ONLY constraints (no patterns) |
| Skill folder structure details in rules | Kept as placement requirements only | Rules state WHAT; skills show HOW (separation) |

## Testing Note
- Tests and illustrative responses belong in skill examples/templates, not in rules.
