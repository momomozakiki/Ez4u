# frontend_dev PROTOCOL

## 1. Capabilities & Tech Stack
*   **Core**: **Next.js 14** (2023-10), **React 19** (2024-04), **TypeScript 5.x**
*   **Tools**: Tailwind CSS 3.4, Radix UI, React Hook Form, Redux Toolkit, Zod

### Framework Versions
| Framework/Library | Target Version | Release Date |
|:---|:---|:---|
| Next.js | v14.2.3 | 2024-04 |
| React | v19.0.0 | 2024-04 |
| TypeScript | v5.4.5 | 2024-04 |
| Tailwind CSS | v3.4.1 | 2023-12 |

## 2. Architectural Standards
*   **Design Pattern**: Component-based (Atomic Design or Feature-Sliced).
*   **Testing Standard**: Mandate unit tests for all core logic. Jest/Vitest for utilities, React Testing Library for components.

## 3. Strict Constraints (DO NOT VIOLATE)
*   **Frontend**: NO direct database calls. NO hardcoded secrets.
*   **General**: NO use of deprecated libraries.

## 4. Allowed Libraries (Allowlist)
*   `radix-ui`
*   `tailwindcss`
*   `react-hook-form`
*   `zod`
*   `@reduxjs/toolkit`
*   `lucide-react` (Icons)

## 5. Development Workflow
1.  Read Task -> 2. Verify Stack -> 3. Implement -> 4. Test -> 5. Review
