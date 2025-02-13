from datetime import datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from db.database import SECRET

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password_and_hash(password: str, hash: str) -> bool:
    try:
        return ph.verify(hash, password)

    except VerifyMismatchError:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm="HS256")
    return encoded_jwt
