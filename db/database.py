import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, create_engine

load_dotenv()
url = os.getenv("PG_URL", "PG_URL")
user = os.getenv("PG_USER", "PG_USER")
password = os.getenv("PG_PASSWORD", "PG_PASSWORD")
hostname = os.getenv("PG_HOSTNAME", "PG_HOSTNAME")
port = os.getenv("PG_PORT", "PG_PORT")
database = os.getenv("PG_DBNAME", "PG_DBNAME")
SECRET = os.getenv("SECRET", "SECRET")

POSTGRES_URL = f"{url}://{user}:{password}@{hostname}:{port}/{database}"
engine = create_engine(POSTGRES_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
