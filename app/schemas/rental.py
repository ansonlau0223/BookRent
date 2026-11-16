from datetime import date

from pydantic import BaseModel, Field


class RentalCreate(BaseModel):
    rentalPeriodDays: int = Field(
        default=30,
        ge=1,
        le=90
    )


class RentalResponse(BaseModel):
    rentalId: int
    bookId: int
    bookCopyId: str
    startDate: date
    dueDate: date
    status: str