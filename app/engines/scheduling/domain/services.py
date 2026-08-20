"""Pure scheduling rules."""

from uuid import UUID

from .entities import Booking, BookingStatus
from .exceptions import BookingConflictError


def ensure_no_conflict(
    existing: list[Booking],
    resource_id: UUID,
    start_at,
    end_at,
) -> None:
    for booking in existing:
        if (
            booking.resource_id == resource_id
            and booking.status != BookingStatus.CANCELLED
            and booking.overlaps(start_at, end_at)
        ):
            raise BookingConflictError(f"Resource {resource_id} already booked")
