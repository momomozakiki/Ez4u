from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import AsyncSessionLocal
from app.database.models import User, TenantMember, Role, Tenant

router = APIRouter()

# Dependency
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# Pydantic Models
class UserRoleInfo(BaseModel):
    tenant_name: str
    role_name: str
    
    model_config = ConfigDict(from_attributes=True)

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
    roles: List[UserRoleInfo] = []

    model_config = ConfigDict(from_attributes=True)
    
    @staticmethod
    def from_orm_custom(user: User, filter_tenant_id: Optional[UUID] = None):
        # Manually map roles from tenant_members
        roles = []
        for tm in user.tenant_members:
            if tm.tenant and tm.role:
                # If a filter is active, only include roles for that tenant
                if filter_tenant_id and tm.tenant_id != filter_tenant_id:
                    continue
                roles.append(UserRoleInfo(tenant_name=tm.tenant.name, role_name=tm.role.name))
        
        # Create response object (Pydantic v2 style)
        return UserDetailResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            addresses=user.addresses,
            phone_numbers=user.phone_numbers,
            emails=user.emails,
            roles=roles
        )

@router.get("/users", response_model=List[UserDetailResponse])
async def read_users(
    tenant_id: Optional[UUID] = Query(None, description="Filter users by tenant ID"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(User).options(
        selectinload(User.addresses),
        selectinload(User.phone_numbers),
        selectinload(User.emails),
        selectinload(User.tenant_members).options(
            selectinload(TenantMember.role),
            selectinload(TenantMember.tenant)
        )
    )
    
    if tenant_id:
        # Join with TenantMember to filter
        stmt = stmt.join(User.tenant_members).where(TenantMember.tenant_id == tenant_id)
        
    result = await db.execute(stmt)
    users = result.scalars().all()
    
    # Use custom mapping to handle the flattened roles list
    return [UserDetailResponse.from_orm_custom(u, tenant_id) for u in users]
