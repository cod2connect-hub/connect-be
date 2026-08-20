"""Domain error handling."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class DomainError(Exception):
    """Base class for business-rule failures."""


ERROR_STATUS_MAP: dict[type[DomainError], int] = {}


def register_error(exc_type: type[DomainError], status: int) -> None:
    ERROR_STATUS_MAP[exc_type] = status


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def handle_domain_error(request: Request, exc: DomainError):
        status = ERROR_STATUS_MAP.get(type(exc), 500)
        return JSONResponse(
            status_code=status,
            content={
                "type": f"https://api.platform.dev/errors/{type(exc).__name__}",
                "title": type(exc).__name__,
                "status": status,
                "detail": str(exc),
                "instance": str(request.url.path),
            },
        )
