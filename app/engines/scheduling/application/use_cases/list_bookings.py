"""List bookings use case."""

from app.engines.scheduling.domain.repository import BookingRepository


class ListBookingsUseCase:
    def __init__(self, repo: BookingRepository):
        self._repo = repo

    async def execute(self, data: ListBookingsInput):
        return await self._repo.list_for_resource(
            data.tenant_id,
            data.resource_id,
            data.window_start,
            data.window_end,
        )
