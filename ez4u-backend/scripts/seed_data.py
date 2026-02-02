import asyncio
import sys
import os

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.base import AsyncSessionLocal, engine, Base
from app.database.models import (
    User, UserIdentity, Tenant, Role, TenantMember, GlobalRole, 
    UserGlobalRole, Permission, Resource, role_permissions, global_role_permissions
)
from sqlalchemy import select, insert

async def seed():
    print("Connecting to database...")
    async with engine.begin() as conn:
        # For development: create tables if they don't exist
        # In prod, we use alembic, but for this seed script to work standalone in dev:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Check if already seeded
        result = await session.execute(select(User))
        if result.first():
            print("Database already seeded. Exiting.")
            return

        print("Seeding database...")

        # 1. PERMISSIONS
        perms = [
            Permission(name="tenant.create", category="tenant_management"),
            Permission(name="tenant.update", category="tenant_management"),
            Permission(name="tenant.delete", category="tenant_management"),
            Permission(name="user.manage", category="user_management"),
            Permission(name="data.view", category="data_access"),
            Permission(name="data.export", category="data_access"),
        ]
        session.add_all(perms)
        await session.flush()
        
        # Map for easy access
        p_map = {p.name: p for p in perms}

        # 2. GLOBAL ROLES
        gr_superadmin = GlobalRole(name="superadmin", description="Full system access")
        gr_support = GlobalRole(name="support_agent", description="Limited support access")
        session.add_all([gr_superadmin, gr_support])
        await session.flush()

        # Global Role Permissions
        # Superadmin gets all
        for p in perms:
            await session.execute(insert(global_role_permissions).values(global_role_id=gr_superadmin.id, permission_id=p.id))

        # 3. USERS
        users = [
            User(email="superadmin@saas.com", full_name="System Admin"),
            User(email="john.doe@gmail.com", full_name="John Doe"),
            User(email="jane.smith@acme.com", full_name="Jane Smith"),
            User(email="alice@initech.com", full_name="Alice Wong"),
            User(email="bob@gmail.com", full_name="Bob Johnson"),
            User(email="carol@umbrella.com", full_name="Carol Lee"),
        ]
        session.add_all(users)
        await session.flush()
        u_map = {u.email: u for u in users}

        # 4. USER IDENTITIES
        identities = [
            UserIdentity(user_id=u_map["superadmin@saas.com"].id, provider="local", subject="superadmin@saas.com", password_hash="hashed_secret"),
            UserIdentity(user_id=u_map["john.doe@gmail.com"].id, provider="google", subject="google|123456789"),
            UserIdentity(user_id=u_map["jane.smith@acme.com"].id, provider="local", subject="jane.smith@acme.com", password_hash="hashed_secret"),
            UserIdentity(user_id=u_map["alice@initech.com"].id, provider="local", subject="alice@initech.com", password_hash="hashed_secret"),
            UserIdentity(user_id=u_map["bob@gmail.com"].id, provider="google", subject="google|987654321"),
            UserIdentity(user_id=u_map["carol@umbrella.com"].id, provider="local", subject="carol@umbrella.com", password_hash="hashed_secret"),
        ]
        session.add_all(identities)

        # Assign Global Role to Superadmin
        session.add(UserGlobalRole(user_id=u_map["superadmin@saas.com"].id, global_role_id=gr_superadmin.id))

        # 5. TENANTS
        tenants = [
            Tenant(name="Acme Corporation", slug="acme"),
            Tenant(name="Initech Systems", slug="initech"),
            Tenant(name="Umbrella Corp", slug="umbrella"),
            Tenant(name="Wayne Enterprises", slug="wayne"),
        ]
        session.add_all(tenants)
        await session.flush()
        t_map = {t.slug: t for t in tenants}
        
        # Globex is child of Acme
        t_globex = Tenant(name="Globex Industries", slug="globex", parent_tenant_id=t_map["acme"].id)
        session.add(t_globex)
        await session.flush()
        t_map["globex"] = t_globex

        # 6. ROLES (Per Tenant)
        # Helper to create standard roles for a tenant
        async def create_tenant_roles(tenant):
            r_owner = Role(tenant_id=tenant.id, name="tenant_owner", is_system_role=True)
            r_customer = Role(tenant_id=tenant.id, name="customer", is_system_role=True)
            session.add_all([r_owner, r_customer])
            await session.flush()
            
            # Permissions
            await session.execute(insert(role_permissions).values(role_id=r_owner.id, permission_id=p_map["tenant.create"].id))
            await session.execute(insert(role_permissions).values(role_id=r_owner.id, permission_id=p_map["tenant.update"].id))
            await session.execute(insert(role_permissions).values(role_id=r_owner.id, permission_id=p_map["user.manage"].id))
            await session.execute(insert(role_permissions).values(role_id=r_customer.id, permission_id=p_map["data.view"].id))
            
            return {"owner": r_owner, "customer": r_customer}

        roles_acme = await create_tenant_roles(t_map["acme"])
        roles_globex = await create_tenant_roles(t_map["globex"])
        roles_initech = await create_tenant_roles(t_map["initech"])
        roles_umbrella = await create_tenant_roles(t_map["umbrella"])
        roles_wayne = await create_tenant_roles(t_map["wayne"])

        # Custom roles
        r_acme_manager = Role(tenant_id=t_map["acme"].id, name="manager", is_system_role=False)
        r_globex_accountant = Role(tenant_id=t_map["globex"].id, name="accountant", is_system_role=False)
        r_initech_supervisor = Role(tenant_id=t_map["initech"].id, name="supervisor", is_system_role=False)
        
        session.add_all([r_acme_manager, r_globex_accountant, r_initech_supervisor])
        await session.flush()

        # Add perms for custom roles
        await session.execute(insert(role_permissions).values(role_id=r_acme_manager.id, permission_id=p_map["user.manage"].id))
        await session.execute(insert(role_permissions).values(role_id=r_globex_accountant.id, permission_id=p_map["data.view"].id))
        await session.execute(insert(role_permissions).values(role_id=r_initech_supervisor.id, permission_id=p_map["data.view"].id))

        # 7. TENANT MEMBERS (The Many-to-Many Logic)
        members = [
            # John Doe -> Acme (customer) + Globex (accountant)
            TenantMember(tenant_id=t_map["acme"].id, user_id=u_map["john.doe@gmail.com"].id, role_id=roles_acme["customer"].id),
            TenantMember(tenant_id=t_map["globex"].id, user_id=u_map["john.doe@gmail.com"].id, role_id=r_globex_accountant.id),
            
            # Jane Smith -> Acme (owner)
            TenantMember(tenant_id=t_map["acme"].id, user_id=u_map["jane.smith@acme.com"].id, role_id=roles_acme["owner"].id),
            
            # Alice Wong -> Initech (owner)
            TenantMember(tenant_id=t_map["initech"].id, user_id=u_map["alice@initech.com"].id, role_id=roles_initech["owner"].id),
            
            # Bob Johnson -> Umbrella (customer) + Wayne (customer)
            TenantMember(tenant_id=t_map["umbrella"].id, user_id=u_map["bob@gmail.com"].id, role_id=roles_umbrella["customer"].id),
            TenantMember(tenant_id=t_map["wayne"].id, user_id=u_map["bob@gmail.com"].id, role_id=roles_wayne["customer"].id),
            
            # Carol Lee -> Acme (manager) + Initech (supervisor) + Umbrella (customer)
            TenantMember(tenant_id=t_map["acme"].id, user_id=u_map["carol@umbrella.com"].id, role_id=r_acme_manager.id),
            TenantMember(tenant_id=t_map["initech"].id, user_id=u_map["carol@umbrella.com"].id, role_id=r_initech_supervisor.id),
            TenantMember(tenant_id=t_map["umbrella"].id, user_id=u_map["carol@umbrella.com"].id, role_id=roles_umbrella["customer"].id),
        ]
        session.add_all(members)

        # 8. RESOURCES (Validation Data)
        resources = [
            Resource(tenant_id=t_map["acme"].id, name="Q3 Sales Report", data={"type": "document"}),
            Resource(tenant_id=t_map["acme"].id, name="Customer List", data={"type": "spreadsheet"}),
            Resource(tenant_id=t_map["globex"].id, name="Expense Tracker", data={"type": "report"}),
            Resource(tenant_id=t_map["initech"].id, name="Project Timeline", data={"type": "document"}),
            Resource(tenant_id=t_map["umbrella"].id, name="Inventory Log", data={"type": "report"}),
            Resource(tenant_id=t_map["wayne"].id, name="Financial Summary", data={"type": "document"}),
            Resource(tenant_id=t_map["acme"].id, name="Marketing Plan", data={"type": "document"}),
        ]
        session.add_all(resources)

        await session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    try:
        asyncio.run(seed())
    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)
