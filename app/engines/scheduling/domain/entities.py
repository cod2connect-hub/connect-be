"""Scheduling domain entities."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Booking:
    id: UUID
    tenant_id: UUID
    resource_id: UUID
    customer_id: UUID
    start_at: datetime
    end_at: datetime
    status: BookingStatus

    def overlaps(self, start: datetime, end: datetime) -> bool:
        return self.start_at < end and start < self.end_at
