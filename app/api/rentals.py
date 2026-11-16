from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.rental import (
    RentalCreate,
    RentalResponse
)
from app.services.rental_service import (
    create_rental,
    get_user_rentals
)

router = APIRouter(
    tags=["rentals"]
)


@router.post(
    "/books/{book_id}/rentals",
    response_model=RentalResponse,
    status_code=201
)
def rent_book(
    book_id: int,
    request: RentalCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return create_rental(
        db,
        current_user.id,
        book_id,
        request.rentalPeriodDays
    )

@router.get(
    "/me/rentals",
    response_model=list[RentalResponse]
)
def my_rentals(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return get_user_rentals(
        db,
        current_user.id
    )