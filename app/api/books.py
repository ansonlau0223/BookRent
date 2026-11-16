from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.book import BookResponse
from app.services.book_service import get_all_books, get_book_by_id


router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.get(
    "",
    response_model=list[BookResponse]
)
def list_books(
    db: Session = Depends(get_db)
):
    return get_all_books(db)


@router.get(
    "/{book_id}",
    response_model=BookResponse
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = get_book_by_id(
        db,
        book_id
    )

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book