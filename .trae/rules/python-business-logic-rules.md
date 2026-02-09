---
alwaysApply: false
description: "Applies when editing Python business logic."
---

# Python Business Logic Rules

## Framework Versions
- Pydantic V2 ^2.12.5
- python-jose ^3.3.0
- passlib ^1.7.4
- httpx ^0.27.0
- pybreaker ^1.1.1

## Testing
- Pytest, Testcontainers
- Mock external services

## ✅ MUST DO
1. Keep logic framework-agnostic
2. Use repository pattern for data access
3. Enforce tenant isolation on all operations
4. Handle transactions (commit/rollback)
5. Raise domain exceptions (e.g., `UserNotFoundError`)
6. Implement circuit breaker (fail fast >3 errors)
7. Set timeouts (5s critical, 30s background)

## ❌ PROHIBITED
1. FastAPI/SQLAlchemy imports
2. Direct DB driver usage
3. HTTP request handling in routes
4. UI/HTML generation
5. Session state storage
6. Bypass tenant_id enforcement
7. External API calls without circuit breaker (max 3 failures)
8. Missing timeouts: critical paths >5s, background jobs >30s
9. Missing domain exceptions