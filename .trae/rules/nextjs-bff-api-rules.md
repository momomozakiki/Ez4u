---
name: nextjs-bff-api-rules
description: Next.js BFF (API Routes) coding standards for AI
---

# Next.js BFF API Routes Rules

## Framework Versions
- Next.js ^16.1.6 (API Routes)
- Zod ^3.23.8 (validation)
- Axios ^1.7.2 (proxy to Backend)
- next-rate-limit ^1.0.0
- @types/jsonwebtoken ^9.0.5

## Testing
- Vitest/Jest for unit tests
- Playwright for E2E
- Mock Backend responses

## ✅ MUST DO
1. Validate requests with Zod schemas
2. Authenticate users before proxying
3. Forward User JWT with `X-User-ID` & `X-Tenant-ID`
4. Return standardized error responses
5. Support N-1 API version backward compatibility
6. Set cache headers for public endpoints

## ❌ PROHIBITED
1. Direct database access (SQLAlchemy/asyncpg)
2. Business logic implementation
3. Long-running processing (>2s)
4. Bypass authentication
5. Direct Business Logic Layer calls
6. HTML/CSS generation
7. Store session state
8. External API calls (use Backend layer)