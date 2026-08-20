"""Tenant onboarding use cases."""

from fastapi import HTTPException, status

from ..domain.entities import Tenant
from ..domain.repository import TenantRepository
from .dto import SubdomainCheckInput, TenantCreateInput
from .services import slugify_subdomain


async def check_subdomain(repo: TenantRepository, data: SubdomainCheckInput) -> dict:
    suggested = slugify_subdomain(data.business_name)
    available = await repo.is_subdomain_available(suggested)
    alternatives = [f"{suggested}{i}" for i in range(1, 4)] if not available else []
    return {
        "suggested_subdomain": suggested,
        "available": available,
        "alternatives": alternatives,
    }


async def create_tenant(
    repo: TenantRepository,
    data: TenantCreateInput,
    password_hash: str,
) -> Tenant:
    if not await repo.is_subdomain_available(data.subdomain):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Subdomain '{data.subdomain}' is already taken",
        )
    if await repo.find_user_by_email(data.owner_email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    return await repo.create_tenant_with_owner(
        business_name=data.business_name,
        subdomain=data.subdomain,
        niche_type=data.niche_type,
        owner_email=data.owner_email,
        owner_password_hash=password_hash,
    )
