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
    confirm_password: str = Field(min_length=4, exclude=True)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_password(self) -> "UserSignUp":
        if self.password and self.confirm_password and self.password == self.confirm_password:
            return self
        else:
            raise ValueError("Password doesn't match")


class UserProfile(BaseModel):
    uuid: UUID = Field(alias="user_id")
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(validate_by_name=True, from_attributes=True)
