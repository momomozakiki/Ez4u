# Comprehensive Login System Implementation Plan

This plan implements a secure, full-stack authentication system for testing Ez4u agents, utilizing **SQLite** for the test environment while preserving the **PostgreSQL** architecture for production.

## 🏗️ Phase 1: Data Foundation (Agent 5)
**Objective:** Enable Dual-Database Support (SQLite for Test, Postgres for Prod) & Dependencies.

1.  **Dependencies:** Update `ez4u-backend/requirements.txt` with:
    *   `aiosqlite` (Async SQLite support)
    *   `passlib[bcrypt]` (Password hashing)
    *   `python-jose[cryptography]` (JWT handling)
    *   `python-multipart` (Form data handling)
2.  **Database Configuration:** Refactor `ez4u-backend/app/database/base.py`:
    *   Introduce `TEST_MODE` environment variable detection.
    *   If `TEST_MODE=True`, initialize `sqlite+aiosqlite:///./test.db`.
    *   Else, default to `postgresql+asyncpg` (Golden State).
3.  **Seeding:** Create `ez4u-backend/app/scripts/seed_admin.py`:
    *   Script to auto-create the `admin` / `admin` user with a hashed password on startup.

## 🧠 Phase 2: Backend Kernel (Agent 4)
**Objective:** Implement Secure Authentication Logic & API Endpoints.

1.  **Security Module:** Create `ez4u-backend/app/core/security.py`:
    *   `verify_password()` & `get_password_hash()` utilities.
    *   `create_access_token()` for JWT generation.
2.  **Auth Router:** Create `ez4u-backend/app/routers/auth.py`:
    *   `POST /api/login`: Validates credentials, sets **HttpOnly Secure Cookie** with JWT.
    *   `POST /api/logout`: Clears the cookie.
    *   `GET /api/me`: Validates session and returns current user info.
3.  **Integration:** Register router in `ez4u-backend/app/main.py`.

## 🌐 Phase 3: API Gateway & Frontend (Agent 1 & 3)
**Objective:** Connect Frontend to Backend via Proxy (Simulating Gateway).

1.  **Gateway Config (Agent 3):** Update `ez4u-frontend/next.config.ts`:
    *   Add `rewrites()` to proxy `/api/:path*` -> `http://127.0.0.1:8000/api/:path*`.
    *   *Rationale:* Ensures Frontend never talks directly to Backend ports (Architecture Rule).
2.  **Login UI (Agent 1):** Create `ez4u-frontend/app/login/page.tsx`:
    *   **UI:** Centered Card layout with Tailwind CSS.
    *   **Form:** Username/Password inputs using `react-hook-form` + `zod` validation.
    *   **Feedback:** Error alerts for invalid credentials.
    *   **Logic:** `POST /api/login` (via Gateway proxy).

## ✅ Phase 4: Verification & Documentation (Agent 6)
**Objective:** Validate and Document.

1.  **Unit Tests:** Create `ez4u-backend/tests/test_auth.py` (Pytest) to verify hashing and token logic.
2.  **Documentation:** Create `ez4u-backend/README_AUTH.md` with:
    *   Setup instructions (`TEST_MODE=True`).
    *   Default credentials (`admin`/`admin`).
    *   API Contract details.
