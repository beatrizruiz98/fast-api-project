from sqlmodel import create_engine, Session
from .config import settings

SQLMODEL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"  
engine = create_engine(SQLMODEL_DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
