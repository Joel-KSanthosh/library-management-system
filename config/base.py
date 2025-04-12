import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # API Settings
    api_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    # DATABASE
    POSTGRES_URL: str

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    SECRET: str

    # SUPERUSER
    super_user: dict


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


settings = Settings()  # type: ignore
