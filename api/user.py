from typing import Annotated

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from db.sessions import DBSession
from models.user import UserSignUp
from schemas.user import User
from utils.auth import hash_password

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signup")
async def insert_user(user: Annotated[UserSignUp, Body()], session: DBSession):
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
