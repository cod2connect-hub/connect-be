"""FastAPI composition root for the modular backend."""

from fastapi import FastAPI

from .api.v1.admin.router import admin_router_v1
from .api.v1.onboarding.router import onboarding_router_v1
from .api.v1.platform.router import platform_router_v1
from .api.v1.public.router import public_router_v1
from .core.config import settings
from .core.db import lifespan
from .core.errors import install_exception_handlers


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multi-niche website builder backend",
    lifespan=lifespan,
)

install_exception_handlers(app)
app.include_router(admin_router_v1)
app.include_router(public_router_v1)
app.include_router(platform_router_v1)
app.include_router(onboarding_router_v1)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "service": settings.app_name, "version": settings.app_version}


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": settings.app_name, "version": settings.app_version}
