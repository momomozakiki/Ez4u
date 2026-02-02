# Ez4u Authentication System (Test Mode)

This module provides a secure authentication mechanism for testing the Ez4u platform. It supports a **Dual-Database Architecture**, allowing lightweight SQLite usage for development/testing while strictly adhering to PostgreSQL for production.

## 🚀 Setup & Usage

### 1. Enable Test Mode (SQLite)
To run the backend with the local SQLite database (bypassing the PostgreSQL requirement), set the `TEST_MODE` environment variable:

```bash
# Windows PowerShell
$env:TEST_MODE="True"; uvicorn app.main:app --reload

# Linux/Mac
export TEST_MODE=True && uvicorn app.main:app --reload
```

### 2. Seed Default Admin
On first run, initialize the database and create the admin user:

```bash
# From ez4u-backend directory
$env:TEST_MODE="True"; python -m app.scripts.seed_admin
```

### 3. Default Credentials
*   **Username:** `admin`
*   **Password:** `admin`

## 📡 API Endpoints

### `POST /api/login`
Authenticates a user and sets a secure `HttpOnly` cookie.
*   **Body:** `{"username": "admin", "password": "admin"}`
*   **Response:** `200 OK`

### `POST /api/logout`
Clears the authentication cookie.

### `GET /api/me`
Returns the currently authenticated user's profile.
*   **Headers:** Requires `access_token` cookie (handled automatically by browser).

## 🧪 Testing
Run the unit tests to verify hashing and token logic:

```bash
pytest tests/test_auth.py
```
