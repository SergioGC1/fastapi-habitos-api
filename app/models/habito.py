from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Habit(SQLModel, table=True):
    """
    Hábito que pertenece a un usuario.
    Ejemplo: "leer 20 minutos", "hacer ejercicio", etc.
    """

    __tablename__ = "habitos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="usuarios.id")

    nombre: str
    descripcion: Optional[str] = None
    activo: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class HabitLog(SQLModel, table=True):
    """
    Registro del cumplimiento de un hábito en una fecha concreta.
    Ejemplo: el 2025-11-21 hice el hábito "leer 20 minutos".
    """

    __tablename__ = "registros_habitos"

    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habitos.id")

    fecha: date
    completado: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
