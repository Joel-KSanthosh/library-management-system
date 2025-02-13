from typing import Annotated

from fastapi import APIRouter, Body

from db.database import SessionDep
from models.user import UserSignUp, hash_password
from schemas.user import User

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signup")
def insert_user(user: Annotated[UserSignUp, Body()], session: SessionDep):
    if user:
        user.password = hash_password(user.password)
        db_user = User(**user.model_dump())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
