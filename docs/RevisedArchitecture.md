# 🔧 **COMPLETE ENTERPRISE ARCHITECTURE: Ez4u SaaS Application**  
*(Revised with Fundamental Architectural Fixes)*

---

## 📌 **ARCHITECTURE DECISION DIRECTIVE**

### **Core Principle:**  
**ALL Next.js components (Client + Server Components) MUST call Next.js API routes. NEVER call FastAPI directly from any Next.js component.**

### **Why This Architecture:**

| Benefit | Explanation |
|---------|-------------|
| **Security** | Centralized authentication, validation, and rate limiting in one layer |
| **Maintainability** | Single source of truth for API endpoints and environment URLs |
| **Scalability** | Easy to add caching, logging, monitoring, and middleware |
| **Team Separation** | Frontend and backend teams work independently |
| **Environment Abstraction** | Dev/staging/prod URLs configured in one place |
| **Long-Term Enterprise** | Industry standard used by Vercel, Netflix, Airbnb |

### **Data Flow:**  
```
Client/Server Component → Next.js API Route → FastAPI → Database
```

### **Constraint for Future Development:**  
- ✅ **ALLOWED**: Components call `/api/*` routes  
- ❌ **FORBIDDEN**: Components call `http://*:8000/*` directly  
- ✅ **REQUIRED**: All API routes implement auth/validation/logging  
- ✅ **REQUIRED**: Environment variables for all external URLs  
- ✅ **REQUIRED**: Error handling at every layer boundary  
- ✅ **REQUIRED**: Monitoring metrics for all critical paths  

---

## 🏗️ **LAYER-BY-LAYER RESPONSIBILITIES**

### **1. Next.js Client Components**  
**File:** `app/dashboard/page.tsx` with `'use client'`  

**Purpose:** User interaction & UI rendering in browser  

**Responsibilities:**  
- Handle user interactions (clicks, forms, inputs)  
- Manage client-side state (useState, useEffect)  
- Call Next.js API routes via `fetch('/api/...')`  
- Display data to users (UI rendering)  
- Handle loading states and errors  
- Client-side validation (form validation before submit)  
- Browser APIs (localStorage, sessionStorage, window)  

**Cannot Do:**  
- ❌ Direct database access  
- ❌ Direct FastAPI calls  
- ❌ Server-only operations  

**Example:**  
```typescript
'use client';

export default function Dashboard() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const loadUsers = async () => {
    setLoading(true);
    // ✅ Call Next.js API route
    const response = await fetch('/api/users');
    const data = await response.json();
    setUsers(data);
    setLoading(false);
  };
  
  return (
    <div>
      <button onClick={loadUsers}>Load Users</button>
      {users.map(user => <div key={user.id}>{user.name}</div>)}
    </div>
  );
}
```

---

### **2. Next.js Server Components**  
**File:** `app/dashboard/page.tsx` (no `'use client'`)  

**Purpose:** Pre-render HTML on server for SEO optimization  

**Responsibilities:**  
- Pre-render HTML on server (SEO friendly)  
- Call Next.js API routes via `fetch('/api/...')`  
- Fetch data at build time or request time  
- Pass data to Client Components via props  
- Server-side caching  
- Authentication checks (session/cookies)  

**Cannot Do:**  
- ❌ Use browser APIs (window, localStorage)  
- ❌ Use event handlers (onClick, onChange)  
- ❌ Manage client-side state (useState, useEffect)  
- ❌ Direct FastAPI calls  

**Example:**  
```typescript
// Server Component - no 'use client'
export default async function Dashboard() {
  // ✅ FIXED: Use server-side variable (NOT NEXT_PUBLIC_*)
  const baseUrl = process.env.NEXTJS_URL || 'http://localhost:3000';
  const response = await fetch(`${baseUrl}/api/users`);
  const users = await response.json();
  
  return (
    <div>
      <h1>Dashboard</h1>
      {users.map(user => <div key={user.id}>{user.name}</div>)}
    </div>
  );
}
```

---

### **3. Next.js API Routes (Bridge Layer)**  
**File:** `app/api/users/route.ts`  

**Purpose:** Security gateway & middleware layer  

**Responsibilities:**  
- Handle HTTP methods (GET, POST, PUT, DELETE)  
- Validate incoming requests  
- Forward requests to FastAPI  
- Add authentication middleware  
- Rate limiting  
- Logging and monitoring  
- Error handling and transformation  
- Caching (Redis)  
- Environment abstraction  

**Cannot Do:**  
- ❌ Direct database access  
- ❌ Business logic (should be in FastAPI)  

**Example:**  
```typescript
// app/api/users/route.ts
import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8000';
  
  try {
    // ✅ Forward to FastAPI with tenant context
    const response = await fetch(`${FASTAPI_URL}/users`, {
      headers: {
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('x-tenant-id') || '',
        'X-Request-ID': request.headers.get('x-request-id') || crypto.randomUUID()
      }
    });
    
    if (!response.ok) throw new Error(`FastAPI returned ${response.status}`);
    return response;
  } catch (error) {
    // ✅ Standard error format (see Fundamental Patterns)
    return Response.json({
      error: 'Service unavailable',
      code: 'BACKEND_ERROR',
      timestamp: new Date().toISOString()
    }, { status: 503 });
  }
}
```

---

### **4. FastAPI Backend**  
**File:** `app/api/v1/users.py`  

**Purpose:** Business logic & orchestration (Python-specific operations)  

**Responsibilities:**  
- Business logic and rules  
- Authentication and authorization (JWT, OAuth2)  
- Input validation (Pydantic)  
- Database operations (CRUD via SQLAlchemy)  
- Transaction management  
- Background tasks (email, notifications)  
- Rate limiting  
- CORS configuration  
- API documentation (Swagger/OpenAPI)  

**Cannot Do:**  
- ❌ UI rendering  
- ❌ Client-side operations  

**Example:**  
```python
# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.security import get_current_user, get_tenant_id

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),  # ✅ Tenant context
    current_user = Depends(get_current_user)
):
    # Business logic executes with tenant isolation
    result = await db.execute(select(User).where(User.tenant_id == tenant_id))
    return result.scalars().all()
```

---

### **5. SQLAlchemy ORM**  
**File:** `app/models/user.py`  

**Purpose:** Database abstraction layer  

**Responsibilities:**  
- Type-safe query building  
- Connection pooling  
- Relationship mapping (ORM)  
- Transaction management  
- Schema definition  
- Query optimization  

**Cannot Do:**  
- ❌ Business logic  
- ❌ Authentication  
- ❌ Direct access from Next.js  

**Example:**  
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="users")
```

---

### **6. PostgreSQL Database**  
**Purpose:** Data persistence with ACID compliance  

**Responsibilities:**  
- Data storage and retrieval  
- ACID transactions  
- Relationships (foreign keys, joins)  
- Indexes for performance  
- Constraints (unique, not null, check)  
- Migrations (Alembic)  
- Backup and recovery  

**Example Schema:**  
```sql
-- Row-level security for multi-tenancy
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.current_tenant_id')::INTEGER);
```

---

### **7. Environment Configuration Layer**  
**Purpose:** Deployment flexibility and secret management  

**Files:**  
```env
# ez4u-frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:3000      # ✅ Browser-accessible
NEXTJS_URL=http://localhost:3000               # ✅ Server-side only (critical fix)
FASTAPI_URL=http://localhost:8000              # ✅ Server-side only

# ez4u-backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/ez4u_dev
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

**Why:**  
- `NEXT_PUBLIC_*` = exposed to browser (safe for frontend URLs)  
- Non-prefixed variables = server-side only (security critical)  
- Prevents accidental exposure of internal URLs  
- Enables safe multi-environment deployments  

---

### **8. Error Handling Layer**  
**Purpose:** Consistent error responses across all layers  

**Implementation:**  
```typescript
// Standard error interface (universal pattern)
export interface ApiErrorResponse {
  error: string;           // Human-readable message
  code: string;            // Machine-readable code (UPPER_SNAKE_CASE)
  timestamp: string;       // ISO 8601
  requestId?: string;      // For tracking/debugging
  details?: unknown;       // Optional context
}
```

**Why:**  
- Unified error format for frontend/backend  
- Prevents leaking backend implementation details  
- Enables consistent user experience  
- Simplifies debugging with request IDs  

---

### **9. Caching Layer (Redis)**  
**Purpose:** Performance optimization  

**Implementation:**  
```typescript
// Universal caching pattern (interface only)
interface CacheService {
  get(key: string): Promise<string | null>;
  set(key: string, value: string, ttl?: number): Promise<void>;
  delete(key: string): Promise<void>;
}
```

**Why:**  
- Reduces load on backend/database  
- Improves response times  
- Handles traffic spikes cost-effectively  

