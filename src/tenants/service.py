"""Business logic for tenant management"""
import re
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.tenants.models import Tenant, User, TenantStatus, UserRole
from src.tenants.schemas import (
    SubdomainCheckRequest,
    SubdomainCheckResponse,
    TenantCreateRequest,
    TenantResponse,
)
from src.core.security import get_password_hash


def slugify_subdomain(business_name: str) -> str:
    """Convert business name to subdomain-safe slug"""
    slug = business_name.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug)
    slug = slug.strip("-")
    return slug[:63]  # Max subdomain length


async def check_subdomain_availability(
    db: AsyncSession,
    subdomain: str
) -> bool:
    """Check if subdomain is available"""
    result = await db.execute(
        select(Tenant).where(Tenant.subdomain == subdomain)
    )
    return result.scalar_one_or_none() is None


async def generate_subdomain_alternatives(
    db: AsyncSession,
    base: str,
    count: int = 3
) -> list[str]:
    """Generate alternative subdomain suggestions"""
    alternatives = []
    for i in range(1, count + 1):
        candidate = f"{base}{i}"
        if await check_subdomain_availability(db, candidate):
            alternatives.append(candidate)
    return alternatives


async def check_subdomain(
    db: AsyncSession,
    request: SubdomainCheckRequest
) -> SubdomainCheckResponse:
    """Check subdomain availability and suggest alternatives"""
    suggested = slugify_subdomain(request.business_name)
    available = await check_subdomain_availability(db, suggested)

    alternatives = []
    if not available:
        alternatives = await generate_subdomain_alternatives(db, suggested)

    return SubdomainCheckResponse(
        suggested_subdomain=suggested,
        available=available,
        alternatives=alternatives
    )


async def create_tenant(
    db: AsyncSession,
    request: TenantCreateRequest
) -> TenantResponse:
    """Create a new tenant and owner user"""

    # Check subdomain availability
    if not await check_subdomain_availability(db, request.subdomain):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Subdomain '{request.subdomain}' is already taken"
        )

    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == request.owner_email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create tenant
    tenant = Tenant(
        business_name=request.business_name,
        subdomain=request.subdomain,
        niche_type=request.niche_type,
        status=TenantStatus.ONBOARDING
    )
    db.add(tenant)
    await db.flush()

    # Create owner user
    user = User(
        tenant_id=tenant.id,
        email=request.owner_email,
        hashed_password=get_password_hash(request.owner_password),
        role=UserRole.TENANT_OWNER,
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(tenant)

    return TenantResponse(
        id=str(tenant.id),
        business_name=tenant.business_name,
        subdomain=tenant.subdomain,
        custom_domain=tenant.custom_domain,
        niche_type=tenant.niche_type,
        status=tenant.status.value,
        logo_url=tenant.logo_url,
        description=tenant.description,
        created_at=tenant.created_at
    )
