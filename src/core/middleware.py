"""Middleware for request processing, tenant resolution, and logging"""
from typing import Callable, Optional
import time
import logging
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import async_session_maker

logger = logging.getLogger(__name__)


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Resolves tenant from subdomain/custom domain and attaches to request.state
    Example: restaurant.connect.app -> tenant_id resolved and set
    """

    async def dispatch(self, request: Request, call_next: Callable):
        # Extract host
        host = request.headers.get("host", "").split(":")[0]

        # Skip tenant resolution for platform/health endpoints
        if request.url.path.startswith(("/health", "/docs", "/openapi.json", "/platform_api")):
            request.state.tenant_id = None
            return await call_next(request)

        # Extract subdomain or custom domain
        tenant_id = await self._resolve_tenant(host)

        # Attach tenant_id to request state
        request.state.tenant_id = tenant_id

        # Set PostgreSQL session variable for Row-Level Security
        if tenant_id:
            async with async_session_maker() as session:
                await session.execute(
                    f"SET LOCAL app.tenant_id = '{tenant_id}'"
                )

        return await call_next(request)

    async def _resolve_tenant(self, host: str) -> Optional[str]:
        """
        Resolve tenant_id from host (subdomain or custom domain)
        TODO: Implement actual database lookup
        """
        # For now, return None - will implement with tenants table
        # This should query: SELECT id FROM tenants WHERE subdomain = ? OR custom_domain = ?
        return None


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with timing"""

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        logger.info(f"Request: {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} Time: {process_time:.3f}s"
        )

        response.headers["X-Process-Time"] = str(process_time)
        return response
