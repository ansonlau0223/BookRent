from app.db.session import SessionLocal
from app.models.book import Book, BookCopy


def seed_database():
    db = SessionLocal()

    try:
        if db.query(Book).count() > 0:
            print("Books already exist.")
            return

        book1 = Book(
            id=120,
            title="Clean Code",
            author="Robert C. Martin"
        )

        book2 = Book(
            id=121,
            title="Design Patterns",
            author="Erich Gamma et al."
        )

        book3 = Book(
            id=122,
            title="Introduction to Algorithms",
            author="Cormen et al."
        )

        db.add_all([
            book1,
            book2,
            book3
        ])

        db.flush()

        copies = [
            BookCopy(
                id="120-001",
                book_id=120,
                status="available"
            ),
            BookCopy(
                id="120-002",
                book_id=120,
                status="available"
            ),
            BookCopy(
                id="121-001",
                book_id=121,
                status="available"
            ),
            BookCopy(
                id="122-001",
                book_id=122,
                status="available"
            ),
            BookCopy(
                id="122-002",
                book_id=122,
                status="available"
            ),
            BookCopy(
                id="122-003",
                book_id=122,
                status="available"
            )
        ]

        db.add_all(copies)

        db.commit()

        print("Sample books added.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()