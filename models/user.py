from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Role(str, Enum):
    user = "USER"
    admin = "ADMIN"
    librarian = "LIBRARIAN"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True)
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr = Field(index=True, unique=True)
    password: str
    role: Role = Field(default=Role.user)

    created_at: datetime | None = Field(
        nullable=False, sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"}
    )

    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )
