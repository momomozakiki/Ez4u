from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
import os

# Check for TEST_MODE flag
TEST_MODE = os.getenv("TEST_MODE", "False").lower() == "true"

if TEST_MODE:
    # Use SQLite for testing/dev if explicitly requested
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"
    print("⚠️  RUNNING IN TEST MODE: Using SQLite database")
else:
    # Default to Golden State Postgres
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/ez4u")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass
