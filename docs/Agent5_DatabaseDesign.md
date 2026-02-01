# 🌐 FINAL SaaS DATABASE DESIGN: AI PROMPT FOR IMPLEMENTATION  
*(Copy/paste this entire block to generate production-ready code)*  

```prompt
ROLE: You are an enterprise SaaS database architect specializing in SQLAlchemy ORM (v2.0+) and PostgreSQL. Generate **production-ready, secure, scalable** code implementing the validated unified identity model below.  

## 🔑 CORE DESIGN PRINCIPLES (NON-NEGOTIABLE)  
1. **UNIFIED IDENTITY**: Single `users` table for ALL entities (SuperAdmin, tenant staff, customers)  
2. **SINGLE MEMBERSHIP TABLE**: `tenant_members` handles ALL user-tenant relationships (employees + customers)  
3. **MANY-TO-MANY SUPPORT**: One user → multiple tenants (e.g., customer in Tenant A + accountant in Tenant B)  
4. **STRICT DATA ISOLATION**: All tenant-scoped tables require `tenant_id` + RLS policies (provided as SQL comment)  
5. **TENANT-CUSTOMIZABLE RBAC**: Roles/permissions scoped per tenant; global roles separate  
6. **AUTH FLEXIBILITY**: `user_identities` supports OAuth (Google) + local auth in one table  
7. **ENTERPRISE AUDITING**: Global role assignments track `granted_by`, `expires_at`  

## 📐 TABLE SPECIFICATIONS (SQLAlchemy ORM + PostgreSQL)  
*Use modern mapped_column syntax. All PKs = UUID(as_uuid=True). All timestamps = DateTime(timezone=True).*  

### CORE IDENTITY LAYER  
```python  
# users.py  
class User(Base):  
    __tablename__ = "users"  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)  
    full_name: Mapped[Optional[str]] = mapped_column(String(255))  
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    # Relationships  
    identities: Mapped[List["UserIdentity"]] = relationship(back_populates="user", cascade="all, delete-orphan")  
    tenant_members: Mapped[List["TenantMember"]] = relationship(back_populates="user", cascade="all, delete-orphan")  
    global_roles: Mapped[List["UserGlobalRole"]] = relationship(foreign_keys="[UserGlobalRole.user_id]", back_populates="user")  
```  

```python  
# user_identities.py  
class UserIdentity(Base):  
    __tablename__ = "user_identities"  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # "google", "local", etc.  
    subject: Mapped[str] = mapped_column(String(500), nullable=False)  # OAuth sub or email  
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))  # NULL for OAuth  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    __table_args__ = (  
        UniqueConstraint("provider", "subject", name="uq_provider_subject"),  
        Index("ix_user_identities_user_id", "user_id")  
    )  
    user: Mapped["User"] = relationship(back_populates="identities")  
