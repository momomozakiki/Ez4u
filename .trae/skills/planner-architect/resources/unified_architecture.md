# UNIFIED 5-LAYER ARCHITECTURE & TECHNOLOGY STANDARD

---

## **Layer 1: Frontend Next.js (Client + Server)**
**Agent Name:** `nextjs_ClientServer`

### **Responsibilities**
- UI rendering with React Server Components and Client Components
- Client-side state management (Zustand)
- Server-side data fetching (initial page load)
- Form handling with React Hook Form + Zod validation
- SEO metadata generation
- Streaming with Suspense boundaries

### **Core Frameworks**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **Next.js** | App Router, Server Components, SSR | ✅ Matches document |
| **React** | UI components, React Server Components | ✅ Latest React 19 |
| **TypeScript** | Type safety, strict typing | ✅ Required by document |

### **UI & Styling**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **Tailwind CSS** | Utility-first CSS framework | ✅ Document specifies Tailwind |
| **Radix UI** | Unstyled, accessible primitives | ✅ Modern UI library |

### **State Management**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **Zustand** | Client-side state management | ✅ Explicitly required |
| **TanStack Query** | Server state caching, mutations | ✅ Modern data fetching |

### **Forms & Validation**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **React Hook Form** | Form handling, validation | ✅ Required by document |
| **Zod** | Schema validation | ✅ Explicitly required |

### **HTTP Client**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **Axios** | HTTP requests to API routes | ✅ Standard choice |

### **Strict Protocol (MUST DO)**
- ✅ Use `'use client'` directive for interactive components
- ✅ Fetch initial data from Backend (Layer 3) for SSR performance
- ✅ Call API Routes (Layer 2) for user-triggered actions
- ✅ Implement loading states and error boundaries
- ✅ Use TypeScript strict typing (no `any`)
- ✅ Include Service Token in headers for direct Server→Backend calls

### **Strict Constraints (MUST NOT DO)**
- ❌ Direct calls to Backend (Layer 3) from **CLIENT Components** (runs in browser)
- ✅ Direct calls to Backend (Layer 3) from **SERVER Components** (allowed for SSR)
- ❌ Direct database access
- ❌ Access non-public environment variables
- ❌ Implement business logic
- ❌ Use `pages/` directory (Next.js 16+ App Router only)

---

## **Layer 2: Next.js API Routes (BFF - Backend for Frontend)**
**Agent Name:** `nextjs_BFF_API_Routes`

### **Responsibilities**
- Reverse proxy between Frontend and Backend
- Authentication token validation and transformation
- Request/response transformation
- Rate limiting and throttling
- API versioning (v1, v2)
- Error standardization and user-friendly messaging
- Response caching (public data, CDN headers)

### **Core Frameworks**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **Next.js API Routes** | Built-in API route handlers | ✅ Native to Next.js |

### **Validation & Security**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **Zod** | Request/response validation | ✅ Explicitly required |
| **@types/jsonwebtoken** | JWT type definitions | ✅ Auth token handling |

### **Rate Limiting**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **next-rate-limit** | Rate limiting middleware | ✅ Required by document |

### **Strict Protocol (MUST DO)**
- ✅ Validate all incoming requests with Zod schemas
- ✅ Authenticate users before proxying to Backend
- ✅ Forward User JWT to Backend with `X-User-ID`, `X-Tenant-ID` headers
- ✅ Return standardized error responses (user-friendly messages)
- ✅ Support N-1 API version backward compatibility
- ✅ Set cache headers for public endpoints

### **Strict Constraints (MUST NOT DO)**
- ❌ Implement business logic
- ❌ Direct database access
- ❌ Long-running processing (offload to Backend)
- ❌ Bypass authentication for protected routes

---

## **Layer 3: FastAPI Backend (HTTP/API Layer)**
**Agent Name:** `fastapi_HTTP_API`

### **Responsibilities**
- HTTP server with async endpoints
- Request routing and validation
- **Dual authentication middleware** (User JWT + Service Token)
- Multi-tenancy enforcement (inject `tenant_id`)
- OpenAPI documentation generation
- Background task queuing
- Prometheus metrics collection

### **Core Frameworks**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **FastAPI** | HTTP server, async endpoints | ✅ Latest stable |
| **Uvicorn** | ASGI server | ✅ Required |
| **Starlette** | ASGI framework (FastAPI dependency) | ✅ Included |

### **Authentication & Security**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **python-jose** | JWT operations | ✅ Required |
| **passlib** | Password hashing (bcrypt) | ✅ Required |
| **python-multipart** | Form data parsing | ✅ Standard |

### **Validation & Types**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **Pydantic** | Data validation, schemas | ✅ Pydantic V2 required |
| **email-validator** | Email validation | ✅ Standard |

