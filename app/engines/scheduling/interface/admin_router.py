"""Scheduling admin router."""

from fastapi import APIRouter, Depends, Request, Response, status

from app.core.permissions import require_feature, require_permission
from app.engines.scheduling.application.dto import CreateBookingInput
from app.engines.scheduling.application.use_cases.create_booking import CreateBookingUseCase
from app.engines.scheduling.interface.deps import get_create_booking_use_case
from app.engines.scheduling.interface.schemas import BookingResponse, CreateBookingRequest


router = APIRouter(
    prefix="/scheduling",
    tags=["scheduling:admin"],
    dependencies=[
        Depends(require_feature("table_reservation")),
        Depends(require_permission("scheduling.manage")),
    ],
)


@router.post("/bookings", status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: CreateBookingRequest,
    request: Request,
    response: Response,
    uc: CreateBookingUseCase = Depends(get_create_booking_use_case),
):
    booking = await uc.execute(
        CreateBookingInput(
            tenant_id=request.state.tenant_id,
            resource_id=payload.resource_id,
            customer_id=payload.customer_id,
            start_at=payload.start_at,
            end_at=payload.end_at,
        )
    )
    response.headers["Location"] = f"/api/v1/admin/scheduling/bookings/{booking.id}"
    return BookingResponse.from_domain(booking)
