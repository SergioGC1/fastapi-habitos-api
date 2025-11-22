from datetime import date, datetime
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


class HabitLogBase(SQLModel):
    fecha: date
    completado: bool = True


class HabitLogCreate(HabitLogBase):
    """
    Datos para crear un registro de hábito.
    """


class HabitLogRead(HabitLogBase):
    id: int
    habit_id: int
    created_at: datetime


class HabitStats(SQLModel):
    habit_id: int
    total_registros: int
    dias_cumplidos: int
    racha_actual: int
    porcentaje_cumplimiento: float
