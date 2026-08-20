"""Tenant repository contract."""

from typing import Protocol
from uuid import UUID

from .entities import Tenant, User


class TenantRepository(Protocol):
    async def is_subdomain_available(self, subdomain: str) -> bool: ...

    async def find_user_by_email(self, email: str) -> User | None: ...

    async def create_tenant_with_owner(
        self,
        *,
        business_name: str,
        subdomain: str,
        niche_type: str | None,
        owner_email: str,
        owner_password_hash: str,
    ) -> Tenant: ...
