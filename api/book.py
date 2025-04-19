from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError

from db.sessions import DBSession
from models.book import AuthorInsert, BookFilter, BookSerializer, Pagination
from schemas.book import Author, Book, Genre, Publisher

router = APIRouter(prefix="/book", tags=["book"])


@router.post("/author")
async def insert_author(author: Annotated[AuthorInsert, Body()], session: DBSession):
    try:
        session.add(Author(**author.model_dump()))
        await session.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"details": "Author inserted successfully"})
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Author with email already exist")


@router.post("/genre")
async def insert_genre(name: Annotated[str, Body(embed=True)], session: DBSession):
    if name:
        try:
            session.add(Genre(name=name))
            await session.commit()
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"details": "Genre inserted successfully"})
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Genre already exist")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")


@router.post("/publisher")
async def insert_publisher(name: Annotated[str, Body(embed=True)], session: DBSession):
    if name:
        try:
            session.add(Publisher(name=name))
            await session.commit()
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"details": "Publisher inserted successfully"})
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Publisher already exist")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")


@router.post("/insert")
async def insert_book(book_details: BookSerializer, session: DBSession):
    book = Book(**book_details.model_dump())
    try:
        session.add(book)
        await session.commit()
        result = jsonable_encoder(book_details)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"details": result})
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Isbn already exists")


# @router.get("")
# async def filter_books(filter: Annotated[BookFilter, Query()], pagination: Annotated[Pagination, Query()], session: DBSession):
#     if filter:
#         query = Book.__table__.select().offset(pagination.offset).limit(pagination.limit)
#         result = await session.execute(query)
#         return result.scalars.all()
