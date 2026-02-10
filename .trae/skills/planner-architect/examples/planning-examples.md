# Planning Examples

## Example 1: User Authentication Feature Plan

### Stack Verification
```
Verified: Next.js v14.0.0, Python v3.12, FastAPI v0.104.1
Architecture: Standard TRAE Stack (Next.js + FastAPI + SQLAlchemy)
```

### Implementation Plan
```markdown
## Phase 1: Foundation (Database & Models)
- [ ] **[Agent: Data-Foundation]** Create migration for table `users` (Ref: sqlalchemy-orm-database-rules)
- [ ] **[Agent: Data-Foundation]** Create migration for table `sessions` with user_id foreign key
- [ ] **[Agent: Backend-Kernel]** Define Pydantic models for `User` schema (email, password_hash, created_at)
- [ ] **[Agent: Backend-Kernel]** Define Pydantic models for `Session` schema (token, expires_at)

## Phase 2: Core Logic (Backend)
- [ ] **[Agent: Backend-Kernel]** Implement `UserService` class with business logic
- [ ] **[Agent: Backend-Kernel]** Implement `AuthService` with password hashing (bcrypt)
- [ ] **[Agent: API-Gateway]** Create FastAPI route `POST /auth/register`
- [ ] **[Agent: API-Gateway]** Create FastAPI route `POST /auth/login`
- [ ] **[Agent: API-Gateway]** Create FastAPI route `POST /auth/logout`

## Phase 3: BFF Layer (Next.js API)
- [ ] **[Agent: BFF-Bridge]** Create Next.js API route `/api/auth/register`
- [ ] **[Agent: BFF-Bridge]** Create Next.js API route `/api/auth/login`
- [ ] **[Agent: BFF-Bridge]** Create Next.js API route `/api/auth/logout`
- [ ] **[Agent: BFF-Bridge]** Implement session management middleware

## Phase 4: Frontend Components
- [ ] **[Agent: Frontend-UI]** Create `LoginForm` component with validation
- [ ] **[Agent: Frontend-UI]** Create `RegisterForm` component with validation
- [ ] **[Agent: Frontend-UI]** Create `AuthProvider` context for session state
- [ ] **[Agent: Frontend-UI]** Implement protected route wrapper
```

## Example 2: Database Schema Update Plan

### Stack Verification
```
Verified: SQLAlchemy v2.0.23, Alembic v1.12.1, PostgreSQL v15
Architecture: Standard ORM with Migration Pattern
```

### Implementation Plan
```markdown
## Phase 1: Schema Analysis
- [ ] **[Agent: Data-Foundation]** Analyze existing `products` table structure
- [ ] **[Agent: Data-Foundation]** Identify foreign key constraints and indexes
- [ ] **[Agent: Data-Foundation]** Check for existing data that might conflict

## Phase 2: Migration Creation
- [ ] **[Agent: Data-Foundation]** Create Alembic migration for adding `category_id` column
- [ ] **[Agent: Data-Foundation]** Add foreign key constraint to `categories` table
- [ ] **[Agent: Data-Foundation]** Create index on `category_id` for performance
- [ ] **[Agent: Data-Foundation]** Set up cascade behavior for deletes

## Phase 3: Model Updates
- [ ] **[Agent: Backend-Kernel]** Update `Product` Pydantic model with `category_id` field
- [ ] **[Agent: Backend-Kernel]** Update `Product` SQLAlchemy model with relationship
- [ ] **[Agent: Backend-Kernel]** Add validation for category existence
- [ ] **[Agent: Backend-Kernel]** Update CRUD operations to handle category
```
