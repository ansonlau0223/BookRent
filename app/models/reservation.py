from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id")
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="waiting"
    )
    