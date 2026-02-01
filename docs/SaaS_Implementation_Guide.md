# 📋 SaaS DATABASE DESIGN: CORE REQUIREMENTS & ANTI-PATTERNS  
*SQLAlchemy ORM Implementation Guide (PostgreSQL)*  

--- 

## ✅ MUST DO: Critical Requirements (Non-Negotiable) 

### Identity Layer (`users` + `user_identities`) 
| Rule | Why | Example | 
|------|-----|---------| 
| **✅ ONE human = ONE `users` record** | Prevents duplicate identities across tenants | John Doe (human) → `users.id = u123` (never duplicated) | 
| **✅ Authentication method = `user_identities` record** | Enables multiple login methods per human | John has 2 identities: `(google, sub123)` + `(local, john@acme.com)` | 
| **✅ `UniqueConstraint("provider", "subject")` on `user_identities`** | Prevents duplicate OAuth logins | Google `sub123` can't map to 2 different humans | 
| **✅ `password_hash` ONLY for `provider='local'`** | Security best practice | OAuth identities MUST have `password_hash = NULL` | 
| **✅ Tenant staff creation → HARD-CODE `provider='local'`** | Enforces your business rule | `UserIdentity(provider='local', ...)` during tenant bootstrap | 

### Tenancy Layer (`tenants` + `tenant_members`) 
| Rule | Why | Example | 
|------|-----|---------| 
| **✅ `tenant_members` = ONLY bridge between users/tenants** | Enables true many-to-many relationships | John → Acme (customer) + John → Globex (accountant) = 2 rows | 
| **✅ `UniqueConstraint("user_id", "tenant_id")` on `tenant_members`** | Prevents duplicate memberships | Same user can't have 2 roles in same tenant (use role hierarchy instead) | 
| **✅ ALL business tables MUST have `tenant_id` FK** | Enables RLS data isolation | `resources.tenant_id` → RLS policy enforcement | 
| **✅ System roles created during tenant bootstrap** | Ensures consistent customer experience | Auto-create `roles(name='customer', is_system_role=True)` per tenant | 
| **✅ Customer OAuth flow → auto-create `tenant_members`** | Seamless onboarding | Google login at `acme.app.com` → auto-membership with `role='customer'` | 

### Security Layer (RLS + Application Context) 
| Rule | Why | Example | 
|------|-----|---------| 
| **✅ RLS policies on ALL tenant-scoped tables** | Database-enforced isolation (not app-layer) | `CREATE POLICY ... ON resources USING (tenant_id = current_setting('app.current_tenant_id'))` | 
| **✅ Context validation BEFORE setting RLS variables** | Prevents tenant spoofing attacks | `if tenant not in user.memberships: raise SecurityError()` | 
| **✅ SuperAdmin has ZERO `tenant_members` records** | Global access ≠ tenant membership | SuperAdmin bypasses RLS via global role checks | 
| **✅ `ondelete="CASCADE"` on tenant-scoped FKs** | Prevents orphaned data on tenant deletion | `resources.tenant_id` → cascade delete on tenant removal | 

--- 

## ⚠️ SHOULD DO: Best Practices (Strongly Recommended) 

| Area | Recommendation | Why | 
|------|----------------|-----| 
| **Password Management** | Store bcrypt hashes with work factor ≥12 | Industry standard security | 
| **Tenant Slug Validation** | Enforce `[a-z0-9-]{3,50}` regex | Prevents subdomain routing conflicts | 
| **Membership Status** | Use `'active'`, `'invited'`, `'suspended'` | Enables invitation flows + soft deletes | 
| **Global Role Expiry** | Set `expires_at` for support agents | Least privilege principle | 
| **Audit Columns** | `created_at`/`updated_at` on ALL tables | Critical for compliance investigations | 
| **Indexing** | Index all FK columns + `tenant_id` | Query performance at scale (>10k tenants) | 
| **JSONB Validation** | Add CHECK constraint for required fields | Prevents malformed tenant data | 

--- 

## ❌ MUST NOT DO: Critical Anti-Patterns (Security Risks) 

