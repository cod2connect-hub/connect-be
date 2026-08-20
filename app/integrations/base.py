"""Protocols for integration adapters."""

from typing import Protocol
from uuid import UUID


class PaymentProvider(Protocol):
    async def create_charge(
        self, tenant_id: UUID, amount_cents: int, currency: str, metadata: dict
    ) -> str: ...

    async def create_subscription(self, tenant_id: UUID, price_ids: list[str]) -> str: ...


class NotificationProvider(Protocol):
    async def send(self, to: str, template_key: str, context: dict) -> None: ...
