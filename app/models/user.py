from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Modelo de usuario para la base de datos.
    Más adelante lo usaremos para registro, login, etc.
    """

    __tablename__ = "usuarios"  # nombre de la tabla en la BD

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
