import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()
# url = os.getenv("PG_URL", "PG_URL")
# user = os.getenv("PG_USER", "PG_USER")
# password = os.getenv("PG_PASSWORD", "PG_PASSWORD")
# hostname = os.getenv("PG_HOSTNAME", "PG_HOSTNAME")
# port = os.getenv("PG_PORT", "PG_PORT")
# database = os.getenv("PG_DBNAME", "PG_DBNAME")
# api_prefix = os.getenv("API_PREFIX", "API_PREFIX")
# debug = os.getenv("DEBUG", False) == "True"
# project_name = os.getenv("PROJECT_NAME", "PROJECT_NAME")
# version = os.getenv("VERSION", "VERSION")
# description = os.getenv("DESCRIPTION", "DESCRIPTION")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "ACCESS_TOKEN_EXPIRE_MINUTES"))
# REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "REFRESH_TOKEN_EXPIRE_MINUTES"))
# ALGORITHM = os.getenv("ALGORITHM", "ALGORITHM")

# POSTGRES_URL = f"{url}://{user}:{password}@{hostname}:{port}/{database}"


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


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


settings = Settings()  # type: ignore