### **Observability**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **prometheus-fastapi-instrumentator** | Prometheus metrics | ✅ Required |
| **opentelemetry-api** | Distributed tracing | ✅ Trace propagation |
| **opentelemetry-sdk** | OpenTelemetry SDK | ✅ Required |

### **Strict Protocol (MUST DO)**
- ✅ Use Pydantic V2 models for all schemas
- ✅ Support dual authentication modes:
  - **User JWT**: From BFF, contains `user_id`, `tenant_id`, `roles`
  - **Service Token**: From Server Components, contains `service_name`, `tenant_id`, `scope`
- ✅ Validate `tenant_id` is always present before processing
- ✅ Inject `tenant_id` into request state via middleware
- ✅ Call Business Logic Layer (Layer 4) for domain operations
- ✅ Return structured errors: `{ error_code, message, field }`
- ✅ Propagate OpenTelemetry `trace_id` across layers

### **Strict Constraints (MUST NOT DO)**
- ❌ Direct database queries (delegate to Layer 4/5)
- ❌ Implement complex business rules
- ❌ Generate HTML/CSS
- ❌ Store state in memory

---

## **Layer 4: Business Logic Layer**
**Agent Name:** `python_business_logic`

### **Responsibilities**
- Core domain rules and calculations
- Workflow orchestration
- Service classes and use cases
- Repository pattern implementation
- External API integrations (with circuit breakers)
- Multi-tenancy isolation enforcement
- Transaction boundary management

### **Core Frameworks**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **Pydantic** | Domain models, validation | ✅ Required |

### **External Integrations**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **httpx** | Async HTTP client | ✅ Circuit breaker pattern |
| **pybreaker** | Circuit breaker implementation | ✅ Required |

### **Strict Protocol (MUST DO)**
- ✅ Keep logic framework-agnostic (no FastAPI/SQLAlchemy imports)
- ✅ Use repository pattern for data access abstraction
- ✅ Enforce tenant isolation on all operations
- ✅ Handle transaction boundaries (commit/rollback)
- ✅ Validate business invariants
- ✅ Raise domain exceptions (e.g., `InsufficientStockError`, `UserNotFoundError`)
- ✅ Use dedicated integration services (e.g., `StripeService`, `SendGridService`)
- ✅ Implement circuit breaker pattern (fail fast after 3 failures)
- ✅ Set timeouts: 5s for critical paths, 30s for background jobs

### **Strict Constraints (MUST NOT DO)**
- ❌ HTTP request handling
- ❌ Direct database driver usage
- ❌ UI/HTML generation
- ❌ Store session state

---

## **Layer 5: Database & SQLAlchemy ORM Layer**
**Agent Name:** `DB_sqlalchemy_ORM`

### **Responsibilities**
- PostgreSQL schema definition
- SQLAlchemy async models
- Alembic migrations (Expand-Contract pattern)
- Connection pooling and indexing
- Row-Level Security (RLS) enforcement
- Data integrity constraints
- Slow query logging (>100ms threshold)

### **Core Frameworks**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **SQLAlchemy** | ORM, async support | ✅ SQLAlchemy 2.0 required |
| **Alembic** | Database migrations | ✅ Required |

### **Database Drivers**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **asyncpg** | Async PostgreSQL driver | ✅ Recommended |
| **psycopg2-binary** | Sync PostgreSQL driver | ✅ Fallback option |

### **UUID Support**
| Package | Purpose | Document Alignment |
|---------|---------|-------------------|
| **uuid7** | UUID v7 generation | ✅ Time-ordered UUIDs |

### **Strict Protocol (MUST DO)**
- ✅ Use UUID v7 primary keys (time-ordered, distributed-safe)
- ✅ Include `tenant_id` on all tenant-scoped tables
- ✅ Use `JSONB` for flexible schemas with GIN indexes
- ✅ Generate versioned Alembic migrations
- ✅ Lead composite indexes with `tenant_id`
- ✅ Implement zero-downtime migrations (Expand-Contract)
- ✅ Enforce constraints (foreign keys, check, unique)
- ✅ Row-Level Security policies:
  ```sql
  CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
  ```

### **Strict Constraints (MUST NOT DO)**
- ❌ Business logic in stored procedures
- ❌ Direct access from Frontend or BFF layers
- ❌ Nullable foreign keys (unless explicitly optional)

---

## **Layer-to-Layer Communication Matrix**

