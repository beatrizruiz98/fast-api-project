from fastapi import FastAPI, HTTPException, status, Depends
from .database import engine, get_session

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

from sqlmodel import Session, SQLModel, select

from .routers import posts, users, auth

# Crea tablas de SQLModel (requiere que models esté importado)
SQLModel.metadata.create_all(engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

# @app.get("/sqlalchemy-health", status_code=status.HTTP_200_OK)
# def get_sqlalchemy_health(db: Session = Depends(get_session)):
#     db.execute(text("SELECT 1"))
#     return {"status": "ok"}

# Conexión psycopg2 (bloqueante hasta que conecte)
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",       # <-- igual que en database.py
#             user="postgres",
#             password="postgres",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as e:
#         print("Database connection failed!", e)
#         time.sleep(2)

@app.get("/")
def root():
    return {"Hello": "World"}