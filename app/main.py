from fastapi import FastAPI, HTTPException, status, Depends
from .database import engine, get_session

from sqlmodel import Session, SQLModel, select

from .routers import posts, users, auth

# Crea tablas de SQLModel (requiere que models esté importado)
SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="FastAPI Project",
    description="API created in FastAPI course",
    version="1.0.0"
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Hello": "World"}