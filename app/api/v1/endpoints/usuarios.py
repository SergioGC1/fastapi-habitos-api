from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.user import User
from app.schemas.usuario import UserCreate, UserRead
from app.core.security import get_password_hash

router = APIRouter()


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_usuario(
    usuario_in: UserCreate,
    session: Session = Depends(get_session),
):
    # Comprobar si ya existe un usuario con ese email
    existing_user = session.exec(
        select(User).where(User.email == usuario_in.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    # Crear usuario con contraseña hasheada
    usuario = User(
        email=usuario_in.email,
        hashed_password=get_password_hash(usuario_in.password),
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.get("/", response_model=list[UserRead])
def listar_usuarios(
    session: Session = Depends(get_session),
):
    usuarios = session.exec(select(User)).all()
    return usuarios
