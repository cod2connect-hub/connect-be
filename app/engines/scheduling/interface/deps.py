"""Dependency wiring for scheduling."""

from fastapi import Depends

from app.core.db import get_db
from app.core.events import InProcessEventPublisher
from app.engines.scheduling.application.use_cases.create_booking import CreateBookingUseCase
from app.engines.scheduling.infrastructure.repository_impl import AsyncpgBookingRepository


async def get_create_booking_use_case(conn=Depends(get_db)) -> CreateBookingUseCase:
    return CreateBookingUseCase(
        repo=AsyncpgBookingRepository(conn),
        events=InProcessEventPublisher(),
    )
