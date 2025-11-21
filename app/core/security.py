from passlib.context import CryptContext

# Contexto de hash de contraseñas usando bcrypt
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Devuelve un hash seguro de la contraseña en texto plano.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Comprueba si una contraseña en texto plano coincide con su hash almacenado.
    """
    return pwd_context.verify(plain_password, hashed_password)
