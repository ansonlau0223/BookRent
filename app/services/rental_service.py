from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.book import Book, BookCopy
from app.models.rental import Rental


def create_rental(
    db: Session,
    user_id: int,
    book_id: int,
    rental_period_days: int
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

    try:
        copy = (
            db.query(BookCopy)
            .filter(
                BookCopy.book_id == book_id,
                BookCopy.status == "available"
            )
            .with_for_update()
            .first()
        )

        if copy is None:
            raise HTTPException(
                status_code=409,
                detail="No copy is currently available"
            )

        start_date = date.today()

        due_date = (
            start_date
            + timedelta(days=rental_period_days)
        )

        rental = Rental(
            user_id=user_id,
            book_id=book_id,
            book_copy_id=copy.id,
            start_date=start_date,
            due_date=due_date,
            status="active"
        )

        copy.status = "rented"

        db.add(rental)

        db.commit()
        db.refresh(rental)

        return {
            "rentalId": rental.id,
            "bookId": book_id,
            "bookCopyId": copy.id,
            "startDate": start_date,
            "dueDate": due_date,
            "status": rental.status
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise

def get_user_rentals(
    db: Session,
    user_id: int
):
    rentals = (
        db.query(Rental)
        .filter(
            Rental.user_id == user_id
        )
        .order_by(
            Rental.id.desc()
        )
        .all()
    )

    result = []

    for rental in rentals:
        result.append({
            "rentalId": rental.id,
            "bookId": rental.book_id,
            "bookCopyId": rental.book_copy_id,
            "startDate": rental.start_date,
            "dueDate": rental.due_date,
            "status": rental.status
        })

    return result