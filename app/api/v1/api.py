from fastapi import APIRouter

from app.api.v1.endpoints import usuarios, auth, habitos

api_router = APIRouter()

api_router.include_router(
    usuarios.router,
    prefix="/usuarios",
    tags=["usuarios"],
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

api_router.include_router(
    habitos.router,
    prefix="/habitos",
    tags=["habitos"],
)
