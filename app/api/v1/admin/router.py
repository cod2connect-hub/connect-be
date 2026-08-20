"""Admin API composition for v1."""

from fastapi import APIRouter

from app.engines.scheduling.interface.admin_router import router as scheduling_router


admin_router_v1 = APIRouter(prefix="/api/v1/admin")
admin_router_v1.include_router(scheduling_router)
