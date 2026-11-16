from sqlalchemy.orm import Session

from app.models.book import Book, BookCopy


from sqlalchemy import func


def get_all_books(db: Session):
    copy_counts = (
        db.query(
            BookCopy.book_id,
            func.count(BookCopy.id).label("available_count")
        )
        .filter(BookCopy.status == "available")
        .group_by(BookCopy.book_id)
        .all()
    )

    counts = {
        book_id: available_count
        for book_id, available_count in copy_counts
    }

    books = db.query(Book).all()

    result = []

    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "availableCopies": counts.get(book.id, 0)
        })

    return result


def get_book_by_id(db: Session, book_id: int):
    book = (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )

    if book is None:
        return None

    available_copies = (
        db.query(BookCopy)
        .filter(
            BookCopy.book_id == book.id,
            BookCopy.status == "available"
        )
        .count()
    )

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "availableCopies": available_copies
    }