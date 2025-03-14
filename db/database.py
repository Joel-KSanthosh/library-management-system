from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from config.base import settings

async_engine = create_async_engine(settings.POSTGRES_URL, echo=True, future=True)


async def get_async_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session  # type: ignore


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
