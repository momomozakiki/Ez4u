I will implement the **Agent 5 (Data Foundation)** layer within the `ez4u-backend` directory, strictly following the specifications in `Agent5_DatabaseDesign.md`.

### **Phase 1: Database Scaffolding**
1.  **Create Directory Structure:**
    *   `ez4u-backend/app/database/` - For core database logic.
    *   `ez4u-backend/scripts/` - For administrative scripts (seeding).

2.  **Implement Core Infrastructure (`app/database/base.py`):**
    *   Setup `SQLAlchemy` async engine and `DeclarativeBase`.
    *   Configure `AsyncSession` factory.

### **Phase 2: Schema Implementation**
3.  **Create Models (`app/database/models.py`):**
    *   Implement all ORM classes: `User`, `UserIdentity`, `Tenant`, `Role`, `TenantMember`, `GlobalRole`, `Permission`, `Resource`.
    *   Apply all constraints: `UniqueConstraint`, `ForeignKey(ondelete="CASCADE")`, and Indexes.
    *   Add the **RLS Policy** as a SQL comment block at the end of the file.

### **Phase 3: Data Seeding & Validation**
4.  **Create Seed Script (`scripts/seed_data.py`):**
    *   Implement the transaction logic to insert the 6 Users, 5 Tenants, and 9 Memberships defined in the design doc.
    *   Include the "Resources" sample data (7 rows) to validate RLS.
    *   Add error handling to rollback on failure.

### **Phase 4: Alembic Setup (Migration Engine)**
5.  **Initialize Alembic:**
    *   Run `alembic init -t async migrations` (if not already present).
    *   Configure `alembic.ini` and `env.py` to use the async engine and import `models.py`.

*Note: I will use standard environment variable patterns (e.g., `DATABASE_URL`) for connection strings.*