### **Decision Matrix**
| From Layer | To Layer | Status | Authentication | When to Use | When NOT to Use |
|------------|----------|--------|----------------|-------------|-----------------|
| **L1 Client** | L2 BFF | ✅ Required | User JWT | User actions, mutations, auth flows | Never bypass BFF from client |
| **L1 Server** | L2 BFF | ⚠️ Optional | Service Token | When user context needed in SSR | When performance critical |
| **L1 Server** | L3 Backend | ✅ Allowed | Service Token | Page load, SSR, authenticated system data | User-specific mutations |
| **L2 BFF** | L3 Backend | ✅ Required | Forward User JWT | All proxied requests | Never skip Backend layer |
| **L2 BFF** | L4 Business | ❌ Forbidden | — | — | Always go through HTTP layer |
| **L3 Backend** | L4 Business | ✅ Required | N/A (internal) | All domain operations | Never implement logic in routes |
| **L3 Backend** | L5 Database | ❌ Forbidden | — | — | Always use repository pattern |
| **L4 Business** | L5 Database | ✅ Exclusive | tenant_id param | All data access | Never expose DB to other layers |
| **L4 Business** | External APIs | ✅ Allowed | API keys (env) | Third-party integrations | Must handle failures gracefully |
| **Any Layer** | L5 Database | ❌ Forbidden | — | — | Database is private to Business Logic |

### **Communication Rules**
1. **Client Components NEVER bypass BFF** - Prevents credential exposure in browser
2. **Server Components MAY bypass BFF** - Performance optimization with service tokens
3. **BFF NEVER talks to Database** - Layer violation
4. **Backend NEVER implements business logic** - Separation of concerns
5. **Business Logic NEVER handles HTTP** - Framework agnostic
6. **Database is PRIVATE** - Only accessible by Business Logic Layer
7. **tenant_id MUST be validated** - Before any data access operation
8. **Service tokens have limited scope** - Cannot perform user mutations

---

## **Detailed Scenarios**

### **Scenario 1: User Login Flow**
```
Layer 1 (Client Component)
    ↓ POST /api/v1/auth/login (with credentials)
Layer 2 (BFF)
    ↓ Zod validation → Forward to Backend with X-CSRF-Token
Layer 3 (FastAPI)
    ↓ Middleware validates request → Call AuthService.authenticate()
Layer 4 (Business Logic)
    ↓ UserRepository.find_by_email(email)
    ↓ If not found → raise UserNotFoundError
    ↓ Validate password against hashed_password (bcrypt in L4)
    ↓ Generate JWT with claims: { user_id, tenant_id, roles, exp }
Layer 5 (Database)
    ← Return user record (RLS enforced)
Layer 4
    ← Return { token, sanitized_user }
Layer 3
    ← Return { token, user }
Layer 2
    ← Set HTTP-only cookie, return sanitized user
Layer 1
    ← Store session, redirect to dashboard
```

### **Scenario 2: Dashboard Page Load (SSR)**
```
Layer 1 (Server Component)
    ↓ fetch(BACKEND_URL/v1/dashboard, {
        headers: { 'X-Service-Token': process.env.SERVICE_TOKEN }
      })
Layer 3 (FastAPI)
    ↓ Middleware validates service token → extracts tenant_id from JWT claims
    ↓ Call DashboardService.get_data(tenant_id)
Layer 4 (Business Logic)
    ↓ Parallel repository calls with tenant_id filter
Layer 5 (Database)
    ← Return data (RLS enforced: tenant_id = current_setting('app.tenant_id'))
Layer 4
    ← Apply business rules, calculations
Layer 3
    ← Return { stats, charts, notifications }
Layer 1
    ← Render HTML with data (TTFB optimized, no BFF overhead)
```

---

## ✅ **VALIDATION CHECKLIST**

> **Note:** Refer to `package.json` and `requirements.txt` for active versions. Ensure all new packages added to the project are reflected in the Architectural Purpose tables above.

| Requirement | Status | Notes |
|-------------|--------|-------|
| **Layer 1: Zustand for client state** | ✅ | Required for client state |
| **Layer 1: TanStack Query for server state** | ✅ | Required for server state |
| **Layer 1: React Hook Form + Zod** | ✅ | Required for forms |
| **Layer 2: Zod validation** | ✅ | Required for validation |
| **Layer 2: Rate limiting** | ✅ | Required for BFF |
| **Layer 3: Pydantic V2** | ✅ | Required for validation |
| **Layer 3: Dual auth (JWT + Service Token)** | ✅ | Required for security |
| **Layer 3: Prometheus metrics** | ✅ | Required for observability |
| **Layer 3: OpenTelemetry tracing** | ✅ | Required for tracing |
| **Layer 4: Framework-agnostic logic** | ✅ | No FastAPI/SQLAlchemy imports |
| **Layer 4: Circuit breaker pattern** | ✅ | Required for stability |
| **Layer 4: Repository pattern** | ✅ | Design pattern |
| **Layer 5: SQLAlchemy 2.0** | ✅ | Required ORM |
| **Layer 5: Alembic migrations** | ✅ | Required migrations |
| **Layer 5: Async PostgreSQL driver** | ✅ | Required driver |
| **Layer 5: UUID v7 support** | ✅ | Required for PKs |
| **FastAPI version aligned** | ✅ | Matches requirements.txt |
| **Next.js version aligned** | ✅ | Matches package.json |
