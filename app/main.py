from fastapi import FastAPI

from app.db import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    """
    Código que se ejecuta cuando arranca la aplicación.
    Aquí creamos las tablas en la base de datos.
    """
    create_db_and_tables()


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
