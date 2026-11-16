from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id")
    )

    book_copy_id: Mapped[str] = mapped_column(
        ForeignKey("book_copies.id")
    )

    start_date: Mapped[date] = mapped_column(
        Date
    )

    due_date: Mapped[date] = mapped_column(
        Date
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active"
    )