import asyncio
import uuid
import random
import sys
import os

# Add the current directory to sys.path to ensure we can import app modules
sys.path.append(os.getcwd())

from sqlalchemy import select
from app.database.base import AsyncSessionLocal
from app.database.models import User, Tenant, Role, TenantMember, UserEmail, UserPhoneNumber, UserAddress

# Constants
TENANT_NAMES = ["Acme Corp", "Globex", "Soylent Corp", "Umbrella Corp", "Stark Ind"]
SUB_TENANT_SUFFIXES = ["North", "South", "Labs", "Retail", "Ops"]
FIRST_NAMES = ["John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"]
LAST_NAMES = ["Smith", "Doe", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis", "Garcia", "Rodriguez"]

async def seed_data():
    async with AsyncSessionLocal() as db:
        print("🌱 Seeding 100 hierarchical users...")
        
        # 1. Create Root Tenants
        root_tenants = []
        for name in TENANT_NAMES:
            tenant = Tenant(
                name=name,
                slug=name.lower().replace(" ", "-"),
                is_active=True
            )
            db.add(tenant)
            root_tenants.append(tenant)
        
        await db.flush() # flush to get IDs

        # 2. Create Roles for each Tenant (Standard roles)
        # We need to create specific Role entities for each tenant because Roles are scoped to Tenants in this schema
        tenant_roles_map = {} # {tenant_id: {role_name: role_obj}}
        
        all_tenants = list(root_tenants)
        
        # Create Sub-Tenants
        for root in root_tenants:
            # Create 2 sub-tenants
            for i in range(2):
                sub_name = f"{root.name} {SUB_TENANT_SUFFIXES[i]}"
                sub_tenant = Tenant(
                    name=sub_name,
                    slug=sub_name.lower().replace(" ", "-"),
                    parent_tenant_id=root.id,
                    is_active=True
                )
                db.add(sub_tenant)
                all_tenants.append(sub_tenant)
        
        await db.flush()

        # Create Roles for ALL tenants
        for tenant in all_tenants:
            roles = {}
            for role_name in ["admin", "staff", "customer"]:
                role = Role(
                    tenant_id=tenant.id,
                    name=role_name,
                    description=f"{role_name.capitalize()} role for {tenant.name}",
                    is_system_role=True
                )
                db.add(role)
                roles[role_name] = role
            tenant_roles_map[tenant.id] = roles
        
        await db.flush()

        # 3. Create Users linked to Tenants
        users_created = 0
        
        for tenant in all_tenants:
            # Determine distribution based on hierarchy level (Root vs Sub)
            # Root: 1 Admin, 2 Staff, 5 Customers
            # Sub: 1 Admin, 3 Staff, 5 Customers
            
            # Create Admin
            await create_user_with_role(db, tenant, tenant_roles_map[tenant.id]["admin"], "admin")
            users_created += 1
            
            # Create Staff (2-3)
            for _ in range(random.randint(2, 3)):
                await create_user_with_role(db, tenant, tenant_roles_map[tenant.id]["staff"], "staff")
                users_created += 1
                
            # Create Customers (5-8)
            for _ in range(random.randint(5, 8)):
                await create_user_with_role(db, tenant, tenant_roles_map[tenant.id]["customer"], "customer")
                users_created += 1

        await db.commit()
        print(f"✅ Successfully seeded {users_created} users across {len(all_tenants)} tenants.")

async def create_user_with_role(db, tenant, role, role_name_str):
    f_name = random.choice(FIRST_NAMES)
    l_name = random.choice(LAST_NAMES)
    full_name = f"{f_name} {l_name}"
    # Ensure unique email
    email = f"{f_name.lower()}.{l_name.lower()}.{uuid.uuid4().hex[:6]}@example.com"
    
    user = User(
        email=email,
        full_name=full_name,
        is_active=True
    )
    db.add(user)
    await db.flush() # get user ID
    
    # Link to Tenant
    member = TenantMember(
        tenant_id=tenant.id,
        user_id=user.id,
        role_id=role.id,
        status="active"
    )
    db.add(member)
    
    # Add Phone
    phone = UserPhoneNumber(
        user_id=user.id,
        phone_number=f"+1-555-01{random.randint(10, 99)}",
        is_primary=True,
        is_verified=True
    )
    db.add(phone)
    
    # Add Email (Detail)
    u_email = UserEmail(
        user_id=user.id,
        email=email,
        is_primary=True,
        verified_at=None
    )
    db.add(u_email)

    # Add Address (Randomly)
    if random.choice([True, False]):
        addr = UserAddress(
            user_id=user.id,
            street=f"{random.randint(100, 999)} Main St",
            city="Metropolis",
            state="NY",
            postal_code="10001",
            country="USA",
            is_primary=True
        )
        db.add(addr)

if __name__ == "__main__":
    asyncio.run(seed_data())
