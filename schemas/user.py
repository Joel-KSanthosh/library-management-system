from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import func
from sqlmodel import Field, SQLModel, text


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
    role: str = Field(default=Role.user.value)
    created_at: datetime | None = Field(nullable=False, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")})
    updated_at: datetime | None = Field(
        nullable=False,
        default_factory=datetime.now,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )
