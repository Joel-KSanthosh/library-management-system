import typing as t

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .book import Author, Book, Genre, Publisher  # noqa: E402
from .library import Borrow, Library, UserFine  # noqa: E402
from .user import User  # noqa: E402
