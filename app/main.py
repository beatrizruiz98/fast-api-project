from fastapi import FastAPI
from .database import engine
from sqlmodel import SQLModel
from .routers import posts, users, auth
from .config import settings

# Crea tablas de SQLModel (requiere que models esté importado)
SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="FastAPI Project",
    description="API built with FastAPI and SQLModel",
    version="1.0.0"
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Hello": "World"}