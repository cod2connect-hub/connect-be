"""Row-to-entity mappers for scheduling."""

from app.engines.scheduling.domain.entities import Booking, BookingStatus


def to_booking(row) -> Booking:
    return Booking(
        id=row["id"],
        tenant_id=row["tenant_id"],
        resource_id=row["resource_id"],
        customer_id=row["customer_id"],
        start_at=row["start_at"],
        end_at=row["end_at"],
        status=BookingStatus(row["status"]),
    )
