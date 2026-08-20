"""Tenant dependencies."""

from fastapi import Depends

from app.core.db import get_db
from app.tenants.infrastructure.repository_impl import AsyncpgTenantRepository


async def get_tenant_repository(conn=Depends(get_db)) -> AsyncpgTenantRepository:
    return AsyncpgTenantRepository(conn)
