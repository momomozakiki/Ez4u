---
name: sqlalchemy-orm-database-rules
description: SQLAlchemy ORM & Database Layer coding standards for AI
---

# SQLAlchemy ORM Database Rules

## Framework Versions
- SQLAlchemy ^2.0.32 (async ORM)
- Alembic ^1.13.3 (migrations)
- asyncpg ^0.29.0 (PostgreSQL async driver)
- psycopg2-binary ^2.9.9 (sync fallback)
- uuid7 ^0.1.0 (UUID v7 generation)
- PostgreSQL 16.x

## Testing
- Pytest for unit tests
- Testcontainers for DB integration tests
- Alembic autogenerate for migration validation

## ✅ MUST DO
1. Use UUID v7 primary keys
2. Include `tenant_id` on scoped tables
3. Use `JSONB` for flexible schemas (GIN index)
4. Generate versioned Alembic migrations
5. Implement zero-downtime migrations (Expand-Contract)
6. Enforce RLS policies for tenant isolation

## ❌ PROHIBITED
1. Business logic in stored procedures
2. Direct access from Frontend/BFF layers
3. Nullable foreign keys (unless explicitly optional)
4. Bypass RLS policies
5. Non-UUID v7 primary keys
6. Missing `tenant_id` on tenant-scoped tables
7. Non-zero-downtime migrations
8. Raw SQL queries (use SQLAlchemy ORM)