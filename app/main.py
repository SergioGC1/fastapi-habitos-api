from fastapi import FastAPI

from app.db import create_db_and_tables
from app.api.v1.api import api_router

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


# Aquí montamos todas las rutas de la API v1
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
