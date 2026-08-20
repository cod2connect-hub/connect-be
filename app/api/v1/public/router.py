"""Public API composition for v1."""

from fastapi import APIRouter

from app.tenants.interface.router import router as tenants_router


public_router_v1 = APIRouter(prefix="/api/v1/public")
public_router_v1.include_router(tenants_router)
