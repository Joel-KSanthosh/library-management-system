import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()
url = os.getenv("PG_URL", "PG_URL")
user = os.getenv("PG_USER", "PG_USER")
password = os.getenv("PG_PASSWORD", "PG_PASSWORD")
hostname = os.getenv("PG_HOSTNAME", "PG_HOSTNAME")
port = os.getenv("PG_PORT", "PG_PORT")
database = os.getenv("PG_DBNAME", "PG_DBNAME")
SECRET = os.getenv("SECRET", "SECRET")

POSTGRES_URL = f"{url}://{user}:{password}@{hostname}:{port}/{database}"
async_engine = create_async_engine(POSTGRES_URL, echo=True, future=True)


async def get_async_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session  # type: ignore


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
