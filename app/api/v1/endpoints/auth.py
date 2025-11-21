from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.user import User
from app.schemas.auth import LoginRequest, Token
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    credenciales: LoginRequest,
    session: Session = Depends(get_session),
):
    # Buscar usuario por email
    usuario = session.exec(
        select(User).where(User.email == credenciales.email)
    ).first()

    if not usuario or not verify_password(
        credenciales.password, usuario.hashed_password
    ):
        # No damos pistas: mismo mensaje para email o password mal
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generar JWT con el id de usuario en el campo "sub"
    access_token = create_access_token({"sub": str(usuario.id)})

    return Token(access_token=access_token, token_type="bearer")
