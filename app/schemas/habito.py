from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class HabitBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


class HabitCreate(HabitBase):
    """
    Datos necesarios para crear un nuevo hábito.
    Por ahora son los mismos que HabitBase.
    """
    pass


class HabitRead(HabitBase):
    id: int
    created_at: datetime
    updated_at: datetime
