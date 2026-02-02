from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import AsyncSessionLocal
from app.database.models import User

router = APIRouter()

# Dependency
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# Pydantic Models
class UserAddressResponse(BaseModel):
    id: UUID
    street: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str
    is_primary: bool
    label: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserPhoneNumberResponse(BaseModel):
    id: UUID
    phone_number: str
    is_primary: bool
    label: Optional[str] = None
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)

class UserEmailResponse(BaseModel):
    id: UUID
    email: str
    is_primary: bool
    label: Optional[str] = None
    verified_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class UserDetailResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    addresses: List[UserAddressResponse]
    phone_numbers: List[UserPhoneNumberResponse]
    emails: List[UserEmailResponse]

    model_config = ConfigDict(from_attributes=True)

@router.get("/users", response_model=List[UserDetailResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    stmt = select(User).options(
        selectinload(User.addresses),
        selectinload(User.phone_numbers),
        selectinload(User.emails)
    )
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users
