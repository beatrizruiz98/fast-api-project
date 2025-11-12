from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from .config import settings  # Mantiene la configuración disponible en todo el módulo.
from .database import engine
from .routers import posts, users, auth, votes

# Crear automáticamente las tablas definidas en models al iniciar la app (útil en desarrollo).
SQLModel.metadata.create_all(engine)

# Instancia principal de FastAPI exportada al servidor ASGI.
app = FastAPI(
    title="FastAPI Project",
    description="API built with FastAPI and SQLModel",
    version="1.0.0",
)

# Fuentes permitidas para peticiones provenientes de navegadores.
origins = [
    "http://192.168.1.128",
    "http://localhost",
]

# Middleware encargado de la negociación CORS (métodos, headers, cookies, etc.).
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro modular de cada conjunto de endpoints.
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    """Endpoint de salud sencillo para comprobar que el servicio está vivo."""
    return {"Hello": "World"}
