from app.db.base import Base
from app.db.session import engine

from app.models.book import Book, BookCopy
from app.models.user import User
from app.models.rental import Rental
from app.models.reservation import Reservation

def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created.")