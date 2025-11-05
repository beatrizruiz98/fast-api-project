from fastapi import FastAPI, HTTPException, status, Depends

from .schemas import PostIn, PostBase, UserBase, UserIn # Lo añado como response_model en la def del endpoint y serán los datos devueltos en la response del endpoint
from .database import engine, get_session
from .models import Posts, Users  # Este es el modelo SQLModel, así es como debe importarse la ddbb
from .utils import get_password_hash

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy import text
from sqlmodel import Session, SQLModel, select

# Crea tablas de SQLModel (requiere que models esté importado)
SQLModel.metadata.create_all(engine)

app = FastAPI()

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

@app.get("/posts", status_code=status.HTTP_200_OK, response_model=list[PostIn])
def get_posts(db: Session = Depends(get_session)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.exec(select(Posts)).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostIn)
def create_post(payload: PostIn, db: Session = Depends(get_session)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = Posts(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_a_post(id: int, db: Session = Depends(get_session)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_session)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted = cursor.fetchone()
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    db.delete(post)
    db.commit()
    # conn.commit()
    return

@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostBase)
def update_post(id: int, payload: PostIn, db: Session = Depends(get_session)):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, post.published, id),
    # )
    # updated = cursor.fetchone()
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    # actualizamos los campos manualmente
    post.title = payload.title
    post.content = payload.content
    post.published = payload.published

    db.add(post)      # opcional, pero recomendable
    db.commit()
    db.refresh(post)  # para devolver el valor actualizado
    # conn.commit()
    return post

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=UserBase)
def create_user(payload: UserIn, db: Session = Depends(get_session)):
    payload.password = get_password_hash(payload.password)
    user = Users(**payload.model_dump())
    if db.exec(select(Users).where(Users.email == user.email)).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    db.add(user, id)
    db.commit()
    db.refresh(user)
    return user