```  

### TENANCY & RBAC LAYER  
```python  
# tenants.py  
class Tenant(Base):  
    __tablename__ = "tenants"  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    name: Mapped[str] = mapped_column(String(255), nullable=False)  
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)  # for subdomain routing  
    parent_tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("tenants.id", ondelete="SET NULL"), index=True)  
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    # Relationships  
    parent: Mapped[Optional["Tenant"]] = relationship(remote_side=[id], backref="children")  
    roles: Mapped[List["Role"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")  
    tenant_members: Mapped[List["TenantMember"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")  
    resources: Mapped[List["Resource"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
```  

```python  
# roles.py  
class Role(Base):  
    __tablename__ = "roles"  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)  
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # "customer", "accountant", etc.  
    description: Mapped[Optional[str]] = mapped_column(Text)  
    is_system_role: Mapped[bool] = mapped_column(Boolean, default=False)  # Pre-created roles (e.g., "customer")  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    __table_args__ = (  
        UniqueConstraint("tenant_id", "name", name="uq_tenant_role_name"),  
        Index("ix_roles_tenant_id", "tenant_id")  
    )  
    tenant: Mapped["Tenant"] = relationship(back_populates="roles")  
    tenant_members: Mapped[List["TenantMember"]] = relationship(back_populates="role")  
    permissions: Mapped[List["Permission"]] = relationship(secondary="role_permissions", viewonly=True)  
```  

```python  
# tenant_members.py  
class TenantMember(Base):  
    __tablename__ = "tenant_members"  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True)  
    status: Mapped[str] = mapped_column(String(20), default="active")  # "active", "invited", "suspended"  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    __table_args__ = (  
        UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),  # CRITICAL: Prevent duplicate memberships  
        Index("ix_tenant_members_tenant_id", "tenant_id"),  
        Index("ix_tenant_members_user_id", "user_id")  
    )  
    tenant: Mapped["Tenant"] = relationship(back_populates="tenant_members")  
    user: Mapped["User"] = relationship(back_populates="tenant_members")  
    role: Mapped["Role"] = relationship(back_populates="tenant_members")  
```  

### GLOBAL ACCESS LAYER (SuperAdmin)  
```python  
# global_roles.py  
class GlobalRole(Base):  
    __tablename__ = "global_roles"  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # "superadmin", "support_agent"  
    description: Mapped[Optional[str]] = mapped_column(Text)  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    permissions: Mapped[List["Permission"]] = relationship(secondary="global_role_permissions", viewonly=True)  

class UserGlobalRole(Base):  
    __tablename__ = "user_global_roles"  
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)  
    global_role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("global_roles.id", ondelete="CASCADE"), primary_key=True)  
    granted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)  
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="global_roles")  
    granter: Mapped[Optional["User"]] = relationship(foreign_keys=[granted_by])  
    global_role: Mapped["GlobalRole"] = relationship()  
```  

### PERMISSIONS LAYER (Shared Registry)  
```python  
# permissions.py  
class Permission(Base):  
    __tablename__ = "permissions"  
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # "tenant.create", "data.view"  
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # "tenant_management", "data_access"  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  

# Association tables (no ORM class needed)  
role_permissions = Table(  
    "role_permissions",  
    Base.metadata,  
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),  
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)  
)  

global_role_permissions = Table(  
    "global_role_permissions",  
    Base.metadata,  
    Column("global_role_id", UUID(as_uuid=True), ForeignKey("global_roles.id", ondelete="CASCADE"), primary_key=True),  
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)  
)  
```  

### BUSINESS DATA LAYER (SaaS Content)
```python
# resources.py
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB

