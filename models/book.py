from pydantic import BaseModel, EmailStr, Field, model_validator


class AuthorInsert(BaseModel):
    name: str
    email: EmailStr


class BookSerializer(BaseModel):
    isbn: str
    title: str
    genre_id: int = Field(gt=0)
    author_id: int = Field(gt=0)
    no_of_pages: int = Field(gt=0)
    publisher_id: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_isbn(self) -> "BookSerializer":
        if len(self.isbn) == 13 and self.isbn.startswith("978") or self.isbn.startswith("979"):
            return self
        raise ValueError("Invalid isbn")


class BookFilter(BaseModel):
    genre: int | None = Field(gt=0)
    author: int | None = Field(gt=0)
    publisher: int | None = Field(gt=0)


class Pagination(BaseModel):
    offset: int = Field(gt=0, default=1)
    limit: int = Field(gt=0, default=100)
