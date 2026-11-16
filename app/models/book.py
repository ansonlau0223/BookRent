from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    author: Mapped[str] = mapped_column(
        String(255)
    )

    copies: Mapped[list["BookCopy"]] = relationship(
        back_populates="book"
    )


class BookCopy(Base):
    __tablename__ = "book_copies"

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id")
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="available"
    )

    book: Mapped["Book"] = relationship(
        back_populates="copies"
    )