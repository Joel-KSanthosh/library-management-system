from fastapi import APIRouter, Body, status
from sqlalchemy import select

from db.sessions import DBSession
from models.user import UserProfile
from schemas.user import User

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/list", response_model=list[UserProfile])
async def get_all_users(session: DBSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()
