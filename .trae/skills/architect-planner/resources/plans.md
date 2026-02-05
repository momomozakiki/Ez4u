# General 5-Layer Architectural Plan (Master Blueprint)

## Phase 1: Foundation (Database & Models)
- [ ] **[Agent: Data-Foundation]** Design and implement database schema with Alembic migrations.
    - *Focus*: `users`, `tenants`, `roles` tables with UUIDv7 and RLS policies.
- [ ] **[Agent: Backend-Kernel]** Define core Pydantic V2 models (`schemas/`) mirroring the DB structure.
    - *Focus*: Strict validation, `tenant_id` injection in base models.

## Phase 2: Core Logic (Backend Business Layer)
- [ ] **[Agent: Backend-Kernel]** Implement Business Logic Services (`services/`).
    - *Focus*: Repository pattern usage, domain rule enforcement (e.g., "One User, Multiple Tenants"), transaction management.
- [ ] **[Agent: API-Gateway]** Develop FastAPI Routes (`routers/`).
    - *Focus*: Dual-auth middleware (JWT + Service Token), request validation, standard error responses.

## Phase 3: Interface (Frontend & BFF)
- [ ] **[Agent: Frontend-Client]** Build Reusable UI Components.
    - *Focus*: Radix UI primitives, Tailwind styling, Client Components for interactivity.
- [ ] **[Agent: Frontend-Server]** Implement Server Components & BFF API Routes.
    - *Focus*: SSR data fetching with Service Tokens, BFF proxying for client-side security.
