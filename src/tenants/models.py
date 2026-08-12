"""Database models for tenants and users"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from src.core.database import Base


class TenantStatus(str, enum.Enum):
    """Tenant lifecycle status"""
    ONBOARDING = "onboarding"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class Tenant(Base):
    """Tenant/Business account"""
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    business_name: Mapped[str] = mapped_column(String(255), nullable=False)
    subdomain: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    custom_domain: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    niche_type: Mapped[Optional[str]] = mapped_column(String(100))
    status: Mapped[TenantStatus] = mapped_column(
        SQLEnum(TenantStatus),
        default=TenantStatus.ONBOARDING,
        nullable=False
    )

    # Business info
    logo_url: Mapped[Optional[str]] = mapped_column(String(500))
    description: Mapped[Optional[str]]
    address: Mapped[Optional[str]]
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    business_hours: Mapped[Optional[dict]] = mapped_column(JSON)

    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class UserRole(str, enum.Enum):
    """User role types"""
    PLATFORM_ADMIN = "platform_admin"
    TENANT_OWNER = "tenant_owner"
    TENANT_STAFF = "tenant_staff"
    TENANT_CUSTOMER = "tenant_customer"


class User(Base):
    """User account (platform staff, tenant owners/staff, or customers)"""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,  # NULL for platform staff
        index=True
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.TENANT_STAFF,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime)
