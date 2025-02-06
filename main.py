import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
user = os.getenv("PG_USER", "PG_USER")
password = os.getenv("PG_PASSWORD", "PG_PASSWORD")
hostname = os.getenv("PG_HOSTNAME", "PG_HOSTNAME")
port = os.getenv("PG_PORT", "PG_PORT")
database = os.getenv("PG_DBNAME", "PG_DBNAME")

app = FastAPI()

POSTGRES_URL = f"postgresql://{user}:{password}@{hostname}:{port}/{database}"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
