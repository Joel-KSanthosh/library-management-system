import contextlib
from typing import Annotated, Any, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker, create_async_engine

from config.base import settings


class AsyncDatabaseSessionManager:
    def __init__(self, host: str = settings.POSTGRES_URL, engine_kwargs: dict[str, Any] = {"future": True, "echo": True}) -> None:
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def close(self):
        if self._engine is None:
            raise Exception("AsyncDatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("AsyncDatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("AsyncDatabaseSessionManager is not initialized")

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


sessionmanager = AsyncDatabaseSessionManager()


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db_session)]
