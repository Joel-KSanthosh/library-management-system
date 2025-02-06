from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(index=True, unique=True)
    books: list["Book"] = Relationship(back_populates="author")


class Genre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    books: list["Book"] = Relationship(back_populates="genre")


class Publisher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    books: list["Book"] = Relationship(back_populates="publisher")


class Book(SQLModel, Table=True):
    id: int | None = Field(default=None, primary_key=True)
    isbn: str = Field(index=True, unique=True)
    title: str
    genre: Genre | None = Relationship(back_populates="books")
    author: Author | None = Relationship(back_populates="books")
    no_of_pages: int
    publisher: Publisher | None = Relationship(back_populates="books")
