"""JWT helpers."""

from datetime import UTC, datetime, timedelta

from jose import jwt

from .config import settings


def create_access_token(subject: str, tenant_id: str | None, expires_minutes: int = 60) -> str:
    payload = {
        "sub": subject,
        "tenant_id": tenant_id,
        "exp": datetime.now(UTC) + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
