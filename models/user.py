from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


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


class UserProfile(BaseModel):
    user_id: UUID
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    created_time: datetime
    updated_time: datetime
