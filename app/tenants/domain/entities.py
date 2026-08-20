"""Tenant domain entities."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class TenantStatus(str, Enum):
    ONBOARDING = "onboarding"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class UserRole(str, Enum):
    PLATFORM_ADMIN = "platform_admin"
    TENANT_OWNER = "tenant_owner"
    TENANT_STAFF = "tenant_staff"
    TENANT_CUSTOMER = "tenant_customer"


@dataclass(slots=True)
class Tenant:
    id: UUID
    business_name: str
    subdomain: str
    niche_type: str | None
    status: TenantStatus
    created_at: datetime | None = None


@dataclass(slots=True)
class User:
    id: UUID
    tenant_id: UUID | None
    email: str
    hashed_password: str
    role: UserRole
    is_active: bool = True
