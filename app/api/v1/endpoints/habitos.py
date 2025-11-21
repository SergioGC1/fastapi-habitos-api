from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.habito import Habit
from app.models.user import User
from app.schemas.habito import HabitCreate, HabitRead
from app.core.security import get_current_user

router = APIRouter()


@router.post(
    "/",
    response_model=HabitRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_habito(
    habito_in: HabitCreate,
    session: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user),
):
    """
    Crea un nuevo hábito asociado al usuario autenticado.
    """
    habito = Habit(
        user_id=usuario_actual.id,
        nombre=habito_in.nombre,
        descripcion=habito_in.descripcion,
        activo=habito_in.activo,
    )

    session.add(habito)
    session.commit()
    session.refresh(habito)

    return habito


@router.get(
    "/",
    response_model=List[HabitRead],
)
def listar_habitos(
    session: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user),
):
    """
    Lista todos los hábitos del usuario autenticado.
    """
    consulta = select(Habit).where(Habit.user_id == usuario_actual.id)
    habitos = session.exec(consulta).all()
    return habitos


@router.delete(
    "/{habito_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_habito(
    habito_id: int,
    session: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user),
):
    """
    Elimina (o desactiva) un hábito del usuario actual.
    De momento lo borramos físicamente.
    """
    habito = session.get(Habit, habito_id)

    if not habito or habito.user_id != usuario_actual.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hábito no encontrado",
        )

    session.delete(habito)
    session.commit()
