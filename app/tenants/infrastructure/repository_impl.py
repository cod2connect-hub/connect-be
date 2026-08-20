"""asyncpg tenant repository implementation."""

import asyncpg

from app.tenants.domain.entities import Tenant, TenantStatus, User, UserRole
from app.tenants.domain.repository import TenantRepository


class AsyncpgTenantRepository(TenantRepository):
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def is_subdomain_available(self, subdomain: str) -> bool:
        row = await self._conn.fetchrow(
            "select 1 from tenants where subdomain = $1",
            subdomain,
        )
        return row is None

    async def find_user_by_email(self, email: str) -> User | None:
        row = await self._conn.fetchrow(
            """
            select id, tenant_id, email, hashed_password, role, is_active
            from users
            where email = $1
            """,
            email,
        )
        if row is None:
            return None
        return User(
            id=row["id"],
            tenant_id=row["tenant_id"],
            email=row["email"],
            hashed_password=row["hashed_password"],
            role=UserRole(row["role"]),
            is_active=row["is_active"],
        )

    async def create_tenant_with_owner(
        self,
        *,
        business_name: str,
        subdomain: str,
        niche_type: str | None,
        owner_email: str,
        owner_password_hash: str,
    ) -> Tenant:
        row = await self._conn.fetchrow(
            """
            insert into tenants (business_name, subdomain, niche_type, status)
            values ($1, $2, $3, $4)
            returning id, business_name, subdomain, niche_type, status, created_at
            """,
            business_name,
            subdomain,
            niche_type,
            TenantStatus.ONBOARDING.value,
        )
        await self._conn.execute(
            """
            insert into users (tenant_id, email, hashed_password, role, is_active)
            values ($1, $2, $3, $4, true)
            """,
            row["id"],
            owner_email,
            owner_password_hash,
            UserRole.TENANT_OWNER.value,
        )
        return Tenant(
            id=row["id"],
            business_name=row["business_name"],
            subdomain=row["subdomain"],
            niche_type=row["niche_type"],
            status=TenantStatus(row["status"]),
            created_at=row["created_at"],
        )
