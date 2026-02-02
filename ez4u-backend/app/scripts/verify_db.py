import asyncio
import os
from sqlalchemy import select
from app.database.base import AsyncSessionLocal
from app.database.models import User, UserIdentity
from app.core.security import verify_password

async def verify():
    print(f"Checking Database: {os.getenv('DATABASE_URL')}")
    async with AsyncSessionLocal() as session:
        # Check Users
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"\nTotal Users: {len(users)}")
        for u in users:
            print(f" - ID: {u.id}, Email: {u.email}")

        # Check Identities
        result = await session.execute(select(UserIdentity))
        identities = result.scalars().all()
        print(f"\nTotal Identities: {len(identities)}")
        for i in identities:
            print(f" - UserID: {i.user_id}, Provider: {i.provider}, Subject: {i.subject}")
            hash_val = i.password_hash or "None"
            print(f"   Hash: {hash_val[:20]}...")
            
            # Test 'admin' password
            if i.subject == "admin" and i.password_hash:
                is_valid = verify_password("admin", i.password_hash)
                print(f"   >>> Password 'admin' valid? {is_valid}")

if __name__ == "__main__":
    asyncio.run(verify())
