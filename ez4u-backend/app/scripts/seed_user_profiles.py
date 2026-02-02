import asyncio
import logging
import random
from typing import List
from faker import Faker
from sqlalchemy import select
from app.database.base import AsyncSessionLocal, engine, Base
from app.database.models import User, UserIdentity, UserAddress, UserPhoneNumber, UserEmail
from app.core.security import get_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker()

async def init_db():
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)

async def create_random_user(session, index: int):
    # 1. Basic User Info
    full_name = fake.name()
    email = fake.unique.email()
    
    user = User(
        email=email,
        full_name=full_name,
        is_active=True
    )
    session.add(user)
    await session.flush() # Get ID

    # 2. Identity (Login)
    username = f"user{index}"
    identity = UserIdentity(
        user_id=user.id,
        provider="local",
        subject=username,
        password_hash=get_password_hash("password123")
    )
    session.add(identity)

    # 3. Addresses (1-3 random addresses)
    num_addresses = random.randint(1, 3)
    for i in range(num_addresses):
        addr = UserAddress(
            user_id=user.id,
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            postal_code=fake.postcode(),
            country=fake.country(),
            is_primary=(i == 0), # First one is primary
            label=random.choice(["Home", "Work", "Billing"])
        )
        session.add(addr)

    # 4. Phone Numbers (1-2 random phones)
    num_phones = random.randint(1, 2)
    for i in range(num_phones):
        phone = UserPhoneNumber(
            user_id=user.id,
            phone_number=fake.phone_number(),
            is_primary=(i == 0),
            label=random.choice(["Mobile", "Home", "Work"]),
            is_verified=random.choice([True, False])
        )
        session.add(phone)

    # 5. Secondary Emails (0-2 random emails)
    num_emails = random.randint(0, 2)
    for i in range(num_emails):
        email_entry = UserEmail(
            user_id=user.id,
            email=fake.email(),
            is_primary=False, # Main user.email is primary
            label=random.choice(["Personal", "Work", "Recovery"]),
            verified_at=fake.date_time_this_year() if random.choice([True, False]) else None
        )
        session.add(email_entry)

    logger.info(f"Created User: {username} ({full_name}) with {num_addresses} addresses, {num_phones} phones")

async def seed_profiles():
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Check if we already have users (skip if populated)
        result = await session.execute(select(User))
        existing_users = result.scalars().all()
        
        if len(existing_users) > 5: # Arbitrary check
            logger.info("Database already seems populated. Skipping massive seed.")
            return

        logger.info("Seeding 10 random users with complex profiles...")
        
        for i in range(1, 11):
            await create_random_user(session, i)
        
        await session.commit()
        logger.info("✅ Seeding Complete!")

if __name__ == "__main__":
    asyncio.run(seed_profiles())
