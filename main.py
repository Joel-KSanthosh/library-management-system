import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

load_dotenv()
user = os.getenv("PG_USER", "PG_USER")
password = os.getenv("PG_PASSWORD", "PG_PASSWORD")
hostname = os.getenv("PG_HOSTNAME", "PG_HOSTNAME")
port = os.getenv("PG_PORT", "PG_PORT")
database = os.getenv("PG_DBNAME", "PG_DBNAME")

app = FastAPI()

POSTGRES_URL = f"postgresql://{user}:{password}@{hostname}:{port}/{database}"
engine = create_engine(POSTGRES_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
