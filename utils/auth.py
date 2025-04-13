import uuid
from datetime import datetime, timedelta
from typing import Any

import jwt
import redis
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status

from config.base import settings

r = redis.Redis(host=settings.redis_host, password=settings.redis_password, db=settings.redis_db)
ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hash: str) -> bool:
    try:
        return ph.verify(hash, password)

    except VerifyMismatchError:
        return False


async def verify_refresh_token(token: str) -> dict[str, str]:
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


async def create_access_token(user_id: str, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode: dict[str, Any] = {"sub": user_id}
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET, algorithm=settings.ALGORITHM)
    return token


async def create_refresh_token(user_id: str, expires_delta: timedelta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)) -> tuple[str, str, datetime]:
    to_encode: dict[str, Any] = {"sub": user_id}
    expire = datetime.now() + expires_delta
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "jti": jti})
    token = jwt.encode(to_encode, settings.SECRET, algorithm=settings.ALGORITHM)
    return token, jti, expire


async def store_refresh_token(jti: str, user_id: str, exp: datetime) -> None:
    key = f"refresh:{jti}"
    ttl = int((exp - datetime.now()).total_seconds())
    r.set(key, user_id, ttl)


async def is_refresh_token_valid(jti: str):
    key = f"refresh:{jti}"
    return r.exists(key)


async def revoke_refresh_token(jti: str) -> None:
    key = f"refresh{jti}"
    r.delete(key)
