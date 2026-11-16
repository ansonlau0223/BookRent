from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.book import Book, BookCopy
from app.models.reservation import Reservation


def create_reservation(
    db: Session,
    user_id: int,
    book_id: int
):
    book = (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    available_copy = (
        db.query(BookCopy)
        .filter(
            BookCopy.book_id == book_id,
            BookCopy.status == "available"
        )
        .first()
    )

    if available_copy is not None:
        raise HTTPException(
            status_code=409,
            detail="A copy is currently available; rent it instead"
        )

    existing_reservation = (
        db.query(Reservation)
        .filter(
            Reservation.user_id == user_id,
            Reservation.book_id == book_id,
            Reservation.status == "waiting"
        )
        .first()
    )

    if existing_reservation is not None:
        return {
            "reservationId": existing_reservation.id,
            "bookId": existing_reservation.book_id,
            "status": existing_reservation.status
        }

    reservation = Reservation(
        user_id=user_id,
        book_id=book_id,
        status="waiting"
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "reservationId": reservation.id,
        "bookId": reservation.book_id,
        "status": reservation.status
    }

def cancel_reservation(
    db: Session,
    user_id: int,
    reservation_id: int
):
    reservation = (
        db.query(Reservation)
        .filter(
            Reservation.id == reservation_id
        )
        .first()
    )

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    if reservation.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot cancel another user's reservation"
        )

    reservation.status = "cancelled"

    db.commit()