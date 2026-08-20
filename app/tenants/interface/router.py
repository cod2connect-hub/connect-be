"""Tenant onboarding routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import create_access_token, get_password_hash, verify_password
from app.tenants.application.dto import SubdomainCheckInput, TenantCreateInput
from app.tenants.application.use_cases import check_subdomain, create_tenant as create_tenant_uc
from app.tenants.interface.deps import get_tenant_repository
from app.tenants.interface.schemas import (
    SubdomainCheckRequest,
    SubdomainCheckResponse,
    TenantCreateRequest,
    TenantResponse,
    TokenResponse,
    UserLoginRequest,
)

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/check-subdomain", response_model=SubdomainCheckResponse)
async def check_subdomain_route(
    request: SubdomainCheckRequest,
    repo=Depends(get_tenant_repository),
):
    payload = await check_subdomain(repo, SubdomainCheckInput(business_name=request.business_name))
    return SubdomainCheckResponse(**payload)


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant_route(
    request: TenantCreateRequest,
    repo=Depends(get_tenant_repository),
):
    tenant = await create_tenant_uc(
        repo,
        TenantCreateInput(
            business_name=request.business_name,
            subdomain=request.subdomain,
            owner_email=request.owner_email,
            owner_password=request.owner_password,
            niche_type=request.niche_type,
        ),
        password_hash=get_password_hash(request.owner_password),
    )
    return TenantResponse(
        id=str(tenant.id),
        business_name=tenant.business_name,
        subdomain=tenant.subdomain,
        niche_type=tenant.niche_type,
        status=tenant.status.value,
        created_at=tenant.created_at,
    )


@router.post("/auth/login", response_model=TokenResponse)
async def login_route(
    request: UserLoginRequest,
    repo=Depends(get_tenant_repository),
):
    user = await repo.find_user_by_email(request.email)
    if user is None or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    token = create_access_token(subject=str(user.id), tenant_id=str(user.tenant_id) if user.tenant_id else None)
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        email=user.email,
        role=user.role.value,
    )
