"""Scheduling event payloads."""

from uuid import UUID

from pydantic import BaseModel


class BookingCreatedV1(BaseModel):
    booking_id: UUID
    tenant_id: UUID


class BookingCancelledV1(BaseModel):
    booking_id: UUID
    tenant_id: UUID
