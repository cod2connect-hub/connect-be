"""Feature and permission checks."""

from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status


@dataclass
class TenantStaff:
    tenant_id: UUID
    staff_id: UUID
    role: str
    permissions: set[str]


class PermissionDeniedError(Exception):
    """Raised when a staff member lacks a permission."""


class FeatureNotEnabledError(Exception):
    """Raised when a tenant has not enabled a feature."""


async def get_current_staff(request: Request) -> TenantStaff:
    staff = getattr(request.state, "staff", None)
    if staff is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return staff


def require_permission(perm: str):
    async def checker(staff: TenantStaff = Depends(get_current_staff)) -> None:
        if staff.role != "owner" and perm not in staff.permissions:
            raise PermissionDeniedError(perm)

    return checker


def require_feature(feature_key: str):
    async def checker(request: Request) -> None:
        enabled = getattr(request.state, "enabled_features", set())
        if feature_key not in enabled:
            raise FeatureNotEnabledError(feature_key)

    return checker
