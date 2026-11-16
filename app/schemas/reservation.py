from pydantic import BaseModel


class ReservationResponse(BaseModel):
    reservationId: int
    bookId: int
    status: str