### Identity Anti-Patterns 
| Anti-Pattern | Risk | Correct Approach | 
|--------------|------|------------------| 
| **❌ Merge identities into `users` table** | Can't support multiple auth methods per human | Keep `user_identities` separate | 
| **❌ Allow OAuth identities for tenant staff** | Breaks your "local auth only" requirement | Application must enforce `provider='local'` during tenant creation | 
| **❌ Store passwords for OAuth identities** | Security violation (OAuth shouldn't have passwords) | `password_hash = NULL` for non-local providers | 
| **❌ Use email as primary identity key** | Email changes break authentication | Use `provider+subject` as identity key | 

### Tenancy Anti-Patterns 
| Anti-Pattern | Risk | Correct Approach | 
|--------------|------|------------------| 
| **❌ Add `tenant_id` column to `users` table** | Breaks many-to-many relationships | Use `tenant_members` bridge table | 
| **❌ Skip `tenant_id` on business tables** | RLS impossible → data leakage risk | ALL tenant data MUST have `tenant_id` FK | 
| **❌ Allow customers to create tenants** | Violates your business rule | Application must check `role.permissions` before tenant creation | 
| **❌ Store tenant data in separate schemas** | Operational nightmare at scale | Shared schema + RLS = cloud-native approach | 

### Security Anti-Patterns 
| Anti-Pattern | Risk | Correct Approach | 
|--------------|------|------------------| 
| **❌ Rely on app-layer filtering only** | Single bug → cross-tenant data leak | RLS policies enforced at PostgreSQL level | 
| **❌ Set RLS context without validation** | Tenant spoofing via header injection | Validate membership BEFORE `SET app.current_tenant_id` | 
| **❌ Use boolean `is_superadmin` flag** | No audit trail, no temporary access | Use `user_global_roles` with `granted_by` + `expires_at` | 
| **❌ Hardcode tenant IDs in queries** | Accidental cross-tenant queries | Always use RLS context variables | 

--- 

## 🔑 KEY CONCEPTS: Why This Design Works 

### The Identity Separation Principle 
```python 
# ✅ CORRECT: Human identity vs. authentication method 
user = User(email="john@acme.com")          # ← Human (1 per person) 
identity1 = UserIdentity(                   # ← Login method #1 
    user_id=user.id, 
    provider="local", 
    subject="john@acme.com", 
    password_hash="bcrypt..." 
) 
identity2 = UserIdentity(                   # ← Login method #2 
    user_id=user.id, 
    provider="google", 
    subject="google|abc123", 
    password_hash=None  # OAuth has no password 
) 

# ❌ WRONG: Merged identity (breaks multi-auth) 
user = User( 
    email="john@acme.com", 
    password_hash="...",      # ← What if he also uses Google? 
    google_sub="abc123"       # ← Schema explosion! 
) 
``` 

### The Membership Bridge Principle 
```python 
# ✅ CORRECT: Many-to-many via bridge table 
tenant_members = [ 
    TenantMember(user_id=u123, tenant_id=t_acme, role_id=r_customer), 
    TenantMember(user_id=u123, tenant_id=t_globex, role_id=r_accountant), 
    TenantMember(user_id=u123, tenant_id=t_initech, role_id=r_supervisor) 
] 

# ❌ WRONG: Single tenant_id column (breaks multi-tenancy) 
user = User( 
    email="john@acme.com", 
    tenant_id=t_acme  # ← Can't belong to Globex/Initech! 
) 
``` 

### The RLS Enforcement Principle 
```sql 
-- ✅ CORRECT: Database-enforced isolation 
CREATE POLICY tenant_isolation ON resources 
USING (tenant_id = current_setting('app.current_tenant_id')::uuid); 

-- Application sets context AFTER validation: 
BEGIN; 
SELECT validate_membership('u123', 't_acme');  -- ← Critical validation step 
SET app.current_tenant_id = 't_acme'; 
SELECT * FROM resources;  -- ← PostgreSQL auto-filters to tenant_id='t_acme' 
COMMIT; 

-- ❌ WRONG: App-layer filtering only (vulnerable to bugs) 
# Python pseudo-code (DANGEROUS): 
resources = Resource.query.all()  # ← Fetches ALL tenants' data! 
filtered = [r for r in resources if r.tenant_id == current_tenant_id]  # ← Bug here = data leak 
``` 

--- 

## 🧪 VALIDATION CHECKLIST FOR IMPLEMENTATION 

Before deploying, verify these **critical checks** pass: 

### Identity Layer Checks 
- [ ] `SELECT COUNT(*) FROM user_identities WHERE provider != 'local' AND password_hash IS NOT NULL` → **MUST RETURN 0**  
  *(OAuth identities must never have passwords)* 
- [ ] `SELECT user_id, COUNT(*) FROM user_identities GROUP BY user_id HAVING COUNT(*) > 1` → **Allowed**  
  *(One human CAN have multiple identities)* 
- [ ] Tenant creation flow → `INSERT INTO user_identities (provider) VALUES ('local')` → **MUST SUCCEED**  
- [ ] Tenant creation flow → `INSERT INTO user_identities (provider) VALUES ('google')` → **MUST FAIL** (app-layer enforcement) 

### Tenancy Layer Checks 
- [ ] `SELECT user_id, tenant_id, COUNT(*) FROM tenant_members GROUP BY 1,2 HAVING COUNT(*) > 1` → **MUST RETURN 0**  
  *(UniqueConstraint enforcement)* 
- [ ] `SELECT * FROM tenant_members WHERE user_id = 'superadmin_id'` → **MUST RETURN 0 ROWS**  
  *(SuperAdmin has no tenant memberships)* 
- [ ] OAuth customer login → `INSERT INTO tenant_members (role_id) SELECT id FROM roles WHERE name='customer'` → **MUST SUCCEED** 

### Security Layer Checks 
- [ ] `SELECT COUNT(*) FROM pg_policies WHERE tablename = 'resources'` → **MUST BE ≥1**  
  *(RLS policy exists)* 
- [ ] Direct DB query without context → `SELECT * FROM resources` → **MUST RETURN 0 ROWS**  
  *(RLS blocks access without context)* 
- [ ] Context spoofing attempt → `SET app.current_tenant_id = 'other_tenant_id'` → **MUST FAIL** at app layer before query execution 

--- 

## 💡 IMPLEMENTATION SNIPPETS (SQLAlchemy ORM) 

### Tenant Creation Flow (Enforcing Local Auth Only) 
```python 
# ✅ CORRECT: Hardcode provider='local' for tenant staff 
def create_tenant(superadmin_user, tenant_name: str, owner_email: str, owner_password: str): 
    with Session() as session: 
        # 1. Create tenant 
        tenant = Tenant(name=tenant_name, slug=slugify(tenant_name)) 
        session.add(tenant) 
        session.flush()  # Get tenant.id 
        
        # 2. Create system roles (including 'customer') 
        customer_role = Role( 
            tenant_id=tenant.id, 
            name="customer", 
            is_system_role=True, 
            description="Auto-created customer role" 
        ) 
        owner_role = Role( 
            tenant_id=tenant.id, 
            name="tenant_owner", 
            is_system_role=True, 
            description="Full tenant access" 
        ) 
        session.add_all([customer_role, owner_role]) 
        session.flush() 
        
        # 3. Create OWNER USER with LOCAL IDENTITY ONLY ⚠️ CRITICAL 
        owner_user = User(email=owner_email, full_name="Tenant Owner") 
        session.add(owner_user) 
        session.flush() 
        
        # ⚠️ HARD-CODE provider='local' - NO OAUTH ALLOWED HERE 
        owner_identity = UserIdentity( 
            user_id=owner_user.id, 
            provider="local",  # ← ENFORCED BY BUSINESS RULE 
            subject=owner_email, 
            password_hash=hash_password(owner_password)  # bcrypt hash 
        ) 
        session.add(owner_identity) 
        
        # 4. Create membership with owner role 
        membership = TenantMember( 
            user_id=owner_user.id, 
            tenant_id=tenant.id, 
            role_id=owner_role.id, 
            status="active" 
        ) 
        session.add(membership) 
        session.commit() 
``` 

### Customer OAuth Flow (Auto-Creating Membership) 
```python 
# ✅ CORRECT: Auto-create customer membership on first OAuth login 
def handle_oauth_callback(tenant_slug: str, oauth_provider: str, oauth_subject: str): 
    with Session() as session: 
        # 1. Resolve tenant from context (subdomain/URL) 
        tenant = session.execute( 
            select(Tenant).where(Tenant.slug == tenant_slug, Tenant.is_active == True) 
        ).scalar_one() 
        
        # 2. Find or create user + identity 
        identity = session.execute( 
            select(UserIdentity) 
            .where(UserIdentity.provider == oauth_provider, UserIdentity.subject == oauth_subject) 
            .options(joinedload(UserIdentity.user)) 
        ).scalar_one_or_none() 
        
        if not identity: 
            # Create new human + identity 
            user = User(email=None, full_name=None)  # Email may come later from OAuth profile 
            session.add(user) 
            session.flush() 
            
            identity = UserIdentity( 
                user_id=user.id, 
                provider=oauth_provider, 
                subject=oauth_subject, 
                password_hash=None  # OAuth has no password 
            ) 
            session.add(identity) 
            session.flush() 
        else: 
            user = identity.user 
        
        # 3. Auto-create customer membership if missing ⚠️ KEY REQUIREMENT 
        existing_membership = session.execute( 
            select(TenantMember) 
            .where(TenantMember.user_id == user.id, TenantMember.tenant_id == tenant.id) 
        ).scalar_one_or_none() 
        
        if not existing_membership: 
            # Get system 'customer' role for this tenant 
            customer_role = session.execute( 
                select(Role) 
                .where(Role.tenant_id == tenant.id, Role.name == "customer", Role.is_system_role == True) 
            ).scalar_one() 
            
            membership = TenantMember( 
                user_id=user.id, 
                tenant_id=tenant.id, 
                role_id=customer_role.id, 
                status="active" 
            ) 
            session.add(membership) 
            session.commit()  # Commit before login to persist membership 
        
        # 4. Login user + set RLS context (after validation!) 
        return login_user_with_tenant_context(user.id, tenant.id) 
``` 

--- 

## 🚨 FINAL WARNING: Where Security Lives 

| Layer | Responsibility | Your Requirement Enforcement | 
|-------|----------------|------------------------------| 
| **Database Schema** | Enforce data integrity (FKs, constraints) | ✅ `UniqueConstraint` prevents duplicate memberships | 
| **RLS Policies** | Enforce tenant data isolation | ✅ PostgreSQL blocks cross-tenant queries | 
| **Application Logic** | Enforce business rules (auth types, permissions) | ⚠️ **YOUR CODE MUST ENFORCE**: <br> • Tenant staff = local auth only <br> • Customers = OAuth only <br> • Context validation before RLS | 
| **UI/UX** | Guide users to correct login flows | ✅ Show password fields ONLY for tenant staff login pages | 

> 🔑 **Golden Rule**: The database provides the *foundation* for security (isolation, integrity). **Your application code provides the enforcement** of business rules (auth types, permissions). Never rely on UI alone to enforce security boundaries. 