class Resource(Base):
    """Generic resource table demonstrating RLS protection"""
    __tablename__ = "resources"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # RLS CRITICAL: All business data MUST have tenant_id
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb")) # Flexible schema
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    tenant: Mapped["Tenant"] = relationship(back_populates="resources")
```

## 🌰 SAMPLE DATA SCENARIO (Generate INSERT logic demonstrating):  
*Illustrate critical relationships with 5+ rows per relevant table*  

### **users** table (6 rows - showing one user in multiple tenants)
| id | email | full_name | is_active |
|----|-------|-----------|-----------|
| 1 | superadmin@saas.com | System Admin | true |
| 2 | john.doe@gmail.com | John Doe | true |
| 3 | jane.smith@acme.com | Jane Smith | true |
| 4 | alice@initech.com | Alice Wong | true |
| 5 | bob@gmail.com | Bob Johnson | true |
| 6 | carol@umbrella.com | Carol Lee | true |

### **user_identities** table (6 rows - OAuth + local auth)
| id | user_id | provider | subject | password_hash |
|----|---------|----------|---------|---------------|
| 1 | 1 | local | superadmin@saas.com | $2b$12$hashed... |
| 2 | 2 | google | google\|123456789 | NULL |
| 3 | 3 | local | jane.smith@acme.com | $2b$12$hashed... |
| 4 | 4 | local | alice@initech.com | $2b$12$hashed... |
| 5 | 5 | google | google\|987654321 | NULL |
| 6 | 6 | local | carol@umbrella.com | $2b$12$hashed... |

### **tenants** table (5 rows - with hierarchy)
| id | name | slug | parent_tenant_id | is_active |
|----|------|------|------------------|-----------|
| 1 | Acme Corporation | acme | NULL | true |
| 2 | Globex Industries | globex | 1 | true |
| 3 | Initech Systems | initech | NULL | true |
| 4 | Umbrella Corp | umbrella | NULL | true |
| 5 | Wayne Enterprises | wayne | NULL | true |

### **roles** table (12 rows - tenant-specific roles including system roles)
| id | tenant_id | name | is_system_role |
|----|-----------|------|----------------|
| 1 | 1 | tenant_owner | true |
| 2 | 1 | customer | true |
| 3 | 1 | manager | false |
| 4 | 1 | accountant | false |
| 5 | 2 | tenant_owner | true |
| 6 | 2 | customer | true |
| 7 | 2 | accountant | false |
| 8 | 3 | tenant_owner | true |
| 9 | 3 | customer | true |
| 10 | 3 | supervisor | false |
| 11 | 4 | tenant_owner | true |
| 12 | 4 | customer | true |
| 13 | 5 | tenant_owner | true |
| 14 | 5 | customer | true |

### **tenant_members** table (CRITICAL MANY-TO-MANY - 9 rows)
| id | tenant_id | user_id | role_id | status |
|----|-----------|---------|---------|--------|
| 1 | 1 | 2 | 2 | active | *John Doe → Acme → customer* |
| 2 | 2 | 2 | 7 | active | *John Doe → Globex → accountant* |
| 3 | 1 | 3 | 1 | active | *Jane Smith → Acme → tenant_owner* |
| 4 | 3 | 4 | 8 | active | *Alice Wong → Initech → tenant_owner* |
| 5 | 4 | 5 | 12 | active | *Bob Johnson → Umbrella → customer* |
| 6 | 5 | 5 | 14 | active | *Bob Johnson → Wayne → customer* |
| 7 | 1 | 6 | 3 | active | *Carol Lee → Acme → manager* |
| 8 | 3 | 6 | 10 | active | *Carol Lee → Initech → supervisor* |
| 9 | 4 | 6 | 12 | active | *Carol Lee → Umbrella → customer* |

**KEY DEMONSTRATIONS:**
- **User 2 (John Doe)**: 2 memberships → Acme (customer) + Globex (accountant)
- **User 5 (Bob Johnson)**: 2 memberships → Umbrella (customer) + Wayne (customer)
- **User 6 (Carol Lee)**: 3 memberships → Acme (manager) + Initech (supervisor) + Umbrella (customer)
- **User 1 (SuperAdmin)**: 0 memberships → global access only

### **resources** table (7 rows — tenant-scoped business data)
| id | tenant_id | name | data |
|----|-----------|------|------|
| 1 | 1 | Q3 Sales Report | {"type": "document"} |
| 2 | 1 | Customer List | {"type": "spreadsheet"} |
| 3 | 2 | Expense Tracker | {"type": "report"} |
| 4 | 3 | Project Timeline | {"type": "document"} |
| 5 | 4 | Inventory Log | {"type": "report"} |
| 6 | 5 | Financial Summary | {"type": "document"} |
| 7 | 1 | Marketing Plan | {"type": "document"} |

### **global_roles** table (2 rows)
| id | name | description |
|----|------|-------------|
| 1 | superadmin | Full system access |
| 2 | support_agent | Limited support access |

### **user_global_roles** table (1 row)
| user_id | global_role_id | granted_by | expires_at |
|---------|----------------|------------|------------|
| 1 | 1 | NULL | NULL |

### **permissions** table (6 rows - common permissions)
| id | name | category |
|----|------|----------|
| 1 | tenant.create | tenant_management |
| 2 | tenant.update | tenant_management |
| 3 | tenant.delete | tenant_management |
| 4 | user.manage | user_management |
| 5 | data.view | data_access |
| 6 | data.export | data_access |

### **role_permissions** table (10+ rows - role-to-permission mapping)
| role_id | permission_id |
|---------|---------------|
| 1 | 1 | *tenant_owner → tenant.create* |
| 1 | 2 | *tenant_owner → tenant.update* |
| 1 | 4 | *tenant_owner → user.manage* |
| 2 | 5 | *customer → data.view* |
| 3 | 4 | *manager → user.manage* |
| 3 | 5 | *manager → data.view* |
| 4 | 5 | *accountant → data.view* |
| 4 | 6 | *accountant → data.export* |
| 7 | 5 | *accountant → data.view* |
| 7 | 6 | *accountant → data.export* |
| 10 | 5 | *supervisor → data.view* |

### **global_role_permissions** table (2 rows - superadmin has all)
| global_role_id | permission_id |
|----------------|---------------|
| 1 | 1 |
| 1 | 2 |
| 1 | 3 |
| 1 | 4 |
| 1 | 5 |
| 1 | 6 |

## 🛡️ RLS POLICY EXAMPLE (Add as SQL comment in models.py)  
```sql  
/*  
EXECUTE IN MIGRATION SCRIPT FOR ALL TENANT-SCOPED TABLES (e.g., resources):  
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;  

CREATE POLICY tenant_isolation_policy ON resources  
USING (  
  tenant_id = current_setting('app.current_tenant_id', true)::uuid  
  AND EXISTS (  
    SELECT 1 FROM tenant_members tm  
    WHERE tm.user_id = current_setting('app.current_user_id', true)::uuid  
      AND tm.tenant_id = resources.tenant_id  
      AND tm.status = 'active'  
  )  
);  

-- APPLICATION MUST SET AT REQUEST START:  
-- SET app.current_tenant_id = '<tenant_uuid>';  
-- SET app.current_user_id = '<user_uuid>';  
-- VALIDATE MEMBERSHIP BEFORE SETTING CONTEXT (prevent spoofing)  
*/  
```  

## 🚫 STRICT OUTPUT RULES  
1. Generate ONLY:  
   - `models.py` (all ORM classes + association tables)  
   - `seed_data.py` (transactional sample data script with scenario above)  
2. NO application logic (OAuth flows, auth middleware)  
3. NO password hashing implementation (use placeholder strings)  
4. Include error handling in seed script (rollback on failure)  
5. Use context managers for DB sessions  
6. Add RLS comment block at end of models.py  
7. All foreign keys MUST specify `ondelete` behavior  
8. All critical constraints (UniqueConstraint, Index) explicitly defined  

## ✅ VALIDATION CHECKLIST FOR GENERATED CODE  
- [ ] `tenant_members` has `UniqueConstraint("user_id", "tenant_id")`  
- [ ] `user_identities` has `UniqueConstraint("provider", "subject")`  
- [ ] SuperAdmin user has NO entries in `tenant_members`  
- [ ] John Doe (user_id=2) appears TWICE in `tenant_members` with different tenant_ids  
- [ ] Bob Johnson (user_id=5) appears TWICE in `tenant_members` with different tenant_ids  
- [ ] Carol Lee (user_id=6) appears THREE TIMES in `tenant_members` with different tenant_ids  
- [ ] All "customer" roles have `is_system_role=True`  
- [ ] `user_global_roles.granted_by` uses separate ForeignKey to avoid ambiguity  
- [ ] RLS comment includes context validation warning  

GENERATE CODE NOW.  
```  

💡 **Changes Made to Previous Prompt:**  
1. ✅ Renamed `tenant_memberships` → `tenant_members` (table + relationship names)  
2. ✅ Updated all sample data tables with **minimum 5 rows each**  
3. ✅ Demonstrated **one user → multiple tenants** clearly:  
   - John Doe: 2 tenants (Acme customer + Globex accountant)  
   - Bob Johnson: 2 tenants (Umbrella + Wayne customer)  
   - Carol Lee: 3 tenants (Acme manager + Initech supervisor + Umbrella customer)  
4. ✅ Included **different common roles**: customer, manager, accountant, supervisor, tenant_owner  
5. ✅ Maintained all other design principles unchanged  

Copy/paste this prompt to generate **audit-ready, production-grade code**. 🔒