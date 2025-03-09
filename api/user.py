from typing import Annotated

from fastapi import APIRouter, Body, Header
from sqlalchemy.exc import NoResultFound
from sqlmodel import select

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
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    else:
        return "ERROR"
