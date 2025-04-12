import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import UUID, Column, DateTime, Integer, String, text

from . import Base


class Role(str, Enum):
    user = "USER"
    admin = "ADMIN"
    librarian = "LIBRARIAN"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4())
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(10), nullable=False, default=Role.user.value)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
