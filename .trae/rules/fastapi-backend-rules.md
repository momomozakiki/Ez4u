---
name: fastapi-backend-rules
description: FastAPI HTTP/API layer coding standards for AI assistance
---

# FastAPI Backend Rules

## Framework Versions
- FastAPI ^0.128.0, Uvicorn ^0.40.0
- Pydantic V2 ^2.12.5 (schemas)
- python-jose ^3.3.0 (JWT), passlib ^1.7.4 (bcrypt)
- SQLAlchemy ^2.0.32, asyncpg ^0.29.0 (PostgreSQL)
- OpenTelemetry ^1.26.0 (tracing)
- Prometheus instrumentation ^7.0.0

## Testing
- Pytest for unit/integration tests
- HTTPX for API testing
- Testcontainers for DB integration tests

## ✅ MUST DO
1. Use Pydantic V2 models for all schemas
2. Support Dual Auth (User JWT + Service Token)
3. Validate & Inject `tenant_id` via middleware
4. Call Business Logic Layer (L4) for domain ops
5. Return structured errors `{ error_code, message }`
6. Propagate OpenTelemetry `trace_id`

## ❌ PROHIBITED
1. Direct SQLAlchemy queries in route handlers
2. Business logic in HTTP routes (delegate to services)
3. HTML/CSS generation in API endpoints
4. In-memory state storage (use Redis if needed)
5. Skip tenant_id validation middleware
6. Bypass service layer for data access
7. Store secrets in route handlers
8. Long-running sync operations (>2s)