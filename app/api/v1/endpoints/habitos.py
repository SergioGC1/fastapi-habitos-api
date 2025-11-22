from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.habito import Habit, HabitLog
from app.models.user import User
from app.schemas.habito import (
    HabitCreate,
    HabitRead,
    HabitLogCreate,
    HabitLogRead,
    HabitStats,
)
from app.core.security import get_current_user

router = APIRouter()


def _obtener_habito_de_usuario(
    habito_id: int,
    usuario_actual: User,
    session: Session,
) -> Habit:
    """
    Devuelve el hábito si pertenece al usuario actual, o lanza 404.
    """
    habito = session.get(Habit, habito_id)

    if not habito or habito.user_id != usuario_actual.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hábito no encontrado",
        )

    return habito


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
    Elimina (por ahora borrado físico) un hábito del usuario actual.
    """
    habito = _obtener_habito_de_usuario(habito_id, usuario_actual, session)

    session.delete(habito)
    session.commit()


@router.post(
    "/{habito_id}/logs",
    response_model=HabitLogRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_log_habito(
    habito_id: int,
    log_in: HabitLogCreate,
    session: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user),
):
    """
    Crea un registro de cumplimiento para un hábito concreto en una fecha.
    Validaciones:
    - El hábito debe ser del usuario actual.
    - La fecha no puede ser futura.
    - No puede haber más de un registro por día para el mismo hábito.
    """
    habito = _obtener_habito_de_usuario(habito_id, usuario_actual, session)

    # Validar fecha
    if log_in.fecha > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha no puede estar en el futuro",
        )

    # Comprobar si ya existe un registro ese día
    consulta = select(HabitLog).where(
        HabitLog.habit_id == habito.id,
        HabitLog.fecha == log_in.fecha,
    )
    existente = session.exec(consulta).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un registro para este hábito en esa fecha",
        )

    log = HabitLog(
        habit_id=habito.id,
        fecha=log_in.fecha,
        completado=log_in.completado,
    )

    session.add(log)
    session.commit()
    session.refresh(log)

    return log


@router.get(
    "/{habito_id}/logs",
    response_model=List[HabitLogRead],
)
def listar_logs_habito(
    habito_id: int,
    session: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user),
):
    """
    Lista todos los registros de un hábito del usuario actual.
    """
    habito = _obtener_habito_de_usuario(habito_id, usuario_actual, session)

    consulta = (
        select(HabitLog)
        .where(HabitLog.habit_id == habito.id)
        .order_by(HabitLog.fecha.desc())
    )

    logs = session.exec(consulta).all()
    return logs


@router.get(
    "/{habito_id}/stats",
    response_model=HabitStats,
)
def estadisticas_habito(
    habito_id: int,
    session: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user),
):
    """
    Devuelve estadísticas básicas de un hábito:
    - total_registros
    - dias_cumplidos
    - racha_actual (días seguidos cumplidos hasta la última fecha registrada)
    - porcentaje_cumplimiento (dias_cumplidos / total_registros * 100)
    """
    habito = _obtener_habito_de_usuario(habito_id, usuario_actual, session)

    consulta = (
        select(HabitLog)
        .where(
            HabitLog.habit_id == habito.id,
            HabitLog.completado == True,  # noqa: E712
        )
        .order_by(HabitLog.fecha.desc())
    )

    logs = session.exec(consulta).all()

    total_registros = len(logs)
    dias_cumplidos = total_registros

    # Calcular racha actual (consecutivos hacia atrás desde la última fecha registrada)
    racha_actual = 0
    if logs:
        fechas_unicas = sorted(
            {log.fecha for log in logs}, reverse=True
        )
        racha_actual = 1
        dia_anterior = fechas_unicas[0]

        for fecha in fechas_unicas[1:]:
            if fecha == dia_anterior - timedelta(days=1):
                racha_actual += 1
                dia_anterior = fecha
            else:
                break

    porcentaje_cumplimiento = (
        (dias_cumplidos / total_registros) * 100 if total_registros > 0 else 0.0
    )

    return HabitStats(
        habit_id=habito.id,
        total_registros=total_registros,
        dias_cumplidos=dias_cumplidos,
        racha_actual=racha_actual,
        porcentaje_cumplimiento=porcentaje_cumplimiento,
    )
