"""Repository contract for scheduling."""

from typing import Protocol
from uuid import UUID

from .entities import Booking


class BookingRepository(Protocol):
    async def list_for_resource(
        self,
        tenant_id: UUID,
        resource_id: UUID,
        window_start,
        window_end,
    ) -> list[Booking]: ...

    async def get(self, tenant_id: UUID, booking_id: UUID) -> Booking | None: ...

    async def save(self, booking: Booking) -> None: ...
