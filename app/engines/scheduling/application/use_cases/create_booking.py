"""Create booking use case."""

from uuid import uuid4

from app.contracts.events.booking_events import BookingCreatedV1
from ..dto import CreateBookingInput
from ..ports import EventPublisher
from app.engines.scheduling.domain.entities import Booking, BookingStatus
from app.engines.scheduling.domain.repository import BookingRepository
from app.engines.scheduling.domain.services import ensure_no_conflict


class CreateBookingUseCase:
    def __init__(self, repo: BookingRepository, events: EventPublisher):
        self._repo = repo
        self._events = events

    async def execute(self, data: CreateBookingInput) -> Booking:
        existing = await self._repo.list_for_resource(
            data.tenant_id,
            data.resource_id,
            data.start_at,
            data.end_at,
        )
        ensure_no_conflict(existing, data.resource_id, data.start_at, data.end_at)
        booking = Booking(
            id=uuid4(),
            tenant_id=data.tenant_id,
            resource_id=data.resource_id,
            customer_id=data.customer_id,
            start_at=data.start_at,
            end_at=data.end_at,
            status=BookingStatus.PENDING,
        )
        await self._repo.save(booking)
        await self._events.publish(
            "booking.created",
            BookingCreatedV1(booking_id=booking.id, tenant_id=data.tenant_id),
        )
        return booking
