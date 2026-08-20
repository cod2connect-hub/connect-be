"""Cancel booking use case."""

from ....contracts.events.booking_events import BookingCancelledV1
from ..dto import CancelBookingInput
from ..ports import EventPublisher
from ...domain.entities import BookingStatus
from ...domain.exceptions import BookingNotFoundError
from ...domain.repository import BookingRepository


class CancelBookingUseCase:
    def __init__(self, repo: BookingRepository, events: EventPublisher):
        self._repo = repo
        self._events = events

    async def execute(self, data: CancelBookingInput):
        booking = await self._repo.get(data.tenant_id, data.booking_id)
        if booking is None:
            raise BookingNotFoundError(str(data.booking_id))
        booking.status = BookingStatus.CANCELLED
        await self._repo.save(booking)
        await self._events.publish(
            "booking.cancelled",
            BookingCancelledV1(booking_id=booking.id, tenant_id=data.tenant_id),
        )
        return booking
