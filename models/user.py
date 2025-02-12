from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

ph = PasswordHasher()


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(extra="forbid")


class UserSignUp(UserLogin):
    first_name: str
    middle_name: str | None = None
    last_name: str
    password: str = Field(min_length=4)
    confirm_password: str = Field(min_length=4)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_password(self) -> "UserSignUp":
        if (
            self.password
            and self.confirm_password
            and self.password == self.confirm_password
        ):
            return self
        else:
            raise ValueError("Password doesn't match")


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password_and_hash(password: str, hash: str) -> bool:
    try:
        return ph.verify(hash, password)

    except VerifyMismatchError:
        return False
