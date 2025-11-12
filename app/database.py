from sqlmodel import create_engine, Session
from .config import settings

# Cadena de conexión dinámica tomada del archivo .env.
SQLMODEL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

# Motor de base de datos global para reutilizar conexiones en toda la aplicación.
engine = create_engine(SQLMODEL_DATABASE_URL, echo=False)


def get_session():
    """Provee una sesión nueva por petición y garantiza su cierre al finalizar."""
    with Session(engine) as session:
        yield session
