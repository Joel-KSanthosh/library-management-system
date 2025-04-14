from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from db.sessions import DBSession
from models.user import UserProfile
from schemas.user import User
from utils.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/list", response_model=list[UserProfile])
async def get_all_users(session: DBSession, user: User = Depends(get_current_user)):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/profile", response_model=UserProfile, response_class=JSONResponse)
async def profile(user: User = Depends(get_current_user)):
    return user
