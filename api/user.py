from typing import Annotated

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Body, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from db.database import SessionDep
from models.user import UserProfile, UserSignUp
from schemas.user import User
from utils.auth import hash_password

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signup")
async def insert_user(user: Annotated[UserSignUp, Body()], session: SessionDep):
    if user:
        user.password = hash_password(user.password)
        db_user = User(**user.model_dump())
        try:
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"details": "Successfully Created User"})
        except IntegrityError:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"details": f"User with the email - {user.email} already exists"})


# @router.get("/list")
# async def get_all_users(session: SessionDep):
#     stmt = select(User)
#     return session.exec(stmt)
