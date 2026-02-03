from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import AsyncSessionLocal
from app.database.models import Tenant

router = APIRouter()

# Dependency
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# Pydantic Models
class TenantResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    parent_tenant_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.get("/tenants", response_model=List[TenantResponse])
async def read_tenants(
    parent_id: Optional[UUID] = Query(None, description="Filter by parent tenant ID"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Tenant)
    
    if parent_id:
        query = query.where(Tenant.parent_tenant_id == parent_id)
    else:
        # If no parent_id is provided, return root tenants (where parent_tenant_id is NULL)
        query = query.where(Tenant.parent_tenant_id.is_(None))
        
    result = await db.execute(query)
    tenants = result.scalars().all()
    return tenants
