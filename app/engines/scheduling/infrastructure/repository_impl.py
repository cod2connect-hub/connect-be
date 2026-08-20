"""asyncpg implementation of the scheduling repository."""

import asyncpg

from app.core.scoping import assert_scoped
from app.engines.scheduling.domain.entities import Booking
from app.engines.scheduling.domain.repository import BookingRepository
from app.engines.scheduling.infrastructure.mappers import to_booking


class AsyncpgBookingRepository(BookingRepository):
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def list_for_resource(self, tenant_id, resource_id, window_start, window_end) -> list[Booking]:
        assert_scoped(tenant_id, context="bookings.list_for_resource")
        rows = await self._conn.fetch(
            """
            select id, tenant_id, resource_id, customer_id, start_at, end_at, status
            from bookings
            where tenant_id = $1
              and resource_id = $2
              and status != 'cancelled'
              and start_at < $4
              and $3 < end_at
            """,
            tenant_id,
            resource_id,
            window_start,
            window_end,
        )
        return [to_booking(row) for row in rows]

    async def get(self, tenant_id, booking_id):
        assert_scoped(tenant_id, context="bookings.get")
        row = await self._conn.fetchrow(
            """
            select id, tenant_id, resource_id, customer_id, start_at, end_at, status
            from bookings
            where tenant_id = $1 and id = $2
            """,
            tenant_id,
            booking_id,
        )
        return to_booking(row) if row else None

    async def save(self, booking: Booking) -> None:
        await self._conn.execute(
            """
            insert into bookings (id, tenant_id, resource_id, customer_id, start_at, end_at, status)
            values ($1, $2, $3, $4, $5, $6, $7)
            on conflict (id) do update set
              resource_id = excluded.resource_id,
              customer_id = excluded.customer_id,
              start_at = excluded.start_at,
              end_at = excluded.end_at,
              status = excluded.status
            """,
            booking.id,
            booking.tenant_id,
            booking.resource_id,
            booking.customer_id,
            booking.start_at,
            booking.end_at,
            booking.status.value,
        )
