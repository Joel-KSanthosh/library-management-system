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
def insert_user(user: Annotated[UserSignUp, Body()], session: SessionDep):
    if user:
        user.password = hash_password(user.password)
        db_user = User(**user.model_dump())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)


@router.get("/profile")
def get_user_detail(bearer: Annotated[str, Header()], session: SessionDep):
    statement = select(User).where(User.id == id)
    user = session.exec(statement)
    if user:
        try:
            user = user.one()
            user_profile = UserProfile(**user.model_dump())
            return user_profile
        except NoResultFound:
            return "USER DOESN'T EXIST"
    else:
        raise Exception("Critical Error")
