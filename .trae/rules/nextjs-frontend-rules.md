---
name: nextjs-frontend-rules
description: Next.js Frontend (React Components) coding standards for AI
---

# Next.js Frontend Rules

## Framework Versions
- Next.js ^16.1.6 (App Router only)
- React ^19.2.3
- TypeScript ^5.9.3 (strict mode)
- Zustand ^5.0.0, TanStack Query ^5.48.2
- React Hook Form ^7.52.1, Zod ^3.23.8
- Axios ^1.7.2, Tailwind CSS ^4.1.18

## Testing
- Jest/Vitest for unit tests
- Playwright for E2E
- React Testing Library for components

## ✅ MUST DO
1. Use `'use client'` for interactive components
2. Fetch initial data from Backend (L3) for SSR
3. Call API Routes (L2) for user actions
4. Implement loading states and error boundaries
5. Use TypeScript strict typing (no `any`)
6. Include Service Token headers for SSR calls

## ❌ PROHIBITED
1. Direct Backend API calls from Client Components
2. Direct database access (Prisma/Drizzle)
3. `pages/` directory (use `app/` only)
4. Non-public env vars in browser code
5. Business logic in components
6. `any` TypeScript types
7. Browser APIs in Server Components
8. Service tokens in client bundle