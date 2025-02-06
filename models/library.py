from datetime import date, timedelta
from uuid import UUID

from sqlmodel import Field, SQLModel


class Library(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", unique=True)
    quantity: int = Field(ge=0)


class Borrow(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id")
    user_id: UUID = Field(foreign_key="user.uuid")
    borrowed_date: date = Field(
        nullable=False, sa_column_kwargs={"server_default": date.today()}
    )
    actual_return_date: date = Field(
        nullable=False,
        sa_column_kwargs={"server_default": date.today() + timedelta(days=10)},
    )

    returned_date: date | None = Field(default=None)


class UserFine(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.uuid", unique=True)
    amount: float = Field(default=0.0)
