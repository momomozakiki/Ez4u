import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    UUID, String, Boolean, DateTime, ForeignKey, 
    UniqueConstraint, Index, Text, Table, Column, func, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database.base import Base

# ----------------------------------------------------------------------
# CORE IDENTITY LAYER
# ----------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    identities: Mapped[List["UserIdentity"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    tenant_members: Mapped[List["TenantMember"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    global_roles: Mapped[List["UserGlobalRole"]] = relationship(foreign_keys="[UserGlobalRole.user_id]", back_populates="user")

class UserIdentity(Base):
    __tablename__ = "user_identities"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # "google", "local", etc.
    subject: Mapped[str] = mapped_column(String(500), nullable=False)  # OAuth sub or email
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))  # NULL for OAuth
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("provider", "subject", name="uq_provider_subject"),
        Index("ix_user_identities_user_id", "user_id")
    )
    user: Mapped["User"] = relationship(back_populates="identities")

# ----------------------------------------------------------------------
# TENANCY & RBAC LAYER
# ----------------------------------------------------------------------

class Tenant(Base):
    __tablename__ = "tenants"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)  # for subdomain routing
    parent_tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("tenants.id", ondelete="SET NULL"), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    parent: Mapped[Optional["Tenant"]] = relationship(remote_side=[id], backref="children")
    roles: Mapped[List["Role"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    tenant_members: Mapped[List["TenantMember"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    resources: Mapped[List["Resource"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # "customer", "accountant", etc.
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_system_role: Mapped[bool] = mapped_column(Boolean, default=False)  # Pre-created roles (e.g., "customer")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_tenant_role_name"),
        Index("ix_roles_tenant_id", "tenant_id")
    )
    tenant: Mapped["Tenant"] = relationship(back_populates="roles")
    tenant_members: Mapped[List["TenantMember"]] = relationship(back_populates="role")
    permissions: Mapped[List["Permission"]] = relationship(secondary="role_permissions", viewonly=True)

class TenantMember(Base):
    __tablename__ = "tenant_members"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="active")  # "active", "invited", "suspended"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),  # CRITICAL: Prevent duplicate memberships
        Index("ix_tenant_members_tenant_id", "tenant_id"),
        Index("ix_tenant_members_user_id", "user_id")
    )
    tenant: Mapped["Tenant"] = relationship(back_populates="tenant_members")
    user: Mapped["User"] = relationship(back_populates="tenant_members")
    role: Mapped["Role"] = relationship(back_populates="tenant_members")

# ----------------------------------------------------------------------
# GLOBAL ACCESS LAYER (SuperAdmin)
# ----------------------------------------------------------------------

class GlobalRole(Base):
    __tablename__ = "global_roles"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # "superadmin", "support_agent"
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    permissions: Mapped[List["Permission"]] = relationship(secondary="global_role_permissions", viewonly=True)

class UserGlobalRole(Base):
    __tablename__ = "user_global_roles"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    global_role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("global_roles.id", ondelete="CASCADE"), primary_key=True)
    granted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="global_roles")
    granter: Mapped[Optional["User"]] = relationship(foreign_keys=[granted_by])
    global_role: Mapped["GlobalRole"] = relationship()

# ----------------------------------------------------------------------
# PERMISSIONS LAYER (Shared Registry)
# ----------------------------------------------------------------------

class Permission(Base):
    __tablename__ = "permissions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # "tenant.create", "data.view"
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # "tenant_management", "data_access"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

# Association tables (no ORM class needed)
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)

global_role_permissions = Table(
    "global_role_permissions",
    Base.metadata,
    Column("global_role_id", UUID(as_uuid=True), ForeignKey("global_roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)

# ----------------------------------------------------------------------
# BUSINESS DATA LAYER (SaaS Content)
# ----------------------------------------------------------------------

class Resource(Base):
    """Generic resource table demonstrating RLS protection"""
    __tablename__ = "resources"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # RLS CRITICAL: All business data MUST have tenant_id
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb")) # Flexible schema
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    tenant: Mapped["Tenant"] = relationship(back_populates="resources")

# ----------------------------------------------------------------------
# RLS POLICY (SQL COMMENT)
# ----------------------------------------------------------------------
"""
EXECUTE IN MIGRATION SCRIPT FOR ALL TENANT-SCOPED TABLES (e.g., resources):
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON resources
USING (
  tenant_id = current_setting('app.current_tenant_id', true)::uuid
  AND EXISTS (
    SELECT 1 FROM tenant_members tm
    WHERE tm.user_id = current_setting('app.current_user_id', true)::uuid
      AND tm.tenant_id = resources.tenant_id
      AND tm.status = 'active'
  )
);

-- APPLICATION MUST SET AT REQUEST START:
-- SET app.current_tenant_id = '<tenant_uuid>';
-- SET app.current_user_id = '<user_uuid>';
-- VALIDATE MEMBERSHIP BEFORE SETTING CONTEXT (prevent spoofing)
"""
