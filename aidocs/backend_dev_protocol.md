# backend_dev PROTOCOL

## 1. Capabilities & Tech Stack
*   **Core**: **Python 3.12**, **FastAPI 0.109+**
*   **Tools**: Pydantic v2, SQLAlchemy 2.0 (ORM), Alembic, Pytest

### Framework Versions
| Framework/Library | Target Version | Release Date |
|:---|:---|:---|
| Python | 3.12 | 2023-10 |
| FastAPI | 0.109+ | 2024-01 |
| SQLAlchemy | 2.0.x | 2023-01 |
| Pydantic | v2.x | 2023-06 |

## 2. Architectural Standards
*   **Design Pattern**: Service-Repository Pattern (Route -> Service -> CRUD).
*   **Testing Standard**: Mandate unit tests for all core logic. Pytest for endpoints and services.

## 3. Strict Constraints (DO NOT VIOLATE)
*   **Backend**: NO html/css generation (return JSON only).
*   **General**: NO use of deprecated libraries.

## 4. Allowed Libraries (Allowlist)
*   `fastapi`
*   `uvicorn`
*   `sqlalchemy`
*   `alembic`
*   `pydantic`
*   `pytest`
*   `python-jose` (JWT)
*   `passlib` (Hashing)

## 5. Development Workflow
1.  Read Task -> 2. Verify Stack -> 3. Implement -> 4. Test -> 5. Review
