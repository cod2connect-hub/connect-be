"""API routes for tenant onboarding and management"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import get_db
from src.core.security import create_access_token
from src.tenants import service
from src.tenants.models import User
from src.tenants.schemas import (
    SubdomainCheckRequest,
    SubdomainCheckResponse,
    TenantCreateRequest,
    TenantResponse,
    UserLoginRequest,
    TokenResponse,
)
from src.core.security import verify_password

router = APIRouter(prefix="/public", tags=["tenants"])


@router.post("/tenants/check-subdomain", response_model=SubdomainCheckResponse)
async def check_subdomain(
    request: SubdomainCheckRequest,
    db: AsyncSession = Depends(get_db)
):
    """Check subdomain availability and get suggestions"""
    return await service.check_subdomain(db, request)


@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    request: TenantCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create a new tenant account"""
    return await service.create_tenant(db, request)


@router.post("/auth/login", response_model=TokenResponse)
async def login(
    request: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token"""

    # Find user by email
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create access token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "tenant_id": str(user.tenant_id) if user.tenant_id else None
        }
    )

    return TokenResponse(
        access_token=access_token,
        user_id=str(user.id),
        email=user.email,
        role=user.role.value
    )
