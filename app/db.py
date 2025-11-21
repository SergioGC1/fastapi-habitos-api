from sqlmodel import SQLModel, create_engine, Session

# URL de conexión a SQLite
sqlite_url = "sqlite:///./habitos.db"

# echo=True hace que se vean las sentencias SQL en consola (útil para aprender)
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    """
    Crea las tablas definidas en los modelos que hereden de SQLModel.
    De momento no hay modelos, pero más adelante añadiremos User, Habit, etc.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Más adelante la usaremos en los endpoints.
    """
    with Session(engine) as session:
        yield session
