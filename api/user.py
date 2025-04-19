from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select

from db.sessions import DBSession
from models.user import UserProfile
from schemas.user import User
from utils.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile", response_model=UserProfile)
async def profile(user: User = Depends(get_current_user)):
    json_user = jsonable_encoder(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"details": json_user})
