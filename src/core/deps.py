"""FastAPI dependencies for auth, tenant, and feature enforcement"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.core.security import decode_access_token

security = HTTPBearer()


async def get_current_tenant(request: Request) -> Optional[str]:
    """Get current tenant_id from request state (set by TenantMiddleware)"""
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id and not request.url.path.startswith(("/health", "/docs", "/platform_api")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found for this domain"
        )
    return tenant_id


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # TODO: Load user from database
    return {"id": user_id, "email": payload.get("email")}


def require_feature(feature_key: str):
    """
    Dependency factory for feature enforcement
    Usage: @router.post("/bookings", dependencies=[Depends(require_feature("table_reservation"))])
    """
    async def checker(
        tenant_id: str = Depends(get_current_tenant),
        db: AsyncSession = Depends(get_db)
    ):
        # TODO: Check if tenant has feature enabled in tenant_features table
        # For now, allow all features
        pass

    return checker
