from datetime import date

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import Base


class Library(Base):
    __tablename__ = "library"

    book_id = Column(Integer, ForeignKey("book.id"), unique=True, primary_key=True)
    quantity = Column(Integer, default=0)


class Borrow(Base):
    __tablename__ = "borrow"

    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), primary_key=True, nullable=False)
    borrowed_date = Column(DateTime, nullable=False, server_default=text("CURRENT_DATE"))
    actual_return_date = Column(DateTime, nullable=False, server_default=text("CURRENT_DATE + INTERVAL '10 DAY'"))
    returned_date = Column(
        DateTime,
        nullable=True,
    )


class UserFine(Base):
    __tablename__ = "user_fine"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), unique=True, primary_key=True)
    amount = Column(Float, default=0.0, nullable=False)
