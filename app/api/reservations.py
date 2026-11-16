from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.reservation import ReservationResponse
from app.services.reservation_service import (
    create_reservation,
    cancel_reservation
)


router = APIRouter(
    tags=["reservations"]
)


@router.post(
    "/books/{book_id}/reservations",
    response_model=ReservationResponse,
    status_code=201
)
def reserve_book(
    book_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return create_reservation(
        db,
        current_user.id,
        book_id
    )


@router.delete(
    "/reservations/{reservation_id}",
    status_code=204
)
def delete_reservation(
    reservation_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    cancel_reservation(
        db,
        current_user.id,
        reservation_id
    )

    return Response(
        status_code=204
    )