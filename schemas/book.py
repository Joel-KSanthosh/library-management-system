from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), index=True, unique=True, nullable=False)
    books = relationship("Book", back_populates="author", uselist=True)


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    books = relationship("Book", back_populates="genre", uselist=True)


class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    books = relationship("Book", back_populates="publisher", uselist=True)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    isbn = Column(String(255), index=True, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=False)
    genre = relationship("Genre", back_populates="books")
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author = relationship("Author", back_populates="books")
    no_of_pages = Column(Integer, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publisher.id"), nullable=False)
    publisher = relationship("Publisher", back_populates="books")
