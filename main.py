import uvicorn
from fastapi import FastAPI

from api import user
from config.base import HealthCheck, settings

app = FastAPI(title=settings.project_name, version=settings.version, root_path=settings.api_prefix, openapi_url="/openapi.json", debug=settings.debug)
app.include_router(user.router)


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check():
    return {"name": settings.project_name, "version": settings.version, "description": settings.description}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
