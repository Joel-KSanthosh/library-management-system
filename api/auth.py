from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.sessions import DBSession
from models.user import UserLogin, UserSignUp
from schemas.user import User
from utils.auth import create_access_token, create_refresh_token, hash_password, is_refresh_token_valid, revoke_refresh_token, store_refresh_token, verify_refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def insert_user(user: Annotated[UserSignUp, Body()], session: DBSession) -> JSONResponse:
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


@router.post("/login")
async def login(user: Annotated[UserLogin, Body()], session: DBSession) -> JSONResponse:
    result = await session.execute(select(User).where(User.email == user.email))
    user_details = result.scalar()
    if user_details:
        user_id = str(user_details.uuid)
        refresh_token, jti, exp = await create_refresh_token(user_id)
        await store_refresh_token(jti, user_id, exp)
        access_token = await create_access_token(user_id)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"access-token": access_token, "refresh-token": refresh_token})
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"details": "User doesn't exists!"})


@router.post("/refresh")
async def refresh(refresh_token: Annotated[str, Body(embed=True)], session: DBSession) -> JSONResponse:
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing token")
    payload = await verify_refresh_token(refresh_token)
    user_id = payload.get("sub", "")
    jti = payload.get("jti", "")

    if not await is_refresh_token_valid(jti):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token reuse detected or revoked")

    await revoke_refresh_token(jti)
    new_refresh_token, new_jti, new_exp = await create_refresh_token(user_id)
    await store_refresh_token(new_jti, user_id, new_exp)

    new_access_token = await create_access_token(user_id)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"access_token": new_access_token, "refresh_token": new_refresh_token})
