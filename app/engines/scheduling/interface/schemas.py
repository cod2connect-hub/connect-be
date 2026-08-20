"""Pydantic schemas for scheduling HTTP endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateBookingRequest(BaseModel):
    resource_id: UUID
    customer_id: UUID
    start_at: datetime
    end_at: datetime


class BookingResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    resource_id: UUID
    customer_id: UUID
    start_at: datetime
    end_at: datetime
    status: str = Field(..., description="Booking status")

    @classmethod
    def from_domain(cls, booking) -> "BookingResponse":
        return cls(
            id=booking.id,
            tenant_id=booking.tenant_id,
            resource_id=booking.resource_id,
            customer_id=booking.customer_id,
            start_at=booking.start_at,
            end_at=booking.end_at,
            status=booking.status.value,
        )
