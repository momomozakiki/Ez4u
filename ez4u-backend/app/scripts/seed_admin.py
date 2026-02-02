import asyncio
import logging
from sqlalchemy import select
from app.database.base import AsyncSessionLocal, engine, Base
from app.database.models import User, UserIdentity
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    async with engine.begin() as conn:
        # Create tables if they don't exist (Crucial for SQLite Test Mode)
        await conn.run_sync(Base.metadata.create_all)

async def seed_admin():
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Check if admin exists
        stmt = select(UserIdentity).where(
            UserIdentity.provider == "local",
            UserIdentity.subject == "admin"
        )
        result = await session.execute(stmt)
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            logger.info("Admin user already exists.")
            return

        logger.info("Creating default admin user...")
        
        # Create User
        new_user = User(
            email="admin@ez4u.com",
            full_name="System Admin",
            is_active=True
        )
        session.add(new_user)
        await session.flush()  # To get the ID

        # Create Identity
        new_identity = UserIdentity(
            user_id=new_user.id,
            provider="local",
            subject="admin",
            password_hash=get_password_hash("admin")
        )
        session.add(new_identity)
        
        await session.commit()
        logger.info("Admin user created successfully (admin/admin).")

if __name__ == "__main__":
    asyncio.run(seed_admin())