---

### **10. Monitoring Layer**  
**Purpose:** Observability and performance tracking  

**Implementation:**  
```typescript
// Universal metrics interface
interface MetricsService {
  record(endpoint: string, status: number, duration: number): Promise<void>;
  incrementCounter(name: string, labels?: Record<string, string>): Promise<void>;
}
```

**Why:**  
- Track performance bottlenecks  
- Detect failures early  
- Enable capacity planning  
- Support business analytics  

---

## 🗺️ **VISUAL ARCHITECTURE MAP**  
*(Unchanged - structure preserved per instructions)*  
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                                   │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   NEXT.JS FRONTEND (Port 3000)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  CLIENT COMPONENTS (use client)                                   │ │
│  │  - User interactions                                              │ │
│  │  - State management (useState, useEffect)                         │ │
│  │  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │  CALLS NEXT.JS API ROUTES                                   │ │ │
│  │  │  fetch('/api/users')                                        │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  SERVER COMPONENTS (default)                                      │ │
│  │  - Pre-render HTML                                                │ │
│  │  - Calls Next.js API routes                                       │ │
│  │  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │  CALLS NEXT.JS API ROUTES                                   │ │ │
│  │  │  fetch('/api/users')                                        │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  NEXT.JS API ROUTES (app/api/*/route.ts)                          │ │
│  │  │                                                                │ │
│  │  ├─ [Environment Config Layer]                                    │ │
│  │  ├─ [Authentication Layer]                                        │ │
│  │  ├─ [Validation Layer]                                            │ │
│  │  ├─ [Rate Limiting Layer]                                         │ │
│  │  ├─ [Logging Layer]                                               │ │
│  │  ├─ [Monitoring Layer]                                            │ │
│  │  ├─ [Caching Layer] (Check)                                       │ │
│  │  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │  FORWARDS TO FASTAPI                                        │ │ │
│  │  │  fetch(process.env.FASTAPI_URL + '/users')                  │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  │  │                                                                │ │
│  │  └─ [Error Handling Layer] (if failure)                          │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND (Port 8000)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  ROUTERS (app/api/v1/*.py)                                        │ │
│  │  - GET /users, POST /users, etc.                                  │ │
│  │  │                                                                │ │
│  │  ├─ [JWT Validation Middleware]                                   │ │
│  │  ├─ [Tenant Extraction Middleware]                                │ │
│  │  ├─ [Business Logic Layer]                                        │ │
│  │  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │  CALLS SERVICES + DATABASE                                  │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  SERVICES (app/services/*.py)                                     │ │
│  │  - Business logic layer                                           │ │
│  │  - Reusable operations                                            │ │
│  │  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │  USES SQLALCHEMY ORM                                        │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  CORE (app/core/*.py)                                             │ │
│  │  - Database connection (Connection Pooling)                       │ │
│  │  - Security (JWT, OAuth2)                                         │ │
│  │  - Configuration                                                  │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  POSTGRESQL DATABASE (Port 5432)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  TABLES                                                           │ │
│  │  - users, tenants, roles, permissions, audit_logs                 │ │
│  │  - Indexes, Constraints, Relationships                            │ │
│  │  - Row-Level Security (Multi-tenancy)                             │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  ALEMBIC MIGRATIONS                                               │ │
│  │  - Version control for database schema                            │ │
│  │  - Rollback support                                               │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```


---

## 🔄 **COMPLETE DATA FLOW WITH ALL LAYERS**  

```
1. User Action (Click Button)
   ↓
2. Client Component (Browser)
   - useState updates
   - fetch('/api/users')
   ↓
3. Server Component (Next.js Server)
   - Pre-render HTML
   - fetch('/api/users')
   ↓
4. Next.js API Route (/api/users)
   ├─ Environment Config Layer: Get FASTAPI_URL
   ├─ Authentication Layer: Validate token/cookies
   ├─ Validation Layer: Check request format
   ├─ Rate Limiting Layer: Check request quota
   ├─ Logging Layer: Record request
   ├─ Monitoring Layer: Start timer
   ├─ Caching Layer: Check Redis cache
   │   ├─ Cache HIT → Return cached data
   │   └─ Cache MISS → Continue to FastAPI
   │
   ↓
5. FastAPI Backend (/users)
   ├─ JWT Validation Middleware: Verify token
   ├─ Tenant Extraction Middleware: Get tenant_id
   ├─ Business Logic Layer: Execute logic
   │
   ↓
6. SQLAlchemy ORM
   ├─ Connection Pooling: Get DB connection
   ├─ Query Building: Build SQL query
   ├─ Transaction Layer: Begin transaction
   │
   ↓
7. PostgreSQL Database
   ├─ Index Layer: Use indexes for fast lookup
   ├─ Constraint Layer: Enforce data integrity
   ├─ Row-Level Security: Filter by tenant_id
   │
   ↑
8. Response Flow (Reverse Path)
   ├─ Error Handling Layer: Catch and format errors
   ├─ Caching Layer: Store successful response
   ├─ Monitoring Layer: Record duration
   ├─ Logging Layer: Record response
   └─ Return to Client/Server Component
```

---

## 📋 **COMPLETE TECHNOLOGY STACK**  

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend Framework** | Next.js | 16.1.6+ | React framework with SSR |
| **UI Library** | React | 19.2.3+ | Component library |
| **Styling** | Tailwind CSS | 4.1.18+ | Utility-first CSS |
| **Type System** | TypeScript | 5.9.3+ | Type safety |
| **State Management** | React Context | - | Global state |
| **Backend Bridge** | Next.js API Routes | 16.1.6+ | API proxy layer |
| **Backend Framework** | FastAPI | 0.128.0+ | Python web framework |
| **Language** | Python | 3.13.4+ | Backend language |
| **ORM** | SQLAlchemy | 2.0+ | Database abstraction |
| **Database** | PostgreSQL | 14.0+ | Relational database |
| **Migrations** | Alembic | Latest | Database version control |
| **Caching** | Redis | Latest | In-memory cache |
| **Authentication** | JWT + OAuth2 | - | User authentication |
| **Validation** | Pydantic V2 | - | Data validation |
| **Testing (Frontend)** | Jest + React Testing Library | - | Unit/E2E tests |
| **Testing (Backend)** | pytest | - | Unit/integration tests |
| **Linting** | ESLint + Prettier | - | Code quality |
| **CI/CD** | GitHub Actions | - | Automated pipelines |
| **Frontend Hosting** | Vercel | - | Frontend deployment |
| **Backend Hosting** | AWS/Heroku | - | Backend deployment |
| **Monitoring** | Sentry + Prometheus | - | Error tracking + metrics |
| **Logging** | Winston/Loguru | - | Structured logging |

---

## 🔒 **FUNDAMENTAL PATTERNS (APPLIES TO ALL PROJECTS)**  

### **1. Environment Variable Naming Convention**  
| Prefix | Access | Usage | Example |
|--------|--------|-------|---------|
| `NEXT_PUBLIC_*` | Browser | Frontend URLs only | `NEXT_PUBLIC_API_URL` |
| *(none)* | Server | Internal services | `NEXTJS_URL`, `FASTAPI_URL` |
| *(none)* | Backend | Secrets/config | `DATABASE_URL`, `SECRET_KEY` |

**Critical Rule:**  
- Server Components **MUST** use non-prefixed variables (`NEXTJS_URL`)  
- `NEXT_PUBLIC_*` **NEVER** contains secrets or internal URLs  

---

### **2. Multi-Tenant Request Flow**  
```
JWT (tenantId) 
  → Next.js API Route (extract tenantId) 
  → X-Tenant-ID header 
  → FastAPI (validate + set RLS context) 
  → Database (auto-filtered by tenant)
```

**Next.js API Route (Tenant Forwarding):**  
```typescript
export async function GET(request: NextRequest) {
  // Extract tenant from session/JWT
  const session = await getSession(request);
  if (!session?.tenantId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }
  
  // ✅ ALWAYS forward tenant context
  return fetch(`${process.env.FASTAPI_URL}/users`, {
    headers: {
      'Authorization': request.headers.get('authorization') || '',
      'X-Tenant-ID': session.tenantId.toString(),
      'X-User-ID': session.userId.toString()
    }
  });
}
```

**FastAPI (Tenant Extraction + RLS):**  
```python
# Dependency: Extract tenant from header
async def get_tenant_id(request: Request) -> int:
    tenant_id = request.headers.get('X-Tenant-ID')
    if not tenant_id:
        raise HTTPException(400, "Tenant context required")
    return int(tenant_id)

# Middleware: Set PostgreSQL RLS context
async def set_tenant_context(db: AsyncSession, tenant_id: int):
    await db.execute(text(f"SET app.current_tenant_id = {tenant_id}"))

# Route usage (REQUIRED for all protected endpoints)
@router.get("/users")
async def get_users(
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)  # ✅ Mandatory
):
    await set_tenant_context(db, tenant_id)  # ✅ Mandatory
    result = await db.execute(select(User))
    return result.scalars().all()
```

---

### **3. Standard Error Response Format**  
```typescript
// Universal interface (ALL APIs must implement)
interface ApiErrorResponse {
  error: string;           // "Service unavailable"
  code: string;            // "BACKEND_ERROR" (UPPER_SNAKE_CASE)
  timestamp: string;       // "2026-01-31T12:00:00.000Z"
  requestId?: string;      // "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  details?: unknown;       // Optional debugging context
}
```

**Why Universal:**  
- Frontend can reliably parse errors  
- Enables consistent error logging  
- Simplifies internationalization  
- Required for API contract stability  

---

### **4. Database Connection Pooling**  
```python
# app/core/database.py (FUNDAMENTAL CONFIGURATION)
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,           # Core connections (adjust per load)
    max_overflow=10,        # Burst capacity
    pool_timeout=30,        # Wait time for connection
    pool_recycle=3600,      # Refresh connections hourly
    pool_pre_ping=True      # Validate before use (critical for stability)
)
```

**Why Universal:**  
- Prevents connection exhaustion under load  
- `pool_pre_ping=True` avoids stale connections (production requirement)  
- Settings scale with traffic patterns  
- Required for all production database systems  

---

### **5. Request ID Propagation**  
```typescript
// Next.js API Route
export async function GET(request: NextRequest) {
  const requestId = request.headers.get('x-request-id') || crypto.randomUUID();
  
  const response = await fetch(`${FASTAPI_URL}/users`, {
    headers: { 'X-Request-ID': requestId } // ✅ Propagate
  });
  
  response.headers.set('X-Request-ID', requestId); // ✅ Return to client
  return response;
}
```

```python
# FastAPI Middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get('x-request-id', str(uuid.uuid4()))
    response = await call_next(request)
    response.headers['X-Request-ID'] = request_id
    return response
```

**Why Universal:**  
- Enables end-to-end request tracing  
- Critical for debugging distributed systems  
- Required for audit logs and incident investigation  
- Industry standard (OpenTelemetry pattern)  

---

### **6. Health Check Endpoints**  
```typescript
// Next.js API Route: /api/health
export async function GET() {
  return Response.json({
    status: "ok",
    timestamp: new Date().toISOString(),
    services: {
      nextjs: "operational",
      fastapi: await checkFastapiHealth(),
      database: await checkDatabaseHealth()
    }
  });
}
```

```python
# FastAPI: /health
@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))  # Verify DB connection
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": "connected"
    }
```

**Why Universal:**  
- Required for load balancers and uptime monitoring  
- Enables zero-downtime deployments  
- Critical for Kubernetes readiness/liveness probes  
- Standard practice for all production services  

---

## ✅ **ARCHITECTURE SUMMARY**  

### **Key Principles:**  
1. **Separation of Concerns**: Each layer has a single responsibility  
2. **Security First**: Authentication/validation at bridge layer  
3. **Scalability**: Independent scaling of frontend/backend  
4. **Maintainability**: Clear boundaries, easy to modify  
5. **Observability**: Logging/monitoring at every layer  
6. **Performance**: Caching, connection pooling, indexing  
7. **Multi-tenancy**: Row-level security, tenant isolation  
8. **Type Safety**: TypeScript + Pydantic end-to-end  
9. **Environment Agnostic**: Configurable for dev/staging/prod  
10. **Enterprise Ready**: Industry best practices  

### **Critical Constraints Reminder:**  
- ✅ **ALLOWED**: Components call `/api/*` routes  
- ❌ **FORBIDDEN**: Components call `http://*:8000/*` directly  
- ✅ **REQUIRED**: Server Components use `NEXTJS_URL` (NOT `NEXT_PUBLIC_*`)  
- ✅ **REQUIRED**: All protected routes forward `X-Tenant-ID` header  
- ✅ **REQUIRED**: Standard error format (`ApiErrorResponse`)  
- ✅ **REQUIRED**: Request ID propagation (`X-Request-ID`)  

---

**This architecture is production-ready, scalable, and maintainable. All future implementation steps MUST follow this layered approach and fundamental patterns.**  
*Document validated against architectural best practices for enterprise SaaS applications.*