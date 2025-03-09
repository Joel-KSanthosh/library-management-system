from datetime import date
from uuid import UUID

from sqlmodel import Field, SQLModel, text


class Library(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", unique=True, primary_key=True)
    quantity: int = Field(ge=0, default=0)


class Borrow(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", primary_key=True, nullable=False)
    user_id: UUID = Field(foreign_key="user.uuid", primary_key=True, nullable=False)
    borrowed_date: date = Field(nullable=False, sa_column_kwargs={"server_default": text("CURRENT_DATE")})
    actual_return_date: date = Field(
        nullable=False,
        sa_column_kwargs={"server_default": text("CURRENT_DATE + INTERVAL '10 DAY'")},
    )

    returned_date: date | None = None


class UserFine(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.uuid", unique=True, primary_key=True)
    amount: float = Field(default=0.0)
