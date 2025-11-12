from fastapi import FastAPI
from .database import engine
from sqlmodel import SQLModel
from .routers import posts, users, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Crea tablas de SQLModel (requiere que models esté importado)
SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="FastAPI Project",
    description="API built with FastAPI and SQLModel",
    version="1.0.0"
)

origins = [
    "http://192.168.1.128",
    "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"Hello": "World"}