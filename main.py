import uvicorn
from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from api import user
from config.base import HealthCheck, settings
from db.sessions import get_db_session, sessionmanager
from schemas.user import User
from utils.auth import hash_password


async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    if sessionmanager._sessionmaker is not None:
        async with sessionmanager.session() as session:
            if settings.super_user:
                try:
                    password = settings.super_user.get("password", "password")
                    settings.super_user["password"] = hash_password(password)
                    user = User(**settings.super_user)
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                    print(10 * "-", "SUPER USER CREATED", 10 * "-")
                except IntegrityError:
                    pass
                except Exception:
                    raise
            else:
                raise ValueError("SUPERUSER DETAILS MISSING")

    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()
        print("DATABASE CONNECTION TERMINATED")


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    version=settings.version,
    root_path=settings.api_prefix,
    openapi_url="/openapi.json",
    debug=settings.debug,
)
app.include_router(user.router)


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check():
    return {"name": settings.project_name, "version": settings.version, "description": settings.description}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
