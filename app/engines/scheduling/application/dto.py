"""Scheduling application DTOs."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateBookingInput:
    tenant_id: UUID
    resource_id: UUID
    customer_id: UUID
    start_at: datetime
    end_at: datetime


@dataclass
class CancelBookingInput:
    tenant_id: UUID
    booking_id: UUID


@dataclass
class ListBookingsInput:
    tenant_id: UUID
    resource_id: UUID
    window_start: datetime
    window_end: datetime
