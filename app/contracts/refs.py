"""Stable references shared across engines."""

from uuid import UUID

from pydantic import BaseModel


class TenantRef(BaseModel):
    tenant_id: UUID


class CustomerRef(BaseModel):
    tenant_id: UUID
    customer_id: UUID
